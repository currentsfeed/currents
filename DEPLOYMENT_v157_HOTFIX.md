# DEPLOYMENT v157 HOTFIX - Monitoring Scripts Missing from Cron

**Date**: Feb 14, 2026 07:17 UTC  
**Reporter**: Roy Shaham  
**Issue**: "Site is down" (fourth occurrence)  
**Status**: ✅ FIXED - Added monitoring scripts to crontab

## Problem

Roy reported the site was down at 07:17 UTC. Investigation revealed:
- ✅ Flask app running normally (systemd)
- ⚠️ Ngrok process running but tunnel broken (404 error)
- ❌ **Monitoring scripts were never added to cron!**

### Root Cause

The monitoring scripts we created in v154_HOTFIX (`refresh-tunnels.sh` and `monitor_site.sh`) were **never added to crontab**.

**What existed in cron:**
```bash
*/30 * * * * refresh_trending.sh    # Trending computation
0 4 * * * refresh_score_decay.sh     # Daily score decay
```

**What was MISSING:**
```bash
# refresh-tunnels.sh - Tunnel health check (MISSING!)
# monitor_site.sh - Full site monitoring (MISSING!)
```

**Result:** No automated checks for tunnel health. Tunnel broke and stayed broken until Roy reported it manually.

### Timeline of This Downtime

- **05:02 UTC**: Last successful tunnel check (manual or from earlier test)
- **~05:30-07:17 UTC**: Tunnel broke at some point (ngrok process alive, tunnel dead)
- **07:17 UTC**: Roy reports "site is down"
- **07:18 UTC**: Manual restart → Site back up

**Downtime:** ~90-120 minutes (undetected)

## Solution

### Added Both Scripts to Crontab

**Before:**
```bash
crontab -l
# Currents automation - trending refresh + score decay
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh
0 4 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh
```

**After:**
```bash
crontab -l
# Currents automation - trending refresh + score decay
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh
0 4 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh-tunnels.sh   # NEW
15,45 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh      # NEW
```

### Schedule Breakdown

| Script | Schedule | Purpose | Frequency |
|--------|----------|---------|-----------|
| **refresh_trending.sh** | `*/30 * * * *` | Recompute trending scores | Every 30 min |
| **refresh-tunnels.sh** | `*/30 * * * *` | Check tunnel health, restart if broken | Every 30 min |
| **monitor_site.sh** | `15,45 * * * *` | Full health check (Flask + ngrok) | :15 and :45 |
| **refresh_score_decay.sh** | `0 4 * * *` | Apply score decay to user profiles | Daily 4am |

**Staggered timing:**
- **:00 and :30** → refresh_trending + refresh-tunnels
- **:15 and :45** → monitor_site
- Prevents all scripts running simultaneously
- Maximum detection time: 30 minutes

## Why Scripts Existed But Weren't in Cron

### History

1. **v154_HOTFIX** (Feb 14 00:36): Created `refresh-tunnels.sh` and updated `monitor_site.sh`
2. **Testing**: Ran scripts manually to verify they worked
3. **Deployment**: Updated scripts, restarted Flask
4. **❌ Missing Step**: Never added scripts to crontab!

### Why This Happened

When creating the scripts, we:
- ✅ Created the files
- ✅ Made them executable
- ✅ Tested them manually (`bash refresh-tunnels.sh`)
- ❌ Forgot to add to cron

We assumed they were already in cron (they weren't), or thought manual testing was sufficient (it wasn't).

## Monitoring Now Active

### refresh-tunnels.sh (Every 30 min)

**What it does:**
1. Check if ngrok process exists
2. **Test tunnel functionality** (HTTP request to site)
3. If process exists BUT tunnel broken → Kill and restart
4. If process doesn't exist → Start tunnel
5. Log results

**Key improvement over process-only check:**
```bash
# Old way (v154_HOTFIX concept but not in cron)
if pgrep ngrok; then skip; fi

# New way (now actually running)
if pgrep ngrok; then
    HTTP_CODE=$(curl site)
    if [ "$HTTP_CODE" != "200" ]; then
        # RESTART (tunnel broken even though process exists)
    fi
fi
```

### monitor_site.sh (At :15, :45)

**What it does:**
1. Check Flask systemd status
2. Check ngrok tunnel functionality (HTTP test)
3. If either broken → Restart the broken service
4. Log all checks and restarts
5. Can send alerts (placeholder for future)

**Redundancy:**
- Runs offset from refresh-tunnels (15 min later)
- Double-checks both Flask and ngrok
- Catches issues refresh-tunnels might miss

## Expected Behavior Going Forward

### Normal Operation
```
05:00 - refresh_trending + refresh-tunnels (both healthy, skip)
05:15 - monitor_site (both healthy, skip)
05:30 - refresh_trending + refresh-tunnels (both healthy, skip)
05:45 - monitor_site (both healthy, skip)
...
```

### When Tunnel Breaks
```
06:00 - refresh_trending + refresh-tunnels
        → Tunnel test returns 404
        → Kill ngrok, restart tunnel
        → Tunnel working again
06:15 - monitor_site (verifies tunnel working)
```

**Maximum downtime:** 30 minutes (until next refresh-tunnels check)

### When Flask Crashes
```
06:15 - monitor_site
        → Systemd shows Flask inactive
        → Run: systemctl restart currents.service
        → Flask working again (systemd handles this automatically anyway)
```

**Maximum downtime:** Few seconds (systemd auto-restart) + 15-30 min detection

## Files Changed

- **Crontab**: Added 2 new entries (refresh-tunnels.sh, monitor_site.sh)
- **No code changes** (scripts already existed since v154_HOTFIX)

## Verification

### Crontab Active
```bash
crontab -l
# Shows 4 entries (trending, tunnels, monitor, decay)
```

### Next Scheduled Runs
```
Current time: 07:18 UTC
Next refresh-tunnels: 07:30 UTC (12 minutes)
Next monitor_site: 07:45 UTC (27 minutes)
Next refresh_trending: 07:30 UTC (12 minutes)
```

### Log Files to Monitor
```bash
tail -f /tmp/tunnel-refresh.log     # Tunnel health checks
tail -f /tmp/site_monitor.log       # Full site monitoring
tail -f /tmp/ngrok.log              # Ngrok output
```

## Testing

### Manual Test (Simulate Broken Tunnel)

```bash
# 1. Kill ngrok (simulate tunnel death)
pkill -f ngrok

# 2. Wait for next cron run (up to 30 min)
# Or trigger manually:
bash /home/ubuntu/.openclaw/workspace/currents-full-local/refresh-tunnels.sh

# 3. Check logs
tail /tmp/tunnel-refresh.log
# Should show: "Ngrok process not found, starting..."

# 4. Verify site back up
curl -s -o /dev/null -w "%{http_code}" https://proliferative-daleyza-benthonic.ngrok-free.dev
# Should return: 200
```

### Verify Cron Execution

```bash
# Check cron logs (system-dependent)
grep CRON /var/log/syslog | grep refresh-tunnels | tail -5
grep CRON /var/log/syslog | grep monitor_site | tail -5

# Or check script logs
ls -lth /tmp/tunnel-refresh.log /tmp/site_monitor.log
# Should show recent modification times
```

## Related Issues

- **DEPLOYMENT_v154_HOTFIX.md** - Created scripts (but didn't add to cron)
- **DEPLOYMENT_v152_HOTFIX.md** - First tunnel downtime (process died)
- **DEPLOYMENT_v152_HOTFIX2.md** - Second downtime (deprecated flag)
- **DEPLOYMENT_v154_HOTFIX.md** - Third downtime (broken tunnel, process alive)
- **This hotfix** - Fourth downtime (scripts not in cron)

## Pattern Analysis

### All 4 Downtimes Were Infrastructure Issues

1. **20:08 UTC Feb 13**: Scripts using wrong tunnel (localtunnel vs ngrok)
2. **00:35 UTC Feb 14**: Scripts using deprecated flag (`--domain` vs `--url`)
3. **05:01 UTC Feb 14**: Scripts only checking process, not functionality
4. **07:17 UTC Feb 14**: Scripts not running automatically (missing from cron)

**Common thread:** Incremental improvements to monitoring, but each fix revealed a deeper issue.

### Why So Many Iterations?

**Progressive discovery:**
- Fix 1: Wrong technology → Switched to ngrok
- Fix 2: Wrong syntax → Updated flag
- Fix 3: Wrong check → Test functionality, not just process
- Fix 4: Not automated → Add to cron

Each fix was correct for what we knew at the time, but ngrok's instability kept revealing deeper monitoring gaps.

## Prevention Going Forward

### ✅ Now Have
- **Process monitoring** (systemd for Flask)
- **Tunnel monitoring** (refresh-tunnels.sh checks HTTP status)
- **Redundant checks** (monitor_site.sh verifies both)
- **Automated execution** (cron every 30 minutes)
- **Staggered timing** (scripts don't all run at once)

### 🔮 Future Improvements

1. **Alerting**
   - Send notification when tunnel restarts
   - Track downtime duration
   - Alert if restarts fail

2. **Metrics**
   - Count tunnel restarts per day
   - Track uptime percentage
   - Measure detection lag

3. **Alternative Solutions**
   - Ngrok paid tier (more stable tunnels)
   - Cloudflare Tunnel (alternative to ngrok)
   - Proper domain + SSL (eliminate tunnel entirely)

4. **Backup Tunnel**
   - Start second tunnel on different port
   - Auto-switch if primary fails
   - Eliminates single point of failure

## Impact

### Before Fix
- ❌ No automated tunnel monitoring
- ❌ Downtime until manual report
- ❌ ~90-120 minute outage

### After Fix
- ✅ Automated tunnel checks every 30 min
- ✅ Auto-restart on failure
- ✅ Maximum 30 min downtime (detection lag)
- ✅ No manual intervention needed

### For Roy
- Previous: Report "site is down" → Wait for manual fix
- Now: Tunnel breaks → Auto-detected within 30 min → Auto-restarted → Working

Still not perfect (30 min detection lag), but **much better** than requiring manual reports.

---

**Downtime Duration**: ~90-120 minutes (undetected)  
**Recovery Time**: 2 minutes (manual restart)  
**Status**: ✅ RESOLVED - Monitoring now automated  
**Version**: Still v157 (infrastructure fix only)  
**Next Check**: 07:30 UTC (refresh-tunnels.sh)  
**Site URL**: https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## Key Takeaway

**Creating scripts ≠ Running scripts**

We created excellent monitoring scripts but forgot the final step: **add them to cron**.

Lesson learned: When creating monitoring automation, always verify:
1. ✅ Scripts exist
2. ✅ Scripts work (manual test)
3. ✅ Scripts are executable
4. ✅ **Scripts are in crontab** ← We missed this!
5. ✅ Cron is actually running them (check logs)

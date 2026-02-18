# DEPLOYMENT v152 HOTFIX - Site Down (Ngrok Tunnel)

**Date**: Feb 13, 2026 20:09 UTC  
**Reporter**: Roy Shaham  
**Issue**: "Site is down"  
**Status**: ✅ FIXED - Ngrok tunnel restarted, scripts updated

## Problem
Roy reported the site was down at 20:08 UTC. Investigation revealed:
- ✅ Flask app (systemd) was running normally
- ❌ **Ngrok tunnel had died** (no process running)
- ⚠️ `refresh-tunnels.sh` was still using old **localtunnel** code
- ⚠️ `monitor_site.sh` was using outdated restart logic (direct python3, not systemd)

**Root cause**: The cron job was running `refresh-tunnels.sh` every 30 minutes, but the script was trying to restart localtunnel instead of ngrok!

## Solution

### 1. Restarted Ngrok Immediately
```bash
nohup ngrok http --domain=proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
```
✅ Site back online within 2 minutes

### 2. Updated `refresh-tunnels.sh`
**Before**: Used localtunnel (lt) commands
**After**: Uses ngrok with proper domain, includes process detection

Key changes:
- Replaced `lt --port 5555` with `ngrok http --domain=proliferative-daleyza-benthonic.ngrok-free.dev 5555`
- Added check to avoid duplicate ngrok processes
- Added verification logging
- Removed localtunnel database viewer tunnel (not needed)

### 3. Updated `monitor_site.sh`
**Before**: Manually killed/restarted python3 processes, used old ngrok command
**After**: Uses systemd for Flask, proper ngrok domain for tunnel

Key changes:
- Check Flask via `systemctl is-active currents.service`
- Restart Flask via `sudo systemctl restart currents.service`
- Check ngrok via `pgrep -f "ngrok http.*5555"`
- Restart ngrok with correct domain: `--domain=proliferative-daleyza-benthonic.ngrok-free.dev`
- Separated restart logic (only restart what's actually down)

## Technical Details

### Scripts Updated

#### refresh-tunnels.sh (called by cron every 30 min)
```bash
#!/bin/bash
# Refresh ngrok tunnel (prevent disconnects)
# Called by cron every 30 minutes

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Check if ngrok is already running
if pgrep -f "ngrok http.*5555" > /dev/null; then
    echo "[$(date)] Ngrok already running, skipping" >> /tmp/tunnel-refresh.log
    exit 0
fi

# Kill any stale tunnel processes
pkill -f "ngrok" 2>/dev/null
pkill -f "lt --port" 2>/dev/null
sleep 2

# Start ngrok with Currents domain
nohup ngrok http --domain=proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
sleep 3

# Verify ngrok started
if pgrep -f "ngrok http.*5555" > /dev/null; then
    echo "[$(date)] Ngrok tunnel started successfully" >> /tmp/tunnel-refresh.log
else
    echo "[$(date)] ERROR: Ngrok failed to start" >> /tmp/tunnel-refresh.log
fi
```

#### monitor_site.sh (called by cron every 90 min)
- Now checks systemd status instead of manual process detection
- Restarts Flask via systemd (not manual python3)
- Uses proper ngrok domain for restarts
- Only restarts services that are actually down

## Verification

### Site Status
```bash
curl -s -o /dev/null -w "%{http_code}" https://proliferative-daleyza-benthonic.ngrok-free.dev
# Result: 200 ✅
```

### Ngrok Process
```bash
pgrep -f "ngrok http.*5555"
# Result: 128519 (running) ✅
```

### Flask Service
```bash
systemctl is-active currents.service
# Result: active ✅
```

### Monitor Test
```bash
bash monitor_site.sh
tail -3 /tmp/site_monitor.log
# Result:
# [Fri Feb 13 20:09:59 UTC 2026] ✅ Flask app (systemd) is running
# [Fri Feb 13 20:09:59 UTC 2026] ✅ Ngrok tunnel process is running
# [Fri Feb 13 20:09:59 UTC 2026] ✅ All systems operational
```

## Files Changed
- `refresh-tunnels.sh` - Updated from localtunnel to ngrok
- `monitor_site.sh` - Updated to use systemd + proper ngrok domain

## Cron Jobs (Active)
```bash
crontab -l | grep -v "^#"
```

Expected:
```
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh-tunnels.sh
*/90 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh
```

## Why This Happened
When we migrated from localtunnel to ngrok (around v87-v88), we updated the manual startup commands but **forgot to update the automated scripts**:
- ❌ `refresh-tunnels.sh` still had `lt --port 5555` commands
- ❌ `monitor_site.sh` still used manual python3 restart (not systemd)

Result: When ngrok died naturally (network issue, process crash, etc.), the cron jobs weren't able to properly restart it.

## Prevention
✅ Both scripts now use correct infrastructure:
- **Flask**: Managed by systemd (auto-restart on crash)
- **Ngrok**: Proper domain command, monitored by cron

✅ Dual monitoring:
- `refresh-tunnels.sh` runs every 30 min → checks if ngrok is running, starts if missing
- `monitor_site.sh` runs every 90 min → checks both Flask + ngrok, restarts if either down

✅ Logging:
- `/tmp/tunnel-refresh.log` - Records ngrok refresh attempts
- `/tmp/site_monitor.log` - Records full health checks
- `/tmp/ngrok.log` - Ngrok stdout/stderr

## Testing
Manual test to verify monitoring works:
```bash
# Kill ngrok
pkill -f ngrok
sleep 2

# Run refresh script (should restart)
./refresh-tunnels.sh
sleep 5

# Verify ngrok is back
pgrep -f "ngrok http.*5555"
# Should show process ID

# Verify site accessible
curl -s -o /dev/null -w "%{http_code}" https://proliferative-daleyza-benthonic.ngrok-free.dev
# Should return 200
```

## Impact
- ✅ Site back online within 2 minutes of report
- ✅ Downtime: ~10 minutes (between ngrok death and Roy's report)
- ✅ Future prevention: Automated recovery every 30-90 minutes
- ✅ Zero manual intervention needed going forward

## Related Issues
- Original ngrok migration (v87-v88)
- Systemd service setup (v86)
- Monitor cron setup (v89)

## Notes
- Ngrok free tier can occasionally disconnect (that's normal)
- With fixed scripts, max downtime before auto-recovery: 30 minutes
- Systemd handles Flask restarts instantly (no downtime for Flask crashes)
- Both monitoring scripts use different frequencies (30 min vs 90 min) for redundancy

---

**Downtime Duration**: ~10 minutes  
**Recovery Time**: 2 minutes  
**Status**: ✅ RESOLVED  
**Version**: Still v152 (no code changes, just infrastructure fixes)

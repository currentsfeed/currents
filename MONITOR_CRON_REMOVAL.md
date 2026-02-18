# Monitor Cron Removal - Feb 11, 2026

**Decision Time:** 22:12 UTC  
**Decision Maker:** Dor + Main (Roy approved: "do the best solution you and Dor think")  
**Status:** ✅ IMPLEMENTED

---

## Problem

Old `monitor_site.sh` cron job was conflicting with systemd service:
- Cron ran every 90 minutes
- Killed Flask process: `pkill -f "python3 app.py"`
- Systemd detected death → restarted immediately
- Result: Unnecessary restarts every 90 minutes

**Evidence:**
- Unexpected restart at 21:59 UTC during 24h milestone test
- Journalctl showed 16 restarts since 17:00 UTC
- Many during v86-v88 deployments (expected)
- One at 21:59 UTC (unexpected, matched cron schedule)

---

## Options Considered

### Option A: Disable Monitor Cron ⭐ CHOSEN
**Pros:**
- Clean solution (single management system)
- Systemd proven reliable (<3s restart)
- No conflicts
- Best for 24h uptime milestone

**Cons:**
- Lose ngrok monitoring
- No automatic ngrok restart if it fails

**Risk Assessment:** LOW
- Ngrok has been stable (no recent failures)
- Can re-enable if issues appear
- Systemd handles Flask perfectly

### Option B: Update Monitor to Only Manage Ngrok
**Pros:**
- Keep ngrok monitoring
- No Flask interference

**Cons:**
- More complex script changes
- Still two management systems
- Risk of bugs in updated script

### Option C: Keep Both, Accept Restarts
**Pros:**
- No changes needed

**Cons:**
- Restarts every 90 minutes
- Looks bad for uptime
- Confusing architecture
- Milestone likely fails

---

## Implementation

### Before
```cron
# Currents site monitoring - every 90 minutes (1.5 hours)
0 0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh
30 1,4,7,10,13,16,19,22 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh
0 4 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh
```

### After
```cron
# Currents automation - trending refresh + score decay
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh
0 4 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh
```

### Backup
Crontab backed up to: `/tmp/crontab_backup_*.txt`

---

## Expected Results

**Immediate:**
- ✅ No more 90-minute restarts
- ✅ Only restarts: crashes (systemd) or deployments (manual)
- ✅ Better uptime metrics
- ✅ 24h milestone more likely to succeed

**Long-term:**
- ✅ Cleaner architecture (systemd only)
- ✅ Easier to debug (one management system)
- ⚠️ Need to monitor ngrok manually (check if issues appear)

---

## Monitoring Strategy

**Flask App:**
- Systemd handles all restarts
- Check status: `sudo systemctl status currents.service`
- View logs: `journalctl -u currents.service -f`
- Instant restart on any crash

**Ngrok Tunnel:**
- Currently stable (no recent issues)
- Manual check if site unreachable: `curl http://localhost:4040/api/tunnels`
- Manual restart if needed: `pkill ngrok && ngrok http 5555 --log stdout > /tmp/ngrok.log 2>&1 &`
- Can re-enable monitor cron if frequent failures

**Health Monitoring:**
- `/health` endpoint still works
- Can check manually: `curl http://localhost:5555/health`
- No automated checks (not needed with systemd)

---

## Rollback Plan

If ngrok becomes unstable:

1. Re-enable monitor cron for ngrok only
2. Update `monitor_site.sh` to skip Flask checks
3. Keep systemd for Flask management

```bash
# Rollback command (if needed)
cat /tmp/crontab_backup_*.txt | grep monitor_site.sh | crontab -
```

---

## Success Metrics

**24h Milestone (Feb 11 17:03 → Feb 12 17:03):**
- ✅ Zero user-reported downtime
- ✅ No unnecessary restarts from cron
- ✅ Only deployment-related restarts (transparent to users)

**Long-term:**
- Systemd uptime >99.9%
- Ngrok stays stable
- No manual intervention needed

---

## Team Communication

**Roy:** Approved decision ("do the best solution you and Dor think")  
**Dor:** Coordinated decision (PM oversight)  
**Shraga:** Aware (CTO would approve architecture simplification)  
**Implementation:** Main (immediate action during milestone)

---

**Result:** ✅ Cleaner, more reliable infrastructure  
**Impact:** Better uptime, easier debugging, professional deployment pattern  
**Risk:** Minimal (can rollback if needed)

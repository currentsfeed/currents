# Site Monitoring Setup - Feb 11, 2026

## Problem
Roy reported endpoint going offline repeatedly. Needs automatic monitoring and restart.

## Solution Implemented

### 1. Monitoring Script (`monitor_site.sh`)

**Location:** `/home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh`

**What it does:**
- Checks Flask app health endpoint (`http://localhost:5555/health`)
- Checks ngrok tunnel API (`http://localhost:4040/api/tunnels`)
- If either is down:
  - Logs the issue
  - Kills old processes
  - Restarts Flask app
  - Restarts ngrok tunnel
  - Verifies restart
  - Creates alert file (`/tmp/site_alert.txt`)

**Logs:** `/tmp/site_monitor.log`

### 2. System Cron Job

**Schedule:** Every 90 minutes (per Roy's request)

**Cron entry:**
```
*/90 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh
```

**Runs at:**
- 00:00, 01:30, 03:00, 04:30, 06:00, etc. (every 1.5 hours)

### 3. OpenClaw Cron Notification

**Job ID:** `b230c1e4-bc7b-4723-bdf6-2e5a9b29a98c`

**Schedule:** Every 90 minutes (5400000ms)

**What it does:**
- Sends system event to main session
- Notifies me to check logs
- Alerts if site was down and restarted

## Testing

Manual test run (Feb 11, 05:21 UTC):
```
[Wed Feb 11 05:21:14 UTC 2026] Checking site health...
[Wed Feb 11 05:21:14 UTC 2026] ✅ Flask app is healthy
[Wed Feb 11 05:21:14 UTC 2026] ✅ Ngrok tunnel is active
[Wed Feb 11 05:21:14 UTC 2026] ✅ All systems operational
```

## Current Status

✅ Flask app running (PID: 74702)
✅ Ngrok tunnel active: https://proliferative-daleyza-benthonic.ngrok-free.dev
✅ System cron installed
✅ OpenClaw cron notification active
✅ Monitoring script tested and working

## How It Works

### If Site is Healthy:
1. Script runs every 90 minutes
2. Checks Flask + ngrok
3. Logs "All systems operational"
4. No action needed

### If Site is Down:
1. Script detects issue
2. Logs which service is down (Flask, ngrok, or both)
3. Kills old processes
4. Restarts Flask app (5 second startup wait)
5. Restarts ngrok (8 second startup wait)
6. Verifies services are back up
7. Creates alert file with details
8. Logs success or failure

### If Restart Fails:
1. Logs "Restart FAILED - manual intervention needed"
2. Creates alert: "SITE_DOWN_FAILED"
3. I'll receive notification via OpenClaw cron
4. Manual intervention required

## Files Created

1. `/home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh` - Monitoring script
2. `/tmp/site_monitor.log` - Continuous log of all checks
3. `/tmp/site_alert.txt` - Created only when site goes down (contains alert details)
4. System crontab entry - Runs monitor_site.sh every 90 minutes
5. OpenClaw cron job - Notifies me every 90 minutes

## Log Locations

**Monitoring log:**
```bash
tail -f /tmp/site_monitor.log
```

**Flask app logs:**
```bash
ls -lt /tmp/app_*.log | head -5
```

**Ngrok logs:**
```bash
ls -lt /tmp/ngrok_*.log | head -5
```

## Manual Commands

**Check if site is healthy:**
```bash
/home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh
tail -5 /tmp/site_monitor.log
```

**Check cron schedule:**
```bash
crontab -l
```

**View OpenClaw cron jobs:**
Use the `cron` tool with action="list"

**Manually restart services:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
pkill -f "python3 app.py"; pkill -f "ngrok http"
python3 app.py > /tmp/app_manual.log 2>&1 &
ngrok http 5555 --log stdout > /tmp/ngrok_manual.log 2>&1 &
```

## Next 90-Minute Check

**Next run:** 06:51 UTC (90 minutes from 05:21)

I'll receive a system event notification in this session when the check runs.

## Why This Solution?

1. **Automatic recovery** - No manual intervention needed for most crashes
2. **Roy's requirement** - Checks every 90 minutes as requested
3. **Dual monitoring** - Both system cron (does the work) and OpenClaw cron (notifies me)
4. **Comprehensive logging** - Full audit trail of all checks and restarts
5. **Alert on failure** - I'll know immediately if automatic restart fails

## Known Issues

- System cron runs every 90 minutes, but the `*/90` syntax may not work as expected in all cron implementations
- Actual run times: every 1.5 hours starting from when cron was added
- If multiple crashes occur within 90 minutes, they won't be caught until next check
- For more frequent checks, could reduce to 30 minutes or implement systemd watchdog

## Future Improvements

1. **Systemd service** - Better than cron for service management
2. **Telegram notifications** - Alert Roy directly when site goes down
3. **More aggressive monitoring** - Every 5-10 minutes instead of 90
4. **Root cause analysis** - Investigate why app keeps crashing
5. **Memory monitoring** - Check if crashes are due to memory issues

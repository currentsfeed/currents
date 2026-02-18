# DEPLOYMENT v171 - Ngrok Auto-Restart Service

**Date**: Feb 15, 2026 09:11 UTC  
**Issue**: Ngrok keeps crashing, causing site downtime  
**Status**: ✅ FIXED - Ngrok now managed by systemd

---

## Problem

Ngrok free tier is unstable and crashes periodically, causing the site to go down. Manual restart was required each time.

**Symptoms:**
- Site returns 404 or connection refused
- Flask service still running
- Ngrok process not found

---

## Solution

Created systemd service for ngrok with automatic restart on crash.

### Ngrok Service File

**Location**: `/etc/systemd/system/ngrok.service`

```ini
[Unit]
Description=Ngrok Tunnel for Currents
After=network.target currents.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/.openclaw/workspace/currents-full-local
Environment=HOME=/home/ubuntu
ExecStart=/usr/local/bin/ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555
Restart=always
RestartSec=5
StandardOutput=append:/home/ubuntu/.openclaw/workspace/currents-full-local/ngrok.log
StandardError=append:/home/ubuntu/.openclaw/workspace/currents-full-local/ngrok.log

[Install]
WantedBy=multi-user.target
```

### Key Features

- **Restart=always** - Restarts ngrok if it crashes
- **RestartSec=5** - Waits 5 seconds before restart
- **Logs** - Appends to ngrok.log (doesn't overwrite)
- **Enabled** - Starts automatically on boot

---

## Commands

### Check Status
```bash
sudo systemctl status ngrok.service
```

### Manual Restart
```bash
sudo systemctl restart ngrok.service
```

### View Logs
```bash
tail -50 /home/ubuntu/.openclaw/workspace/currents-full-local/ngrok.log
# OR
sudo journalctl -u ngrok.service -f
```

### Stop (if needed)
```bash
sudo systemctl stop ngrok.service
```

---

## Benefits

**Before:**
- Ngrok crashes → Site down
- Manual intervention required
- Downtime until noticed

**After:**
- Ngrok crashes → Auto-restarts in 5 seconds
- Zero manual intervention
- ~5 second downtime max
- Automatically starts on server reboot

---

## Services Now Managed by Systemd

1. **currents.service** (Flask app on port 5555)
   - Auto-restart on crash
   - Starts on boot

2. **ngrok.service** (Tunnel)
   - Auto-restart on crash
   - Starts on boot
   - Depends on network + currents

3. **db_viewer.py** (port 5556)
   - Manual start (runs in background)
   - TODO: Convert to systemd service

---

## Removed

**Old cron job** for tunnel refresh:
```bash
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh-tunnels.sh
```

No longer needed - systemd handles auto-restart.

---

## Testing

### Simulate Crash

```bash
# Kill ngrok
sudo pkill -9 ngrok

# Wait 5 seconds
sleep 5

# Check if it restarted
sudo systemctl status ngrok.service
```

Should show:
- Active (running)
- Process ID changed
- Recent restart in logs

---

## Files Changed

- `/etc/systemd/system/ngrok.service` - New systemd service
- Removed refresh-tunnels cron job

---

## Monitoring

### Site Health

The existing monitor_site.sh still runs every 30 minutes and checks:
- Flask responding on port 5555
- Ngrok tunnel accessible
- Restarts both if needed

Now with systemd, both services will auto-restart even between monitoring checks.

---

## Future Improvements

1. Convert db_viewer.py to systemd service
2. Add alerting for multiple restarts (crash loop detection)
3. Consider paid ngrok tier for better stability
4. Add uptime monitoring service

---

**Update Time**: ~2 minutes  
**Status**: ✅ COMPLETE  
**Auto-Restart**: Enabled for both Flask and Ngrok  
**Downtime Prevention**: ~5 second max for ngrok crashes

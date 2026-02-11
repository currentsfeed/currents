#!/bin/bash
# Refresh Localtunnel connections only (prevent 503 errors)
# Called by cron every 30 minutes

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Kill only the localtunnel processes
pkill -f "lt --port" 2>/dev/null
sleep 2

# Restart Localtunnel for Currents
nohup lt --port 5555 --subdomain poor-hands-slide > /tmp/currents-tunnel.log 2>&1 &
sleep 2

# Restart Localtunnel for Database Viewer
nohup lt --port 5556 --subdomain brain-db-viewer > /tmp/db-viewer-tunnel.log 2>&1 &
sleep 2

echo "[$(date)] Tunnels refreshed" >> /tmp/tunnel-refresh.log

#!/bin/bash
# Refresh ngrok tunnel (prevent disconnects)
# Called by cron every 30 minutes

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Check if ngrok tunnel is actually working (not just if process exists)
NGROK_WORKING=false
if pgrep -f "ngrok http.*5555" > /dev/null; then
    # Process exists, but is the tunnel functional?
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://proliferative-daleyza-benthonic.ngrok-free.dev)
    if [ "$HTTP_CODE" = "200" ]; then
        NGROK_WORKING=true
        echo "[$(date)] Ngrok tunnel is working (HTTP 200), skipping" >> /tmp/tunnel-refresh.log
        exit 0
    else
        echo "[$(date)] Ngrok process exists but tunnel broken (HTTP $HTTP_CODE), restarting..." >> /tmp/tunnel-refresh.log
    fi
else
    echo "[$(date)] Ngrok process not found, starting..." >> /tmp/tunnel-refresh.log
fi

# Kill any stale tunnel processes
pkill -f "ngrok" 2>/dev/null
pkill -f "lt --port" 2>/dev/null
sleep 2

# Start ngrok with Currents URL (--url replaces deprecated --domain)
nohup ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
sleep 3

# Verify ngrok started
if pgrep -f "ngrok http.*5555" > /dev/null; then
    echo "[$(date)] Ngrok tunnel started successfully" >> /tmp/tunnel-refresh.log
else
    echo "[$(date)] ERROR: Ngrok failed to start" >> /tmp/tunnel-refresh.log
fi

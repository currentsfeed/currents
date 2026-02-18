#!/bin/bash
# Monitor Currents site every 90 minutes
# Checks both Flask app (systemd) and ngrok tunnel

HEALTH_URL="http://localhost:5555/health"
NGROK_API="http://localhost:4040/api/tunnels"
LOG_FILE="/tmp/site_monitor.log"

echo "[$(date)] Checking site health..." >> $LOG_FILE

# Check Flask app via systemd
if systemctl is-active --quiet currents.service; then
    echo "[$(date)] ✅ Flask app (systemd) is running" >> $LOG_FILE
    APP_OK=true
else
    echo "[$(date)] ❌ Flask app (systemd) is DOWN" >> $LOG_FILE
    APP_OK=false
fi

# Check ngrok tunnel (both process AND functionality)
NGROK_OK=false
if pgrep -f "ngrok http.*5555" > /dev/null; then
    # Process exists, check if tunnel is functional
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://proliferative-daleyza-benthonic.ngrok-free.dev)
    if [ "$HTTP_CODE" = "200" ]; then
        echo "[$(date)] ✅ Ngrok tunnel is working (process running + HTTP 200)" >> $LOG_FILE
        NGROK_OK=true
    else
        echo "[$(date)] ❌ Ngrok tunnel broken (process running but HTTP $HTTP_CODE)" >> $LOG_FILE
        NGROK_OK=false
    fi
else
    echo "[$(date)] ❌ Ngrok process not running" >> $LOG_FILE
    NGROK_OK=false
fi

# If either is down, restart and notify
if [ "$APP_OK" = false ] || [ "$NGROK_OK" = false ]; then
    echo "[$(date)] 🔄 Restarting services..." >> $LOG_FILE
    
    # Restart Flask app via systemd
    if [ "$APP_OK" = false ]; then
        echo "[$(date)] Restarting Flask via systemd..." >> $LOG_FILE
        sudo systemctl restart currents.service
        sleep 3
    fi
    
    # Restart ngrok if down
    if [ "$NGROK_OK" = false ]; then
        echo "[$(date)] Restarting ngrok tunnel..." >> $LOG_FILE
        pkill -f "ngrok" 2>/dev/null
        sleep 2
        cd /home/ubuntu/.openclaw/workspace/currents-full-local
        nohup ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
        sleep 5
    fi
    
    # Verify restart
    sleep 3
    if systemctl is-active --quiet currents.service && pgrep -f "ngrok http.*5555" > /dev/null; then
        echo "[$(date)] ✅ Services restarted successfully" >> $LOG_FILE
        
        # Send notification via OpenClaw system event
        echo "SITE_DOWN_RESTARTED: Currents endpoint was offline. Auto-restarted at $(date). App was down: $APP_OK, Ngrok was down: $NGROK_OK" > /tmp/site_alert.txt
    else
        echo "[$(date)] ❌ Restart FAILED - manual intervention needed" >> $LOG_FILE
        echo "SITE_DOWN_FAILED: Currents endpoint restart FAILED at $(date). Manual intervention required." > /tmp/site_alert.txt
    fi
else
    echo "[$(date)] ✅ All systems operational" >> $LOG_FILE
fi

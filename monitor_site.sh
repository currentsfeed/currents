#!/bin/bash
# Monitor Currents site every 90 minutes
# Checks both Flask app and ngrok tunnel

HEALTH_URL="http://localhost:5555/health"
NGROK_API="http://localhost:4040/api/tunnels"
LOG_FILE="/tmp/site_monitor.log"

echo "[$(date)] Checking site health..." >> $LOG_FILE

# Check Flask app
if curl -s -f "$HEALTH_URL" > /dev/null 2>&1; then
    echo "[$(date)] ✅ Flask app is healthy" >> $LOG_FILE
    APP_OK=true
else
    echo "[$(date)] ❌ Flask app is DOWN" >> $LOG_FILE
    APP_OK=false
fi

# Check ngrok tunnel
if curl -s "$NGROK_API" | grep -q "public_url"; then
    echo "[$(date)] ✅ Ngrok tunnel is active" >> $LOG_FILE
    NGROK_OK=true
else
    echo "[$(date)] ❌ Ngrok tunnel is DOWN" >> $LOG_FILE
    NGROK_OK=false
fi

# If either is down, restart and notify
if [ "$APP_OK" = false ] || [ "$NGROK_OK" = false ]; then
    echo "[$(date)] 🔄 Restarting services..." >> $LOG_FILE
    
    # Kill old processes
    pkill -f "python3 app.py" 2>/dev/null
    pkill -f "ngrok http 5555" 2>/dev/null
    sleep 2
    
    # Restart Flask app
    cd /home/ubuntu/.openclaw/workspace/currents-full-local
    python3 app.py > /tmp/app_auto_restart_$(date +%s).log 2>&1 &
    sleep 5
    
    # Restart ngrok
    ngrok http 5555 --log stdout > /tmp/ngrok_auto_restart_$(date +%s).log 2>&1 &
    sleep 8
    
    # Verify restart
    if curl -s -f "$HEALTH_URL" > /dev/null 2>&1; then
        echo "[$(date)] ✅ Services restarted successfully" >> $LOG_FILE
        
        # Send notification via OpenClaw system event
        echo "SITE_DOWN_RESTARTED: Currents endpoint was offline. Auto-restarted at $(date). App OK: $APP_OK, Ngrok OK: $NGROK_OK" > /tmp/site_alert.txt
    else
        echo "[$(date)] ❌ Restart FAILED - manual intervention needed" >> $LOG_FILE
        echo "SITE_DOWN_FAILED: Currents endpoint restart FAILED at $(date). Manual intervention required." > /tmp/site_alert.txt
    fi
else
    echo "[$(date)] ✅ All systems operational" >> $LOG_FILE
fi

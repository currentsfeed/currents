#!/bin/bash
# Watchdog script to keep Currents app alive

while true; do
    # Check if app is running
    if ! curl -s http://localhost:5555/health > /dev/null 2>&1; then
        echo "[$(date)] App not responding, restarting..."
        
        # Kill old process
        pkill -f "python3 app.py" 2>/dev/null
        sleep 2
        
        # Start new process
        cd /home/ubuntu/.openclaw/workspace/currents-full-local
        python3 app.py > /tmp/currents-app.log 2>&1 &
        
        echo "[$(date)] App restarted"
    fi
    
    # Check every 30 seconds
    sleep 30
done

#!/bin/bash
# Enable BRain v1 personalization system
# Reverses rollback_to_v159.sh

set -e

echo "=========================================="
echo "Enabling BRain v1 personalization"
echo "=========================================="
echo ""

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Step 1: Update systemd service to set BRAIN_V1_ENABLED=true
echo "1. Enabling BRain v1 via environment variable..."
sudo sed -i '/Environment="BRAIN_V1_ENABLED=/d' /etc/systemd/system/currents.service
sudo sed -i '/\[Service\]/a Environment="BRAIN_V1_ENABLED=true"' /etc/systemd/system/currents.service
echo "   ✅ Set BRAIN_V1_ENABLED=true in systemd service"

# Step 2: Reload systemd and restart Flask
echo "2. Reloading systemd and restarting Flask..."
sudo systemctl daemon-reload
sudo systemctl restart currents.service
sleep 3

if sudo systemctl is-active --quiet currents.service; then
    echo "   ✅ Flask restarted successfully"
else
    echo "   ❌ Flask failed to start! Check logs: sudo journalctl -u currents.service -n 50"
    exit 1
fi

# Step 3: Re-add BRain v1 cron jobs
echo "3. Re-adding BRain v1 cron jobs..."

# Backup current crontab
BACKUP_FILE="/tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
crontab -l > "$BACKUP_FILE" 2>/dev/null || true
echo "   ✅ Crontab backed up to $BACKUP_FILE"

# Add BRain v1 jobs if not present
(crontab -l 2>/dev/null | grep -v "compute_velocity.sh" | grep -v "impression_tracker" | grep -v "session_manager"; \
 echo "*/5 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/compute_velocity.sh"; \
 echo "0 4 * * * cd /home/ubuntu/.openclaw/workspace/currents-full-local && python3 -c 'from impression_tracker import impression_tracker; impression_tracker.cleanup_old_impressions()'"; \
 echo "0 3 * * * cd /home/ubuntu/.openclaw/workspace/currents-full-local && python3 -c 'from session_manager import session_manager; session_manager.cleanup_expired_sessions()'") | crontab -

echo "   ✅ Added velocity computation (every 5 min)"
echo "   ✅ Added impression cleanup (daily 4am)"
echo "   ✅ Added session cleanup (daily 3am)"

# Step 4: Run velocity computation once
echo "4. Running initial velocity computation..."
bash compute_velocity.sh 2>&1 | tail -3

# Step 5: Verify BRain v1 APIs working
echo "5. Verifying BRain v1 APIs..."
sleep 2

# Test feed API
FEED_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5555/api/brain/feed \
    -H "Content-Type: application/json" \
    -d '{"user_key": "enable_test", "geo_country": "US", "limit": 5}')
if [ "$FEED_STATUS" = "200" ]; then
    echo "   ✅ /api/brain/feed working (HTTP 200)"
else
    echo "   ⚠️  /api/brain/feed returned HTTP $FEED_STATUS"
fi

# Test user API
USER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5555/api/brain/user/enable_test)
if [ "$USER_STATUS" = "200" ]; then
    echo "   ✅ /api/brain/user working (HTTP 200)"
else
    echo "   ⚠️  /api/brain/user returned HTTP $USER_STATUS"
fi

# Test trending API
TREND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5555/api/brain/trending?scope=global&limit=5")
if [ "$TREND_STATUS" = "200" ]; then
    echo "   ✅ /api/brain/trending working (HTTP 200)"
else
    echo "   ⚠️  /api/brain/trending returned HTTP $TREND_STATUS"
fi

# Step 6: Show status
echo ""
echo "=========================================="
echo "BRain v1 Enabled!"
echo "=========================================="
echo ""
echo "Current state:"
echo "  • BRain v1: ENABLED (via BRAIN_V1_ENABLED=true)"
echo "  • Personalization: NEW SYSTEM (v160)"
echo "  • API endpoints: /api/brain/feed, /api/brain/user, /api/brain/trending"
echo "  • Tracking: integrated with BRain v1"
echo "  • Cron jobs: velocity computation, impression cleanup, session cleanup"
echo ""
echo "To rollback:"
echo "  bash rollback_to_v159.sh"
echo ""
echo "To test:"
echo "  • Visit site: https://proliferative-daleyza-benthonic.ngrok-free.dev"
echo "  • Test API: curl -X POST http://localhost:5555/api/brain/feed -H 'Content-Type: application/json' -d '{\"user_key\": \"roy\", \"geo_country\": \"IL\", \"limit\": 10}'"
echo "  • Check logs: sudo journalctl -u currents.service -n 20"
echo ""

#!/bin/bash
# Rollback to v159 (pre-BRain v1)
# Disables BRain v1 via environment variable

set -e

echo "=========================================="
echo "Rolling back to v159 (pre-BRain v1)"
echo "=========================================="
echo ""

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Step 1: Update systemd service to set BRAIN_V1_ENABLED=false
echo "1. Disabling BRain v1 via environment variable..."
sudo sed -i '/Environment="BRAIN_V1_ENABLED=/d' /etc/systemd/system/currents.service
sudo sed -i '/\[Service\]/a Environment="BRAIN_V1_ENABLED=false"' /etc/systemd/system/currents.service
echo "   ✅ Set BRAIN_V1_ENABLED=false in systemd service"

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

# Step 3: Backup current crontab
echo "3. Backing up crontab..."
BACKUP_FILE="/tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
crontab -l > "$BACKUP_FILE" 2>/dev/null || true
echo "   ✅ Crontab backed up to $BACKUP_FILE"

# Step 4: Remove BRain v1 cron jobs
echo "4. Removing BRain v1 cron jobs..."
(crontab -l 2>/dev/null | grep -v "compute_velocity.sh" | grep -v "impression_tracker" | grep -v "session_manager") | crontab - || true
echo "   ✅ Removed velocity computation, impression cleanup, session cleanup"
echo "   ✅ Preserved: trending refresh, score decay, tunnel refresh, site monitoring"

# Step 5: Verify old system working
echo "5. Verifying old system..."
sleep 2

# Test BRain v1 disabled
FEED_TEST=$(curl -s http://localhost:5555/api/brain/feed \
    -H "Content-Type: application/json" \
    -d '{"user_key": "test", "geo_country": "US", "limit": 5}' 2>&1)
if echo "$FEED_TEST" | grep -q "rollback.*true"; then
    echo "   ✅ BRain v1 API correctly disabled"
elif echo "$FEED_TEST" | grep -q "disabled"; then
    echo "   ✅ BRain v1 API correctly disabled"
else
    echo "   ⚠️  BRain v1 API response: $(echo "$FEED_TEST" | head -1)"
fi

# Test old homepage endpoint
HOMEPAGE_TEST=$(curl -s http://localhost:5555/api/homepage 2>&1)
if echo "$HOMEPAGE_TEST" | grep -q "market_id"; then
    echo "   ✅ Old homepage API working"
else
    echo "   ⚠️  Homepage API may have issues"
fi

# Test tracking
TRACK_TEST=$(curl -s -X POST http://localhost:5555/api/track \
    -H "Content-Type: application/json" \
    -d '{"user_key": "rollback_test", "market_id": "test", "event_type": "click"}' 2>&1)
if echo "$TRACK_TEST" | grep -q "success\|recorded"; then
    echo "   ✅ Tracking still working"
else
    echo "   ⚠️  Tracking may have issues"
fi

# Step 6: Show status
echo ""
echo "=========================================="
echo "Rollback Complete!"
echo "=========================================="
echo ""
echo "Current state:"
echo "  • BRain v1: DISABLED (via BRAIN_V1_ENABLED=false)"
echo "  • Personalization: OLD SYSTEM (v159)"
echo "  • Homepage endpoint: /api/homepage (old)"
echo "  • Tracking: backward compatible"
echo "  • BRain v1 tables: PRESERVED (not dropped)"
echo ""
echo "To re-enable BRain v1:"
echo "  bash enable_brain_v1.sh"
echo ""
echo "To verify:"
echo "  • Visit site: https://proliferative-daleyza-benthonic.ngrok-free.dev"
echo "  • Check service: sudo systemctl status currents.service"
echo "  • Check logs: sudo journalctl -u currents.service -n 20"
echo ""

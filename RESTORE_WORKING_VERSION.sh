#!/bin/bash
# RESTORE WORKING MOBILE FEED - v167
# Use this script to restore the last known working mobile feed

set -e

echo "🔄 Restoring working mobile feed (v167)..."

# Backup current version first
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/before_restore_$TIMESTAMP
cp templates/feed_mobile.html backups/before_restore_$TIMESTAMP/ 2>/dev/null || true

# Restore working version
cp backups/v167_working/feed_mobile.html templates/feed_mobile.html

echo "✅ Restored feed_mobile.html from v167"

# Restart service
sudo systemctl restart currents.service

echo "✅ Service restarted"
echo ""
echo "🎉 Working mobile feed restored!"
echo "Test at: https://proliferative-daleyza-benthonic.ngrok-free.dev/"
echo ""
echo "Backup of previous version saved to: backups/before_restore_$TIMESTAMP/"

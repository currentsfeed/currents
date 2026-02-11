#!/bin/bash
# Fix hero section and belief currents visibility

echo "🔧 Fixing hero section and belief currents..."

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Backup
cp templates/index-v2.html .backups/index-v2.html.backup-$(date +%s)

# 1. Make belief currents bar bigger and more visible
sed -i 's/class="h-1.5 bg-gray-800/class="h-3 bg-gray-800/' templates/index-v2.html
sed -i 's/text-\[9px\]/text-xs/g' templates/index-v2.html
sed -i 's/text-\[10px\]/text-xs/g' templates/index-v2.html

# 2. Ensure hero section is properly visible
sed -i 's/h-\[550px\]/h-\[650px\]/' templates/index-v2.html

# 3. Make belief currents container more prominent
sed -i 's/bg-black\/70/bg-black\/80/' templates/index-v2.html
sed -i 's/bg-black\/60/bg-black\/70/' templates/index-v2.html

echo "✅ Fixes applied!"
echo "🔄 Restart the app to see changes"

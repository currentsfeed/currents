#!/bin/bash
# WalletConnect Setup Script
# Usage: ./setup-walletconnect.sh YOUR_PROJECT_ID

if [ -z "$1" ]; then
    echo "❌ Error: Project ID required"
    echo ""
    echo "Usage: ./setup-walletconnect.sh YOUR_PROJECT_ID"
    echo ""
    echo "Get your Project ID from: https://cloud.walletconnect.com/"
    echo "Example: ./setup-walletconnect.sh a1b2c3d4e5f6..."
    exit 1
fi

PROJECT_ID="$1"
echo "🔧 Setting up WalletConnect with Project ID: $PROJECT_ID"

# Create config file
cat > config_walletconnect.py << EOF
# WalletConnect Configuration
WALLETCONNECT_PROJECT_ID = '$PROJECT_ID'
EOF

echo "✅ Config file created: config_walletconnect.py"

# Update app.py to load config
if ! grep -q "config_walletconnect" app.py; then
    echo ""
    echo "⚠️  Manual step required:"
    echo "Add this to app.py:"
    echo ""
    echo "from config_walletconnect import WALLETCONNECT_PROJECT_ID"
    echo ""
    echo "@app.context_processor"
    echo "def inject_walletconnect():"
    echo "    return {'walletconnect_project_id': WALLETCONNECT_PROJECT_ID}"
    echo ""
fi

echo "✅ Done! Project ID configured."
echo ""
echo "Next steps:"
echo "1. Restart Flask app: pkill -f app.py && python3 app.py &"
echo "2. Test wallet connection at: https://poor-hands-slide.loca.lt"

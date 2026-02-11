#!/bin/bash

# Quick test script for Wallet v2
# Run this to test the wallet implementation immediately

echo "======================================"
echo "🔗 WALLET V2 - QUICK TEST"
echo "======================================"
echo ""

# Check if files exist
echo "📁 Checking files..."
files=("wallet_v2.html" "demo_transaction.html" "wallet_integration_guide.md" "WALLET-V2-README.md")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING!)"
        exit 1
    fi
done

echo ""
echo "======================================"
echo "🚀 Starting local server..."
echo "======================================"
echo ""
echo "Test URLs:"
echo "  • http://localhost:8080/wallet_v2.html"
echo "  • http://localhost:8080/demo_transaction.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "======================================"
echo ""

# Start server
python3 -m http.server 8080

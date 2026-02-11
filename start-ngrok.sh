#!/bin/bash
# Start Currents with Ngrok (more reliable than localtunnel)

echo "🌊 Starting Currents with Ngrok..."

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Stop old processes
echo "🛑 Stopping old processes..."
pkill -f "python.*app.py" 2>/dev/null
pkill -f "python.*db_viewer.py" 2>/dev/null
pkill -f "ngrok" 2>/dev/null
sleep 2

# Start Currents app
echo "🚀 Starting Currents app (port 5555)..."
nohup python3 app.py > /tmp/currents-app.log 2>&1 &
sleep 3

# Start Database Viewer
echo "🔍 Starting Database Viewer (port 5556)..."
nohup python3 db_viewer.py > /tmp/db-viewer.log 2>&1 &
sleep 2

# Start Ngrok tunnel
echo "🌐 Starting Ngrok tunnel..."
nohup ngrok http 5555 > /tmp/ngrok.log 2>&1 &
sleep 5

# Get tunnel URL
echo ""
echo "✅ Status Check:"
echo ""

# Check app
if curl -s http://localhost:5555/health > /dev/null; then
    echo "✅ Currents app: Running"
else
    echo "❌ Currents app: Failed"
fi

# Check DB viewer
if curl -s http://localhost:5556/health > /dev/null; then
    echo "✅ Database Viewer: Running"
else
    echo "❌ Database Viewer: Failed"
fi

# Get ngrok URL
echo ""
echo "🌐 Ngrok URL:"
echo ""
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null)

if [ ! -z "$NGROK_URL" ]; then
    echo "$NGROK_URL"
    echo ""
    echo "✅ Done! Currents is running."
    echo ""
    echo "📊 Database: $(sqlite3 brain.db 'SELECT COUNT(*) FROM markets;') markets loaded"
else
    echo "❌ Ngrok tunnel failed to start"
    echo "Check logs: tail -20 /tmp/ngrok.log"
fi

echo ""

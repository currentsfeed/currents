#!/bin/bash
# Currents - One-Command Startup Script
# Usage: ./start.sh

echo "🌊 Starting Currents..."
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Kill any existing processes
echo "🛑 Stopping old processes..."
pkill -f "python3 app.py" 2>/dev/null
pkill -f "python3 db_viewer.py" 2>/dev/null
pkill -f "python3 rain_api_mock.py" 2>/dev/null
pkill -f "lt --port" 2>/dev/null
sleep 2

# Start Currents app
echo "🚀 Starting Currents app (port 5555)..."
python3 app.py > /tmp/currents-app.log 2>&1 &
sleep 2

# Start Database Viewer
echo "🔍 Starting Database Viewer (port 5556)..."
python3 db_viewer.py > /tmp/db-viewer.log 2>&1 &
sleep 2

# Start Localtunnel for Currents
echo "🌐 Starting Currents tunnel..."
nohup lt --port 5555 --subdomain poor-hands-slide > /tmp/currents-tunnel.log 2>&1 &
sleep 2

# Start Localtunnel for Database Viewer
echo "🌐 Starting Database Viewer tunnel..."
nohup lt --port 5556 --subdomain brain-db-viewer > /tmp/db-viewer-tunnel.log 2>&1 &
sleep 3

# Check status
echo ""
echo "✅ Status Check:"
echo ""

# Check app
if curl -s http://localhost:5555/health > /dev/null 2>&1; then
    echo "✅ Currents app: Running"
else
    echo "❌ Currents app: Failed"
fi

# Check database viewer
if curl -s http://localhost:5556/ > /dev/null 2>&1; then
    echo "✅ Database Viewer: Running"
else
    echo "❌ Database Viewer: Failed"
fi

# Show tunnel URLs
echo ""
echo "🌐 Tunnel URLs:"
if [ -f /tmp/currents-tunnel.log ]; then
    grep "your url is" /tmp/currents-tunnel.log
fi
if [ -f /tmp/db-viewer-tunnel.log ]; then
    grep "your url is" /tmp/db-viewer-tunnel.log
fi

echo ""
echo "🔑 Password: 35.172.150.243"
echo ""
echo "✅ Done! Currents is running."
echo ""
echo "📊 Database: $(sqlite3 brain.db 'SELECT COUNT(*) FROM markets;') markets loaded"
echo ""

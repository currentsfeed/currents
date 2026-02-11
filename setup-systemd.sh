#!/bin/bash
# Setup systemd service for Currents (auto-restart on crash)

echo "🔧 Setting up systemd service for Currents..."

# Stop current running instance
echo "🛑 Stopping current Flask instance..."
pkill -f "python.*app.py"
sleep 2

# Copy service file to systemd
echo "📝 Installing systemd service..."
sudo cp currents.service /etc/systemd/system/currents.service

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable service (start on boot)
echo "✅ Enabling service..."
sudo systemctl enable currents.service

# Start service
echo "🚀 Starting Currents service..."
sudo systemctl start currents.service

# Wait and check status
sleep 3
echo ""
echo "📊 Service Status:"
sudo systemctl status currents.service --no-pager | head -15

echo ""
echo "✅ Setup complete!"
echo ""
echo "📌 Useful commands:"
echo "   sudo systemctl status currents    # Check status"
echo "   sudo systemctl restart currents   # Manual restart"
echo "   sudo systemctl stop currents      # Stop service"
echo "   sudo journalctl -u currents -f    # View logs"
echo ""

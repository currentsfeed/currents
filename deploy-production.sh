#!/bin/bash
#
# Currents Production Deployment Script
# Automated setup for Ubuntu 22.04 server
#
# Usage: ./deploy-production.sh YOUR_DOMAIN_NAME
# Example: ./deploy-production.sh currents.global
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if domain provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Domain name required${NC}"
    echo "Usage: ./deploy-production.sh YOUR_DOMAIN"
    echo "Example: ./deploy-production.sh currents.global"
    exit 1
fi

DOMAIN=$1
APP_DIR="/var/www/currents"
USER="currents"

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Currents Production Deployment${NC}"
echo -e "${GREEN}  Domain: $DOMAIN${NC}"
echo -e "${GREEN}================================================${NC}"

# Step 1: System Updates
echo -e "\n${YELLOW}[1/10] Updating system packages...${NC}"
apt update && apt upgrade -y

# Step 2: Install Dependencies
echo -e "\n${YELLOW}[2/10] Installing dependencies...${NC}"
apt install -y python3.11 python3.11-venv python3-pip nginx certbot python3-certbot-nginx \
    sqlite3 git curl supervisor

# Step 3: Create Application User
echo -e "\n${YELLOW}[3/10] Creating application user...${NC}"
if ! id -u $USER > /dev/null 2>&1; then
    useradd -m -s /bin/bash $USER
    echo "User $USER created"
else
    echo "User $USER already exists"
fi

# Step 4: Create Application Directory
echo -e "\n${YELLOW}[4/10] Setting up application directory...${NC}"
mkdir -p $APP_DIR
chown -R $USER:$USER $APP_DIR

# Step 5: Copy Application Files
echo -e "\n${YELLOW}[5/10] Copying application files...${NC}"
# This assumes files are in current directory
cp -r ./* $APP_DIR/ 2>/dev/null || echo "Files already in place"
chown -R $USER:$USER $APP_DIR

# Step 6: Setup Python Virtual Environment
echo -e "\n${YELLOW}[6/10] Setting up Python virtual environment...${NC}"
cd $APP_DIR
sudo -u $USER python3.11 -m venv venv
sudo -u $USER venv/bin/pip install --upgrade pip

# Step 7: Install Python Dependencies
echo -e "\n${YELLOW}[7/10] Installing Python dependencies...${NC}"
if [ -f requirements.txt ]; then
    sudo -u $USER venv/bin/pip install -r requirements.txt
else
    echo "Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
Flask==3.0.2
Flask-CORS==4.0.0
Werkzeug==3.1.5
python-dotenv==1.0.1
requests==2.31.0
EOF
    sudo -u $USER venv/bin/pip install -r requirements.txt
fi

# Step 8: Configure Nginx
echo -e "\n${YELLOW}[8/10] Configuring Nginx...${NC}"
cat > /etc/nginx/sites-available/currents << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://127.0.0.1:5555;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Static files (if needed)
    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/currents /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Step 9: Setup Systemd Service
echo -e "\n${YELLOW}[9/10] Creating systemd service...${NC}"
cat > /etc/systemd/system/currents.service << EOF
[Unit]
Description=Currents Flask Application
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/python3 $APP_DIR/app.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
systemctl daemon-reload
systemctl enable currents.service
systemctl start currents.service

# Step 10: Setup SSL Certificate
echo -e "\n${YELLOW}[10/10] Setting up SSL certificate...${NC}"
echo "Waiting 10 seconds for DNS propagation..."
sleep 10

certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN --redirect

# Final checks
echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\n${YELLOW}Service Status:${NC}"
systemctl status currents.service --no-pager -l

echo -e "\n${YELLOW}Nginx Status:${NC}"
systemctl status nginx --no-pager -l

echo -e "\n${YELLOW}Site URL:${NC}"
echo -e "  https://$DOMAIN"
echo -e "  https://www.$DOMAIN"

echo -e "\n${YELLOW}Management Commands:${NC}"
echo -e "  View logs:      sudo journalctl -u currents.service -f"
echo -e "  Restart app:    sudo systemctl restart currents.service"
echo -e "  Check status:   sudo systemctl status currents.service"
echo -e "  Restart nginx:  sudo systemctl restart nginx"

echo -e "\n${YELLOW}Database Location:${NC}"
echo -e "  $APP_DIR/brain.db"

echo -e "\n${GREEN}Deployment successful! 🚀${NC}"
echo -e "${YELLOW}Note: If site not loading, DNS may still be propagating (can take up to 48h)${NC}"

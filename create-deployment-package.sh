#!/bin/bash
#
# Create Currents Production Deployment Package
# Creates a tar.gz with all necessary files
#

set -e

PACKAGE_NAME="currents-production-$(date +%Y%m%d-%H%M%S).tar.gz"
TEMP_DIR="currents-production-temp"

echo "================================================"
echo "  Creating Currents Deployment Package"
echo "================================================"

# Clean up old temp directory if exists
rm -rf $TEMP_DIR

# Create temporary directory structure
mkdir -p $TEMP_DIR

echo "Copying files..."

# Copy application files
cp app.py $TEMP_DIR/
cp brain.db $TEMP_DIR/
cp requirements.txt $TEMP_DIR/
cp deploy-production.sh $TEMP_DIR/
cp PRODUCTION_DEPLOYMENT_GUIDE.md $TEMP_DIR/README.md

# Copy Python modules
cp feed_composer.py $TEMP_DIR/
cp impression_tracker.py $TEMP_DIR/
cp brain_v1_config.json $TEMP_DIR/
cp compute_trending.py $TEMP_DIR/
cp personalization.py $TEMP_DIR/ 2>/dev/null || echo "personalization.py not found (optional)"

# Copy directories
cp -r static $TEMP_DIR/
cp -r templates $TEMP_DIR/

# Create .env template
cat > $TEMP_DIR/.env.example << 'EOF'
# Production Environment Variables
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=CHANGE_THIS_TO_RANDOM_STRING
DATABASE_PATH=brain.db
PORT=5555
HOST=0.0.0.0
EOF

# Create README for package
cat > $TEMP_DIR/QUICK_START.md << 'EOF'
# Currents Production - Quick Start

## Prerequisites
- Ubuntu 22.04 server with root access
- Domain name pointing to server IP
- SSH access to server

## Deployment Steps

### 1. Copy files to server
```bash
scp currents-production-*.tar.gz root@YOUR_SERVER_IP:/root/
```

### 2. SSH into server
```bash
ssh root@YOUR_SERVER_IP
```

### 3. Extract and deploy
```bash
cd /root
tar -xzf currents-production-*.tar.gz
cd currents-production-temp
chmod +x deploy-production.sh
./deploy-production.sh YOUR_DOMAIN.com
```

### 4. Done!
Your site will be live at https://YOUR_DOMAIN.com

## Post-Deployment

### View logs
```bash
sudo journalctl -u currents.service -f
```

### Restart application
```bash
sudo systemctl restart currents.service
```

### Update WalletConnect
1. Go to https://cloud.walletconnect.com
2. Create new project
3. Add production domain
4. Update Project ID in code

## Support
Full guide: README.md
EOF

# Create the tar.gz
echo "Creating archive..."
tar -czf $PACKAGE_NAME $TEMP_DIR

# Cleanup
rm -rf $TEMP_DIR

# Get file size
SIZE=$(du -h $PACKAGE_NAME | cut -f1)

echo ""
echo "================================================"
echo "  Package Created Successfully!"
echo "================================================"
echo "File: $PACKAGE_NAME"
echo "Size: $SIZE"
echo ""
echo "Next steps:"
echo "1. Copy to production server: scp $PACKAGE_NAME root@SERVER_IP:/root/"
echo "2. SSH into server: ssh root@SERVER_IP"
echo "3. Extract: tar -xzf $PACKAGE_NAME"
echo "4. Deploy: cd currents-production-temp && ./deploy-production.sh YOUR_DOMAIN"
echo ""

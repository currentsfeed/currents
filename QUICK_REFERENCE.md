# Currents Deployment - Quick Reference Card

## 📦 Package Details

**File**: `currents-production-20260218-115852.tar.gz`  
**Size**: 133MB  
**Location**: `/home/ubuntu/.openclaw/workspace/currents-full-local/`  
**Dev Server IP**: `35.172.150.243`  
**Dev Server User**: `ubuntu`

---

## 🚀 Quick Deployment (Copy-Paste Commands)

### Step 1: Create DigitalOcean Server
- Sign up: https://digitalocean.com
- Create: Ubuntu 22.04, 2GB RAM, $12/month
- Get your production server IP

### Step 2: Transfer Package (Server-to-Server)

```bash
# SSH into your NEW production server
ssh root@YOUR_PROD_SERVER_IP

# Copy package from dev server to production
scp ubuntu@35.172.150.243:/home/ubuntu/.openclaw/workspace/currents-full-local/currents-production-20260218-115852.tar.gz /root/
```

### Step 3: Deploy

```bash
# On production server
cd /root
tar -xzf currents-production-20260218-115852.tar.gz
cd currents-production-temp
chmod +x deploy-production.sh
./deploy-production.sh YOUR_DOMAIN.com
```

### Step 4: Done!
Visit: `https://YOUR_DOMAIN.com`

---

## 📁 Files Sent to Telegram

✅ **Documentation:**
- START_HERE.md - Main overview
- DIGITALOCEAN_SETUP.md - Step-by-step guide ⭐
- CREDENTIALS_CHECKLIST.md - Track accounts
- PRODUCTION_DEPLOYMENT_GUIDE.md - General reference
- TRANSFER_PACKAGE.md - How to get full package

✅ **Deployment Files:**
- deploy-production.sh - Automated setup script
- requirements.txt - Python dependencies

❌ **Full Package (133MB):** Too large for Telegram
- Use server-to-server transfer (see TRANSFER_PACKAGE.md)

---

## 💰 Costs

**Monthly:**
- DigitalOcean server: $12/month
- Backups: $2/month (optional)
- Domain: ~$1.25/month
- **Total: ~$15/month**

**One-time:**
- Domain: $10-15/year

---

## 🔑 What You Need

**To start deployment:**
1. Domain name (e.g., currents.global)
2. DigitalOcean account (https://digitalocean.com)
3. Credit card (for server)
4. 30 minutes

**After server created:**
5. Production server IP
6. SSH access (automatic with DigitalOcean)

**Optional (later):**
7. WalletConnect Project ID (for wallet features)

---

## ⚡ Fastest Path (30 minutes)

1. **Create DigitalOcean account** (5 min)
   - https://digitalocean.com
   - Sign up + add payment

2. **Create Droplet** (5 min)
   - Ubuntu 22.04, 2GB RAM, closest region
   - Name: `currents-prod`
   - Copy IP address

3. **Point DNS** (5 min)
   - Login to domain registrar
   - Add A record: `@` → Your server IP
   - Add A record: `www` → Your server IP

4. **Transfer & Deploy** (15 min)
   - SSH into production server
   - Copy package from dev server (scp command above)
   - Extract and run deploy script
   - Done!

---

## 🆘 Need Help?

**Documentation order:**
1. Read: START_HERE.md (overview)
2. Follow: DIGITALOCEAN_SETUP.md (detailed steps)
3. Reference: TRANSFER_PACKAGE.md (for getting package)

**Common Issues:**
- **DNS not resolving?** Wait 30 minutes
- **SSL failed?** Make sure DNS is pointing to server first
- **Site not loading?** Check logs: `sudo journalctl -u currents.service -f`
- **Can't SSH?** Use key: `ssh -i ~/.ssh/currents_prod root@IP`

---

## 📊 What You're Deploying

**Current Features:**
- 353 markets (134 sports, 48 tech, 42 politics, etc.)
- BRain v1 personalization engine
- Mobile TikTok-style feed
- Desktop grid layout
- Yaniv special market (?yaniv=1 access)
- 10 Japanese markets (geo-restricted)
- Waitlist system (54 submissions)
- SSL/HTTPS automatic
- Auto-restart on crash

**All working features from development!**

---

## 🎯 Next Step: Read DIGITALOCEAN_SETUP.md

That file has screenshots, detailed explanations, and troubleshooting.

**Quick questions?** I'm here to help!

---

**Dev Server Details:**
- IP: 35.172.150.243
- User: ubuntu
- Package path: `/home/ubuntu/.openclaw/workspace/currents-full-local/currents-production-20260218-115852.tar.gz`

**Production Setup:**
- Platform: DigitalOcean (recommended)
- OS: Ubuntu 22.04 LTS
- Size: 2GB RAM / 1 CPU / 50GB SSD
- Cost: $12/month

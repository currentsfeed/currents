# 🚀 Currents Production Deployment - START HERE

**Everything you need to deploy Currents to production**

---

## 📦 WHAT YOU HAVE

### 1. Complete Deployment Package
**File**: `currents-production-20260218-115852.tar.gz` (133MB)  
**Location**: `/home/ubuntu/.openclaw/workspace/currents-full-local/`

**Contains:**
- Full Currents application (app.py + all modules)
- Database with 353 markets (including 20 new sports markets + Yaniv market)
- All images and static assets
- HTML templates
- Automated deployment script
- Configuration files

### 2. Documentation
- ✅ `PRODUCTION_DEPLOYMENT_GUIDE.md` - Complete overview
- ✅ `DIGITALOCEAN_SETUP.md` - Step-by-step DigitalOcean guide (RECOMMENDED)
- ✅ `CREDENTIALS_CHECKLIST.md` - Track all accounts and passwords
- ✅ `deploy-production.sh` - Automated deployment script

---

## 🎯 WHAT YOU NEED

### Required (to deploy):
1. **Domain name** (e.g., currents.global)
   - From: Namecheap, GoDaddy, Cloudflare, etc.
   - Cost: ~$10-15/year
   
2. **Server** (Ubuntu 22.04)
   - Recommended: DigitalOcean 2GB droplet
   - Cost: $12/month
   - Alternative: AWS EC2 t3.small ($18/month)

3. **DNS access** (to point domain to server)

### Optional (for full features):
4. **WalletConnect Project ID** (for wallet connections)
5. **Email service** (SendGrid free tier for waitlist emails)

---

## ⚡ QUICK START (Recommended Path)

### Option 1: DigitalOcean (Easiest - 30 minutes total)

#### Step 1: Create Accounts (5 min)
- [ ] Sign up at https://digitalocean.com
- [ ] Get domain at https://namecheap.com (if you don't have one)

#### Step 2: Setup Server (5 min)
- [ ] Create DigitalOcean droplet (2GB, Ubuntu 22.04)
- [ ] Get server IP address
- [ ] Point domain DNS to server IP

**Detailed guide**: `DIGITALOCEAN_SETUP.md`

#### Step 3: Deploy (15 min)
```bash
# Copy package to server
scp currents-production-*.tar.gz root@YOUR_SERVER_IP:/root/

# SSH into server
ssh root@YOUR_SERVER_IP

# Extract and deploy
cd /root
tar -xzf currents-production-*.tar.gz
cd currents-production-temp
./deploy-production.sh YOUR_DOMAIN.com
```

#### Step 4: Done! (5 min)
- Visit https://YOUR_DOMAIN.com
- Verify site works
- Update WalletConnect Project ID

---

## 📚 DOCUMENTATION OVERVIEW

### For Setup Phase:

**1. DIGITALOCEAN_SETUP.md** ⭐ START HERE
- Complete step-by-step guide
- Screenshots and examples
- Troubleshooting section
- Cost breakdown

**2. CREDENTIALS_CHECKLIST.md**
- Track all accounts
- Store passwords securely
- Pre-deployment checklist
- Post-deployment verification

**3. PRODUCTION_DEPLOYMENT_GUIDE.md**
- General overview
- Multiple platform options (DigitalOcean, AWS, etc.)
- Architecture explanation
- Requirements

### For Deployment Phase:

**4. deploy-production.sh**
- Automated deployment script
- One command deploys everything
- Sets up nginx, SSL, systemd
- Usage: `./deploy-production.sh YOUR_DOMAIN.com`

**5. requirements.txt**
- Python dependencies
- Auto-installed by deploy script

---

## 🔑 CREDENTIALS YOU'LL NEED

### Create These Accounts:

1. **DigitalOcean**
   - URL: https://digitalocean.com
   - For: Server hosting
   - Cost: $12/month

2. **Domain Registrar** (if you don't have domain)
   - Recommended: Namecheap (https://namecheap.com)
   - For: Domain name
   - Cost: $10-15/year

3. **WalletConnect Cloud**
   - URL: https://cloud.walletconnect.com
   - For: Wallet connection features
   - Cost: Free

### Track Everything:
Use `CREDENTIALS_CHECKLIST.md` to store all logins securely!

---

## 💰 TOTAL COSTS

### Monthly Recurring:
- Server: $12/month (DigitalOcean 2GB)
- Backups: $2/month (recommended)
- Domain: ~$1.25/month ($15/year)
- **Total: ~$15/month**

### One-Time:
- Domain registration: $10-15 (first year)
- SSL certificate: $0 (Let's Encrypt free)

### Free Tier Options:
- DigitalOcean: Often has $200 credit for new accounts
- WalletConnect: Free tier (unlimited for now)
- SendGrid: 100 emails/day free

**No surprises, no hidden costs!**

---

## 🚦 DEPLOYMENT STATUS CHECKLIST

### Phase 1: Preparation
- [ ] Read DIGITALOCEAN_SETUP.md
- [ ] Create DigitalOcean account
- [ ] Purchase/have domain ready
- [ ] Fill out CREDENTIALS_CHECKLIST.md

### Phase 2: Server Setup
- [ ] Create DigitalOcean droplet
- [ ] Generate SSH keys
- [ ] Get server IP address
- [ ] Point DNS to server

### Phase 3: Deployment
- [ ] Copy deployment package to server
- [ ] Run deploy-production.sh script
- [ ] Verify SSL certificate installed
- [ ] Check site loads

### Phase 4: Verification
- [ ] Test main feed
- [ ] Test market detail pages
- [ ] Test user switcher
- [ ] Test mobile view
- [ ] Verify SSL (green lock icon)

### Phase 5: Configuration
- [ ] Update WalletConnect Project ID
- [ ] Setup monitoring (optional)
- [ ] Enable backups
- [ ] Test Yaniv market access (?yaniv=1)

---

## 🎬 STEP-BY-STEP VISUAL GUIDE

### 1️⃣ Download Package (on current dev server)
```bash
# Already created at:
/home/ubuntu/.openclaw/workspace/currents-full-local/currents-production-20260218-115852.tar.gz

# Copy to your local machine:
scp ubuntu@DEV_SERVER:/path/to/package.tar.gz ~/Downloads/
```

### 2️⃣ Create DigitalOcean Account
- Go to https://digitalocean.com
- Click "Sign Up"
- Verify email
- Add payment method
- Look for promo code ($200 credit often available)

### 3️⃣ Create Server
- Click green "Create" button
- Choose "Droplets"
- Select: Ubuntu 22.04, 2GB RAM, closest region
- Add SSH key (generate first: `ssh-keygen -t ed25519`)
- Name: `currents-prod`
- Click "Create Droplet"
- Copy IP address when ready

### 4️⃣ Setup DNS
- Login to domain registrar (Namecheap/GoDaddy/etc.)
- Find DNS settings
- Add A record: `@` → Your server IP
- Add A record: `www` → Your server IP
- Save changes

### 5️⃣ Deploy Application
```bash
# Copy package to server
scp -i ~/.ssh/currents_prod ~/Downloads/currents-production-*.tar.gz root@SERVER_IP:/root/

# SSH into server
ssh -i ~/.ssh/currents_prod root@SERVER_IP

# Extract
cd /root
tar -xzf currents-production-*.tar.gz
cd currents-production-temp

# Deploy!
./deploy-production.sh YOUR_DOMAIN.com
```

### 6️⃣ Verify & Celebrate! 🎉
- Visit https://YOUR_DOMAIN.com
- Should see Currents site with SSL
- Test feed, markets, mobile view
- Done!

---

## 🆘 HELP & SUPPORT

### If Something Goes Wrong:

**DNS not resolving?**
- Wait 30 minutes (DNS propagation)
- Check with: `dig YOUR_DOMAIN.com`

**SSL certificate failed?**
- Make sure DNS is pointing to server first
- Wait 30 minutes after DNS change
- Retry: `sudo certbot --nginx -d YOUR_DOMAIN.com`

**Site not loading?**
- Check service: `sudo systemctl status currents.service`
- Check logs: `sudo journalctl -u currents.service -f`
- Restart: `sudo systemctl restart currents.service`

**Can't SSH?**
- Check IP is correct
- Use SSH key: `ssh -i ~/.ssh/currents_prod root@IP`
- Check DigitalOcean firewall settings

### Get More Help:
- DigitalOcean: https://docs.digitalocean.com
- Let's Encrypt: https://certbot.eff.org/
- Check deployment script logs on server

---

## 📊 WHAT'S IN THE DATABASE

Current deployment includes:
- **353 total markets**
- **134 Sports markets** (20 brand new, Feb 19-24)
- **1 Special market** (Yaniv - access via ?yaniv=1)
- **10 Japanese markets** (geo-restricted to Japan)
- **All past events removed** (clean, fresh content)

Categories:
- Sports: 134
- Technology: 48
- Politics: 42
- Economics: 34
- World: 32
- Crypto: 23
- Entertainment: 16
- Culture: 14
- Crime: 9
- Business: 1 (Yaniv)

---

## ✅ WHAT YOU GET

### After Deployment:
- ✅ Full Currents site at your domain
- ✅ SSL certificate (HTTPS with green lock)
- ✅ Auto-restart on crash (systemd)
- ✅ Professional nginx setup
- ✅ 353 markets ready to go
- ✅ Mobile-optimized TikTok feed
- ✅ BRain v1 personalization
- ✅ Yaniv special access market
- ✅ All features from dev environment

### What Works Out of Box:
- Feed personalization
- Market detail pages
- User switching
- Mobile/desktop responsive
- Waitlist system
- Geo-targeting (Japan, Israel)
- Special market access (Yaniv)
- Image loading
- Probability graphs

---

## 🎯 NEXT STEPS

**Right Now:**
1. Open `DIGITALOCEAN_SETUP.md`
2. Follow steps 1-10
3. Deploy!

**After Deployment:**
1. Test thoroughly
2. Update WalletConnect Project ID
3. Share with team
4. Monitor for 24h
5. Enable backups
6. Setup uptime monitoring (optional)

**Questions?**
- Review documentation files
- Check deployment script comments
- All guides are self-contained

---

## 📁 FILE STRUCTURE

```
currents-full-local/
├── START_HERE.md                              ← YOU ARE HERE
├── DIGITALOCEAN_SETUP.md                      ← Start here for deployment
├── PRODUCTION_DEPLOYMENT_GUIDE.md             ← General overview
├── CREDENTIALS_CHECKLIST.md                   ← Track accounts
├── currents-production-20260218-115852.tar.gz ← Deployment package (133MB)
├── deploy-production.sh                       ← Automated deploy script
└── requirements.txt                           ← Python dependencies
```

---

## 🚀 READY TO DEPLOY?

**Recommended order:**
1. Read this file (you're doing it! ✓)
2. Open `DIGITALOCEAN_SETUP.md`
3. Follow steps 1-10
4. Celebrate! 🎉

**Estimated time**: 30-45 minutes from start to finish

**Good luck! You've got this! 💪**

---

*Last updated: February 18, 2026*  
*Package version: v205*  
*Markets: 353 (including 20 new sports + Yaniv special access)*

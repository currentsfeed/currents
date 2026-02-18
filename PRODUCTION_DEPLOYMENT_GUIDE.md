# Currents Production Deployment Guide

**Complete deployment to new production server**

## 1. SERVER REQUIREMENTS

### Recommended Platform: **DigitalOcean** (simplest, best value)
**Alternative options**: AWS EC2, Linode, Vultr, Hetzner

### Server Specs:
- **Size**: 2GB RAM / 1 CPU / 50GB SSD ($12/month DigitalOcean)
- **OS**: Ubuntu 22.04 LTS
- **Location**: Choose closest to your users (US East, EU, etc.)

### Why DigitalOcean?
- Simple setup (5 minutes)
- Great documentation
- $200 free credit for new accounts
- Easy firewall management
- One-click backups

---

## 2. CREDENTIALS & ACCESS NEEDED

### Domain (currents.global or your choice)
- [ ] Domain registrar access (Namecheap, GoDaddy, Cloudflare, etc.)
- [ ] Ability to add DNS A records

### WalletConnect
- [ ] WalletConnect Cloud account (https://cloud.walletconnect.com)
- [ ] Create new project for production
- [ ] Get Project ID for production domain

### Server Access
- [ ] Root SSH access to new server
- [ ] SSH key (we'll generate one)

### Optional (for advanced features)
- [ ] Email service (SendGrid, AWS SES) for waitlist confirmations
- [ ] Analytics (Plausible, Google Analytics)
- [ ] Error tracking (Sentry)

---

## 3. PLATFORM SETUP

### Option A: DigitalOcean (Recommended)

#### Step 1: Create Account
1. Go to https://digitalocean.com
2. Sign up with email
3. Add payment method (credit card)
4. Apply promo code for free credit if available

#### Step 2: Create Droplet
1. Click "Create" → "Droplets"
2. **Choose Region**: New York, San Francisco, or Frankfurt (closest to users)
3. **Choose Image**: Ubuntu 22.04 LTS
4. **Choose Size**: Basic / Regular / $12/mo (2GB RAM, 1 CPU, 50GB)
5. **Authentication**: SSH Key (we'll generate below)
6. **Hostname**: currents-prod
7. Click "Create Droplet"

#### Step 3: Get Server IP
- Wait 60 seconds for droplet to boot
- Copy the IP address (e.g., `167.172.123.45`)

### Option B: AWS EC2

#### Step 1: Create Account
1. Go to https://aws.amazon.com
2. Sign up (requires credit card, phone verification)
3. Free tier available (12 months)

#### Step 2: Launch Instance
1. Go to EC2 Console
2. Click "Launch Instance"
3. **Name**: currents-prod
4. **AMI**: Ubuntu Server 22.04 LTS
5. **Instance Type**: t3.small (2GB RAM)
6. **Key Pair**: Create new or use existing
7. **Network**: Allow HTTP (80), HTTPS (443), SSH (22)
8. Click "Launch Instance"

#### Step 3: Get Server IP
- Wait for "Running" status
- Copy Public IPv4 address

---

## 4. DNS CONFIGURATION

### Point Domain to Server

#### If using Namecheap:
1. Login to Namecheap
2. Go to Domain List → Manage
3. Advanced DNS tab
4. Add A Record:
   - **Host**: `@`
   - **Value**: `YOUR_SERVER_IP`
   - **TTL**: Automatic
5. Add A Record for www:
   - **Host**: `www`
   - **Value**: `YOUR_SERVER_IP`
   - **TTL**: Automatic
6. Save changes (propagation: 5-30 minutes)

#### If using Cloudflare:
1. Login to Cloudflare
2. Select your domain
3. DNS tab
4. Add A Record:
   - **Name**: `@`
   - **IPv4**: `YOUR_SERVER_IP`
   - **Proxy**: OFF (orange cloud disabled)
5. Add A Record:
   - **Name**: `www`
   - **IPv4**: `YOUR_SERVER_IP`
   - **Proxy**: OFF
6. Save

#### If using GoDaddy/Others:
Similar process - add A records for `@` and `www` pointing to server IP.

---

## 5. SSH KEY GENERATION (Local Machine)

Run on your local computer:

```bash
# Generate new SSH key for production server
ssh-keygen -t ed25519 -C "currents-prod" -f ~/.ssh/currents_prod

# Display public key (copy this)
cat ~/.ssh/currents_prod.pub
```

**For DigitalOcean**: Paste public key during droplet creation  
**For AWS EC2**: Create key pair or import this public key

---

## 6. DEPLOYMENT PACKAGE

I'll create a complete deployment package with:
- All code files (app.py, templates, static assets)
- SQLite database (353 markets)
- Configuration files
- Automated setup script
- systemd service files
- nginx configuration

### Files Included:
```
currents-production/
├── app.py                      # Flask application
├── brain.db                    # Database (353 markets)
├── requirements.txt            # Python dependencies
├── .env.production             # Environment variables
├── deploy.sh                   # Automated deployment script
├── config/
│   ├── nginx.conf              # Nginx configuration
│   ├── currents.service        # systemd service
│   └── ssl-setup.sh            # SSL certificate setup
├── static/                     # All images, CSS, JS
├── templates/                  # HTML templates
└── README.md                   # Quick start guide
```

---

## 7. DEPLOYMENT STEPS (After Server Ready)

### Connect to Server:
```bash
ssh -i ~/.ssh/currents_prod root@YOUR_SERVER_IP
```

### Run Automated Deployment:
```bash
# On production server
wget https://YOUR_DEPLOYMENT_URL/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

The script will:
1. Update system packages
2. Install Python 3.11, nginx, certbot
3. Create application directory
4. Copy all files
5. Install Python dependencies
6. Configure nginx reverse proxy
7. Set up SSL certificate (Let's Encrypt)
8. Create systemd service (auto-restart)
9. Start application
10. Run health checks

**Total time**: ~15 minutes

---

## 8. WHAT YOU NEED TO PROVIDE NOW

### Immediate:
1. **Domain name**: What domain will you use? (e.g., currents.global)
2. **Platform choice**: DigitalOcean, AWS, or other?
3. **Server region**: US East, US West, Europe?

### After server setup:
4. **Server IP address**: From DigitalOcean/AWS console
5. **SSH access**: Root password or key

### For full features:
6. **WalletConnect Project ID**: For production domain
7. **Email service** (optional): For waitlist confirmations

---

## 9. NEXT STEPS

**I will create:**
1. ✅ Complete deployment package (tar.gz with all files)
2. ✅ Automated deployment script
3. ✅ Server setup instructions
4. ✅ Post-deployment checklist
5. ✅ Monitoring & maintenance guide

**Please provide:**
- Domain name you want to use
- Preferred platform (DigitalOcean recommended)
- Once server created, send me IP address

Then I'll create a **one-command deployment** that sets everything up automatically! 🚀

---

## 10. COSTS ESTIMATE

### Ongoing Monthly:
- **Server**: $12/month (DigitalOcean 2GB) or $18/month (AWS t3.small)
- **Domain**: $10-15/year
- **Backups**: $2/month (optional, recommended)
- **Total**: ~$15-20/month

### One-time:
- Domain registration: $10-15 (if new)
- SSL certificate: $0 (Let's Encrypt free)

**No other costs required** - everything else is included in server!

---

Ready to proceed? Let me know your domain and platform choice, and I'll create the complete deployment package!

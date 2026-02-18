# DigitalOcean Setup Guide for Currents

**Complete step-by-step guide for DigitalOcean deployment**

---

## WHY DIGITALOCEAN?

- ✅ Simplest setup (5 minutes)
- ✅ Best value ($12/month for production-ready server)
- ✅ $200 free credit for new accounts (search for promo codes)
- ✅ Excellent documentation and support
- ✅ One-click backups ($2/month)
- ✅ Easy firewall management
- ✅ Great uptime (99.99% SLA)

---

## STEP 1: CREATE DIGITALOCEAN ACCOUNT

### 1.1 Sign Up
1. Go to https://digitalocean.com
2. Click **"Sign Up"**
3. Enter email and create password
4. Verify email

### 1.2 Add Payment
1. Click profile icon → **Billing**
2. Add credit card (required even for free credits)
3. Apply promo code if you have one (often $200 free credit)

**Estimated time**: 5 minutes

---

## STEP 2: GENERATE SSH KEY (On Your Computer)

### 2.1 Mac/Linux
Open Terminal and run:
```bash
# Generate key
ssh-keygen -t ed25519 -C "currents-prod" -f ~/.ssh/currents_prod

# Press Enter for all prompts (no passphrase for simplicity)

# Display public key
cat ~/.ssh/currents_prod.pub
```

### 2.2 Windows
Open PowerShell and run:
```powershell
# Generate key
ssh-keygen -t ed25519 -C "currents-prod" -f $env:USERPROFILE\.ssh\currents_prod

# Display public key
type $env:USERPROFILE\.ssh\currents_prod.pub
```

**IMPORTANT**: Copy the entire public key output (starts with `ssh-ed25519`). You'll need it in next step!

**Estimated time**: 2 minutes

---

## STEP 3: CREATE DROPLET (Server)

### 3.1 Start Creation
1. Login to DigitalOcean
2. Click green **"Create"** button (top right)
3. Select **"Droplets"**

### 3.2 Choose Region
**Recommended regions:**
- **New York (NYC1)** - Best for US East Coast
- **San Francisco (SFO3)** - Best for US West Coast
- **Frankfurt (FRA1)** - Best for Europe
- **Singapore (SGP1)** - Best for Asia

**Choose the region closest to your main users!**

### 3.3 Choose Image
- Select **Ubuntu**
- Version: **22.04 (LTS) x64**

### 3.4 Choose Size
- Click **"Basic"** plan
- Click **"Regular"** (not Premium)
- Select **"2 GB / 1 CPU / 50 GB SSD / 2 TB transfer"** - $12/month

### 3.5 Add SSH Key
1. Click **"New SSH Key"**
2. Paste your public key (from Step 2)
3. Name it: "Currents Production"
4. Click **"Add SSH Key"**

### 3.6 Finalize Details
- **Choose hostname**: `currents-prod`
- **Backups**: Enable ($2/month - RECOMMENDED!)
- **Monitoring**: Enable (free)
- Leave other options default

### 3.7 Create Droplet
1. Click **"Create Droplet"** (bottom)
2. Wait 60 seconds for droplet to boot

**Estimated time**: 3 minutes

---

## STEP 4: GET SERVER IP ADDRESS

1. Your new droplet will appear in the dashboard
2. Look for the **IP address** (e.g., `167.172.123.45`)
3. **COPY THIS IP** - you'll need it!

---

## STEP 5: SETUP DNS (Point Domain to Server)

### 5.1 If Using Namecheap
1. Login to Namecheap
2. Go to **Domain List** → Click **"Manage"** next to your domain
3. Click **"Advanced DNS"** tab
4. Delete all existing A records (if any)
5. Add new A Record:
   - **Type**: A Record
   - **Host**: `@`
   - **Value**: Your droplet IP (e.g., `167.172.123.45`)
   - **TTL**: Automatic
6. Add another A Record:
   - **Type**: A Record
   - **Host**: `www`
   - **Value**: Your droplet IP (same as above)
   - **TTL**: Automatic
7. Click **"Save All Changes"**

### 5.2 If Using GoDaddy
1. Login to GoDaddy
2. Go to **My Products** → **Domains**
3. Click **"DNS"** next to your domain
4. Find A Records section
5. Edit `@` record → Change IP to your droplet IP
6. Edit `www` record → Change IP to your droplet IP
7. Click **"Save"**

### 5.3 If Using Cloudflare
1. Login to Cloudflare
2. Select your domain
3. Click **"DNS"** tab
4. Add A Record:
   - **Type**: A
   - **Name**: `@`
   - **IPv4 address**: Your droplet IP
   - **Proxy status**: OFF (gray cloud, not orange!)
   - **TTL**: Auto
5. Add A Record:
   - **Type**: A
   - **Name**: `www`
   - **IPv4 address**: Your droplet IP
   - **Proxy status**: OFF
   - **TTL**: Auto
6. Click **"Save"**

**DNS Propagation**: Takes 5-30 minutes (sometimes up to 48 hours)

**Estimated time**: 5 minutes

---

## STEP 6: TEST SSH CONNECTION

### 6.1 Mac/Linux
```bash
ssh -i ~/.ssh/currents_prod root@YOUR_DROPLET_IP
```

### 6.2 Windows
```powershell
ssh -i $env:USERPROFILE\.ssh\currents_prod root@YOUR_DROPLET_IP
```

**Expected output:**
```
Welcome to Ubuntu 22.04.3 LTS
...
root@currents-prod:~#
```

If you see the `root@currents-prod:~#` prompt, **SUCCESS!** You're connected.

**Estimated time**: 1 minute

---

## STEP 7: COPY DEPLOYMENT PACKAGE TO SERVER

### 7.1 From Your Computer
Open a NEW terminal window (keep SSH connection open) and run:

**Mac/Linux:**
```bash
scp -i ~/.ssh/currents_prod ~/Downloads/currents-production-*.tar.gz root@YOUR_DROPLET_IP:/root/
```

**Windows:**
```powershell
scp -i $env:USERPROFILE\.ssh\currents_prod $env:USERPROFILE\Downloads\currents-production-*.tar.gz root@YOUR_DROPLET_IP:/root/
```

**Expected output:**
```
currents-production-20260218-115852.tar.gz    100%  133MB   5.2MB/s   00:25
```

**Estimated time**: 2-5 minutes (depending on your internet speed)

---

## STEP 8: DEPLOY APPLICATION

### 8.1 In SSH Session (on server)
```bash
# Extract package
cd /root
tar -xzf currents-production-*.tar.gz
cd currents-production-temp

# Make script executable
chmod +x deploy-production.sh

# Run deployment (replace YOUR_DOMAIN.com with your actual domain!)
./deploy-production.sh YOUR_DOMAIN.com
```

**Example:**
```bash
./deploy-production.sh currents.global
```

**What happens:**
1. Installs Python, nginx, certbot
2. Creates application user
3. Sets up Python environment
4. Installs dependencies
5. Configures nginx
6. Creates systemd service
7. Gets SSL certificate (Let's Encrypt)
8. Starts application

**Estimated time**: 10-15 minutes

---

## STEP 9: VERIFY DEPLOYMENT

### 9.1 Check Service Status
```bash
sudo systemctl status currents.service
```

**Expected**: Shows `active (running)` in green

### 9.2 Check Nginx
```bash
sudo systemctl status nginx
```

**Expected**: Shows `active (running)` in green

### 9.3 Test Site
Open browser and visit:
- `https://YOUR_DOMAIN.com`
- `https://www.YOUR_DOMAIN.com`

**Expected**: Currents site loads with markets feed

**If not loading yet**: DNS might still be propagating. Wait 10-30 minutes.

---

## STEP 10: POST-DEPLOYMENT

### 10.1 View Application Logs
```bash
sudo journalctl -u currents.service -f
```

Press `Ctrl+C` to exit log view.

### 10.2 Common Commands
```bash
# Restart application
sudo systemctl restart currents.service

# Restart nginx
sudo systemctl restart nginx

# View logs
sudo journalctl -u currents.service -n 100

# Check disk space
df -h

# Check memory usage
free -h
```

### 10.3 Update WalletConnect
1. Go to https://cloud.walletconnect.com
2. Create new project: "Currents Production"
3. Add your domain to allowed domains
4. Copy Project ID
5. Update in code (search for WalletConnect Project ID and replace)

---

## TROUBLESHOOTING

### Site not loading?
1. **Check DNS**: `dig YOUR_DOMAIN.com` - should show your droplet IP
2. **Check service**: `sudo systemctl status currents.service`
3. **Check nginx**: `sudo systemctl status nginx`
4. **Check logs**: `sudo journalctl -u currents.service -n 50`
5. **Wait for DNS**: Can take up to 48 hours (usually 5-30 minutes)

### SSL certificate failed?
1. Make sure DNS is pointing to server (wait 30 minutes after DNS change)
2. Check ports 80 and 443 are open: `sudo ufw status`
3. Retry: `sudo certbot --nginx -d YOUR_DOMAIN.com -d www.YOUR_DOMAIN.com`

### Can't SSH?
1. Check IP address is correct
2. Check you're using correct key: `ssh -i ~/.ssh/currents_prod root@IP`
3. Check DigitalOcean firewall allows SSH (port 22)

### Application crashed?
1. Check logs: `sudo journalctl -u currents.service -n 100`
2. Restart: `sudo systemctl restart currents.service`
3. Check disk space: `df -h` (if 100% full, that's the issue)

---

## COST BREAKDOWN

### Monthly Costs:
- **Droplet (2GB)**: $12.00/month
- **Backups**: $2.40/month (optional, recommended)
- **Bandwidth**: $0 (2TB included, more than enough)
- **SSL Certificate**: $0 (Let's Encrypt free)
- **Domain**: $1-1.50/month (depends on registrar)

**Total**: ~$15-16/month

### One-Time Costs:
- **Domain registration**: $10-15/year
- **Setup**: $0 (DIY)

**No free tier limits** - runs 24/7 with no restrictions!

---

## NEXT STEPS

1. ✅ Test site thoroughly
2. ✅ Update WalletConnect Project ID
3. ✅ Setup monitoring (optional): UptimeRobot for uptime alerts
4. ✅ Enable backups (already done if you checked the box)
5. ✅ Share site with team/users!

---

## SUPPORT

### DigitalOcean Support
- Docs: https://docs.digitalocean.com
- Community: https://www.digitalocean.com/community
- Support tickets: From dashboard (click "?" icon)

### Let's Encrypt SSL
- Docs: https://letsencrypt.org/docs/
- Certbot docs: https://certbot.eff.org/

### Application Issues
- Check logs: `sudo journalctl -u currents.service -f`
- Restart service: `sudo systemctl restart currents.service`
- Database location: `/var/www/currents/brain.db`

---

**Congratulations! Your Currents production site is live! 🚀**

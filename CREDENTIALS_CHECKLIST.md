# Currents Production - Credentials & Access Checklist

Use this checklist to track what you need for production deployment.

## 1. DOMAIN & DNS

### Domain Registrar
- [ ] **Platform**: _______________ (Namecheap, GoDaddy, Cloudflare, etc.)
- [ ] **Domain Name**: _______________ (e.g., currents.global)
- [ ] **Login Email**: _______________
- [ ] **Password**: _______________ (store securely!)
- [ ] **DNS Access**: Can you add A records? Yes/No

### DNS Configuration Required
After server setup, you'll need to add:
- [ ] A Record: `@` → Server IP
- [ ] A Record: `www` → Server IP

---

## 2. SERVER PLATFORM

### Recommended: DigitalOcean

#### Account Setup
- [ ] **Email**: _______________
- [ ] **Password**: _______________ (store securely!)
- [ ] **2FA Enabled**: Yes/No (recommended!)
- [ ] **Payment Method**: Added? Yes/No

#### Server Details (after creation)
- [ ] **Droplet Name**: currents-prod
- [ ] **Region**: _______________ (NYC1, SFO2, FRA1, etc.)
- [ ] **Size**: 2GB RAM / $12/month
- [ ] **IP Address**: _______________ (e.g., 167.172.123.45)
- [ ] **Root Password**: _______________ (if using password auth)

### Alternative: AWS EC2

#### Account Setup
- [ ] **Email**: _______________
- [ ] **Password**: _______________ (store securely!)
- [ ] **AWS Account ID**: _______________
- [ ] **Payment Method**: Added? Yes/No

#### Instance Details (after creation)
- [ ] **Instance Name**: currents-prod
- [ ] **Instance ID**: _______________ (e.g., i-1234567890abcdef0)
- [ ] **Region**: _______________ (us-east-1, eu-west-1, etc.)
- [ ] **Instance Type**: t3.small
- [ ] **Public IP**: _______________ (e.g., 54.123.45.67)
- [ ] **Key Pair Name**: _______________

---

## 3. SSH ACCESS

### SSH Key (create on your local machine)
```bash
ssh-keygen -t ed25519 -C "currents-prod" -f ~/.ssh/currents_prod
```

- [ ] **Public Key Location**: `~/.ssh/currents_prod.pub`
- [ ] **Private Key Location**: `~/.ssh/currents_prod`
- [ ] **Uploaded to Platform**: Yes/No

### SSH Connection Test
```bash
ssh -i ~/.ssh/currents_prod root@YOUR_SERVER_IP
```
- [ ] **Connection Successful**: Yes/No

---

## 4. WALLETCONNECT (for wallet features)

### Account
- [ ] **Platform**: https://cloud.walletconnect.com
- [ ] **Email**: _______________
- [ ] **Password**: _______________ (store securely!)

### Production Project
- [ ] **Project Name**: Currents Production
- [ ] **Project ID**: _______________ (get after creating project)
- [ ] **Allowed Domains**: Add your production domain
- [ ] **Network**: Arbitrum (Chain ID 42161)

### How to Get Project ID:
1. Go to https://cloud.walletconnect.com
2. Create new project: "Currents Production"
3. Copy Project ID
4. Update in code: Search for old Project ID and replace

---

## 5. OPTIONAL SERVICES

### Email (for waitlist confirmations)

#### Option A: SendGrid (Recommended - Free tier 100/day)
- [ ] **Email**: _______________
- [ ] **API Key**: _______________ (after signup)
- [ ] **Sender Email**: _______________ (must verify)

#### Option B: AWS SES
- [ ] **AWS Account**: Use same as EC2 if on AWS
- [ ] **Access Key**: _______________
- [ ] **Secret Key**: _______________ (store securely!)
- [ ] **Region**: _______________

### Analytics

#### Option A: Plausible (Privacy-focused, recommended)
- [ ] **Account**: https://plausible.io
- [ ] **Domain Added**: Yes/No
- [ ] **Script Tag**: _______________ (copy from dashboard)

#### Option B: Google Analytics
- [ ] **Account**: Google Analytics 4
- [ ] **Property ID**: _______________ (G-XXXXXXXXXX)
- [ ] **Tracking Code**: Added? Yes/No

---

## 6. DEPLOYMENT PACKAGE

### Files Needed
- [ ] **Package File**: `currents-production-YYYYMMDD-HHMMSS.tar.gz` (133MB)
- [ ] **Location**: `/home/ubuntu/.openclaw/workspace/currents-full-local/`
- [ ] **Copied to Local Machine**: Yes/No

### Download Package
From current server:
```bash
scp ubuntu@CURRENT_SERVER_IP:/home/ubuntu/.openclaw/workspace/currents-full-local/currents-production-*.tar.gz ~/Downloads/
```

---

## 7. DEPLOYMENT CREDENTIALS SUMMARY

### Copy this and save securely (password manager recommended!)

```
=== CURRENTS PRODUCTION CREDENTIALS ===

Domain:
- Name: _______________
- Registrar: _______________
- Login: _______________
- Password: _______________

Server:
- Platform: _______________ (DigitalOcean/AWS/etc.)
- IP Address: _______________
- SSH Key: ~/.ssh/currents_prod
- Root Password: _______________ (if applicable)

WalletConnect:
- Project ID: _______________
- Email: _______________

Email Service (optional):
- API Key: _______________

SSL Certificate:
- Provider: Let's Encrypt (automatic)
- Email: admin@YOUR_DOMAIN
- Auto-renewal: Enabled

Database:
- Type: SQLite
- Location: /var/www/currents/brain.db
- Backup: Managed by server platform

=== END CREDENTIALS ===
```

---

## 8. POST-DEPLOYMENT CHECKLIST

After running deployment script:

### Verify Site
- [ ] Visit https://YOUR_DOMAIN - loads correctly
- [ ] Visit https://www.YOUR_DOMAIN - redirects to main domain
- [ ] SSL certificate shows as secure (green lock)
- [ ] Feed loads with markets
- [ ] User switcher works
- [ ] Mobile view works
- [ ] Detail pages load

### Update WalletConnect
- [ ] Project ID updated in code
- [ ] Production domain added to allowed domains
- [ ] Test wallet connection

### Setup Monitoring
- [ ] Uptime monitoring (optional: UptimeRobot free)
- [ ] Error tracking (optional: Sentry free tier)
- [ ] Analytics installed

### Backup Setup
- [ ] Server backups enabled (DigitalOcean/AWS)
- [ ] Database backup schedule
- [ ] Weekly snapshot recommended

### Security
- [ ] Firewall configured (UFW or platform firewall)
- [ ] Only ports 80, 443, 22 open
- [ ] SSH key auth only (disable password auth)
- [ ] Regular updates scheduled

---

## 9. SUPPORT CONTACTS

### Technical Issues
- Server platform support (DigitalOcean/AWS)
- SSL certificate: Let's Encrypt community forum
- DNS issues: Domain registrar support

### Emergency Contacts
- **Server Admin**: _______________
- **Domain Manager**: _______________
- **Developer**: _______________

---

## 10. NEXT STEPS

1. [ ] Fill out this checklist
2. [ ] Create accounts (domain, server platform)
3. [ ] Generate SSH keys
4. [ ] Create server
5. [ ] Point DNS to server IP
6. [ ] Copy deployment package to server
7. [ ] Run deployment script
8. [ ] Verify site works
9. [ ] Update WalletConnect
10. [ ] Celebrate! 🚀

---

**Save this document securely!** You'll need these credentials for maintenance and updates.

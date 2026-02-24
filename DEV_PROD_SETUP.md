# Dev & Production Setup

**Updated**: February 24, 2026

## Overview

Two separate running instances:

| Environment | Branch | Port | Database | Domain | Status |
|-------------|--------|------|----------|--------|--------|
| **Production** | main | 5555 | production.db | currents.global | ✅ Running |
| **Development** | dev | 5556 | brain.db | sonic-ben-weekends-sao.trycloudflare.com | ✅ Running |

## Current Status

### ✅ Production (currents.global)
- **Location**: `/home/ubuntu/.openclaw/workspace/currents-full-local`
- **Branch**: main
- **Port**: 5555
- **Service**: `currents.service`
- **Database**: brain.db (will become production.db)
- **URL**: https://currents.global

```bash
# Check status
sudo systemctl status currents

# View logs
sudo journalctl -u currents -f

# Restart
sudo systemctl restart currents
```

### ✅ Development (dev environment)
- **Location**: `/home/ubuntu/.openclaw/workspace/currents-dev`
- **Branch**: dev
- **Port**: 5556
- **Service**: `currents-dev.service`
- **Database**: brain.db (separate copy)
- **URL**: https://sonic-ben-weekends-sao.trycloudflare.com
- **Tunnel**: Cloudflare Quick Tunnel (free, no account needed)

```bash
# Check status
sudo systemctl status currents-dev

# View logs
sudo journalctl -u currents-dev -f

# Restart
sudo systemctl restart currents-dev
```

## Dev URL Options

### Option 1: Cloudflare Tunnel (Recommended - Free, Permanent)

**Pros**: Free, stable URL, unlimited bandwidth, custom subdomain
**Cons**: Requires Cloudflare account (free)

**Setup**:
1. Create free Cloudflare account
2. Add domain currents.global (if not already)
3. Create tunnel:
```bash
cloudflared tunnel login
cloudflared tunnel create currents-dev
cloudflared tunnel route dns currents-dev dev.currents.global
```

4. Create config file `/etc/cloudflared/config.yml`:
```yaml
tunnel: <tunnel-id>
credentials-file: /home/ubuntu/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: dev.currents.global
    service: http://localhost:5556
  - service: http_status:404
```

5. Start tunnel service:
```bash
sudo cloudflared service install
sudo systemctl start cloudflared
```

**Result**: https://dev.currents.global (permanent)

### Option 2: Cloudflare Quick Tunnel (Temporary)

**Pros**: No account needed, instant
**Cons**: URL changes each restart, no uptime guarantee

**Setup**:
```bash
cloudflared tunnel --url http://localhost:5556
```

**Result**: https://random-words-here.trycloudflare.com (changes each time)

### Option 3: Upgrade Ngrok ($10/month)

**Pros**: Custom subdomain, higher bandwidth
**Cons**: Costs money

**Setup**:
1. Upgrade at https://dashboard.ngrok.com/billing
2. Reserve subdomain: `currents-dev.ngrok.app`
3. Update ngrok config

**Result**: https://currents-dev.ngrok-free.app (permanent)

### Option 4: Direct Access (No tunnel)

**Pros**: Free, simple
**Cons**: Only accessible from server IP

**Access**: http://35.172.150.243:5556 (dev server IP + port)

## Workflow: Dev → Production

### 1. Make Changes on Dev Branch

```bash
cd /home/ubuntu/.openclaw/workspace/currents-dev
git checkout dev
git pull origin dev

# Make changes, test locally at dev URL
# Changes are isolated - prod is unaffected

git add .
git commit -m "Description of changes"
git push origin dev
```

### 2. Test on Dev Environment

Visit dev URL and verify:
- New features work
- No regressions
- Mobile/desktop both good
- Images load correctly

### 3. Deploy to Production (When Ready)

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git checkout main
git pull origin main

# Merge dev changes
git merge origin/dev

# Or cherry-pick specific commits
git cherry-pick <commit-hash>

# Push to main
git push origin main

# Restart production
sudo systemctl restart currents
```

### 4. Verify Production

Visit https://currents.global and confirm changes deployed correctly

## Key Commands

### Check Both Services
```bash
sudo systemctl status currents       # Production
sudo systemctl status currents-dev   # Development
```

### View Logs
```bash
sudo journalctl -u currents -f       # Production logs
sudo journalctl -u currents-dev -f   # Development logs
```

### Restart Services
```bash
sudo systemctl restart currents      # Production
sudo systemctl restart currents-dev  # Development
```

### Update Code
```bash
# Production
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git pull origin main
sudo systemctl restart currents

# Development
cd /home/ubuntu/.openclaw/workspace/currents-dev
git pull origin dev
sudo systemctl restart currents-dev
```

## Safety Features

✅ **Separate directories** - Changes in dev don't affect prod files
✅ **Separate databases** - Dev testing won't corrupt prod data
✅ **Separate ports** - Both can run simultaneously
✅ **Separate branches** - Git keeps changes isolated
✅ **Separate services** - Can restart one without affecting the other

## Troubleshooting

### Dev service won't start
```bash
# Check logs
sudo journalctl -u currents-dev -n 50

# Common issue: Port in use
sudo lsof -i :5556

# Common issue: Missing dependencies
cd /home/ubuntu/.openclaw/workspace/currents-dev
pip3 install -r requirements.txt
```

### Production affected by dev changes
**This shouldn't happen!** They're completely separate. If it does:
1. Check you're on the right branch: `git branch`
2. Check correct directory: `pwd`
3. Check which service you restarted

### Want to sync databases
```bash
# Copy production to dev (for testing with real data)
cp /home/ubuntu/.openclaw/workspace/currents-full-local/brain.db /home/ubuntu/.openclaw/workspace/currents-dev/brain.db
sudo systemctl restart currents-dev
```

## Next Steps

**Immediate**:
1. ✅ Dev instance is running on port 5556
2. ⏳ Choose dev URL option (recommend Cloudflare Tunnel)
3. ⏳ Set up dev URL

**Optional**:
- Rename `brain.db` to `production.db` in production directory
- Set up automated deployment scripts
- Add staging environment monitoring

## Summary

**Current State**:
- ✅ Production running: currents.global (port 5555)
- ✅ Dev running: localhost:5556 (needs public URL)
- ✅ Both using separate databases
- ✅ Both using separate git branches
- ✅ Both running as systemd services

**You control when to deploy**: Make changes on dev, test thoroughly, then manually merge to main when ready.

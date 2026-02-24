# Environment Configuration Guide

**Updated**: February 24, 2026

## Overview

We maintain two separate environments to prevent production and development from interfering with each other:

| Environment | Branch | Domain | Database | Use Case |
|-------------|--------|--------|----------|----------|
| **Production** | main | currents.global | production.db | Live site for users |
| **Development** | dev | localhost/ngrok | brain.db | Testing & new features |

## Quick Start

### Switching Environments

Use the provided script to switch between environments:

```bash
# Switch to production
./switch-env.sh production

# Switch to development
./switch-env.sh dev
```

This script:
1. Copies the appropriate `.env.*` file to `.env`
2. Shows current configuration
3. Reminds you to switch git branch and restart service

### Manual Setup

If you prefer to set up manually:

**For Production:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git checkout main
cp .env.production .env
sudo systemctl restart currents
```

**For Development:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git checkout dev
cp .env.development .env
sudo systemctl restart currents
```

## Environment Files

### `.env.production`
- Used on production server (currents.global)
- Points to `production.db`
- Debug mode OFF
- Higher security settings
- Used with `main` branch

### `.env.development`
- Used for local testing
- Points to `brain.db`
- Debug mode ON
- Relaxed rate limits for testing
- Used with `dev` branch

### `.env` (Active Config)
- This file is git-ignored
- Copy from `.env.production` or `.env.development`
- Never commit this file (contains active config)

## Database Separation

Each environment uses its own database:

| Environment | File | Purpose |
|-------------|------|---------|
| Production | `production.db` | Live user data |
| Development | `brain.db` | Test data, safe to reset |

**Important**: Databases are git-ignored (too large). Transfer manually if needed.

## Workflow Examples

### Working on New Feature (Development)

```bash
# 1. Switch to dev environment
git checkout dev
./switch-env.sh dev

# 2. Make changes and test
# (app uses brain.db, won't affect production)

# 3. Commit to dev branch
git add .
git commit -m "Add new feature"
git push origin dev

# 4. Test thoroughly on dev
# Visit localhost:5555 or ngrok URL
```

### Deploying to Production

```bash
# 1. Switch to main branch
git checkout main

# 2. Merge dev changes (if tested)
git merge dev

# 3. Switch to production environment
./switch-env.sh production

# 4. Push to main
git push origin main

# 5. On production server (currents.global):
#    - Pull latest: git pull origin main
#    - Ensure .env.production is active
#    - Restart: sudo systemctl restart currents
```

### Emergency Rollback

If something breaks in production:

```bash
# On production server
git checkout main
git log --oneline -10  # Find last good commit
git reset --hard <commit-hash>
sudo systemctl restart currents
```

## Checking Current Environment

```bash
# Check which environment is active
grep ENV= .env

# Output:
# ENV=production  (you're in prod)
# ENV=development (you're in dev)

# Check which branch you're on
git branch

# Check which database is being used
grep DATABASE_PATH= .env
```

## Configuration Options

### Common Settings (Both Environments)

- `BRAIN_V1_ENABLED=True` - Use BRain v1 personalization
- `COMING_SOON_REDIRECT=False` - Coming Soon page disabled

### Production-Specific

- `DEBUG=False` - No debug output
- `RATE_LIMIT_MAX=3` - Strict rate limiting
- `LOG_LEVEL=INFO` - Less verbose logging
- `FLASK_DEBUG=0` - Production Flask mode

### Development-Specific

- `DEBUG=True` - Show debug output
- `RATE_LIMIT_MAX=100` - Relaxed for testing
- `LOG_LEVEL=DEBUG` - Verbose logging
- `FLASK_DEBUG=1` - Development Flask mode
- `USE_NGROK=True` - Enable tunneling

## Safety Features

### Separation Guarantees

✅ **Different databases** - Dev can't corrupt prod data
✅ **Different branches** - Changes isolated until merged
✅ **Different domains** - No URL conflicts
✅ **Git-ignored configs** - No accidental overwrites

### Best Practices

1. **Always check your environment** before making changes
2. **Test on dev first** before pushing to main
3. **Never work on main directly** - use dev branch
4. **Keep databases separate** - don't copy prod to dev
5. **Commit to correct branch** - dev for features, main for releases

## Troubleshooting

### "Which environment am I in?"

```bash
grep ENV= .env
git branch
```

### "Wrong database being used"

```bash
# Fix: Switch to correct environment
./switch-env.sh [production|dev]
sudo systemctl restart currents
```

### "Changes not appearing"

```bash
# Did you restart the service?
sudo systemctl restart currents

# Are you on the right branch?
git branch

# Is the correct .env active?
cat .env
```

### "Merged wrong branch"

```bash
# Undo last merge
git reset --hard HEAD~1

# Or reset to specific commit
git log --oneline
git reset --hard <commit-hash>
```

## File Structure

```
currents-full-local/
├── .env                    # Active config (git-ignored)
├── .env.production         # Production template
├── .env.development        # Development template
├── switch-env.sh           # Environment switcher script
├── production.db           # Production database (git-ignored)
├── brain.db                # Development database (git-ignored)
├── app.py                  # Main application
└── ...
```

## Summary

**Golden Rule**: Keep production and development completely separate

- ✅ Use different branches (main vs dev)
- ✅ Use different databases (production.db vs brain.db)
- ✅ Use different configs (.env.production vs .env.development)
- ✅ Always know which environment you're in
- ✅ Test on dev before deploying to main

**Quick Reference**:
```bash
./switch-env.sh dev          # Development mode
./switch-env.sh production   # Production mode
grep ENV= .env               # Check current environment
git branch                   # Check current branch
```

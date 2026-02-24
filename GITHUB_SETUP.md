# GitHub Repository Setup

**Updated**: February 24, 2026
**Repository**: https://github.com/currentsfeed/currents

## Access Token

**New Token**: `ghp_***` (stored securely, not in repo)

✅ Remote URL updated successfully
✅ Push/pull permissions verified

**Note**: The actual token is configured in the git remote URL but never committed to the repository for security reasons.

## Branch Structure

### Current Branches

| Branch | Purpose | Current State |
|--------|---------|---------------|
| `main` | Production environment | ✅ Latest (v208 - Nigeria feed) |
| `dev` | Development/Staging | ⚠️ Earlier state (v205-ish) |

**Note**: Roy mentioned "stg" (staging) branch, but the remote has "dev" instead. Need clarification on branch naming.

### Current Commit Status

**main** (local & remote):
```
0e716ee Fix epl-ucl-winner.jpg image (Champions League football)
174c56c Fix nigeria-inflation-2027.jpg image (Lagos cityscape)
55e2b8a Fix nigeria-caf-player.jpg image (was corrupted, now proper trophy photo)
8496c98 Add deployment doc for v208
5294041 v208: Add Nigeria-focused feed with 16 new markets
```

**dev** (remote only):
```
d2a86b9 Update requirements.txt
eddab9b Add database separation guides and schema files
92320bc Initial commit - Currents v205 production ready
```

## Workflow

### For Production Changes (main branch)

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Make changes, test locally
git add .
git commit -m "Description of changes"
git push origin main

# Production deployment (currents.global)
# SSH to production server and pull latest
```

### For Staging Changes (dev/stg branch)

**Option 1: Work on dev branch directly**
```bash
# Switch to dev branch
git checkout -b dev origin/dev

# Make changes, test
git add .
git commit -m "Staging: description"
git push origin dev
```

**Option 2: Create stg branch from dev**
```bash
# Rename dev to stg (if preferred)
git branch -m dev stg
git push origin stg
git push origin --delete dev
```

## Separation Strategy

To ensure deployments don't interfere:

### 1. Environment Variables
- Production: Uses production DB, production domain
- Staging: Uses staging DB, staging/dev domain

### 2. Branch Protection
- `main`: Protected, requires review (optional)
- `dev/stg`: Open for testing

### 3. Deployment Targets
- `main` → currents.global (production)
- `dev/stg` → dev.currents.global or ngrok/tunnel (staging)

### 4. Database Separation
- Production: PostgreSQL on separate server OR SQLite (production.db)
- Staging: SQLite (brain.db) in dev environment

### 5. Configuration Files
Create environment-specific configs:

```bash
# Production (main branch)
config/production.env
- DATABASE_URL=postgresql://...
- DOMAIN=currents.global
- DEBUG=False

# Staging (dev/stg branch)
config/staging.env
- DATABASE_URL=sqlite:///brain.db
- DOMAIN=dev.currents.global
- DEBUG=True
```

## Current Setup Status

✅ **Completed**:
- New GitHub token configured
- Remote URL updated
- Push access verified
- Branch structure identified

⚠️ **Needs Clarification**:
- Branch naming: dev vs stg?
- Should dev be renamed to stg?
- Should we create a new stg branch?

❓ **Questions for Roy**:
1. Should I rename `dev` to `stg`, or keep it as is?
2. Do you want a local staging environment with separate DB?
3. Should staging use a different domain/tunnel?

## Quick Reference

### Check Current Branch
```bash
git branch
```

### Switch Branches
```bash
git checkout main       # Production
git checkout dev        # Staging (if kept as dev)
git checkout stg        # Staging (if renamed)
```

### Push to Specific Branch
```bash
git push origin main    # Production
git push origin dev     # Staging (current name)
git push origin stg     # Staging (if renamed)
```

### Verify Remote
```bash
git remote -v
git ls-remote --heads origin
```

## Next Steps

1. ✅ Confirm branch naming (dev vs stg)
2. ⏳ Set up staging environment if needed
3. ⏳ Create environment-specific configs
4. ⏳ Document deployment process for both environments

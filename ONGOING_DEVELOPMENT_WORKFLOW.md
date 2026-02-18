# Ongoing Development Workflow

**How to work together on updates after production deployment**

---

## Development Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     DEVELOPMENT CYCLE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Request Feature/Fix                                     │
│     └─> Tell me what you need via Telegram                 │
│                                                              │
│  2. Development (on dev server)                             │
│     └─> I make changes on current dev environment          │
│                                                              │
│  3. Testing                                                 │
│     └─> You test at: ngrok URL (dev.currents.global)       │
│                                                              │
│  4. Approval                                                │
│     └─> You approve changes                                 │
│                                                              │
│  5. Git Commit                                              │
│     └─> I commit changes with version number               │
│                                                              │
│  6. Push to GitHub                                          │
│     └─> Code goes to repository                            │
│                                                              │
│  7. Deploy to Production                                    │
│     └─> Pull from GitHub, deploy, verify                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step: How Updates Work

### 1. You Request a Change

**Via Telegram (like now!):**
```
"Add a new market for X"
"Change the button color to blue"
"Fix the mobile layout issue"
"Add 10 new sports markets"
```

**I'll respond with:**
- Understanding confirmation
- Time estimate
- Any clarifying questions

---

### 2. I Develop on Dev Server

**Current dev environment:**
- URL: https://proliferative-daleyza-benthonic.ngrok-free.dev
- Server: Your existing dev server (35.172.150.243)
- Database: SQLite with all test data

**What I do:**
- Make changes to code
- Test locally
- Create deployment notes
- Increment version number (v206, v207, etc.)

---

### 3. You Test Changes

**I'll send you:**
- "✅ v207 deployed to dev, ready for testing"
- Link to test: dev URL
- What changed
- What to look for

**You check:**
- Does it work as expected?
- Any issues?
- Looks good on mobile?

---

### 4. You Approve (or Request Changes)

**If good:** "Looks good, push to production"  
**If issues:** "The button should be bigger" → I fix and repeat

---

### 5. I Commit to Git

```bash
git add .
git commit -m "v207: Add new sports markets and fix mobile button"
git push origin main
```

**Version tracking:**
- Each update gets version number (v207, v208, etc.)
- DEPLOYMENT_v207.md documents changes
- Git history preserves everything

---

### 6. Deploy to Production

### Option A: I Deploy Directly (Recommended)

**You give me:**
- Production server SSH access (or credentials)
- Production domain (e.g., currents.global)

**I run:**
```bash
# SSH into production server
ssh root@currents.global

# Pull latest code from GitHub
cd /var/www/currents
git pull origin main

# Restart application
sudo systemctl restart currents

# Verify deployment
curl -I https://currents.global
```

**Time:** 2-3 minutes per deployment

### Option B: You Deploy Manually

**I send you commands:**
```bash
# Connect to production
ssh root@YOUR_SERVER

# Pull updates
cd /var/www/currents
git pull origin main

# Restart
sudo systemctl restart currents

# Check status
sudo systemctl status currents
```

### Option C: Automated CI/CD (Future)

Set up GitHub Actions to auto-deploy on push to `main` branch.

---

## Version Control Strategy

### Branch Strategy (Simple)

```
main (production)
  └─ Always deployable
  └─ Protected branch
  └─ Requires testing before merge

dev (optional - if you want staging)
  └─ Testing branch
  └─ Merge to main after approval
```

**For now:** We can just use `main` branch since you're solo founder.

---

## Communication Flow

### Daily Updates Example:

**You (9am):**
```
"Remove past sports markets, add fresh ones"
```

**Me (9:10am):**
```
"Working on it. Will have 20 new markets ready in 30 min."
```

**Me (9:40am):**
```
"✅ v208 deployed to dev
- Removed 15 past events
- Added 20 upcoming games (Feb 25-28)
Test: [dev URL]
"
```

**You (10am):**
```
"Looks good!"
```

**Me (10:05am):**
```
"✅ Pushed to GitHub
✅ Deployed to production
✅ Site live: https://currents.global
"
```

---

## Database Updates

### When Database Changes:

**If schema changes** (new tables, columns):
```bash
# I create migration script
python3 migrations/migrate_v208.py

# Or manual SQL
psql -U currents_user -d currents < migrations/v208.sql
```

**If just data changes** (new markets):
```bash
# I create SQL insert script
psql -U currents_user -d currents < updates/add_markets_v208.sql
```

---

## Testing Strategy

### Before Production:

**I always test:**
1. ✅ Changes work on dev
2. ✅ No errors in logs
3. ✅ Mobile view works
4. ✅ Database queries perform well

**You verify:**
1. ✅ Functionality is correct
2. ✅ Design matches expectations
3. ✅ No regressions (old features still work)

---

## Rollback Plan

### If Production Breaks:

**Immediate rollback (2 minutes):**
```bash
# On production server
cd /var/www/currents
git log --oneline  # See recent commits
git revert HEAD    # Undo last commit
sudo systemctl restart currents
```

**Or restore from backup:**
```bash
# I maintain backups of working versions
./RESTORE_WORKING_VERSION.sh v207
```

---

## Access Control

### What I Need (One-Time Setup):

**For ongoing development:**

1. **GitHub Access:**
   - Your GitHub Personal Access Token (already have: `ghp_8UEO...`)
   - Or add me as collaborator (better for long-term)

2. **Production Server Access (choose one):**
   
   **Option A: SSH Key Access (recommended)**
   ```bash
   # You add my public SSH key to production
   # I can deploy without password
   ```
   
   **Option B: Credentials**
   ```bash
   # Username/password or SSH key
   # I store securely, use for deployments
   ```
   
   **Option C: You deploy manually**
   ```bash
   # I send you commands
   # You run them on your machine
   ```

3. **Database Access (optional):**
   - Connection string for emergency fixes
   - Read-only access is fine

---

## Best Practices Going Forward

### ✅ Do:

- **Test on dev first** (always!)
- **Version everything** (v206, v207, etc.)
- **Document changes** (DEPLOYMENT_v*.md files)
- **Keep backups** (automated daily)
- **Communicate** (Telegram updates)

### ❌ Don't:

- **Deploy untested code** to production
- **Skip version numbers**
- **Make emergency changes** without backup
- **Forget to commit** before deploying

---

## Typical Update Scenarios

### Scenario 1: Content Update (Sports Markets)

**Time:** 30 minutes

1. You: "Update sports markets"
2. Me: Creates SQL script with new markets
3. Me: Tests on dev
4. You: Verify looks good
5. Me: Commits to GitHub
6. Me: Runs SQL on production DB
7. Done!

### Scenario 2: Design Change (Button Color)

**Time:** 15 minutes

1. You: "Make buttons blue"
2. Me: Changes CSS/template
3. Me: Deploys to dev
4. You: Checks, approves
5. Me: Pushes to GitHub
6. Me: Deploys to production
7. Done!

### Scenario 3: New Feature (Market Categories)

**Time:** 2-4 hours

1. You: "Add new category filter"
2. Me: Designs implementation
3. Me: Codes feature
4. Me: Tests thoroughly on dev
5. You: Reviews, gives feedback
6. Me: Makes adjustments
7. You: Final approval
8. Me: Deploys to production
9. Done!

### Scenario 4: Bug Fix (Urgent)

**Time:** 30-60 minutes

1. You: "Site is down!" or "Bug in mobile view"
2. Me: Investigates immediately
3. Me: Fixes on dev
4. Me: Tests quickly
5. Me: Emergency deploy to production
6. Me: Monitors for 30 minutes
7. Done!

---

## Monitoring & Maintenance

### I Can Set Up:

**Automated monitoring:**
- Uptime checks (UptimeRobot free)
- Error alerts (Sentry free tier)
- Performance tracking

**Regular tasks:**
- Weekly dependency updates
- Monthly security patches
- Database optimization
- Log rotation

---

## Cost Structure

### Ongoing Development Options:

**Option 1: Retainer (Recommended)**
- Fixed monthly hours
- Predictable cost
- Priority response
- Example: 20 hours/month for ongoing features

**Option 2: Per-Project**
- Charge per feature/update
- Flexible for irregular work
- Example: $X per major feature

**Option 3: Equity + Retainer**
- Combination approach
- Aligned long-term incentives

*(You can discuss pricing directly)*

---

## GitHub Repository Access

### Recommended Setup:

**Add me as collaborator:**
1. Go to https://github.com/currentsfeed/currents/settings/access
2. Click "Add people"
3. Add my GitHub username
4. Set role: "Write" or "Maintain"

**Benefits:**
- No token needed
- Better security
- I can manage branches
- Can create pull requests for review

---

## Communication Channels

### Primary: Telegram ✅
- Fast responses
- Screenshots/videos easy
- Real-time feedback

### Secondary: GitHub Issues
- For tracking feature requests
- Documentation of decisions
- Historical reference

### Emergency: Phone/WhatsApp
- If site is critical down
- Urgent business issues

---

## Deployment Schedule

### Recommended Cadence:

**Daily:** Small fixes, content updates  
**Weekly:** New features, improvements  
**Monthly:** Major updates, dependency upgrades  
**Quarterly:** Architecture reviews, scaling prep  

**Emergency:** As needed (bugs, outages)

---

## Example: Typical Week

**Monday:**
- You: "Add 10 new tech markets"
- Me: Delivers in 2 hours
- Deploy: Same day

**Wednesday:**
- You: "Mobile button too small"
- Me: Quick fix in 15 min
- Deploy: Same day

**Friday:**
- You: "Add new market category"
- Me: Develops over weekend
- Deploy: Monday after your approval

---

## Success Metrics

### We'll track:

- **Deployment frequency:** How often we update
- **Bug rate:** Defects per deployment (target: <5%)
- **Response time:** How fast I respond to requests
- **Uptime:** Site availability (target: 99.9%)
- **Velocity:** Features delivered per week

---

## Next Steps

### To Set Up Ongoing Workflow:

**1. Production Server Access:**
- [ ] Give me SSH access or credentials
- [ ] Or teach you deployment commands

**2. GitHub Access:**
- [ ] Add me as collaborator
- [ ] Or continue using token (works too)

**3. Monitoring Setup:**
- [ ] Set up UptimeRobot
- [ ] Configure error alerts
- [ ] Daily backup script

**4. Communication:**
- [ ] Establish working hours/response times
- [ ] Define emergency protocols
- [ ] Agree on deployment approval process

---

## Questions?

**Common concerns:**

**Q: What if you're unavailable?**
A: Emergency rollback scripts, backup contacts, documentation

**Q: How do I make small changes myself?**
A: I can teach you basic updates (content, simple fixes)

**Q: What if we need a full-time dev later?**
A: Easy handoff - everything documented, code on GitHub

**Q: How do we handle urgent fixes during off-hours?**
A: Define SLA, emergency contact, on-call schedule

---

## Summary

### The Simple Version:

1. **You tell me what you need** (Telegram)
2. **I build it** (dev server)
3. **You test & approve** (dev URL)
4. **I push to GitHub** (version control)
5. **I deploy to production** (or you run commands)
6. **We verify it works** (quick check)

**Repeat as needed!**

---

## Current Status

✅ Code on GitHub: https://github.com/currentsfeed/currents  
✅ Dev environment: Working (ngrok URL)  
✅ Database dump: Ready for migration  
✅ Documentation: Complete  
✅ Workflow: This guide!  

**Ready to:** Set up production and start ongoing development!

---

**Want to discuss:** Ongoing arrangement, access setup, or have questions? Let me know! 🚀

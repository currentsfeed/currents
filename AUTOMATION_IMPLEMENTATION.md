# Automation Implementation - Trending & Score Decay

**Implemented:** Feb 11, 2026 17:01 UTC  
**Priority:** Milestone 1 - Platform Stability  
**Purpose:** Automate trending refresh and score decay  

---

## 🎯 Automations Implemented

### 1. Trending Refresh (Every 30 Minutes)

**Script:** `refresh_trending.sh`
**Cron:** `*/30 * * * *` (runs every 30 minutes)
**Log:** `/tmp/trending_refresh.log`

**What it does:**
- Runs `compute_trending.py`
- Recalculates trending scores for all 326 markets
- Formula: 85% interest + 15% volume (24h rolling window)
- Updates `trending_cache` table in database

**Why 30 minutes:**
- Balance between freshness and CPU usage
- Roy confirmed 30-minute cadence
- Aligns with typical market activity cycles

**Verification:**
```bash
# Check last run
tail /tmp/trending_refresh.log

# Run manually
/home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh

# Check cron schedule
crontab -l | grep trending
```

---

### 2. Score Decay (Daily at 04:00 UTC)

**Script:** `refresh_score_decay.sh`
**Cron:** `0 4 * * *` (runs daily at 4am UTC)
**Log:** `/tmp/score_decay.log`

**What it does:**
- Applies 5% decay every 7 days to user topic scores
- Daily decay factor: 0.992754 (calculated as 0.95^(1/7))
- Updates all scores > 0 in `user_topic_scores` table
- Ensures stale interests gradually fade

**Why 04:00 UTC:**
- Low traffic period
- Before European morning traffic
- Minimal user impact

**Formula:**
```
Daily decay factor = (0.95)^(1/7) = 0.992754
After 7 days: 0.992754^7 = 0.95 (5% decay)
After 30 days: ~20% decay
After 90 days: ~50% decay
```

**Verification:**
```bash
# Check last run
tail /tmp/score_decay.log

# Run manually (careful - this decays scores!)
/home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh

# Check cron schedule
crontab -l | grep decay
```

---

## 📋 Cron Jobs Summary

```bash
$ crontab -l | grep refresh_
*/30 * * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh
0 4 * * * /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh
```

**Other cron jobs:**
- `refresh-tunnels.sh` - Ngrok tunnel refresh (every 30 min)
- `monitor_site.sh` - Site health check (every 90 min)

---

## ✅ Testing Results

### Trending Refresh:
```bash
$ /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh
$ tail -5 /tmp/trending_refresh.log

new_60010: 0.573
new_60025: 0.571
new_60046: 0.557
517310: 0.503
2026-02-11 17:00 UTC - Trending refresh completed
```
✅ Working - 326 markets scored

### Score Decay:
```bash
$ /home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh
$ tail -5 /tmp/score_decay.log

2026-02-11 17:00 UTC - Score decay: 26 scores updated
2026-02-11 17:00 UTC - Score decay completed
```
✅ Working - 26 user topic scores decayed

---

## 📊 Impact on Personalization

### Trending Refresh Impact:
**Before:** Trending scores static, not reflecting current interest
**After:** Trending scores update every 30 minutes
- Fresh content bubbles up faster
- Declining interest markets fade faster
- Feed stays current with user behavior

### Score Decay Impact:
**Before:** Old interests persist forever, stale user profiles
**After:** Interests gradually fade if not reinforced
- User profiles stay current
- Prevents "locked in" filter bubbles
- Allows users to evolve interests naturally

**Example timeline:**
- Day 0: User likes basketball (score: 100)
- Day 7: If no more basketball interactions → score: 95
- Day 30: If no interactions → score: 80
- Day 90: If no interactions → score: 50
- User's current interests always weighted higher

---

## 🔧 Maintenance

### Monitoring:
```bash
# Check trending refresh is running
ls -lt /tmp/trending_refresh.log
tail -1 /tmp/trending_refresh.log

# Check score decay is running
ls -lt /tmp/score_decay.log
tail -1 /tmp/score_decay.log

# Verify cron jobs scheduled
crontab -l | grep refresh_
```

### Log Rotation:
If logs grow too large:
```bash
# Archive old logs
mv /tmp/trending_refresh.log /tmp/trending_refresh.log.$(date +%Y%m%d)
mv /tmp/score_decay.log /tmp/score_decay.log.$(date +%Y%m%d)

# Logs will recreate automatically on next run
```

### Troubleshooting:
```bash
# If trending not updating:
# 1. Check cron is running
systemctl status cron

# 2. Run manually to see errors
/home/ubuntu/.openclaw/workspace/currents-full-local/refresh_trending.sh

# 3. Check database is accessible
sqlite3 /home/ubuntu/.openclaw/workspace/currents-full-local/brain.db "SELECT COUNT(*) FROM trending_cache;"

# If score decay not working:
# 1. Check scores before/after
sqlite3 brain.db "SELECT COUNT(*), AVG(score) FROM user_topic_scores WHERE score > 0;"

# 2. Run manually
/home/ubuntu/.openclaw/workspace/currents-full-local/refresh_score_decay.sh

# 3. Check log for errors
tail -20 /tmp/score_decay.log
```

---

## 🎯 Milestone 1 Status Update

**Objective:** Platform Stability & Automation

- ✅ **Systemd service** (auto-restart, zero downtime)
- ✅ **Trending refresh automation** (every 30 minutes)
- ✅ **Score decay automation** (daily at 04:00 UTC)
- 🔄 **Image fixes** (Rox working on all 326 markets)

**Core automation: COMPLETE** ✅

---

**Next Steps:**
- Wait for Rox's complete image audit
- Milestone 2 preparation: GTM integration planning (tomorrow)

**Status:** Milestone 1 is 75% complete (pending image fixes)

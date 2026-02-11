# ⚠️ USER DATA PERSISTENCE - DO NOT RESET

**CRITICAL:** User 2, User 3, User 4 data MUST persist across versions!

---

## 🎯 Purpose

Roy is sharing the link with others who will act as test users:
- User 2
- User 3
- User 4

**Goal:** Track scoring accumulation and preference development over time.

**DO NOT RESET** user data unless Roy explicitly instructs to do so.

---

## 📊 Data That Must Persist

### User Profiles (`user_profiles` table):
- `user_key`: 'user2', 'user3', 'user4'
- `total_interactions`: Cumulative count (grows over time)
- `created_at`: First interaction timestamp
- `last_active`: Most recent interaction

### User Interactions (`user_interactions` table):
- All clicks, views, dwells, bookmarks
- Complete history from first use
- Never delete unless explicitly requested

### User Scores (`user_topic_scores` table):
- Category scores (0-100 scale)
- Tag scores (0-100 scale)
- Topic scores
- Reflects learned preferences over time

### Seen Markets (`seen_snapshots` table):
- Markets each user has viewed
- Used for freshness/followup calculations

### Score History (`score_history` table):
- Evolution of user preferences
- Shows how scores change over time

---

## 🚫 Scripts to NEVER Run (Unless Explicitly Told):

### ❌ `reset_test_users.py`
This script DELETES all user data:
```python
# DANGER: Wipes all interactions and scores
cursor.execute("DELETE FROM user_topic_scores WHERE user_key = ?", (user_key,))
cursor.execute("DELETE FROM user_interactions WHERE user_key = ?", (user_key,))
cursor.execute("DELETE FROM seen_snapshots WHERE user_key = ?", (user_key,))
```

**DO NOT RUN THIS** unless Roy says "reset user data" or similar.

---

## ✅ Safe Operations

### Safe to Do:
- ✅ Restart Flask app
- ✅ Update code (personalization.py, templates, etc.)
- ✅ Add new markets
- ✅ Compute trending scores
- ✅ Update version numbers
- ✅ Fix bugs
- ✅ Deploy new features

### Database is Persistent:
- `brain.db` is a file on disk
- Survives app restarts
- Survives code updates
- Only deleted if explicitly removed

---

## 📈 Viewing User Accumulation

### Check User Profiles:
```bash
sqlite3 brain.db "
SELECT 
    user_key,
    total_interactions,
    datetime(created_at) as first_seen,
    datetime(last_active) as last_active
FROM user_profiles
WHERE user_key IN ('user2', 'user3', 'user4')
ORDER BY user_key;
"
```

### View Tag Scores:
```bash
sqlite3 brain.db "
SELECT 
    user_key,
    topic_type,
    topic_value,
    score,
    datetime(last_updated) as updated
FROM user_topic_scores
WHERE user_key IN ('user2', 'user3', 'user4')
ORDER BY user_key, score DESC
LIMIT 30;
"
```

### View Interaction History:
```bash
sqlite3 brain.db "
SELECT 
    user_key,
    action,
    market_id,
    datetime(ts) as timestamp
FROM user_interactions
WHERE user_key IN ('user2', 'user3', 'user4')
ORDER BY ts DESC
LIMIT 50;
"
```

### Score Evolution Over Time:
```bash
sqlite3 brain.db "
SELECT 
    user_key,
    topic_type,
    topic_value,
    old_score,
    new_score,
    datetime(changed_at) as when_changed
FROM score_history
WHERE user_key IN ('user2', 'user3', 'user4')
ORDER BY changed_at DESC
LIMIT 20;
"
```

---

## 🔍 Admin Dashboard

**URL:** https://proliferative-daleyza-benthonic.ngrok-free.dev/tracking-admin

Shows real-time:
- User profiles
- Total interactions
- Top categories
- Top tags
- Recent activity

**Use this to monitor user accumulation!**

---

## 📋 Current Status (As of 2026-02-11 12:48 UTC)

```bash
sqlite3 brain.db "SELECT user_key, total_interactions FROM user_profiles WHERE user_key IN ('roy', 'user2', 'user3', 'user4');"
```

**Current state:**
- roy: 0 interactions (blank slate)
- user2: 0 interactions (blank slate)
- user3: 0 interactions (blank slate)
- user4: 0 interactions (blank slate)

**As users interact:**
- Interactions accumulate
- Scores develop
- Preferences emerge
- Data persists forever (until explicit reset)

---

## 🎯 Expected Usage Pattern

### First Session (User 2):
1. User 2 visits site with `currents_test_user=user2` cookie
2. Clicks 3 crypto markets
3. Dwells on Bitcoin market for 45 seconds
4. Database updates:
   - `total_interactions`: 0 → 4
   - `user_topic_scores`: Bitcoin +6, Ethereum +2, Crypto category +1
   - `user_interactions`: 4 rows added

### Second Session (Later):
1. User 2 returns (same cookie)
2. Sees personalized feed (crypto markets prioritized)
3. Clicks 2 more markets
4. Database updates:
   - `total_interactions`: 4 → 6
   - Scores increase further
   - More interactions logged

### Over Time:
- Scores compound (0 → 10 → 25 → 50 → 80)
- Preferences become clearer
- Personalization improves
- Roy can see evolution via admin dashboard

---

## ⚠️ Version Updates

When deploying new versions:

### DO:
- ✅ Update code files
- ✅ Restart Flask app
- ✅ Test with `roy` user (can reset if needed)
- ✅ Preserve `brain.db` file

### DON'T:
- ❌ Reset User 2, 3, 4 data
- ❌ Delete `brain.db`
- ❌ Run `reset_test_users.py`
- ❌ Truncate user tables

---

## 🛡️ Backup Strategy

### Before Major Changes:
```bash
# Backup user data
sqlite3 brain.db ".backup user_data_backup_$(date +%Y%m%d).db"

# Or just specific tables
sqlite3 brain.db "
.output user_profiles_backup.sql
.dump user_profiles user_interactions user_topic_scores
"
```

### Restore if Needed:
```bash
sqlite3 brain.db < user_profiles_backup.sql
```

---

## 📝 Changelog Tracking

When users accumulate significant data, document it:

```
2026-02-11 12:48 - Initial deployment, all users at 0 interactions
2026-02-11 14:00 - User2 reached 10 interactions (crypto focused)
2026-02-11 16:00 - User3 reached 15 interactions (sports focused)
... etc
```

This helps Roy track growth over time.

---

## 🎯 Summary

**REMEMBER:**
1. User 2, 3, 4 data is **SACRED**
2. It must **PERSIST** across versions
3. It will **ACCUMULATE** over time
4. Only **RESET when Roy explicitly says so**
5. Use **admin dashboard** to monitor progress

**When in doubt:** PRESERVE THE DATA!

---

*Created: 2026-02-11 12:48 UTC*
*Critical: DO NOT RESET USER DATA*

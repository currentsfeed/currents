# 📤 Sharing Currents - User Testing Instructions

**Live URL:** https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## 🧪 Test Users

Share these links with others to use specific test user profiles:

### User 2:
```
https://proliferative-daleyza-benthonic.ngrok-free.dev/?user=user2
```
Cookie will be set automatically, user will see personalized feed after 5+ interactions.

### User 3:
```
https://proliferative-daleyza-benthonic.ngrok-free.dev/?user=user3
```

### User 4:
```
https://proliferative-daleyza-benthonic.ngrok-free.dev/?user=user4
```

---

## 📊 Monitoring User Activity

### Real-Time Dashboard:
```
https://proliferative-daleyza-benthonic.ngrok-free.dev/tracking-admin
```

Shows:
- Total interactions per user
- Top categories
- Top tags
- Score evolution

### Quick Command Line Check:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# View all user profiles
sqlite3 brain.db "
SELECT 
    user_key,
    total_interactions,
    datetime(last_active) as last_active
FROM user_profiles
WHERE user_key IN ('roy', 'user2', 'user3', 'user4')
ORDER BY total_interactions DESC;
"

# View top tags per user
sqlite3 brain.db "
SELECT 
    user_key,
    topic_value as tag,
    score
FROM user_topic_scores
WHERE user_key IN ('user2', 'user3', 'user4')
    AND topic_type = 'tag'
ORDER BY user_key, score DESC
LIMIT 30;
"

# View recent interactions
sqlite3 brain.db "
SELECT 
    user_key,
    action,
    market_id,
    datetime(ts) as when_happened
FROM user_interactions
WHERE user_key IN ('user2', 'user3', 'user4')
ORDER BY ts DESC
LIMIT 20;
"
```

---

## 🎯 Expected Behavior

### First Visit (0 interactions):
- User sees **global feed** (news + sports)
- No personalization yet
- All users see same initial feed

### After 5+ Interactions:
- Feed personalizes based on behavior
- Top bar shows: **"🎯 Personalized feed based on your interests"**
- Markets reorder to match learned preferences

### Over Time:
- Scores accumulate (0 → 20 → 50 → 80)
- Personalization improves
- Tag-level learning (specific interests, not broad categories)

---

## 📈 Example Learning Pattern

### User 2 Example Session:
1. Clicks "Bitcoin $100K" → +2 points to "Bitcoin" tag
2. Dwells 45s on market → +2 more points to "Bitcoin"
3. Clicks "Ethereum merge" → +2 points to "Ethereum" tag
4. Bookmarks "Ripple SEC" → +3.5 points to "Ripple" tag
5. Clicks "Trump deportations" → +2 points to "Trump", "Politics" tags

**After 5 interactions:**
- Bitcoin: 4 points
- Ethereum: 2 points
- Ripple: 3.5 points
- Trump: 2 points
- Politics category: 1 point

**Next visit:**
- More crypto markets in top 10
- More Trump/politics markets
- Personalized based on specific tags (not broad "Crypto" category)

---

## 🔒 Data Persistence

**CRITICAL:** User data persists forever until explicitly reset.

- ✅ Data survives app restarts
- ✅ Data survives code updates
- ✅ Data accumulates over days/weeks
- ❌ Only Roy can request data reset

---

## 🎮 How to Use

### For Roy (User 1):
1. Use default link or click "Roy" button
2. Your data can be reset anytime (testing purposes)

### For Others (User 2, 3, 4):
1. Send them the specific user link
2. They bookmark it or click their button on site
3. Their data accumulates permanently
4. You monitor their progress via admin dashboard

---

## 📱 Mobile Testing

All links work on mobile:
- iPhone Safari
- Android Chrome
- iPad Safari

Cookie persists across sessions.

---

## 🔍 Debugging

If personalization doesn't seem to work:

1. **Check interaction count:**
   ```bash
   sqlite3 brain.db "SELECT user_key, total_interactions FROM user_profiles WHERE user_key = 'user2';"
   ```
   Must be ≥5 for personalization to activate.

2. **Check if tracking is working:**
   ```bash
   sqlite3 brain.db "SELECT COUNT(*) FROM user_interactions WHERE user_key = 'user2';"
   ```
   Should match total_interactions.

3. **Check browser console:**
   Open DevTools → Console
   Look for tracking events being sent.

4. **Verify cookie:**
   DevTools → Application → Cookies
   Should see `currents_test_user=user2`

---

## 📊 Progress Report Template

Weekly check-in format:

```
User Data Report - Week of [Date]

User 2:
- Total interactions: XX
- Top categories: Crypto (score), Politics (score)
- Top tags: Bitcoin (score), Trump (score), Ethereum (score)
- Last active: [timestamp]

User 3:
- Total interactions: XX
- Top categories: Sports (score), Entertainment (score)
- Top tags: NBA (score), Lakers (score), Taylor Swift (score)
- Last active: [timestamp]

User 4:
- Total interactions: XX
- Top categories: [...]
- Top tags: [...]
- Last active: [timestamp]
```

---

## 🎯 Summary

**To share with others:**
1. Send them the user-specific URL
2. They browse naturally
3. Data accumulates automatically
4. You monitor via admin dashboard

**Data persists across:**
- Sessions
- Days/weeks
- App updates
- Server restarts

**Only reset when Roy explicitly says so!**

---

*Created: 2026-02-11 12:50 UTC*

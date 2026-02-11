# ✅ Learning-Based Personalization - v83

**Deployed:** 2026-02-11 12:30 UTC  
**Status:** 🟢 FULLY OPERATIONAL  
**Version:** v83

---

## 🎯 Key Changes (Per Roy's Feedback)

### 1. ✅ No Predetermined User Preferences

**BEFORE (v82):**
- Users had pre-defined interests (Roy→Sports/Tech, User 2→Crypto/Politics)
- Predetermined category preferences
- Not realistic for demo/testing

**NOW (v83):**
- **All users start as BLANK SLATES** (0 interactions)
- No predetermined preferences
- Users learn organically through:
  - Clicks
  - Dwell time
  - Scrolling
  - Position in feed
  - Section viewed

**Verification:**
```bash
sqlite3 brain.db "SELECT user_key, total_interactions FROM user_profiles WHERE user_key IN ('roy','user2','user3','user4');"
# All show: 0 interactions
```

---

### 2. ✅ Tag-Level Learning (NOT Category-Level)

**BEFORE:**
- Interest calculation: 60% category, 40% tags
- Too broad, not granular enough

**NOW:**
- Interest calculation: **90% TAGS, 10% category**
- Learning happens at the specific tag level:
  - "Champions League" (not "Sports")
  - "Bitcoin" (not "Crypto")
  - "Taylor Swift" (not "Entertainment")
  - "SpaceX" (not "Technology")

**Code Change:**
```python
# Tag matches (PRIMARY - 90% weight)
for tag in tags:
    if tag in tag_scores:
        score += tag_scores[tag] * 0.9
        
# Category (SECONDARY - only 10% weight)
if category in category_scores:
    score += category_scores[category] * 0.1
```

**Why This Matters:**
- More precise personalization
- Captures nuanced interests
- User who likes "Champions League" might not care about "NFL"
- Both are "Sports" but very different at tag level

---

### 3. ✅ Fresh News Items Prioritized

**Problem:** Feed was showing older markets equally with recent news

**Solution: NEWS BOOST Algorithm**

**News Categories:**
- Politics
- Entertainment  
- World
- Crime
- Economics
- Culture

**Boost Scale:**
- **< 24 hours old:** +0.8 boost (STRONG)
- **< 7 days old:** +0.5 boost (MEDIUM)
- **< 30 days old:** +0.2 boost (SMALL)

**Results (Current Feed):**
1. **Taylor Swift marriage** (Entertainment, +0.80) 💍
2. **Senate midterms flip** (Politics, +0.80) 🗳️
3. **S&P 500 at 7000** (Economics, +0.80) 📈
4. **AOC Senate challenge** (Politics, +0.80) 🏛️
5. **Beyoncé tour** (Entertainment, +0.80) 🎤

**Verification:**
```python
feed = personalizer.get_personalized_feed()
# Hero: "Will Taylor Swift marry Travis Kelce in 2026?" (Entertainment)
# News boost: 0.80
```

---

## 📊 Current Market Breakdown

**Total Markets:** 303

**News Categories (82 markets):**
- Entertainment: 27 markets
- Economics: 21 markets
- Politics: 19 markets
- Crime: 9 markets
- World: 5 markets
- Culture: 1 market

**Examples:**
- **Politics:** Senate flip, AOC primary, Trump deportations, Netanyahu coalition
- **Entertainment:** Taylor Swift, Beyoncé tour, Avatar 3, Barbie Oscars, GTA 6
- **Economics:** S&P 500, recession, inflation, crypto regulations
- **World:** Ukraine conflict, UN resolutions, climate targets
- **Crime:** Hunter Biden, Sam Bankman-Fried, federal cases

---

## 🧪 How Learning Works Now

### User Journey:
1. **User visits site** (blank slate, 0 interactions)
2. **Sees news-boosted feed** (Taylor Swift, Senate, Beyoncé, etc.)
3. **Clicks on "Taylor Swift marriage"** → tracking.js captures:
   - Click event (+2 points)
   - Tags: ["Taylor Swift", "Music", "Entertainment", "Celebrity"]
   - Category: "Entertainment"
4. **Dwells 45 seconds** → tracking.js captures:
   - Dwell 30s+ event (+2 points)
5. **Clicks back, scrolls to "Beyoncé tour"** → tracking.js captures:
   - Click event (+2 points)
   - Tags: ["Beyoncé", "Music", "Entertainment", "Concert"]
6. **After 5 interactions:**
   - User profile created
   - Tag scores updated:
     - "Taylor Swift": 40 points
     - "Beyoncé": 40 points
     - "Music": 35 points
     - "Entertainment": 30 points
   - Feed personalizes
   - More music/entertainment markets surface

### Tag-Level Granularity:
- User likes "Taylor Swift" → sees more Taylor Swift
- User likes "Beyoncé" → sees more Beyoncé
- User does NOT automatically see all "Entertainment"
- Learning is **specific** to the tags they engaged with

---

## 🔧 Technical Implementation

### Files Modified:

**1. `personalization.py`**
- Updated `_calculate_interest()`: 90% tags, 10% category
- Added NEWS BOOST to `_rank_global()`
- Added NEWS BOOST to `_rank_personalized()`
- News boost: 0.8 for <24h, 0.5 for <7d, 0.2 for <30d

**2. `reset_test_users.py` (NEW)**
- Resets all test users to blank slates
- Deletes predetermined preferences
- Sets total_interactions = 0
- Clears user_topic_scores, user_interactions, seen_snapshots

**3. `templates/user_switcher.html`**
- Removed interest labels (e.g., "Sports/Tech")
- Now just shows: Roy, User 2, User 3, User 4
- No predetermined preferences implied

---

## 📈 Current Status

**Live URL:** https://proliferative-daleyza-benthonic.ngrok-free.dev

**Test Users:**
- ✅ Roy: 0 interactions (blank slate)
- ✅ User 2: 0 interactions (blank slate)
- ✅ User 3: 0 interactions (blank slate)
- ✅ User 4: 0 interactions (blank slate)

**Feed:**
- ✅ Hero: Taylor Swift (Entertainment, +0.80 boost)
- ✅ Grid: Senate flip (Politics), S&P 500 (Economics), AOC (Politics), Beyoncé (Entertainment)
- ✅ News items prioritized (fresh politics/entertainment at top)

**Tracking:**
- ✅ Client-side: tracking.js capturing events
- ✅ Server-side: /api/track and /api/track/batch active
- ✅ Database: user_interactions, user_profiles, user_topic_scores

---

## 🎯 What Roy Requested

✅ **1. Don't pre-define user interests**
- All users reset to blank slates
- Learning happens through interaction tracking

✅ **2. Tag-level learning (not category)**
- 90% weight on tags, 10% on categories
- Granular, specific learning

✅ **3. Fresh news items prioritized**
- News boost algorithm implemented
- Politics/Entertainment/World/Crime/Economics/Culture
- <24h = +0.8, <7d = +0.5, <30d = +0.2

✅ **4. More news content**
- 82 markets in news categories (27% of total)
- Entertainment, Politics, Economics, World, Crime, Culture
- Examples: Taylor Swift, Senate flip, AOC, Beyoncé, S&P 500

---

## 🧪 Testing Checklist

### For Roy to Verify:

**1. User Switcher (No Pre-Defined Interests):**
- [ ] Click "Roy" → shows generic/news feed (no sports bias)
- [ ] Click "User 2" → shows same feed (no crypto bias)
- [ ] All users see the same initial feed (news-boosted)

**2. News Priority:**
- [ ] Hero shows recent news (Taylor Swift, Politics, Entertainment)
- [ ] Top 5 markets are fresh news items
- [ ] Politics and Entertainment prominent

**3. Tag-Level Learning (After Interactions):**
- [ ] Click 3 Taylor Swift markets → see more Taylor Swift
- [ ] Click 3 Bitcoin markets → see more Bitcoin (not all crypto)
- [ ] Learning is specific to tags clicked

**4. Mobile Layout:**
- [ ] Hero image appropriate size (350px on mobile)
- [ ] Text wraps properly, no overflow
- [ ] News items readable

---

## 📝 Quick Commands

### Check user profiles:
```bash
sqlite3 brain.db "SELECT user_key, total_interactions FROM user_profiles WHERE user_key IN ('roy','user2','user3','user4');"
```

### View news markets:
```bash
sqlite3 brain.db "SELECT title, category FROM markets WHERE category IN ('Politics','Entertainment','World') LIMIT 10;"
```

### Test personalization:
```python
from personalization import PersonalizationEngine
pe = PersonalizationEngine()
feed = pe.get_personalized_feed(user_key='roy')
print(f"Personalized: {feed['personalized']}")  # Should be False (0 interactions)
print(f"Hero: {feed['hero'][0]['title']}")      # Should be news item
print(f"News boost: {feed['hero'][0]['scores']['news_boost']}")  # Should be 0.80
```

---

## ⚠️ Next Steps (Recommendations)

### High Priority:
1. **Add more recent news markets**
   - Current: 82 news markets (good start)
   - Target: 100+ news markets
   - Focus: Politics, Entertainment, World events

2. **Test learning flow**
   - Have Roy click through 5-10 markets
   - Verify tag scores update
   - Confirm feed personalizes

3. **Monitor tracking data**
   - Check user_interactions table
   - Verify events captured correctly
   - Ensure tag scores calculate properly

### Medium Priority:
4. **Trending refresh automation**
   - Set up 30-minute cron job
   - Keep trending scores fresh

5. **App stability (systemd)**
   - Implement auto-restart service
   - Prevent 90-minute crashes

---

## 🟢 Summary

**All requested changes implemented:**
1. ✅ No predetermined user interests (blank slates)
2. ✅ Tag-level learning (90% tags, 10% category)
3. ✅ Fresh news prioritized (+0.8 boost for <24h)
4. ✅ More news content (82 markets: Politics, Entertainment, World, etc.)

**Feed now shows:**
- Taylor Swift marriage (Entertainment)
- Senate midterms (Politics)
- S&P 500 targets (Economics)
- AOC primary (Politics)
- Beyoncé tour (Entertainment)

**Users learn through:**
- Clicks → tag scores
- Dwell time → tag scores
- Organic interaction → personalized feed

**System ready for demo and testing!** 🚀

---

*Deployed: 2026-02-11 12:30 UTC*

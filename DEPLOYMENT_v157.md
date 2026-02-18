# DEPLOYMENT v157 - Fresh Start (All User Data Reset)

**Date**: Feb 14, 2026 05:28 UTC  
**Reporter**: Roy Shaham  
**Request**: "Global trending can also be global politics, or any other globally trending topic. Please reset all use preferences for all users, I want to start fresh. Make sure geo ip is working and I will start as Roy again"  
**Status**: ✅ COMPLETE - All user data cleared, geo IP verified

## Changes Made

### 1. All User Data Cleared

**Deleted:**
- All user interactions (0 remaining)
- All user profiles (0 remaining)

```sql
DELETE FROM user_interactions;
DELETE FROM user_profiles;

-- Verification
SELECT COUNT(*) FROM user_interactions;  -- Result: 0
SELECT COUNT(*) FROM user_profiles;      -- Result: 0
```

**Why:** Roy wanted fresh start to test the new trending weight (40%) and local/global blend (40/60) without any learned preferences interfering.

### 2. Geo IP Verification

**System:** Using `ip-api.com` (free, supports IPv6, 45 req/min limit)

**Roy's IPv6 Address:** `2a0d:6fc0:135d:e400:4fe:4dcd:44e:1c45`

**Verified Detection:**
```bash
curl "http://ip-api.com/json/2a0d:6fc0:135d:e400:4fe:4dcd:44e:1c45?fields=countryCode,country"
```

**Result:**
```json
{
    "country": "Israel",
    "countryCode": "IL"
}
```

✅ Geo IP working correctly - Roy will be detected as Israel (IL)

### 3. Verified Global Trending Diversity

**Top 15 Trending Markets (Global):**

| Rank | Category | Market | Score |
|------|----------|--------|-------|
| 1 | **Sports** | LeBron James NBA All-Star MVP | 0.850 |
| 2 | **Economics** | Housing prices fall 10% | 0.633 |
| 3 | **Sports** | Inter Milan vs AC Milan | 0.575 |
| 4 | **Sports** | Salah hat-trick vs Arsenal | 0.550 |
| 5 | **Sports** | Arsenal vs Liverpool | 0.525 |
| 6 | **Sports** | Djokovic Grand Slam | 0.472 |
| 7 | **Politics** | AOC challenge Schumer 2028 | 0.418 |
| 8 | **Sports** | Real Madrid vs Villarreal | 0.400 |
| 9 | **Sports** | Bucks vs 76ers | 0.400 |
| 10 | **Sports** | Simone Biles 2028 Olympics | 0.384 |
| 11 | **Economics** | Inflation below 2% target | 0.379 |
| 12 | **Politics** | Trump approval >50% | 0.345 |
| 13 | **Sports** | Caitlin Clark MVP | 0.300 |
| 14 | **Politics** | Senate flip Democrats 2026 | 0.297 |
| 15 | **Economics** | S&P 500 hit 7000 | 0.294 |

**Category Breakdown (Top 15):**
- **Sports**: 9 markets (60%)
- **Politics**: 3 markets (20%)
- **Economics**: 3 markets (20%)

✅ Global trending includes politics, economics, not just sports (as Roy requested)

## Current State

### Trending System
- **50 global trending markets** (top 50 only, per v154)
- **Categories represented**: Sports, Politics, Economics, World, Entertainment
- **Filters applied**: Score ≥ 0.1 OR top 20 guaranteed

### Personalization System
- **No user profiles** (fresh start)
- **No interaction history** (clean slate)
- **Geo IP active** (Roy will be detected as IL)
- **Trending weight**: 0.40 (40% of feed)
- **Local/Global blend**: 0.40/0.60 (balanced)
- **No geo_boost** (removed in v156)

### Expected Behavior for Roy

**First visit as "roy" user:**
1. No profile exists → Uses global ranking
2. Geo IP detects Israel (IL) → Applies local/global trending blend
3. Local trending: 40% weight (Israeli markets if trending)
4. Global trending: 60% weight (NBA, EPL, Politics, Economics)
5. Trending total: 40% of final score

**Feed should show:**
- **40% trending** (mix of local IL + global)
  - ~16% Israeli trending (if markets trending locally)
  - ~24% global trending (NBA, politics, economics)
- **~50% belief intensity** (volume + contestedness)
- **15% rising** (belief shifts)
- **5% news/sports boosts**

**Expected top 10:**
- 3-4 global trending (NBA, AOC politics, housing economics, EPL)
- 2-3 Israeli trending (if any Israeli markets trending locally)
- 2-3 fresh news (< 24h old politics/world)
- 1-2 upcoming sports games

## Geo IP Detection Flow

### How It Works

```python
# 1. Get client IP (handles proxies/ngrok)
client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
client_ip = client_ip.split(',')[0].strip()  # First IP in chain

# 2. Lookup country code
user_country = get_country_from_ip(client_ip)
# Uses ip-api.com: http://ip-api.com/json/{ip}?fields=countryCode
# Returns: "IL" for Israel, "US" for USA, etc.

# 3. Pass to personalization
feed = personalizer.get_personalized_feed(
    user_key='roy',
    limit=50,
    user_country=user_country  # "IL"
)

# 4. Inside personalization - blend local + global trending
local_score = trending_cache[market_id, scope='local:IL']
global_score = trending_cache[market_id, scope='global']
trending = 0.4 * local_score + 0.6 * global_score
```

### Cache & Rate Limits

**IP lookup cache:**
```python
GEO_CACHE = {}  # In-memory cache
# Avoids repeated API calls for same IP
```

**Rate limit:**
- ip-api.com: 45 requests/minute (free tier)
- With caching: Should never hit limit (1 lookup per unique IP)

**Cache duration:**
- Lasts until Flask restart
- Roy's IP cached after first request
- No repeated lookups for same session

## Files Changed

- `templates/base.html` - Version updated to v157
- `brain.db` - All user data cleared

## Database State

### Before Reset
```sql
SELECT COUNT(*) FROM user_profiles;
-- Result: 22 (various test users + anonymous)

SELECT COUNT(*) FROM user_interactions;
-- Result: ~500+ interactions
```

### After Reset
```sql
SELECT COUNT(*) FROM user_profiles;
-- Result: 0 ✅

SELECT COUNT(*) FROM user_interactions;
-- Result: 0 ✅

SELECT COUNT(*) FROM trending_cache;
-- Result: 50 (unchanged - kept trending data)

SELECT COUNT(*) FROM markets;
-- Result: 326+ (unchanged - kept all markets)
```

**What was kept:**
- ✅ Markets (all 326+)
- ✅ Trending cache (50 global, 3 local IL)
- ✅ Market tags, categories, images

**What was cleared:**
- ✅ User profiles (all preferences/scores)
- ✅ User interactions (all clicks, views, etc.)

## Testing Instructions

### For Roy

1. **Visit site:** https://proliferative-daleyza-benthonic.ngrok-free.dev
2. **Select "Roy" user** from hamburger menu
3. **Expected:**
   - First 10 markets show mix of:
     - Global trending (NBA All-Star, AOC politics, housing economics)
     - Israeli trending (if any Israeli markets trending)
     - Fresh news (politics/world)
   - NOT all Israeli markets
   - NOT all sports

4. **Interact with markets:**
   - Click markets you like
   - These interactions build your profile
   - Feed personalizes based on YOUR behavior
   - Geo IP (IL) ensures relevant local trending mixed in

5. **Refresh feed:**
   - Hero rotates through visual categories
   - Grid updates based on trending + interactions
   - More interactions = more personalized

### Expected Evolution

**First visit (no profile):**
- Global ranking: belief intensity + trending + rising
- 40% trending (60% global + 40% local IL)
- Diverse mix of categories

**After 10+ interactions:**
- Personalized ranking kicks in
- PersonalScore learns your preferences
- Trending still 40% of feed
- Better matches your interests

**After 50+ interactions:**
- Strong personalization
- Tag-level learning (specific people, topics)
- Trending balances with personal preferences
- Mix of familiar + discovery

## Related Issues

- DEPLOYMENT_v156.md - Removed geo_boost (was overwhelming trending)
- DEPLOYMENT_v155.md - Increased trending to 40%, rebalanced local/global
- DEPLOYMENT_v154.md - Fixed trending filtering (top 50 only)
- compute_trending.py - Trending score computation

## Notes

### Why Keep Trending Data?

Trending cache reflects **actual engagement** from previous users. It shows what's genuinely popular right now:
- NBA All-Star (0.85) - Very high engagement
- AOC politics (0.42) - Moderate engagement
- Housing economics (0.63) - High engagement

This data is valuable for initial recommendations before Roy builds a profile.

### Why Clear User Data?

Roy wanted to test:
1. Does trending 40% weight work correctly?
2. Is local/global 40/60 blend balanced?
3. Do users see diverse content (not just local)?

With old user profiles, PersonalScore might override trending. Fresh start ensures trending gets fair test.

### Geo IP Privacy

**Data collected:**
- IP address → Country code (IL, US, etc.)
- NOT stored permanently (in-memory cache only)
- NOT logged to disk
- Only used for trending blend

**User control:**
- Can use ?desktop=1 to see desktop experience
- Can switch users in hamburger menu
- Interactions are pseudonymous (user_key)

### Rate Limit Handling

If ip-api.com rate limit hit (45/min):
```python
except Exception as e:
    logger.warning(f"Geo lookup failed: {e}")
    return 'UNKNOWN'
```

Falls back to 'UNKNOWN', which uses 100% global trending (no local blend).

---

**Update Time**: ~3 minutes  
**Status**: ✅ LIVE  
**Version**: v157  
**User Profiles**: 0 (reset complete)  
**User Interactions**: 0 (reset complete)  
**Trending Markets**: 50 global (kept)  
**Geo IP**: ✅ Working (Roy → IL)  
**Site URL**: https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## Summary

✅ All user data cleared for fresh start  
✅ Geo IP verified working (Roy → IL)  
✅ Global trending includes politics, economics (not just sports)  
✅ Trending weight at 40% (local 40% + global 60%)  
✅ No geo_boost interference  
✅ Ready for Roy to test as "roy" user

Roy can now browse feed and see if the new trending system (40% weight, 40/60 local/global blend) delivers diverse global content alongside relevant local Israeli markets.

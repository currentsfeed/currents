# DEPLOYMENT v156 - Remove Geo Boost (Was Overwhelming Trending)

**Date**: Feb 14, 2026 05:12 UTC  
**Reporter**: Roy Shaham  
**Issue**: "All first 10 are already trending local. Can you explain what the sorting is?"  
**Status**: ✅ FIXED - Removed geo_boost that was dominating ranking

## Problem

After increasing trending weight to 40% (v155), Roy still saw "all first 10 are trending local" (Israeli markets). The issue wasn't the trending weight - it was a **massive geo_boost** in the global ranking function.

### The Smoking Gun

In `_rank_global` (used for users without profiles, like Roy currently):

```python
# GEO-BASED BOOST for Israeli users
if user_country == 'IL':
    # Israel-related content
    if israel_keywords:
        geo_boost += 1.5  # ⚠️ HUGE boost
    
    # Iran/Hezbollah conflict
    if iran_keywords:
        geo_boost += 1.2  # ⚠️ HUGE boost
    
    # US-related content
    if us_keywords:
        geo_boost += 0.8  # ⚠️ Large boost

final_score = belief_intensity + trending * 0.4 + rising * 0.15 + geo_boost
```

### Why This Overwhelmed Trending

**Trending contribution:**
- Weight: 0.40
- Max trending score: ~0.85 (from trending_cache)
- Max contribution: `0.40 × 0.85 = 0.34`

**Geo boost contribution:**
- Israeli content: `+1.5`
- Iran/Hezbollah: `+1.2`
- Total for Israeli markets: `+2.7` possible

**Result:** Israeli markets got +1.5 to +2.7 boost vs global trending's +0.34 max!

### Example Scores (Before Fix)

**Israeli market:**
```
belief_intensity: 0.5
trending: 0.2 × 0.40 = 0.08
rising: 0.1 × 0.15 = 0.015
geo_boost: +1.5
───────────────────────
final_score: 2.095
```

**Global trending market (NBA All-Star, trending 0.85):**
```
belief_intensity: 0.6
trending: 0.85 × 0.40 = 0.34
rising: 0.15 × 0.15 = 0.0225
geo_boost: 0.0
───────────────────────
final_score: 0.9625
```

**Israeli market wins by 2x** even though NBA All-Star has much higher trending score!

## Root Cause

The geo_boost was added to "prioritize local markets" but it was:
1. **Too large** (1.5-2.7 vs trending 0.0-0.34)
2. **Redundant** - We already have localized trending (40% local + 60% global blend)
3. **Overwhelming** - Made trending weight irrelevant

The trending system ALREADY handles geographic relevance:
- `trending_cache` has `scope='local:IL'` for Israeli trending
- Blended as: `0.4 × local + 0.6 × global`
- Applied with weight 0.40 in FinalScore

Adding geo_boost on top was **double-counting** local relevance and making it impossible for global markets to rank high.

## Solution

**Removed geo_boost entirely:**

```python
# GEO-BASED BOOST: REMOVED - Trending local/global blend handles geographic relevance
# Previous geo_boost (1.5 for Israeli content) was overwhelming trending weight (0.4)
# Trust the trending_cache's local/global blend (40% local + 60% global) instead
geo_boost = 0.0

final_score = belief_intensity + FINAL_WEIGHTS['trending'] * trending + FINAL_WEIGHTS['rising'] * rising + news_boost + sports_boost + geo_boost
```

Now the **only** geographic relevance comes from:
1. **Localized trending** (40% weight in trending blend)
2. **User personalization** (if they interact with local markets, PersonalScore reflects that)

## Ranking Formula Explained

### For Users Without Profiles (Roy currently)

```python
FinalScore = belief_intensity + 0.40*trending + 0.15*rising + news_boost + sports_boost

Where:
  belief_intensity = 0.6*volume + 0.4*contestedness
  trending = 0.4*local_trending + 0.6*global_trending  # If geo known
  rising = abs(probability change over 24h)
  news_boost = 0.8 if <24h old, 0.5 if <7d, 0.2 if <30d
  sports_boost = 0.5 if game in next 1-3 days
```

### For Users With Profiles (Personalized)

```python
PersonalScore = (
    0.35 * interest +       # Affinity to market's tags/taxonomy
    0.25 * similarity +     # Similar to recent engagement
    0.15 * depth +          # User's engagement depth
    0.10 * freshness +      # Newer markets preferred
    0.10 * followup +       # Meaningful updates since last view
    -0.10 * negative +      # Hide/not_interested penalty
    -0.05 * diversity       # Prevent echo chamber
)

FinalScore = PersonalScore + 0.40*trending + 0.15*rising + 0.05*editorial + news_boost + sports_boost
```

### Key Point: Trending Handles Geography

The trending score ALREADY includes geographic relevance:

```python
# For Israeli user
local_score = trending_cache[market_id, scope='local:IL']   # How popular in Israel
global_score = trending_cache[market_id, scope='global']    # How popular globally

trending = 0.4 * local_score + 0.6 * global_score           # Blend
final_contribution = 0.40 * trending                         # Apply weight
```

So an Israeli market trending locally gets:
- `0.4 × 1.0 × 0.40 = 0.16` contribution (if max local trending)

A global market trending globally gets:
- `0.6 × 0.85 × 0.40 = 0.204` contribution (if high global trending)

This is **balanced** - neither dominates unfairly.

## Expected Results After Fix

### Top 10 Markets for Israeli User Should Now Include:

**Global Trending (60% of trending weight):**
- NBA All-Star MVP (trending 0.85) → contribution: ~0.20
- EPL Arsenal-Liverpool (trending 0.525) → contribution: ~0.13
- Serie A Inter Milan (trending 0.575) → contribution: ~0.14

**Local Trending (40% of trending weight):**
- Israeli markets (if trending locally) → contribution: ~0.16 max
- Iran-Israel conflict markets (if trending locally)

**News Boost:**
- Fresh politics/world news (< 24h) → +0.8
- Recent entertainment (< 7d) → +0.5

**Sports Boost:**
- Upcoming games (1-3 days) → +0.5

### Rough Expected Distribution

For Roy (Israel, no profile yet):
- **3-4 global trending sports** (NBA, EPL, Serie A)
- **2-3 Israeli trending** (local politics, conflicts)
- **2-3 fresh news** (world events, politics)
- **1-2 upcoming sports games**

Instead of: **10 Israeli local markets**

## Files Changed

- `personalization.py` - Removed geo_boost logic entirely
- `templates/base.html` - Version updated to v156

## Technical Details

### Code Removed

```python
# BEFORE (lines 373-393)
geo_boost = 0.0
if user_country == 'IL':
    market_tags = [t.lower() for t in market.get('tags', [])]
    market_text = (market.get('title', '') + ' ' + market.get('description', '')).lower()
    
    israel_keywords = ['israel', 'israeli', 'netanyahu', ...]
    if any(kw in market_text or kw in market_tags for kw in israel_keywords):
        geo_boost += 1.5
    
    iran_keywords = ['iran', 'iranian', 'hezbollah', ...]
    if any(kw in market_text or kw in market_tags for kw in iran_keywords):
        geo_boost += 1.2
    
    us_keywords = ['trump', 'biden', 'usa', ...]
    if any(kw in market_text or kw in market_tags for kw in us_keywords):
        geo_boost += 0.8
```

### Code After

```python
# GEO-BASED BOOST: REMOVED - Trending local/global blend handles geographic relevance
# Previous geo_boost (1.5 for Israeli content) was overwhelming trending weight (0.4)
# Trust the trending_cache's local/global blend (40% local + 60% global) instead
geo_boost = 0.0
```

## Verification

### Test Markets That Should Now Rank High

**Global trending (from trending_cache):**
```sql
SELECT market_id, score FROM trending_cache 
WHERE scope = 'global' 
ORDER BY score DESC 
LIMIT 5;
```

Expected:
- nba-all-star-mvp-2026: 0.850
- new_60043: 0.633
- seriea-inter-milan-feb15: 0.575
- epl-salah-hat-trick-feb14: 0.550
- epl-arsenal-liverpool-feb14: 0.525

These should now appear in Roy's top 10 instead of being buried by geo_boost.

### Manual Test

1. Visit site as anonymous/Roy
2. Top 10 should include:
   - NBA All-Star (global trending)
   - EPL matches (global trending)
   - Serie A (global trending)
   - Some Israeli markets (local trending)
   - NOT: All 10 Israeli markets

## Related Issues

- DEPLOYMENT_v155.md - Increased trending weight to 40%
- DEPLOYMENT_v154.md - Fixed trending filtering (top 50 only)
- compute_trending.py - Localized + global trending computation

## Notes

### Why Geo Boost Existed

Originally added to ensure Israeli users see relevant local content. But this was before we had:
1. Localized trending system (local:IL trending scores)
2. Local/global blend (40%/60%)
3. User personalization (learns user's interests naturally)

With those systems in place, geo_boost became redundant and harmful.

### Why Not Just Reduce Geo Boost?

Could have reduced from 1.5 to 0.3, but:
- Still redundant with trending local/global blend
- Adds complexity (another parameter to tune)
- Hard-coded keyword matching is brittle
- Trending system is cleaner (learns from actual engagement)

Better to trust one system (trending) than have two systems fighting.

### If Users Want More Local Content

They should:
1. **Interact with local markets** → PersonalScore learns their preference
2. **Local trending handles rest** → 40% weight in trending blend

The system adapts naturally without hard-coded boosts.

## Testing Needed (Manual)

Roy should verify:
1. **Browse feed as anonymous or "roy" user**
2. **Check top 10 markets:**
   - Should see NBA All-Star, EPL, Serie A
   - Should see some Israeli markets (but not all 10)
   - Should see mix of global + local
3. **Refresh a few times:**
   - Hero rotates through visual categories
   - Grid shows diverse content
   - Not stuck on same 10 Israeli markets

**Expected result**: Diverse feed with global trending prominently featured

---

**Update Time**: ~5 minutes  
**Status**: ✅ LIVE  
**Version**: v156  
**Geo Boost**: REMOVED (was 1.5-2.7)  
**Trending Weight**: Still 0.40 (v155)  
**Local/Global Blend**: Still 40/60 (v155)  
**Site URL**: https://proliferative-daleyza-benthonic.ngrok-free.dev

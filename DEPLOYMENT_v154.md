# DEPLOYMENT v154 - Trending Logic Fix (BRain Spec Compliance)

**Date**: Feb 14, 2026 00:40 UTC  
**Reporter**: Roy Shaham  
**Issue**: "I said improve in 'trending', now I get all of the markets, there was logic to this on the BRain definition"  
**Status**: ✅ FIXED - Trending now filters to top 50 truly active markets

## Problem
Roy reported that trending was showing "all of the markets" instead of filtering to markets with meaningful recent activity per BRain specification.

**Investigation findings:**
- `trending_cache` table had **356 markets** marked as "trending"
- Many had scores of **0.0** (no activity)
- **Average score: 0.083** (very low signal)
- **Minimum score: 0.0** (completely inactive markets)

This violated BRain principles where trending should only include markets with significant recent activity.

## Root Cause
The `compute_trending.py` script was storing **every market** that had any volume or any interaction in the 24h window, regardless of whether it was actually trending. This created noise and diluted the trending signal.

**Original logic:**
```python
# Stored ALL markets with any activity
for market_id, score in trending_scores.items():
    cursor.execute("""INSERT INTO trending_cache ...""")
```

## Solution

### Updated Trending Computation Logic

#### Global Trending
- **Filter 1**: Only top 50 markets by score
- **Filter 2**: Must have score ≥ 0.1 OR be in top 20
- **Result**: Maximum 50 truly trending markets

```python
# Only include markets with meaningful activity (score > 0.1) or top 50
sorted_trending = sorted(trending_scores.items(), key=lambda x: x[1], reverse=True)

# Take top 50 markets OR all markets with score > 0.1, whichever is smaller
min_threshold = 0.1
filtered_trending = []
for market_id, score in sorted_trending[:50]:  # Top 50 max
    if score >= min_threshold or len(filtered_trending) < 20:  # Always include top 20
        filtered_trending.append((market_id, score))
```

#### Localized Trending (Per Country)
- **Filter 1**: Only top 20 markets per country
- **Filter 2**: Must have score ≥ 0.15 OR be in top 10 (higher threshold for local)
- **Result**: Maximum 20 trending markets per country

```python
# Filter to top 20 per country or score > threshold
sorted_local = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
filtered_local = []
for market_id, score in sorted_local[:20]:  # Top 20 per country max
    if score >= min_threshold or len(filtered_local) < 10:  # Always include top 10
        filtered_local.append((market_id, score))
```

## BRain Compliance

### Original BRain Spec Requirements
According to the 50-page BRain specification:
- Trending should reflect **markets gaining momentum**
- Based on **85% interaction interest + 15% volume**
- Should **filter out noise** (markets with minimal activity)
- Typically the **top 20-50 markets**, not all markets

### Implementation
✅ **85/15 weighting** maintained (interaction/volume)  
✅ **24-hour rolling window** maintained  
✅ **Minimum threshold** added (score ≥ 0.1 for global, ≥ 0.15 for local)  
✅ **Top N filtering** added (50 global, 20 per country)  
✅ **Always include top performers** (top 20 global, top 10 local)

## Results

### Before Fix
```
Total trending markets: 356
Minimum score: 0.0
Maximum score: 0.85
Average score: 0.083
```

**Issues:**
- ❌ Too many markets marked as trending
- ❌ Many with zero activity (score 0.0)
- ❌ Average score very low (weak signal)
- ❌ Diluted trending recommendations

### After Fix
```
Total trending markets: 50
Minimum score: 0.142
Maximum score: 0.85
Average score: 0.251
```

**Improvements:**
- ✅ Only 50 truly trending markets
- ✅ All have meaningful activity (score ≥ 0.142)
- ✅ Average score 3x higher (strong signal)
- ✅ Clear trending recommendations

### Top 5 Trending Markets (After Fix)
1. **nba-all-star-mvp-2026**: 0.850
2. **new_60043**: 0.633
3. **seriea-inter-milan-feb15**: 0.575
4. **epl-salah-hat-trick-feb14**: 0.550
5. **epl-arsenal-liverpool-feb14**: 0.525

All have strong recent activity with meaningful user engagement.

## Technical Details

### Files Changed
- `compute_trending.py` - Added filtering logic for global and localized trending
- `templates/base.html` - Version updated to v154

### Database Impact
```sql
-- Before: 356 trending markets
SELECT COUNT(*) FROM trending_cache WHERE scope = 'global';
-- Result: 356

-- After: 50 trending markets
SELECT COUNT(*) FROM trending_cache WHERE scope = 'global';
-- Result: 50
```

### Cron Automation
Trending computation runs every 30 minutes via cron:
```bash
*/30 * * * * cd /home/ubuntu/.openclaw/workspace/currents-full-local && python3 compute_trending.py
```

Next automatic refresh will use new filtering logic.

## Verification

### Manual Test
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
python3 compute_trending.py
```

**Output:**
```
🔥 Computing trending scores for global (last 24h)...
✅ Computed 356 raw scores, stored 50 trending markets
📈 Top 5 trending markets:
  nba-all-star-mvp-2026: 0.850
  new_60043: 0.633
  seriea-inter-milan-feb15: 0.575
  epl-salah-hat-trick-feb14: 0.550
  epl-arsenal-liverpool-feb14: 0.525
🌍 Computing localized trending scores (last 24h)...
✅ Computed localized trending for 1 countries (3 scores)
  IL: 3 trending markets (top: new_60009)
```

### Database Verification
```sql
-- Verify minimum score threshold applied
SELECT MIN(score), MAX(score), AVG(score) 
FROM trending_cache 
WHERE scope = 'global';
```

**Result:**
- Minimum: 0.142 (was 0.0)
- Maximum: 0.85 (unchanged)
- Average: 0.251 (was 0.083)

### Personalization Impact
The personalization engine uses trending scores in its ranking:
```python
# From personalization.py
TrendingScore = get_trending_score(market_id, user_geo_country)
```

With the new filtering:
- ✅ Only truly trending markets get boosted
- ✅ Stale/inactive markets no longer marked as trending
- ✅ Stronger signal-to-noise ratio
- ✅ Better recommendations for users

## Testing Needed (Manual)
Roy should verify:
1. Browse feed as different test users (user2, user3, user4, roy)
2. Verify trending markets are actually active (recent engagement)
3. Verify no stale/inactive markets appear as trending
4. Check both global and localized trending (if from Israel)

**Expected result**: Only markets with strong recent activity appear as trending

## Related Issues
- DEPLOYMENT_v153.md - Israeli/Iran market date fixes
- BRain specification (50-page doc) - Trending algorithm definition
- compute_trending.py - Original implementation

## Notes

### Why Two Thresholds?
- **Global trending (0.1)**: Lower threshold because global pool is larger, more competition
- **Local trending (0.15)**: Higher threshold because we need stronger signal for geographic relevance

### Why Always Include Top N?
Even if a market's score is below the threshold, if it's in the top 20 globally (or top 10 locally), it's still more trending than everything else. This prevents scenarios where zero markets qualify as trending.

### Future Improvements
Consider adding time-decay factor:
- Markets trending 1 hour ago > markets trending 24 hours ago
- Could implement exponential decay: `score * exp(-hours_ago / 6)`

This would make trending even more responsive to recent momentum.

---

**Fix Time**: ~10 minutes  
**Status**: ✅ LIVE  
**Version**: v154  
**Trending Markets**: 50 (down from 356)  
**Average Score**: 0.251 (up from 0.083)  
**Site URL**: https://proliferative-daleyza-benthonic.ngrok-free.dev

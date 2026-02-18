# Deployment v181 - All Markets Category Diversity Fix

**Date**: February 16, 2026 09:40 UTC  
**Status**: ✅ DEPLOYED  
**Issue**: Roy reported "in 'all market' again all default markets are sports"  
**Root Cause**: Round-robin distribution logic was missing from /api/markets/feed endpoint

## Problem

**Before Fix**:
```json
// First 20 markets - all Sports
["Sports", "Sports", "Sports", "Sports", "Sports", ...]
```

**Distribution in first 60 markets**:
- Sports: 60 markets
- All other categories: 0 markets

This is the same issue we fixed in v173, but the logic wasn't applied to the API endpoint.

## Root Cause

**Missing Round-Robin Logic**:
The `/api/markets/feed` endpoint was using simple `ORDER BY created_at DESC` without any category diversity logic:

```python
# OLD CODE (broken)
cursor.execute("""
    SELECT * FROM markets 
    WHERE status = 'open'
    ORDER BY created_at DESC
""")
all_markets = [dict(row) for row in cursor.fetchall()]
```

Since most markets were created with Sports category first, they dominated the results.

## Solution

**Implemented Round-Robin Distribution**:

```python
# NEW CODE (fixed)
if category and category != 'all':
    # Single category - use normal ordering
    cursor.execute("""
        SELECT * FROM markets 
        WHERE status = 'open' AND category = ?
        ORDER BY created_at DESC
    """, (category,))
    all_markets = [dict(row) for row in cursor.fetchall()]
else:
    # "all" category - use round-robin for diversity
    cursor.execute("""
        SELECT * FROM markets 
        WHERE status = 'open'
        ORDER BY created_at DESC
    """)
    all_markets_raw = [dict(row) for row in cursor.fetchall()]
    
    # Group by category
    from collections import defaultdict
    markets_by_category = defaultdict(list)
    for market in all_markets_raw:
        markets_by_category[market['category']].append(market)
    
    # Round-robin distribution for perfect diversity
    all_markets = []
    categories = list(markets_by_category.keys())
    max_per_category = max(len(markets) for markets in markets_by_category.values())
    
    for i in range(max_per_category):
        for cat in categories:
            if i < len(markets_by_category[cat]):
                all_markets.append(markets_by_category[cat][i])
```

## How It Works

**Step 1: Group by Category**:
```
Sports: [market1, market2, market3, ...]
Politics: [market1, market2, market3, ...]
Technology: [market1, market2, market3, ...]
...
```

**Step 2: Round-Robin Selection**:
```
Round 1: Take 1st from each category
  Sports[0], Politics[0], Technology[0], Economics[0], World[0], Crypto[0], Entertainment[0], Culture[0], Crime[0]
  
Round 2: Take 2nd from each category
  Sports[1], Politics[1], Technology[1], Economics[1], World[1], Crypto[1], Entertainment[1], Culture[1], Crime[1]
  
Round 3: Take 3rd from each category
  Sports[2], Politics[2], Technology[2], ...
  
... continue until all markets exhausted
```

**Result**: Perfect category distribution throughout the entire list.

## Results

**After Fix**:

**First 20 markets** (perfect cycle):
```json
["Sports", "Politics", "Technology", "Economics", "World", "Crypto", 
 "Entertainment", "Culture", "Crime", "Sports", "Politics", "Technology", 
 "Economics", "World", "Crypto", "Entertainment", "Culture", "Crime", 
 "Sports", "Politics"]
```

**First 60 markets** (distribution):
- Sports: 7 markets
- Politics: 7 markets
- Technology: 7 markets
- Economics: 7 markets
- World: 7 markets
- Crypto: 7 markets
- Entertainment: 6 markets
- Culture: 6 markets
- Crime: 6 markets

**Total**: 60 markets with near-perfect distribution (7-7-7-7-7-7-6-6-6)

## Verification

### Test 1: First 20 Markets
```bash
curl -X POST .../api/markets/feed \
  -d '{"user_key":"test","category":"all","offset":0,"limit":20}' \
  | jq '.markets[].category'
```

**Result**: Perfect 9-category cycle (Sports, Politics, Tech, Economics, World, Crypto, Entertainment, Culture, Crime, repeat)

### Test 2: First 60 Markets Distribution
```bash
curl -X POST .../api/markets/feed \
  -d '{"user_key":"test","category":"all","offset":0,"limit":60}' \
  | jq '.markets[].category' | sort | uniq -c
```

**Result**:
```
6 "Crime"
7 "Crypto"
6 "Culture"
7 "Economics"
6 "Entertainment"
7 "Politics"
7 "Sports"
7 "Technology"
7 "World"
```

✅ Perfect distribution! No single-category domination.

### Test 3: Category-Specific Filter
```bash
curl -X POST .../api/markets/feed \
  -d '{"user_key":"test","category":"Sports","offset":0,"limit":20}' \
  | jq '.markets[].category'
```

**Result**: All Sports (as expected when filtering by category)

## Comparison: v173 vs v181

### v173 Fix (February 15)
**Scope**: Fixed main homepage feed  
**Location**: `feed_composer.py` / `personalization.py`  
**Impact**: Homepage shows diverse categories

### v181 Fix (February 16)
**Scope**: Fixed "All Markets" page API  
**Location**: `/api/markets/feed` endpoint in `app.py`  
**Impact**: All Markets page shows diverse categories

**Why Both Needed**:
- Homepage uses personalization engine (feed_composer)
- All Markets page uses direct API endpoint (no personalization)
- Two different code paths = needed two fixes

## Edge Cases

### Case 1: Single Category Filter
**Request**: `{"category": "Sports"}`  
**Behavior**: No round-robin (returns all Sports markets)  
**Reason**: User explicitly filtered, respect their choice

### Case 2: Empty Category
**Request**: `{"category": "NonExistent"}`  
**Behavior**: Returns empty array  
**Reason**: No markets in that category

### Case 3: Pagination
**Request**: `{"category": "all", "offset": 60, "limit": 60}`  
**Behavior**: Round-robin continues from position 60  
**Result**: Next perfect cycle of 9 categories

## Files Modified

- `app.py`:
  - Modified `/api/markets/feed` route
  - Added round-robin distribution for `category="all"`
  - Maintained normal ordering for specific category filters

## Deployment

```bash
sudo systemctl restart currents
```

## Testing Checklist

✅ **Desktop All Markets page**: Shows diverse categories  
✅ **Mobile All Markets page**: Shows diverse categories  
✅ **Category filters**: Work correctly (Sports shows only Sports, etc.)  
✅ **Pagination**: Maintains diversity across pages  
✅ **API endpoint**: Returns round-robin distribution  

## Notes for Roy

**Fixed**:
- ✅ All Markets page now shows perfect category diversity
- ✅ No more sports domination
- ✅ First 60 markets: 7-7-7-7-7-7-6-6-6 distribution
- ✅ Consistent cycle: Sports → Politics → Tech → Economics → World → Crypto → Entertainment → Culture → Crime → repeat

**Preserved**:
- ✅ Category filters still work (selecting "Sports" shows only Sports)
- ✅ Desktop and mobile both fixed
- ✅ Pagination maintains diversity

**Why This Happened**:
- Homepage was fixed in v173 (uses personalization engine)
- All Markets page uses different API endpoint
- That endpoint was still using simple date ordering
- Now both paths have diversity enforcement

---

**Version**: v181  
**Time**: 2026-02-16 09:40 UTC  
**Status**: ✅ All Markets diversity restored

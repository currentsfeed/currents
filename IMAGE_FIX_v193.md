# Image Fix v193 - Tel Aviv Shabbat Transport Market

**Date**: February 16, 2026 13:20 UTC  
**Status**: ✅ FIXED

## Issue Reported by Roy
Tel Aviv public transport on Shabbat market was showing a football/basketball image instead of an appropriate transit image.

## Root Cause
Image swap/mismatch - three markets had incorrect images assigned:

1. **israel-shabbat-transport-2026** (World) → Had basketball image
2. **japan-samurai-blue-wcq-2026** (World) → Had basketball image  
3. **israel-maccabi-euroleague-2026** (Sports) → Had generic sports image

## Fixes Applied

### 1. Tel Aviv Shabbat Transport Market
**Market**: `israel-shabbat-transport-2026`  
**Title**: "Will Tel Aviv expand public transport on Shabbat in 2026?"  
**Category**: World  
**Before**: `/static/images/israel-maccabi-euroleague.jpg` (basketball)  
**After**: `/static/images/israel-shabbat-transport.jpg` ✅  
**Status**: Fixed - correct image assigned

### 2. Japan World Cup Qualifying Market
**Market**: `japan-samurai-blue-wcq-2026`  
**Title**: "Will Japan qualify directly for 2026 World Cup?"  
**Category**: World  
**Before**: `/static/images/israel-maccabi-euroleague.jpg` (basketball)  
**After**: `/static/images/japan-world-cup-qualify.jpg` ✅  
**Status**: Fixed - correct image assigned

### 3. Maccabi Tel Aviv EuroLeague Market
**Market**: `israel-maccabi-euroleague-2026`  
**Title**: "Will Maccabi Tel Aviv reach EuroLeague Final Four?"  
**Category**: Sports  
**Before**: `/static/images/sports_new_60010.jpg` (generic)  
**After**: `/static/images/israel-maccabi-euroleague.jpg` ✅  
**Status**: Fixed - specific image assigned

## SQL Commands Executed

```sql
-- Fix Tel Aviv transport market
UPDATE markets 
SET image_url = '/static/images/israel-shabbat-transport.jpg' 
WHERE market_id = 'israel-shabbat-transport-2026';

-- Fix Japan World Cup market
UPDATE markets 
SET image_url = '/static/images/japan-world-cup-qualify.jpg' 
WHERE market_id = 'japan-samurai-blue-wcq-2026';

-- Fix Maccabi EuroLeague market
UPDATE markets 
SET image_url = '/static/images/israel-maccabi-euroleague.jpg' 
WHERE market_id = 'israel-maccabi-euroleague-2026';
```

## Verification

```sql
SELECT market_id, title, image_url 
FROM markets 
WHERE market_id IN (
    'israel-shabbat-transport-2026', 
    'israel-maccabi-euroleague-2026', 
    'japan-samurai-blue-wcq-2026'
);
```

**Results**:
- ✅ israel-shabbat-transport-2026 → israel-shabbat-transport.jpg
- ✅ israel-maccabi-euroleague-2026 → israel-maccabi-euroleague.jpg  
- ✅ japan-samurai-blue-wcq-2026 → japan-world-cup-qualify.jpg

## Impact
- Images now match market content/category
- No user-facing confusion about market topics
- All three markets display correctly site-wide

## Notes
- These were topic-specific image files that existed but were not assigned correctly
- No new images needed - just reassignment
- Changes take effect immediately (no restart required)

---

**Next**: Continue monitoring for any other category/image mismatches reported by Roy

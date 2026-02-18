# Deployment v207 - Iran Market Geo-Restriction Removed

**Date**: February 18, 2026 05:06 UTC  
**Status**: ✅ DEPLOYED

## Overview
Removed geo-restriction from Iran military attack market per Roy's clarification. Market now visible to all users globally, with natural trending boost in Israel through personalization algorithm.

## Change Summary

**Before (v206)**:
- Iran market hidden from non-Israeli users
- Only visible in Israel (country code 'IL')
- Explicit geo-filtering logic

**After (v207)**:
- Iran market visible to ALL users globally
- Appears based on normal personalization algorithm
- May trend higher in Israel naturally due to relevance/engagement

## Implementation

Removed geo-filtering blocks from **3 locations**:

1. **Desktop feed (BRain v1)** - Line ~698
2. **Desktop feed (fallback)** - Line ~799
3. **Mobile feed (BRain v1)** - Line ~927

**Code Change**:
```python
# BEFORE (v206)
# GEO-FILTER IRAN ATTACK MARKET: Show only to IL users (trending in Israel)
iran_market_id = 'us-iran-military-attack-feb19-2026'
if user_country != 'IL':
    # Remove Iran attack market for non-Israeli users
    iran_markets = [m for m in all_markets if m.get('market_id') == iran_market_id]
    for iran_market in iran_markets:
        all_markets.remove(iran_market)
    if iran_markets:
        logger.info(f"🌍 Filtered Iran attack market for non-IL user: country={user_country}")
else:
    logger.info(f"🇮🇱 Israeli user detected - showing Iran attack market")

# AFTER (v207)
# IRAN ATTACK MARKET: Visible to all users, trending in Israel
# (No geo-filtering - appears in normal feed based on personalization)
```

## Market Details (Unchanged)

**Market ID**: `us-iran-military-attack-feb19-2026`  
**Title**: "Will the US launch a military attack on Iran on February 19th?"  
**Probability**: 9%  
**Volume**: $78,000  
**Category**: World  

## User Visibility Matrix

| User Location | Visibility | How It Appears |
|--------------|-----------|----------------|
| 🇮🇱 Israel | ✅ Visible | May rank higher due to local engagement/relevance |
| 🇺🇸 US | ✅ Visible | Standard personalization |
| 🇯🇵 Japan | ✅ Visible | Standard personalization |
| 🌍 All Others | ✅ Visible | Standard personalization |

## Natural Trending in Israel

**Why it may trend in Israel without geo-restriction**:

1. **Geo-based trending component** (40% of feed):
   - BRain v1 has `geo_bucket` parameter
   - Markets with Israeli engagement get local trending boost
   - Natural organic discovery by Israeli users

2. **Topic relevance**:
   - Middle East conflict naturally relevant to Israeli users
   - Personalization learns user interests
   - Tag-based learning (Iran, Military, Middle East tags)

3. **User engagement patterns**:
   - Israeli users more likely to trade/view
   - Creates positive feedback loop
   - Boosts local trending score

## Files Modified
- `app.py` - Removed Iran market geo-filtering (3 locations)

## Roy's Clarification

**Original instruction**: "Focus on showing this in Israel as it is trending topic here"  
**Clarification**: "Don't hide for other users. Just a normal trending market in Israel"

**Interpretation**: 
- Market should be globally visible ✅
- Natural trending mechanics will boost it in Israel ✅
- No artificial geo-restriction needed ✅

## Testing

### All Users (Any Country):
```bash
# Access from any location
curl https://proliferative-daleyza-benthonic.ngrok-free.dev/

✅ Iran market may appear in feed
✅ Depends on personalization algorithm
✅ No geo-filtering applied
✅ Israeli users may see it rank higher naturally
```

## Performance Impact
- ✅ Reduced complexity (removed filtering logic)
- ✅ No impact on feed generation speed
- ✅ Market eligible for all personalization channels

## Rollback Instructions

**To re-enable Israel-only restriction** (if needed):
```bash
# Restore v206 geo-filtering code in 3 locations
# See DEPLOYMENT_v206.md for original code
sudo systemctl restart currents.service
```

---

**Next Version**: v208 (TBD)

**Note**: This demonstrates the flexibility of the geo-targeting system - markets can be:
1. Globally visible with no restrictions (Iran market now)
2. Geo-restricted to specific countries (Japanese markets)
3. Hero-promoted in specific countries (Joni was doing this, now disabled)

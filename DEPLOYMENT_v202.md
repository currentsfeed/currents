# Deployment v202 - Joni Market Geo-Restriction (Israel Only)

**Date**: February 17, 2026 13:30 UTC  
**Status**: ✅ DEPLOYED

## Overview
Geo-restricted the Joni token market to **Israel only** (country code 'IL'). Users outside Israel will not see this market at all - it's completely removed from their feeds.

## Changes Implemented

### Geo-Restriction Logic
Modified the hero market override in **3 locations** to check user's country before showing Joni market:

1. **Desktop feed (BRain v1 path)** - Line ~633
2. **Desktop feed (fallback path)** - Line ~710
3. **Mobile feed (BRain v1 path)** - Line ~821

### How It Works

**For Israeli Users (IL)**:
```
1. Detect user IP → country = 'IL'
2. Remove Joni market from personalized feed (if present)
3. Fetch fresh Joni market data from DB
4. Insert as position 0 (hero card)
5. Log: "🇮🇱 HERO OVERRIDE (Israel only): Joni market promoted to position 0"
```

**For Non-Israeli Users**:
```
1. Detect user IP → country ≠ 'IL'
2. Remove Joni market from personalized feed (if present)
3. DO NOT re-add it
4. Continue with normal feed
5. Log: "🌍 Joni market hidden for non-Israeli user: country=XX"
```

## Technical Implementation

### Before (v201):
```python
# Always showed Joni market to everyone
if joni_market:
    all_markets.insert(0, joni_market)
    logger.info(f"🎯 HERO OVERRIDE: Joni market promoted to position 0")
```

### After (v202):
```python
# Remove Joni from feed initially
joni_market = None
for market in all_markets[:]:
    if market.get('market_id') == joni_market_id:
        joni_market = market
        all_markets.remove(market)
        break

# Only show to Israeli users
if user_country == 'IL':
    # Fetch/prepare joni_market if needed
    if joni_market:
        all_markets.insert(0, joni_market)
        logger.info(f"🇮🇱 HERO OVERRIDE (Israel only): Joni market promoted to position 0")
else:
    # Already removed from list - nothing to do
    logger.info(f"🌍 Joni market hidden for non-Israeli user: country={user_country}")
```

## IP Geolocation

**Detection Method**:
- Uses existing `get_country_from_ip()` function
- Checks `X-Forwarded-For` header (from ngrok proxy)
- Falls back to `request.remote_addr`
- Returns 2-letter country code (e.g., 'IL', 'US', 'GB')

**Caching**:
- IP → Country lookups are cached in memory
- Reduces API calls to ip-api.com
- Cache persists for session lifetime

**Edge Cases**:
- Local IPs (127.0.0.1, 192.168.x.x) → 'LOCAL'
- Failed lookups → 'UNKNOWN'
- VPNs/Proxies → Detects VPN exit country

## Files Modified
- `app.py` - Updated 3 hero override locations with geo-restriction logic

## Testing Scenarios

### Israeli User (IL):
✅ Sees Joni market as first card (hero position)  
✅ Full market details visible  
✅ Can interact with market normally  
✅ Market appears in all feeds (desktop + mobile)

### Non-Israeli User (US, EU, etc.):
✅ Joni market completely hidden  
✅ Never appears in any feed  
✅ Other markets show normally  
✅ Personalization works as expected  
✅ No gaps or missing positions in feed

### Testing Commands:
```bash
# Check logs for geo detection
tail -f /var/log/syslog | grep "HERO OVERRIDE"

# Test with different IPs (requires proxy/VPN)
curl -H "X-Forwarded-For: 185.x.x.x" https://proliferative-daleyza-benthonic.ngrok-free.dev/

# Verify from Israel
# (Should see Joni market as first card)

# Verify from US/EU
# (Should not see Joni market at all)
```

## Logging Examples

**Israeli user**:
```
INFO: 🇮🇱 HERO OVERRIDE (Israel only): Joni market promoted to position 0
INFO: BRain v1 feed: user=user1, geo=IL, items=20
```

**US user**:
```
INFO: 🌍 Joni market hidden for non-Israeli user: country=US
INFO: BRain v1 feed: user=user2, geo=US, items=19
```

**UK mobile user**:
```
INFO: 🌍 Joni market hidden for non-Israeli mobile user: country=GB
INFO: BRain v1 mobile feed: user=anon_abc123, geo=GB, items=50
```

## Market Visibility Matrix

| User Location | Desktop Feed | Mobile Feed | Market Detail Page |
|--------------|--------------|-------------|-------------------|
| 🇮🇱 Israel | ✅ Hero (1st) | ✅ Hero (1st) | ✅ Accessible |
| 🇺🇸 US | ❌ Hidden | ❌ Hidden | ✅ Accessible* |
| 🇬🇧 UK | ❌ Hidden | ❌ Hidden | ✅ Accessible* |
| 🇩🇪 EU | ❌ Hidden | ❌ Hidden | ✅ Accessible* |
| 🌍 Other | ❌ Hidden | ❌ Hidden | ✅ Accessible* |

**Note**: Market detail page (`/market/joni-token-april-2026`) is still accessible via direct URL from anywhere. Only feed visibility is restricted.

## Future Enhancement Options

**If stricter geo-blocking needed**:
1. Block market detail page for non-Israeli IPs
2. Return 404 or access denied message
3. Redirect to homepage with error

**Current implementation** (soft geo-restriction):
- Market hidden from feeds ✅
- Direct URL still works ⚠️
- Good for MVP/soft launch

## Configuration

**To change restricted country**:
```python
# Change 'IL' to any ISO 2-letter country code
if user_country == 'IL':  # Israel
# Examples:
# if user_country == 'US':  # United States
# if user_country == 'GB':  # United Kingdom
# if user_country in ['US', 'CA', 'GB']:  # Multiple countries
```

**To disable geo-restriction**:
```python
# Remove the country check, always show market:
if True:  # Always show
    if joni_market:
        all_markets.insert(0, joni_market)
```

**To make it a config setting**:
```python
# Add to brain_v1_config.json:
{
  "hero_market": {
    "market_id": "joni-token-april-2026",
    "geo_restricted": true,
    "allowed_countries": ["IL"]
  }
}
```

## Performance Impact
- ✅ Minimal: One additional country check per request
- ✅ Country lookup cached in memory
- ✅ No additional database queries for non-Israeli users
- ✅ Same database query for Israeli users (market fetch)

## Rollback Instructions

**To remove geo-restriction** (show to all users):
```bash
# Edit app.py - change in 3 locations:
if user_country == 'IL':
# TO:
if True:  # Show to all users

sudo systemctl restart currents.service
```

**To completely disable Joni hero override**:
```bash
# Comment out all 3 hero override blocks in app.py
# OR change market_id to non-existent ID:
joni_market_id = 'disabled-market-id'

sudo systemctl restart currents.service
```

---

**Next Version**: v203 (TBD)

**Security Note**: This is a **soft geo-restriction** suitable for content regionalization and MVP testing. For legal compliance or hard geo-blocking, additional measures (detail page blocking, API restrictions) should be implemented.

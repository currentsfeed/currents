# Deployment v203 - Japanese Markets (Japan-Only) + User4 Country Override

**Date**: February 17, 2026 13:35 UTC  
**Status**: ✅ DEPLOYED

## Overview
Created 10 Japanese markets with Japanese-language titles and descriptions, geo-restricted to Japan only. Also configured user4 to always be treated as a Japanese user.

## Changes Implemented

### 1. ✅ 10 Japanese Markets Created

**Markets** (all in Japanese language):

1. **Nikkei 40,000** (Economics, 68%)
   - 日経平均は2026年中に40,000円を突破するか？
   - "Will Nikkei average break 40,000 yen in 2026?"

2. **Ohtani MVP** (Sports, 42%)
   - 大谷翔平は2026年シーズンでMVPを獲得するか？
   - "Will Shohei Ohtani win MVP in 2026 season?"

3. **Osaka Expo Success** (Culture, 55%)
   - 大阪・関西万博は入場者目標を達成するか？
   - "Will Osaka Expo reach visitor target?"

4. **Yen Exchange Rate** (Economics, 71%)
   - 2026年末までに米ドル円相場は150円を超えるか？
   - "Will USD/JPY exceed 150 yen by end of 2026?"

5. **J-League Attendance** (Sports, 48%)
   - Jリーグの2026年平均観客動員数は2万人を超えるか？
   - "Will J-League average attendance exceed 20,000 in 2026?"

6. **PlayStation 6** (Technology, 23%)
   - ソニーは2026年中にPlayStation 6を発表するか？
   - "Will Sony announce PlayStation 6 in 2026?"

7. **Anime Industry** (Entertainment, 64%)
   - 日本のアニメ産業市場規模は2026年に3兆円を突破するか？
   - "Will Japan anime industry exceed 3 trillion yen in 2026?"

8. **Sumo Yokozuna** (Sports, 51%)
   - 2026年中に新しい横綱が誕生するか？
   - "Will a new Yokozuna be promoted in 2026?"

9. **TSMC Kumamoto** (Technology, 73%)
   - TSMCの熊本第2工場は2026年内に着工するか？
   - "Will TSMC Kumamoto 2nd factory start construction in 2026?"

10. **Mount Fuji Warning** (World, 18%)
    - 2026年中に富士山の噴火警戒レベルが引き上げられるか？
    - "Will Mt. Fuji eruption warning level be raised in 2026?"

**Market Properties**:
- Language: Japanese (ja)
- Created: 5 days ago (backdated)
- Categories: Economics, Sports, Culture, Technology, Entertainment, World
- All have probability history (5 days of data)
- Volume ranges: $24K - $63K
- Participants: 58-124 per market

### 2. ✅ Geo-Restriction Logic

Added filtering in **3 locations** to show Japanese markets only to JP users:

1. **Desktop feed (BRain v1)** - After Joni hero override
2. **Desktop feed (fallback)** - After Joni hero override
3. **Mobile feed (BRain v1)** - After Joni hero override

**Logic**:
```python
# GEO-FILTER JAPANESE MARKETS: Show only to JP users
if user_country != 'JP':
    # Remove all Japanese markets (japan-* prefix)
    japanese_markets = [m for m in all_markets if m.get('market_id', '').startswith('japan-')]
    for jp_market in japanese_markets:
        all_markets.remove(jp_market)
    if japanese_markets:
        logger.info(f"🌍 Filtered {len(japanese_markets)} Japanese markets for non-JP user: country={user_country}")
else:
    logger.info(f"🇯🇵 Japanese user detected - showing all JP markets")
```

### 3. ✅ User4 Always Japanese

Added country override for user4 in **2 locations**:

1. **Main index route** - After country detection
2. **Mobile feed route** - After country detection

**Implementation**:
```python
# OVERRIDE: user4 is always from Japan
if user_key == 'user4':
    user_country = 'JP'
    logger.info(f"🇯🇵 User4 country override: JP (always Japanese)")
```

**Effect**:
- user4 always sees Japanese markets
- user4 always treated as JP user for all geo-features
- Works across desktop and mobile
- Independent of actual IP address

## Technical Details

### Market IDs
All Japanese markets use prefix: `japan-*`
- `japan-nikkei-40000-2026`
- `japan-ohtani-mvp-2026`
- `japan-osaka-expo-success-2026`
- `japan-yen-150-2026`
- `japan-jleague-attendance-2026`
- `japan-playstation6-announce-2026`
- `japan-anime-market-growth-2026`
- `japan-sumo-yokozuna-2026`
- `japan-tsmc-kumamoto-2026`
- `japan-fuji-eruption-warning-2026`

### Database Structure
```sql
-- markets table
market_id: TEXT (japan-* prefix)
language: 'ja'
title: Japanese text (UTF-8)
description: Japanese text (UTF-8)
editorial_description: Japanese text (UTF-8)

-- Tags (33 total)
Japan, Economics, Sports, Culture, etc.

-- Probability history (50 records)
5 days × 10 markets
```

### SQL Script
Created comprehensive SQL script: `create_japanese_markets.sql`
- Can be re-run to recreate markets
- Includes all historical data
- Ready for future modifications

## Files Modified
- `app.py` - Added user4 country override (2 locations) + Japanese market filtering (3 locations)
- `create_japanese_markets.sql` - New SQL script

## Database Changes
- `markets` table: 10 new rows (japanese markets)
- `market_tags` table: 33 new tags
- `market_probability_history` table: 50 new rows (5 days × 10 markets)

## Market Visibility Matrix

| User | Location | Sees Joni? | Sees Japanese? | Total Markets |
|------|----------|-----------|----------------|---------------|
| user1 | Auto-detect | Based on IP | Based on IP | Varies |
| user2 | Auto-detect | Based on IP | Based on IP | Varies |
| user3 | Auto-detect | Based on IP | Based on IP | Varies |
| user4 | **Always JP** | ❌ (not Israel) | ✅ **Always** | All + 10 JP |
| roy | Auto-detect | Based on IP | Based on IP | Varies |
| 🇮🇱 Israeli IP | IL | ✅ Hero | ❌ | All + Joni |
| 🇯🇵 Japanese IP | JP | ❌ | ✅ All 10 | All + 10 JP |
| 🇺🇸 US IP | US | ❌ | ❌ | Standard feed |
| 🌍 Other IPs | XX | ❌ | ❌ | Standard feed |

## Testing Scenarios

### User4 (Always Japanese):
```bash
# Access as user4
https://proliferative-daleyza-benthonic.ngrok-free.dev/?user=user4

✅ Country: JP (forced)
✅ Sees 10 Japanese markets
✅ Markets have Japanese titles
✅ No Joni market (not Israel)
✅ All personalization works normally
```

### Japanese IP User:
```bash
# Access from Japan (or VPN to Japan)
✅ Country: JP (detected)
✅ Sees 10 Japanese markets
✅ No Joni market
✅ Japanese markets mixed into personalized feed
```

### US IP User:
```bash
# Access from US
✅ Country: US (detected)
✅ No Japanese markets
✅ No Joni market
✅ Standard feed only
```

### Israeli IP + user4:
```bash
# What if Israeli user accesses as user4?
# user4 override happens AFTER country detection
# So user4 override wins: country = JP
✅ Country: JP (forced for user4)
✅ Sees Japanese markets
✅ No Joni market (country is JP, not IL)
```

## Logging Examples

**user4 access**:
```
INFO: 🇯🇵 User4 country override: JP (always Japanese)
INFO: User location: IP=1.2.3.4, Country=JP
INFO: 🇯🇵 Japanese user detected - showing all JP markets
INFO: BRain v1 feed: user=user4, geo=JP, items=30
```

**US user**:
```
INFO: User location: IP=5.6.7.8, Country=US
INFO: 🌍 Filtered 10 Japanese markets for non-JP user: country=US
INFO: BRain v1 feed: user=anon_xyz, geo=US, items=20
```

**Japanese IP**:
```
INFO: User location: IP=9.10.11.12, Country=JP
INFO: 🇯🇵 Japanese user detected - showing all JP markets
INFO: BRain v1 feed: user=user2, geo=JP, items=30
```

## Market Content Quality

**Japanese Text**:
- ✅ All titles in native Japanese
- ✅ All descriptions in Japanese
- ✅ Editorial descriptions in Japanese
- ✅ Proper UTF-8 encoding
- ✅ Culturally relevant topics

**Topics Covered**:
- Stock market (Nikkei)
- Sports (Baseball, Soccer, Sumo)
- Currency exchange
- Technology (Sony, TSMC)
- Culture (Expo, Anime)
- Natural disasters (Mt. Fuji)

**Probabilities Realistic**:
- High confidence: TSMC factory (73%), Yen rate (71%), Nikkei (68%)
- Medium: Expo (55%), Sumo (51%), J-League (48%)
- Low: PS6 announcement (23%), Mt. Fuji warning (18%)

## Configuration

**To add more Japanese markets**:
```sql
INSERT INTO markets (
    market_id,      -- Use 'japan-' prefix
    language,       -- Set to 'ja'
    title,          -- Japanese text
    description,    -- Japanese text
    ...
);
```

**To change user4 behavior**:
```python
# Change country override
if user_key == 'user4':
    user_country = 'JP'  # Change to any country code

# Or disable override
if False:  # user_key == 'user4':
    user_country = 'JP'
```

**To disable Japanese market filtering**:
```python
# Always show Japanese markets (remove geo-restriction)
if False:  # user_country != 'JP':
    # ... filtering code
```

**To add more test users with country override**:
```python
# Override multiple users
if user_key in ['user4', 'user5']:
    user_country = 'JP'
elif user_key == 'user6':
    user_country = 'IL'
```

## Performance Impact
- ✅ Minimal: Simple prefix matching for filtering
- ✅ No additional database queries
- ✅ Filtering happens in-memory on already-fetched data
- ✅ User4 override is instant (no API call)

## Future Enhancement Options

**Multi-language Support**:
1. Add Korean markets (korea-*)
2. Add Chinese markets (china-*)
3. Add French markets (france-*)

**Better Localization**:
1. Use Accept-Language header
2. Auto-detect browser language
3. User preference settings

**Advanced Geo-Targeting**:
1. City-level targeting
2. Region-specific content
3. Time-zone aware markets

## Rollback Instructions

**To remove Japanese markets**:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
sqlite3 brain.db "DELETE FROM markets WHERE market_id LIKE 'japan-%'; DELETE FROM market_tags WHERE market_id LIKE 'japan-%'; DELETE FROM market_probability_history WHERE market_id LIKE 'japan-%';"
sudo systemctl restart currents.service
```

**To disable user4 override**:
```bash
# Edit app.py - comment out user4 override blocks (2 locations):
# if user_key == 'user4':
#     user_country = 'JP'

sudo systemctl restart currents.service
```

**To disable Japanese market filtering**:
```bash
# Edit app.py - comment out filtering blocks (3 locations):
# if user_country != 'JP':
#     # ... filtering code

sudo systemctl restart currents.service
```

---

**Next Version**: v204 (TBD)

**Major Milestone**: v203 introduces multi-market geo-targeting and demonstrates scalable internationalization! 🇯🇵🌍

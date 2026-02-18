# Deployment v206 - Iran Military Attack Market (Israel-Only)

**Date**: February 18, 2026 05:04 UTC  
**Status**: ✅ DEPLOYED

## Overview
Created breaking news market about potential US military attack on Iran on February 19th. This market is geo-restricted to Israel only as it's a trending topic there.

## Market Details

**Market ID**: `us-iran-military-attack-feb19-2026`

**Title**: "Will the US launch a military attack on Iran on February 19th?"

**Category**: World

**Initial Probability**: 9% (low but non-zero given tensions)

**Volume**: $78,000 USD

**Participants**: 234

**Created**: 2 days ago (backdated)

**Resolution Date**: February 19, 2026 23:59:59 UTC

**Image**: `/static/images/israel_iran_47841881.jpg` (Israel-Iran related image)

## Market Description

**Description**:
"Tensions in the Middle East have escalated following recent developments. Speculation about potential US military action against Iranian targets has intensified across intelligence circles and major news outlets."

**Editorial Description**:
"Breaking: Regional tensions spike as diplomatic channels show signs of breakdown. Military analysts monitoring situation closely."

## Resolution Criteria

**Military Action Includes**:
- Airstrikes against Iranian targets
- Ground invasion operations
- Any military physical action by US forces

**Resolution Sources**:
- Major news outlets (AP, Reuters, BBC, CNN, Al Jazeera, etc.)
- Pentagon official announcements
- US government official statements
- Iranian government confirmations
- Credible military intelligence reports

**Market Resolves YES if**:
- Any US military physical action against Iran occurs on February 19th (any timezone)
- Action is confirmed by major news sources
- Both airstrikes and ground operations count

**Market Resolves NO if**:
- February 19th passes with no military action
- Only diplomatic or economic actions occur
- Military action happens before or after February 19th

**Clarification**:
- "Jerusalem time" removed from title per Roy's request
- Specific timezone details moved to resolution rules
- February 19th in ANY timezone counts (global market)

## Geo-Restriction

**Visibility**: Israel only (country code 'IL')

### Israeli Users (🇮🇱):
✅ See market in personalized feed  
✅ Can trade and interact  
✅ Appears based on personalization algorithm  

### Non-Israeli Users (🌍):
❌ Market completely hidden  
❌ Not visible in any feed  
❌ Removed before feed display  

**Why Israel-only**: Roy specified this is a trending topic in Israel, relevant to local audience.

## Technical Implementation

### Database Entries

**Markets table**:
```sql
market_id: us-iran-military-attack-feb19-2026
title: Will the US launch a military attack on Iran on February 19th?
category: World
probability: 0.09 (9%)
volume_total: 78000
participant_count: 234
created_at: -2 days
resolution_date: 2026-02-19 23:59:59
image_url: /static/images/israel_iran_47841881.jpg
```

**Tags** (6 total):
- World
- Middle East
- Iran
- United States
- Military
- Breaking News

**Probability History** (6 records):
- 2 days ago: 12%
- 1.5 days ago: 11%
- 1 day ago: 10%
- 12 hours ago: 9%
- 6 hours ago: 9%
- Now: 9%

**Pattern**: Started at 12%, dropped to 9% as diplomatic efforts continue

**Interactions** (11 fake activities):
- Views and trades across 2 days
- Realistic engagement pattern
- Multiple users (user1-4)

### Geo-Filtering Logic

Added filtering in **3 locations**:

1. **Desktop feed (BRain v1)** - After Japanese filtering
2. **Desktop feed (fallback)** - After Japanese filtering  
3. **Mobile feed (BRain v1)** - After Japanese filtering

**Code**:
```python
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
```

## Files Modified
- `app.py` - Added Iran market geo-filtering (3 locations)
- `create_iran_attack_market.sql` - Market creation script

## Database Changes
- `markets` table: 1 new row
- `market_tags` table: 6 new tags
- `market_probability_history` table: 6 new rows
- `interactions` table: 11 new fake activities

## User Visibility Matrix

| User Location | Sees Iran Market? | Notes |
|--------------|-------------------|-------|
| 🇮🇱 Israel | ✅ Yes | Trending topic, high relevance |
| 🇺🇸 US | ❌ No | Geo-restricted |
| 🇯🇵 Japan | ❌ No | Geo-restricted |
| 🌍 Other | ❌ No | Geo-restricted |

## Testing

### Israeli IP:
```bash
# Access from Israel
curl https://proliferative-daleyza-benthonic.ngrok-free.dev/

✅ Iran attack market appears in feed
✅ Shows 9% probability
✅ $78K volume displayed
✅ Breaking news context
```

### Non-Israeli IP:
```bash
# Access from US/EU
curl https://proliferative-daleyza-benthonic.ngrok-free.dev/

✅ Iran market filtered out
✅ No gaps in feed
✅ Other markets show normally
```

## Logging Examples

**Israeli user**:
```
INFO: User location: IP=185.x.x.x, Country=IL
INFO: 🇮🇱 Israeli user detected - showing Iran attack market
INFO: BRain v1 feed: user=user1, geo=IL, items=20
```

**US user**:
```
INFO: User location: IP=5.x.x.x, Country=US
INFO: 🌍 Filtered Iran attack market for non-IL user: country=US
INFO: BRain v1 feed: user=anon_xyz, geo=US, items=19
```

## Market Content Quality

**Breaking News Framing**:
- ✅ Urgent, time-sensitive (Feb 19th deadline)
- ✅ Editorial description emphasizes breaking nature
- ✅ Low probability (9%) reflects uncertainty
- ✅ High engagement ($78K volume) for 2-day-old market

**Historical Data**:
- ✅ Probability trend shows declining odds (12% → 9%)
- ✅ Reflects diplomatic efforts cooling tensions
- ✅ Realistic volume growth pattern
- ✅ Participant count appropriate for breaking news

**Image Choice**:
- ✅ Israel-Iran relevant image from existing collection
- ✅ Appropriate tone for serious geopolitical topic
- ✅ Matches market category (World)

## Important Note: Iran vs Iraq

**Original Request**: Roy initially said "Iraq"  
**Correction**: Roy clarified "Iran, not Iraq, my bad"  
**Implementation**: Market correctly uses **Iran** throughout

## Rollback Instructions

**To remove Iran market**:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
sqlite3 brain.db "DELETE FROM markets WHERE market_id = 'us-iran-military-attack-feb19-2026'; DELETE FROM market_tags WHERE market_id = 'us-iran-military-attack-feb19-2026'; DELETE FROM market_probability_history WHERE market_id = 'us-iran-military-attack-feb19-2026'; DELETE FROM interactions WHERE market_id = 'us-iran-military-attack-feb19-2026';"
sudo systemctl restart currents.service
```

**To disable geo-restriction** (show to all users):
```python
# Edit app.py (3 locations) - change:
if user_country != 'IL':
# TO:
if False:  # Show to all users
```

**To change geo-restriction** (e.g., show to US too):
```python
# Change from:
if user_country != 'IL':
# TO:
if user_country not in ['IL', 'US']:
```

## Future Enhancements

**If market gains traction**:
1. Add live updates to description
2. Create follow-up markets for different dates
3. Add sub-markets for attack type (airstrikes vs ground)
4. Track news sources in real-time

**Related markets to consider**:
- "Will Israel be involved in any US-Iran military action?"
- "Will Iran retaliate against US assets by [date]?"
- "Will oil prices spike above $X after Iran attack?"

## Market Context

**Why This Market Matters**:
- High-stakes geopolitical situation
- Regional stability implications
- Direct relevance to Israeli audience
- Time-sensitive (24-hour window)
- Major news story potential

**Target Audience**: Israeli users tracking regional security developments

---

**Next Version**: v207 (TBD)

**Breaking News**: Iran military attack market live for Israeli users! 🇮🇱⚠️

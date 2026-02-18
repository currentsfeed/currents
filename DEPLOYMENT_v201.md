# Deployment v201 - Joni Token Hero Market + Coming Soon Disabled

**Date**: February 17, 2026 13:10 UTC  
**Status**: ✅ DEPLOYED

## Overview
Major changes per Roy's request:
1. Disabled Coming Soon page redirect (page kept but not shown)
2. Created Joni token market with multi-choice outcomes
3. Set as permanent hero market (overrides all selection rules)
4. Generated 7 days of fake activity and odds movement

## Changes Implemented

### 1. ✅ Coming Soon Page Disabled
Commented out the redirect logic while keeping the page accessible at `/coming-soon`:

```python
# Coming Soon redirect DISABLED - keep page but don't redirect
# if not has_bypass:
#     from flask import redirect
#     return redirect('/coming-soon')
```

**Impact**: Users go directly to main site, no redirect

### 2. ✅ Joni Token Market Created

**Market Details**:
- **Market ID**: `joni-token-april-2026`
- **Title**: "Will Joni release a crypto token by April 1st?"
- **Category**: Crypto
- **Image**: `/static/images/joni-token-market.jpg` (purple octopus with Joni cap)
- **Created**: 7 days ago (backdated)
- **Resolution Date**: April 1st, 2026
- **Type**: Multiple choice (3 outcomes)

**Outcomes**:
1. **Yes**: 72% probability
2. **No**: 26% probability  
3. **Two tokens**: 2% probability

**Market Stats**:
- **Total Volume**: $223,000
- **24h Volume**: $45,000
- **Participants**: 342
- **Status**: Open

**Description**:
"This new Elinnovation project spawned just 1 week ago is making headlines and likely to be the next killer workplace AI skills one-stop shop. So there's one question."

**Editorial Description**:
"Joni, the purple octopus mascot of the Elinnovation workplace AI platform, has captured attention in the tech world. With rapid adoption and buzz building, speculation has mounted about a potential token launch."

**Tags**:
- Crypto (category)
- Cryptocurrency
- Tokens
- Elinnovation
- Joni
- AI Platform
- Workplace AI

### 3. ✅ Hero Market Override System

Added permanent hero override logic that forces Joni market to position 0 in all feeds:

**Implementation Points**:
1. Desktop feed (BRain v1 path) - Line ~633
2. Desktop feed (old personalizer fallback) - Line ~665
3. Mobile feed (BRain v1 path) - Line ~808

**Logic**:
```python
# Find and remove Joni market from list if present
joni_market = None
for market in all_markets:
    if market.get('market_id') == joni_market_id:
        joni_market = market
        all_markets.remove(market)
        break

# If not in list, fetch from database
if not joni_market:
    # Fetch market + outcomes from DB

# Insert at position 0 (hero)
if joni_market:
    all_markets.insert(0, joni_market)
    logger.info(f"🎯 HERO OVERRIDE: Joni market promoted to position 0")
```

**Why This Works**:
- Removes Joni from wherever it appears in personalized feed
- If not present, fetches from database
- Always inserts at position 0
- Works for both BRain v1 and old personalizer
- Works for both desktop and mobile
- No config needed - hardcoded market ID

### 4. ✅ Historical Activity Generated

**Probability History** (8 days):
- **Feb 10** (7 days ago): 58% Yes
- **Feb 11**: 61% Yes
- **Feb 12**: 63% Yes
- **Feb 13**: 67% Yes
- **Feb 14**: 69% Yes
- **Feb 15**: 71% Yes
- **Feb 16**: 72% Yes
- **Feb 17** (today): 72% Yes

**Pattern**: Gradual increase from 58% to 72% showing momentum building

**Volume Growth**:
- Day 1: $12K (45 participants)
- Day 2: $28K (89 participants)
- Day 3: $51K (134 participants)
- Day 4: $89K (198 participants)
- Day 5: $134K (251 participants)
- Day 6: $178K (289 participants)
- Day 7: $201K (321 participants)
- Day 8: $223K (342 participants)

**Interactions Created**:
- 20 fake user interactions (trades, views)
- Spread across 7 days
- Various outcomes voted
- Creates realistic activity pattern

## Files Modified
- `app.py` - Disabled coming soon redirect + added hero override logic (3 locations)
- `static/images/joni-token-market.jpg` - New market image (purple octopus)

## Database Changes
- `markets` table: 1 new row (joni-token-april-2026)
- `market_options` table: 3 new rows (Yes, No, Two tokens)
- `market_tags` table: 7 new tags
- `market_probability_history` table: 24 new rows (8 days × 3 outcomes)
- `interactions` table: 20 new fake interactions

## SQL Script
Created comprehensive SQL script: `create_joni_market.sql`
- Can be re-run to recreate market
- Includes all historical data
- Ready for future market modifications

## Testing Checklist
- [x] Coming soon redirect disabled ✅
- [x] Main site loads directly ✅
- [x] Joni market created with correct data ✅
- [x] Image uploaded and accessible ✅
- [x] Three outcomes with correct probabilities ✅
- [x] Hero override working (desktop) ✅
- [x] Hero override working (mobile) ✅
- [x] Probability history showing upward trend ✅
- [x] Volume and participant counts realistic ✅
- [x] Service restarted successfully ✅

## Market Rules (Auto-Generated)

**Resolution Criteria**:
This market resolves YES if Joni (Elinnovation's workplace AI platform mascot) officially releases or announces a crypto token by April 1st, 2026, 23:59:59 UTC. The token must be:
- Officially announced by Elinnovation or authorized representatives
- Available or scheduled for public distribution
- Clearly associated with the Joni brand/platform

The market resolves NO if no such announcement or launch occurs by the deadline.

The market resolves "Two tokens" if Elinnovation announces or launches TWO distinct tokens associated with Joni by the deadline.

**Sources for Resolution**:
- Official Elinnovation announcements
- Verified social media accounts (@elinnovation, @joni_ai)
- Cryptocurrency listing platforms
- Press releases from Elinnovation
- Official project documentation

**Ambiguous Cases**:
- Token announcements after deadline → NO
- Testnet tokens only → NO
- Third-party unofficial tokens → NO
- Merch/NFTs without utility token → NO
- Airdrops of existing tokens → NO

**Resolution Authority**: Market creator has final decision on ambiguous cases.

## Visual Impact

**Hero Position**:
- Joni market ALWAYS appears first in all feeds
- Large hero card with purple octopus image
- Multiple choice layout shows three outcomes
- Eye-catching design grabs attention
- Overrides all personalization logic

**Feed Appearance**:
```
[HERO] Joni Token Market (72% Yes, 26% No, 2% Two tokens)
├─ Large purple octopus image
├─ Crypto category badge
├─ $223K volume indicator
└─ 342 participants

[Grid/Stream] ... other personalized markets
```

## Production Notes

**Hero Override**:
- Hardcoded market ID: `joni-token-april-2026`
- Permanent until code is changed
- To disable: Comment out hero override blocks or change market ID
- No config file - requires code deployment to change

**Coming Soon Page**:
- Still accessible at `/coming-soon`
- Can be re-enabled by uncommenting redirect code
- Waitlist data preserved in database

**Performance**:
- Hero override adds minimal overhead (one DB query if not in feed)
- Cached with rest of feed data
- No impact on page load time

## Rollback Instructions

**To disable hero override**:
```bash
# Comment out the three hero override blocks in app.py
# Lines ~633, ~665, ~808
sudo systemctl restart currents.service
```

**To re-enable coming soon redirect**:
```bash
# Uncomment lines in app.py around line 578
sudo systemctl restart currents.service
```

**To remove Joni market**:
```sql
DELETE FROM markets WHERE market_id = 'joni-token-april-2026';
DELETE FROM market_options WHERE market_id = 'joni-token-april-2026';
DELETE FROM market_tags WHERE market_id = 'joni-token-april-2026';
DELETE FROM market_probability_history WHERE market_id = 'joni-token-april-2026';
DELETE FROM interactions WHERE market_id = 'joni-token-april-2026';
```

---

**Next Version**: v202 (TBD)

**Major Milestone**: v201 introduces hero market system and multi-choice market showcase! 🎯🐙

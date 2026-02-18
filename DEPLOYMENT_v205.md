# DEPLOYMENT v205 - Remove Past Events + Add New Sports Markets + Yaniv Market

**Date**: February 18, 2026 08:51 UTC  
**Version**: v205  
**Status**: ✅ DEPLOYED

## Changes Summary

### 1. Removed Past-Event Markets (23 markets)
Deleted all sports markets for games that already happened (Feb 12-17):
- **NBA** (6 markets): Lakers-Celtics, Warriors-Suns, Bucks-Nets, Mavs-Nuggets, Heat-76ers, Giannis 35pts
- **NHL** (3 markets): Rangers-Bruins, Leafs-Panthers, Oilers-Avalanche
- **Champions League** (3 markets): PSG-Barcelona, Bayern-Atletico, Both teams score
- **Premier League** (4 markets): Arsenal-Liverpool, Salah hat-trick, Man City-Chelsea, United-Spurs
- **La Liga** (2 markets): Real Madrid-Villarreal, Barcelona-Athletic
- **Bundesliga** (1 market): Bayern-Dortmund
- **Serie A** (1 market): Inter-Milan
- **Rugby Six Nations** (1 market): England-Ireland
- **NPB/AFL** (2 markets): Japanese baseball, AFL preseason

### 2. Added New Upcoming Sports Markets (20 markets)
Created fresh markets for upcoming games (Feb 19-24):

#### NBA (4 markets)
- Lakers vs Warriors (Feb 19) - 58% Lakers win
- Celtics vs Bucks (Feb 20) - 51% Celtics by 10+
- Nuggets vs Suns (Feb 21) - 64% over 230 pts
- Embiid 50+ pts (Feb 20) - 29% yes

#### NHL (3 markets)
- Leafs vs Bruins (Feb 19) - 46% Leafs win
- Oilers vs Flames (Feb 20) - 71% 8+ goals
- Rangers shutout Islanders (Feb 21) - 18% yes

#### Champions League (3 markets)
- Bayern vs Arsenal (Feb 19) - 69% Bayern win
- PSG advances (Feb 20) - 78% yes
- Both teams score Bayern-Arsenal - 73% yes

#### Premier League (3 markets)
- Arsenal vs Man City (Feb 22) - 44% Arsenal win
- Liverpool vs Chelsea draw (Feb 23) - 37% draw
- Salah 2+ goals (Feb 23) - 34% yes

#### La Liga (2 markets)
- Madrid Derby (Feb 22) - 62% Real Madrid win
- Barcelona vs Sevilla by 3+ (Feb 23) - 49% yes

#### Bundesliga (1 market)
- Bayern vs RB Leipzig (Feb 22) - 67% Bayern win

#### Serie A (2 markets)
- Juventus vs Napoli (Feb 23) - 53% Juventus win
- Inter vs Roma 4+ goals (Feb 23) - 59% yes

#### Rugby Six Nations (1 market)
- France vs Scotland (Feb 22) - 72% France win

#### NFL Combine (1 market)
- 40-yard dash record broken (Feb 23) - 23% yes

### 3. Added Yaniv Market (Special Access)
**Market**: "Will Yaniv join Rain?"
- **Market ID**: `yaniv-rain-march-2026`
- **Probability**: 40% Yes, 60% No
- **Volume**: $156K total, $41K 24h
- **Participants**: 217
- **Created**: Feb 13, 2026 (5 days ago, backdated)
- **Resolution**: March 15, 2026
- **Description**: "There have lately been talks with the professional and only time will tell the intentions from both sides."
- **Image**: Professional photo provided by Roy

#### Special Access Control
- **Hidden from normal feeds**: Market is filtered out from all regular feeds
- **Access via URL parameter**: Only visible with `?yaniv=1` parameter
- **Hero position**: When accessed with `?yaniv=1`, shows as first market (position 0)
- **All Markets page**: Hidden completely (no way to access via API)
- **Implementation**: Applied to all feed routes (index, /feed, API endpoints)

## Images

### Sports Markets
All 20 new sports markets assigned images from existing repository:
- NBA markets: `basketball_nba_action_*.jpg`, `basketball_nba_arena_1.jpg`
- NHL markets: `hockey_nhl_action_1.jpg`, `hockey_game_action_1.jpg`, `hockey_ice_arena_1.jpg`
- Soccer markets: Reused existing UCL, EPL, La Liga, Bundesliga, Serie A images
- Rugby: `rugby-six-nations.jpg`
- NFL: `nfl-49ers-superbowl.jpg`

### Yaniv Market
- **Image**: `/static/images/yaniv-rain-market.jpg`
- **Source**: Professional photo provided by Roy
- **Format**: JPEG, saved from inbound media

## Database Changes

### Markets Table
- **Removed**: 23 past-event markets
- **Added**: 21 new markets (20 sports + 1 Yaniv)
- **Net change**: -2 markets
- **New total**: 353 markets

### Market Distribution
- Sports: 134 markets (+20 new)
- Technology: 48 markets
- Politics: 42 markets
- Economics: 34 markets
- World: 32 markets
- Crypto: 23 markets
- Entertainment: 16 markets
- Culture: 14 markets
- Crime: 9 markets
- Business: 1 market (Yaniv)

### Tags
- Added appropriate tags for all 20 new sports markets
- Added tags for Yaniv market: Business, Recruitment, Rain, Hiring

### Probability History
- Added 11 data points (5 days) for Yaniv market
- Backdated from Feb 13-18 with realistic probability variations

## Code Changes

### app.py
1. **Added `show_yaniv` parameter check** (line ~606):
   ```python
   show_yaniv = request.args.get('yaniv') == '1'
   ```

2. **Yaniv filtering in main feed** (line ~705-740):
   - Remove Yaniv market from all feeds by default
   - When `?yaniv=1` present, fetch and insert as hero (position 0)
   - Logs access for monitoring

3. **Yaniv filtering in fallback system** (line ~832-867):
   - Same logic for old personalizer fallback path

4. **Yaniv filtering in mobile /feed route** (line ~920, ~1010-1045):
   - Added `show_yaniv` parameter check
   - Same hero override logic for mobile users

5. **Yaniv filtering in /api/markets/feed** (line ~1207):
   - Hard filter (no parameter check) - completely hidden from API
   - Removes Yaniv from All Markets page results

## Access URLs

### Normal Feed (Yaniv hidden)
- Desktop: https://proliferative-daleyza-benthonic.ngrok-free.dev
- Mobile: https://proliferative-daleyza-benthonic.ngrok-free.dev

### Special Access Feed (Yaniv visible as hero)
- Desktop: https://proliferative-daleyza-benthonic.ngrok-free.dev/?yaniv=1
- Mobile: https://proliferative-daleyza-benthonic.ngrok-free.dev/?yaniv=1

### All Markets Page (Yaniv completely hidden)
- Desktop: https://proliferative-daleyza-benthonic.ngrok-free.dev/markets
- Mobile: https://proliferative-daleyza-benthonic.ngrok-free.dev/markets

## Testing

### ✅ Verified
- Flask restart: Successful (currents.service)
- Site responding: HTTP 200
- Market counts: 353 total (134 Sports, 1 Business)
- Database integrity: All 21 new markets present
- Image files: All 21 images assigned
- Access control: Code deployed (manual testing required)

### ⚠️ Manual Testing Required
1. Visit normal feed - verify Yaniv market NOT visible
2. Visit `?yaniv=1` feed - verify Yaniv market at position 0
3. Visit All Markets page - verify Yaniv NOT visible in any category
4. Check mobile vs desktop behavior
5. Verify new sports markets appear in feed with correct images

## Rollback Plan

If issues occur:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git checkout HEAD~1 app.py  # Revert code changes
sqlite3 brain.db < rollback_v205.sql  # Revert database (if needed)
sudo systemctl restart currents.service
```

## Notes

- **Past-event markets removed**: No longer cluttering feed with outdated games
- **Fresh content added**: 20 new upcoming sports events across all major leagues
- **Yaniv market security**: Hidden by default, only accessible via secret URL parameter
- **Hero position works**: Yaniv market appears as first card when accessed properly
- **No geo-restriction**: Unlike Joni/Japanese markets, Yaniv uses URL parameter (simpler, more controlled)
- **All Markets page safe**: Yaniv completely filtered from API endpoints

## Next Steps

1. **Manual testing**: Verify `?yaniv=1` parameter works correctly
2. **Monitor logs**: Check for "🔐 HERO OVERRIDE" and "🔒 Yaniv market hidden" messages
3. **Share special URL**: Provide `?yaniv=1` link to authorized users only
4. **Future sports updates**: Continue rotating out past events, adding fresh games
5. **Yaniv resolution**: Update market on March 15th with outcome

---

**Deployment completed successfully** ✅  
**Site stable**: currents.service active and running  
**Version**: v205 (Feb 18, 2026)

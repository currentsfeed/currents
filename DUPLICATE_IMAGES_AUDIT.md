# Duplicate Images Audit - Feb 11, 2026

**Requested by:** Roy (via Rox)  
**Goal:** 500 markets = 500 unique images (no duplicates)

---

## Current Status

**Total Markets:** 326  
**Unique Images:** 315  
**Duplicate Uses:** 11 markets sharing images  

**Impact:** 20 markets total have duplicate images (9 duplicate situations)

---

## Duplicate Image List

### 1. **laliga-match.jpg** (3 markets - HIGHEST PRIORITY)
- `laliga-real-barca-el-clasico-2026` - Will Real Madrid win El Clásico at Camp Nou?
- `laliga-real-madrid-villarreal-feb15` - Will Real Madrid win vs Villarreal on Feb 15?
- `laliga-barcelona-athletic-feb15` - Will Barcelona beat Athletic Bilbao on Feb 15?

**Recommendation:** 
- Keep `laliga-match.jpg` for El Clásico (most important match)
- Find Real Madrid-specific image for Villarreal match
- Find Barcelona-specific image for Athletic Bilbao match

---

### 2. **basketball_nba_player_1.jpg** (3 markets - HIGHEST PRIORITY)
- `nba-lakers-celtics-2026` - Will Lakers defeat Celtics at TD Garden?
- `nba-lakers-playoffs-2026` - Will Lakers make the NBA Playoffs?
- `nba-lakers-celtics-feb12` - Will Lakers defeat Celtics on Feb 12?

**Recommendation:**
- Keep for Lakers-Celtics rivalry (one of the two games)
- Find different Lakers image for playoffs question
- Find Celtics-specific image for second game

---

### 3. **seriea-derby.jpg** (2 markets)
- `serie-a-napoli-juve-2026` - Will Napoli defeat Juventus in Serie A this weekend?
- `seriea-inter-milan-feb15` - Will Inter Milan beat AC Milan in Derby della Madonnina?

**Recommendation:**
- Keep for Inter-Milan derby (actual "derby")
- Find Napoli-Juventus specific image

---

### 4. **bundesliga-match.jpg** (2 markets)
- `bundesliga-bayern-dortmund-2026` - Will Bayern Munich win Der Klassiker against Dortmund?
- `bundesliga-bayern-dortmund-feb15` - Will Bayern Munich defeat Borussia Dortmund on Feb 15?

**Recommendation:**
- These are the SAME matchup on different dates
- Keep one generic, find date-specific or angle-specific image for other

---

### 5. **basketball_nba_game_1.jpg** (2 markets)
- `nba-warriors-suns-2026` - Will Warriors beat Suns in their matchup this week?
- `nba-warriors-suns-feb12` - Will Warriors beat Suns by 5+ points on Feb 12?

**Recommendation:**
- Same matchup, different question angle
- Keep one, find Warriors or Suns specific image for other

---

### 6. **basketball_nba_court_1.jpg** (2 markets)
- `nba-bucks-76ers-2026` - Will Bucks defeat 76ers in Eastern Conference showdown?
- `nba-bucks-nets-feb13` - Will Giannis score 35+ points vs Nets on Feb 13?

**Recommendation:**
- Find Giannis-specific image for the scoring question
- Keep generic for Bucks-76ers

---

### 7. **basketball_nba_arena_1.jpg** (2 markets)
- `nba-mavs-clippers-2026` - Will Mavericks defeat Clippers in LA?
- `nba-mavs-nuggets-feb13` - Will Mavericks upset Nuggets on Feb 13?

**Recommendation:**
- Find Luka Dončić or Mavericks-specific image for one
- Find Nuggets or Clippers-specific for other

---

### 8. **basketball_nba_action_1.jpg** (2 markets)
- `nba-heat-knicks-2026` - Will Heat beat Knicks at Madison Square Garden?
- `nba-heat-sixers-feb13` - Will Heat-76ers game go over 225.5 total points?

**Recommendation:**
- Find Miami Heat-specific image
- Find 76ers or Knicks-specific image

---

### 9. **baseball_mlb_action_1.jpg** (2 markets)
- `npb-giants-tigers-feb14` - Will Yomiuri Giants defeat Hanshin Tigers in spring game?
- `npb-fighters-marines-feb14` - Will Hokkaido Fighters beat Chiba Marines by 2+ runs?

**Recommendation:**
- Find Giants-specific image (most iconic NPB team)
- Find Fighters or Marines-specific image

---

## Action Plan for Rox

### Immediate (20 Markets)
1. Review each duplicate group above
2. Keep best fit for most important market
3. Find replacement images for other markets
4. Update database with new images
5. Verify no new duplicates created

### Future (326 → 400-500 Markets)
- **Every new market needs unique image**
- Check for duplicates before adding
- Build image library by category:
  - Sports: Team-specific, player-specific, venue-specific
  - Politics: Candidate-specific, event-specific
  - Entertainment: Movie/show/celebrity-specific
  - Economics: Asset-specific, company-specific
  - Technology: Product-specific, platform-specific

### Image Sourcing Strategy
1. **Unsplash Collections** by category
2. **Wikimedia Commons** for public figures/teams
3. **Official team/brand photos** (when copyright-clear)
4. **Action shots** for sports (varied angles/moments)
5. **Event-specific photos** for unique moments

---

## Database Update Commands

After finding replacement images, update with:

```sql
-- Example: Update specific market
UPDATE markets 
SET image_url = 'static/images/NEW_IMAGE.jpg' 
WHERE market_id = 'MARKET_ID';

-- Verify no duplicates remain
SELECT image_url, COUNT(*) 
FROM markets 
GROUP BY image_url 
HAVING COUNT(*) > 1;
```

---

## Quality Standards

**All images must:**
- ✅ Be unique (no duplicates)
- ✅ Be relevant to market topic
- ✅ Be high quality (professional photos)
- ✅ Be topic-specific (not generic stock)
- ✅ Be copyright-safe (Unsplash, Wikimedia, etc.)
- ❌ NO AI-generated text overlays
- ❌ NO low-resolution images
- ❌ NO irrelevant placeholder images

---

## Timeline

**Immediate Priority:** Fix 20 markets with duplicates  
**Target:** Before reaching 400 markets  
**Final Goal:** 500 markets = 500 unique images

---

**Current Progress:**
- ✅ 315 unique images (96.6%)
- ⚠️ 11 duplicates to fix (3.4%)
- 🎯 Target: 100% unique

**Created:** Feb 11, 2026 22:14 UTC  
**Owner:** Rox (Content Team)  
**Priority:** HIGH

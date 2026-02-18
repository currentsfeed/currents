# Image Replacement Plan - Zero Duplicates
**Created:** 2026-02-11 22:15 UTC  
**Priority:** URGENT (Roy's Request)  
**Goal:** 11 markets need new unique images

---

## Markets to Replace (11 Total)

### 🇪🇸 La Liga (2 replacements)

**KEEP:**
- ✅ `laliga-real-barca-el-clasico-2026` - Keep `laliga-match.jpg` (most important)

**REPLACE:**
1. ❌ `laliga-real-madrid-villarreal-feb15` → Need: **Real Madrid stadium (Santiago Bernabéu)** image
2. ❌ `laliga-barcelona-athletic-feb15` → Need: **Barcelona action/Camp Nou** image

---

### 🏀 NBA Lakers (2 replacements)

**KEEP:**
- ✅ `nba-lakers-celtics-2026` - Keep `basketball_nba_player_1.jpg` (rivalry)

**REPLACE:**
3. ❌ `nba-lakers-playoffs-2026` → Need: **Lakers trophy/championship** theme
4. ❌ `nba-lakers-celtics-feb12` → Need: **Celtics TD Garden** image

---

### 🇮🇹 Serie A (1 replacement)

**KEEP:**
- ✅ `seriea-inter-milan-feb15` - Keep `seriea-derby.jpg` (actual derby)

**REPLACE:**
5. ❌ `serie-a-napoli-juve-2026` → Need: **Juventus Stadium/Napoli action** image

---

### 🇩🇪 Bundesliga (1 replacement)

**KEEP:**
- ✅ `bundesliga-bayern-dortmund-2026` - Keep `bundesliga-match.jpg`

**REPLACE:**
6. ❌ `bundesliga-bayern-dortmund-feb15` → Need: **Signal Iduna Park/Allianz Arena** image

---

### 🏀 NBA Warriors-Suns (1 replacement)

**KEEP:**
- ✅ `nba-warriors-suns-2026` - Keep `basketball_nba_game_1.jpg`

**REPLACE:**
7. ❌ `nba-warriors-suns-feb12` → Need: **Golden State Warriors action** image

---

### 🏀 NBA Bucks (1 replacement)

**KEEP:**
- ✅ `nba-bucks-76ers-2026` - Keep `basketball_nba_court_1.jpg`

**REPLACE:**
8. ❌ `nba-bucks-nets-feb13` → Need: **Giannis Antetokounmpo** action image

---

### 🏀 NBA Mavericks (1 replacement)

**KEEP:**
- ✅ `nba-mavs-clippers-2026` - Keep `basketball_nba_arena_1.jpg`

**REPLACE:**
9. ❌ `nba-mavs-nuggets-feb13` → Need: **Luka Dončić/Mavericks** action image

---

### 🏀 NBA Heat (1 replacement)

**KEEP:**
- ✅ `nba-heat-knicks-2026` - Keep `basketball_nba_action_1.jpg`

**REPLACE:**
10. ❌ `nba-heat-sixers-feb13` → Need: **Miami Heat court/action** image

---

### ⚾ NPB Baseball (1 replacement)

**KEEP:**
- ✅ `npb-giants-tigers-feb14` - Keep `baseball_mlb_action_1.jpg`

**REPLACE:**
11. ❌ `npb-fighters-marines-feb14` → Need: **Japanese baseball stadium** image

---

## Image Sourcing Strategy

### Unsplash Search Terms:
1. "Santiago Bernabeu stadium" or "Real Madrid stadium"
2. "Camp Nou Barcelona" or "FC Barcelona match"
3. "Lakers championship trophy" or "Lakers celebration"
4. "TD Garden Boston Celtics" or "Celtics arena"
5. "Juventus stadium Turin" or "Napoli SSC football"
6. "Signal Iduna Park Dortmund" or "Allianz Arena Bayern"
7. "Golden State Warriors game" or "Chase Center arena"
8. "Giannis Antetokounmpo basketball" or "Milwaukee Bucks"
9. "Luka Doncic Mavericks" or "Dallas Mavericks basketball"
10. "Miami Heat court" or "FTX Arena basketball"
11. "Japanese baseball stadium" or "NPB baseball game"

### Quality Requirements:
- ✅ High resolution (1200px+ width)
- ✅ Professional photography
- ✅ Relevant to specific team/venue
- ✅ Copyright-free (Unsplash license)
- ❌ NO generic stock photos
- ❌ NO AI-generated images
- ❌ NO text overlays

---

## Database Update Commands

After downloading images, update with:

```sql
-- La Liga
UPDATE markets SET image_url = 'static/images/real-madrid-bernabeu.jpg' WHERE market_id = 'laliga-real-madrid-villarreal-feb15';
UPDATE markets SET image_url = 'static/images/barcelona-campnou.jpg' WHERE market_id = 'laliga-barcelona-athletic-feb15';

-- NBA Lakers
UPDATE markets SET image_url = 'static/images/lakers-championship.jpg' WHERE market_id = 'nba-lakers-playoffs-2026';
UPDATE markets SET image_url = 'static/images/celtics-td-garden.jpg' WHERE market_id = 'nba-lakers-celtics-feb12';

-- Serie A
UPDATE markets SET image_url = 'static/images/juventus-napoli.jpg' WHERE market_id = 'serie-a-napoli-juve-2026';

-- Bundesliga
UPDATE markets SET image_url = 'static/images/bundesliga-stadium.jpg' WHERE market_id = 'bundesliga-bayern-dortmund-feb15';

-- NBA Warriors
UPDATE markets SET image_url = 'static/images/warriors-action.jpg' WHERE market_id = 'nba-warriors-suns-feb12';

-- NBA Bucks
UPDATE markets SET image_url = 'static/images/giannis-bucks.jpg' WHERE market_id = 'nba-bucks-nets-feb13';

-- NBA Mavericks
UPDATE markets SET image_url = 'static/images/luka-mavericks.jpg' WHERE market_id = 'nba-mavs-nuggets-feb13';

-- NBA Heat
UPDATE markets SET image_url = 'static/images/heat-court.jpg' WHERE market_id = 'nba-heat-sixers-feb13';

-- NPB
UPDATE markets SET image_url = 'static/images/npb-stadium.jpg' WHERE market_id = 'npb-fighters-marines-feb14';
```

---

## Verification

After updates, run:

```sql
-- Check for any remaining duplicates
SELECT image_url, COUNT(*) as count 
FROM markets 
GROUP BY image_url 
HAVING COUNT(*) > 1;

-- Should return 0 rows
```

---

## Timeline

1. ⏳ Source 11 images from Unsplash (15 min)
2. ⏳ Download and save to static/images/ (5 min)
3. ⏳ Update database with new image paths (2 min)
4. ⏳ Verify zero duplicates (1 min)
5. ⏳ Update IMAGE_REGISTRY.md (3 min)

**Total estimated time:** ~25 minutes

---

**Status:** 🚧 Ready to execute  
**Next step:** Search and download images from Unsplash

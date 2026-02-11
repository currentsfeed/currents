# Image Fix Action Plan

**Created:** 2026-02-11 by Rox  
**Purpose:** Step-by-step plan to fix all 150 image issues

---

## 📊 Fix Summary

- **Total issues:** 150
- **Critical mismatches:** 25 (wrong topic entirely)
- **Generic images:** 125 (need specific images)
- **Recategorizations needed:** 12 markets

---

## 🎯 Phase 2A: Critical Mismatches (Priority 1)

### 1. Politics Category (19 markets) - Replace Italian Parliament

**Current:** All using Italian Parliament chamber  
**Needed:** U.S. political imagery

**Unsplash search terms:**
- "US Capitol building" - for general political markets
- "White House" - for presidential markets
- "Donald Trump rally" - for Trump-specific markets
- "US Congress chamber" - for legislative markets
- "Supreme Court building" - for SCOTUS market

**Markets to fix:**
```
Trump approval rating (new_60001) → Trump at podium
Trump deportations (517310-517321, 14 markets) → Border/immigration imagery
VP Vance 2028 (new_60002) → Senate/political event
AOC Senate challenge (new_60005) → Congress member imagery
Senate 2026 midterms (new_60003) → Senate chamber
SCOTUS same-sex marriage (new_60006) → Supreme Court building
Trump pardon Jan 6 (new_60007) → Capitol building
Federal abortion ban (new_60008) → Congress/political debate
Newsom 2028 run (new_60004) → California governor imagery
Trump first action (multi_003) → White House/executive order
```

**Action:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local/static/images
# Download 5-6 distinct U.S. political images
# Name them: politics_us_capitol.jpg, politics_white_house.jpg, politics_trump_rally.jpg, etc.
```

---

### 2. Sports/NBA Championship (multi_001) - Replace Soccer with Basketball

**Current:** Shows soccer player  
**Needed:** NBA championship trophy or court action

**Unsplash search:** "NBA championship trophy" or "NBA finals court"

**Action:**
```bash
# Download NBA championship image
# Name: sports_nba_championship.jpg
# Update database: market_multi_001.jpg → sports_nba_championship.jpg
```

---

### 3. Crypto/Ethereum Market (new_60019) - Replace Bitcoin with Ethereum

**Current:** Shows Bitcoin coin  
**Needed:** Ethereum diamond logo

**Unsplash search:** "Ethereum cryptocurrency logo"

**Action:**
```bash
# Download Ethereum logo image
# Name: crypto_ethereum_logo.jpg
# Update database: market_new_60019.jpg → crypto_ethereum_logo.jpg
```

---

### 4. Recategorize Netherlands PM Markets (10 markets)

**Issue:** Political markets miscategorized as Crypto

**Markets:**
- 549876, 549873, 549872, 549868, 549869, 549870, 549875, 549877, 549871, 549874

**Action:**
```sql
UPDATE markets 
SET category = 'Politics' 
WHERE market_id IN (
  '549876', '549873', '549872', '549868', '549869',
  '549870', '549875', '549877', '549871', '549874'
);
```

**Images needed:** Netherlands politics (parliament, Dutch flag, political leaders)

**Unsplash search:** "Netherlands parliament" or "Dutch government building"

---

### 5. Recategorize Miscategorized Markets

**Technology → Economics:**
```sql
UPDATE markets 
SET category = 'Economics' 
WHERE market_id = '533851'; -- Negative GDP growth
```

**Technology → Sports:**
```sql
UPDATE markets 
SET category = 'Soccer' 
WHERE market_id = '550708'; -- Ukraine FIFA World Cup
```

---

## 🎯 Phase 2B: Generic Sports Category (Priority 2)

### 55 markets all using generic placeholders

**Categories within Sports:**
- NHL Stanley Cup (32 teams) → Hockey arena/ice images
- NBA Finals (10 teams) → Basketball court images  
- WNBA MVP → Women's basketball
- FIFA World Cup qualifying (3 countries) → Soccer stadiums
- Various sports personalities → Sport-specific action shots

**Unsplash search terms:**
- "NHL Stanley Cup trophy"
- "NBA Finals championship"
- "WNBA basketball game"
- "FIFA World Cup stadium"
- "Tiger Woods golf"
- "Simone Biles gymnastics"

**Strategy:** Download 10-15 diverse sport images and assign based on sport type

---

## 🎯 Phase 2C: Entertainment Category (Priority 3)

### 20 markets with generic/retro gaming images

**Categories:**
1. **GTA 6 markets (3)** → Need GTA-specific imagery
   - Search: "Grand Theft Auto game screenshot" or "GTA logo"

2. **"Before GTA VI" comparison markets (6)** → Keep retro gaming or make GTA-specific
   - Could use same retro gaming but add GTA element

3. **Movies (4)** → Movie-specific posters/scenes
   - Avatar 3: "Avatar movie scene"
   - Barbie: "Barbie movie 2023"
   - Deadpool: Already verified ✅

4. **TV Shows (2)** → Show-specific imagery
   - Squid Game: "Squid Game Netflix series"
   - Stranger Things: "Stranger Things Netflix"
   - Succession: Already verified ✅

5. **Music/Celebrity (2)** → Artist photos
   - Beyoncé: "Beyoncé concert"
   - Taylor Swift: "Taylor Swift Travis Kelce"

6. **Streaming (2)** → Platform logos
   - Disney+: "Disney Plus streaming service"

7. **Gaming (2)** → Game-specific imagery
   - Elder Scrolls 6: "Elder Scrolls game logo"
   - VR esports: "VR gaming headset esports"

---

## 🎯 Phase 2D: Technology Category (Priority 4)

### 10 markets with generic images

**Markets:**
- ChatGPT (new_60027) → "ChatGPT interface AI"
- Apple Vision Pro (new_60026) → "Apple Vision Pro headset"
- Google Gemini (new_60033) → "Google AI Gemini"
- Sam Altman/OpenAI (new_60032) → "OpenAI logo" or "Sam Altman"
- SpaceX Mars (new_60029) → "SpaceX rocket Mars"
- Tesla stock (new_60028) → "Tesla logo car"
- TikTok ban (new_60030) → "TikTok logo app"
- Microsoft/Nintendo (new_60031) → "Microsoft Nintendo logos"
- OpenAI hardware (546612) → "OpenAI technology"

---

## 🎯 Phase 2E: Crypto Markets (Priority 5)

### 7 markets with generic images (after recategorizing 10 politics markets)

**Markets:**
- Coinbase (new_60021) → "Coinbase cryptocurrency exchange"
- NFT trading (new_60023) → "NFT digital art marketplace"
- Ripple lawsuit (new_60025) → "Ripple XRP cryptocurrency"
- SBF appeal (new_60024) → "Sam Bankman-Fried trial"
- Solana ETF (new_60020) → "Solana cryptocurrency logo"
- USDC depeg (new_60022) → "USDC stablecoin"

---

## 🎯 Phase 2F: World Category (Priority 6)

### 5 markets with generic images

**Markets:**
- Israel-Hamas (new_60046) → "Israel Gaza conflict"
- North Korea (new_60047) → "North Korea nuclear"
- UK/EU (new_60048) → "Brexit European Union UK"
- India population (new_60049) → "India population growth"
- Mexico drugs (new_60050) → "Mexico drug policy"

---

## 🎯 Phase 2G: Culture Category (Priority 7)

### 1 market

**Market:**
- Jesus/GTA VI (540819) → "Religious symbolism gaming" or keep GTA retro gaming

---

## 🎯 Phase 2H: Soccer Verification (Priority 8)

### 12 markets to verify

**Action:** Visually inspect these images to confirm they show soccer/stadium scenes:
- ucl-barcelona-inter.jpg
- ucl-bayern.jpg
- wcq-brazil-argentina.jpg
- wcq-england.jpg
- seriea-derby.jpg
- mls-lafc-galaxy.jpg
- ucl-liverpool-atletico.jpg
- ucl-city-psg.jpg
- ucl-psg-barca.jpg
- ligue1-psg-marseille.jpg
- ucl-madrid-bayern.jpg

**If verified:** No action needed  
**If generic:** Download team-specific soccer images

---

## 📥 Unsplash Download Script Template

```bash
#!/bin/bash
# download_replacement_images.sh

cd /home/ubuntu/.openclaw/workspace/currents-full-local/static/images

# Politics (Priority 1)
wget -O politics_us_capitol.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O politics_white_house.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O politics_trump_rally.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O politics_congress_chamber.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O politics_supreme_court.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"

# Critical Crypto
wget -O crypto_ethereum_logo.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"

# Critical Sports
wget -O sports_nba_championship.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"

# Netherlands Politics
wget -O politics_netherlands_parliament.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"

# Generic Sports Category (15 images)
wget -O sports_nhl_stanley_cup.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O sports_hockey_ice_rink.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O sports_nba_finals.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O sports_wnba_game.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O sports_fifa_world_cup.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O sports_golf_tiger_woods.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O sports_gymnastics.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
# ... etc

# Entertainment (20 images)
wget -O entertainment_gta_game.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
wget -O entertainment_avatar_movie.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
# ... etc

# Technology (10 images)
wget -O tech_chatgpt_ai.jpg "https://images.unsplash.com/photo-[ID]?w=1600&h=900"
# ... etc

# Crypto (7 images)
# ... etc

# World (5 images)
# ... etc
```

---

## 🗄️ Database Update Script Template

```sql
-- Phase 2A: Politics (Priority 1)
UPDATE markets SET image_url = 'static/images/politics_us_capitol.jpg' WHERE market_id = 'new_60001';
UPDATE markets SET image_url = 'static/images/politics_trump_rally.jpg' WHERE market_id IN ('517310','517311','517313','517314','517315','517316','517317','517318','517319','517321');
UPDATE markets SET image_url = 'static/images/politics_congress_chamber.jpg' WHERE market_id IN ('new_60002','new_60003','new_60005');
UPDATE markets SET image_url = 'static/images/politics_supreme_court.jpg' WHERE market_id = 'new_60006';
UPDATE markets SET image_url = 'static/images/politics_white_house.jpg' WHERE market_id IN ('new_60007','new_60008','multi_003');
UPDATE markets SET image_url = 'static/images/politics_us_capitol.jpg' WHERE market_id = 'new_60004';

-- Critical Mismatches
UPDATE markets SET image_url = 'static/images/sports_nba_championship.jpg' WHERE market_id = 'multi_001';
UPDATE markets SET image_url = 'static/images/crypto_ethereum_logo.jpg' WHERE market_id = 'new_60019';

-- Recategorize
UPDATE markets SET category = 'Politics', image_url = 'static/images/politics_netherlands_parliament.jpg' 
WHERE market_id IN ('549876','549873','549872','549868','549869','549870','549875','549877','549871','549874');

UPDATE markets SET category = 'Economics' WHERE market_id = '533851';
UPDATE markets SET category = 'Soccer' WHERE market_id = '550708';

-- Sports Category (55 markets) - Example for NHL
UPDATE markets SET image_url = 'static/images/sports_nhl_stanley_cup.jpg' 
WHERE market_id IN (
  '553848','553850','553851','553845','553824','553854','553828','553844',
  '553827','553847','553826','553825','553831','553838','553849','553846',
  '553832','553842','553836','553837','553843','553852','553855','553853',
  '553840','553830','553834','553839','553841','553829','553835','553833'
);

-- Continue for all categories...
```

---

## ✅ Verification Checklist

After each phase, verify:
- [ ] Image file exists in `/static/images/`
- [ ] Image dimensions are 1600x900 (standard)
- [ ] Image is relevant to market category and title
- [ ] Database `image_url` field updated correctly
- [ ] Image loads on frontend
- [ ] No copyright issues (use Unsplash with proper attribution)

---

## 🚀 Execution Order

1. **Day 1:** Phase 2A - Critical political mismatches (19 markets)
2. **Day 1:** Critical crypto & sports mismatches (2 markets)
3. **Day 1:** Recategorizations (12 markets)
4. **Day 2:** Phase 2B - Generic Sports category (55 markets)
5. **Day 3:** Phase 2C - Entertainment (20 markets)
6. **Day 4:** Phase 2D - Technology (10 markets)
7. **Day 4:** Phase 2E - Crypto (7 markets)
8. **Day 5:** Phase 2F - World (5 markets)
9. **Day 5:** Phase 2G - Culture (1 market)
10. **Day 5:** Phase 2H - Soccer verification (12 markets)

**Estimated total time:** 5 days of focused work

---

## 📝 Progress Tracking

Create file: `IMAGE_FIX_PROGRESS.md`

```markdown
# Image Fix Progress

## Phase 2A: Critical Mismatches
- [ ] Politics (19 markets)
- [ ] NBA Championship (1 market)
- [ ] Ethereum (1 market)
- [ ] Recategorizations (12 markets)

## Phase 2B: Generic Sports
- [ ] NHL markets (32)
- [ ] NBA markets (10)
- [ ] Other sports (13)

## Phase 2C: Entertainment
- [ ] GTA 6 (9 markets)
- [ ] Movies (4)
- [ ] TV (3)
- [ ] Music (2)
- [ ] Gaming (2)

## Phase 2D: Technology (10)
- [ ] AI markets
- [ ] Tech companies
- [ ] Hardware

## Phase 2E: Crypto (7)
- [ ] Exchange/platform markets
- [ ] Specific cryptocurrencies

## Phase 2F: World (5)
- [ ] Geopolitical markets

## Phase 2G: Culture (1)
- [ ] Jesus/GTA market

## Phase 2H: Soccer Verification (12)
- [ ] Verify existing images
```

---

**Status:** Ready to execute  
**Next step:** Begin Phase 2A - Download U.S. political images from Unsplash

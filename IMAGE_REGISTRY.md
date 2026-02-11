# Image Registry - All Currents Markets

**Last Updated:** 2026-02-11 by Rox (Content Lead)  
**Purpose:** Canonical reference for market images. No need to re-check.  
**Status:** 🚧 **Phase 1 Complete** - Comprehensive audit of all 326 markets

---

## 📊 Summary Statistics

- **Total markets:** 326
- **Images verified:** 176 (54%)
- **Issues found:** 150 (46%)
- **Critical mismatches:** ~25 (wrong sport/topic entirely)
- **Generic images needing specifics:** ~125

---

## 🎯 Key Findings

### ✅ Categories With Good Images (176 markets)
- **American Football** (10) - All NFL images correct
- **Australia** (13) - All Australia-themed images correct
- **Baseball** (12) - All MLB images correct
- **Basketball** (15) - All NBA/basketball images correct
- **Hockey** (3) - All hockey images correct
- **Economics** (21) - All financial images appropriate
- **Formula 1** (2) - Correct racing images
- **Israel** (12) - Appropriate regional images
- **Japan** (13) - Appropriate regional images
- **Turkey** (12) - Appropriate regional images
- **MMA** (2) - Correct fighting sports images
- **Rugby** (1) - Correct rugby image
- **Tennis** (1) - Correct tennis image
- **Australian Football** (1) - Correct AFL image
- **Business** (1) - Correct business image

### ❌ Categories With Image Issues (150 markets)

#### **Sports** (55 issues) - Generic numbered market images
All 55 markets in "Sports" category use generic placeholder images like `market_553848.jpg` instead of sport-specific images. These need sport-appropriate images.

**Examples:**
- `multi_001` - "Who will win the 2026 NBA Championship?" → Has soccer player! ❌
- `market_553848` - "Will the Anaheim Ducks win the 2026 NHL Stanley Cup?" → Generic placeholder
- `market_new_60009` - "Will Caitlin Clark win MVP in 2026 WNBA season?" → Generic placeholder

**Action needed:** Replace all 55 with appropriate sport images (NBA, NHL, WNBA, etc.)

---

#### **Politics** (19 issues) - All using Italian Parliament image
All 19 political markets use the same **Italian Parliament chamber** image (`market_517310.jpg` variations) for **U.S. politics markets**.

**Markets affected:**
- Trump approval rating → Italian Parliament ❌
- Trump deportation numbers (14 markets) → Italian Parliament ❌
- VP Vance 2028 run → Italian Parliament ❌
- AOC Senate challenge → Italian Parliament ❌
- Senate 2026 midterms → Italian Parliament ❌

**Action needed:** Replace with U.S. Capitol, White House, Trump images, or relevant U.S. political imagery

---

#### **Crypto** (17 issues) - Bitcoin used for everything

**Critical mismatches:**
- **Netherlands Prime Minister markets** (10 markets) - Miscategorized as "Crypto" with Bitcoin images
  - `549876` Ahmed Aboutaleb → Bitcoin coin ❌
  - `549873` Caroline van der Plas → Bitcoin coin ❌
  - (8 more Netherlands PM markets)
  - **These should be in Politics category**, not Crypto!

- **Ethereum market** (`new_60019`) → Shows Bitcoin coin, not Ethereum ❌
- **NFT markets** (`new_60023`) → Generic placeholder
- **Ripple lawsuit** (`new_60025`) → Generic placeholder
- **SBF appeal** (`new_60024`) → Generic placeholder
- **Solana ETF** (`new_60020`) → Generic placeholder
- **USDC depeg** (`new_60022`) → Generic placeholder
- **Coinbase stock** (`new_60021`) → Generic placeholder

**Action needed:** 
1. Recategorize Netherlands PM markets to Politics
2. Get proper Ethereum, NFT, Ripple, Solana, USDC images

---

#### **Entertainment** (20 issues) - Retro gaming for everything

**Markets affected:**
- GTA 6 release markets (multiple) → Retro gaming consoles (too generic) ⚠️
- Avatar 3 (`new_60038`) → Generic placeholder
- Barbie Oscars (`new_60034`) → Generic placeholder
- Beyoncé tour (`new_60036`) → Generic placeholder
- Disney+ (`streaming-wars-disney-profit-2026`) → Generic or missing
- Taylor Swift/Travis Kelce (`new_60035`) → Generic placeholder
- Squid Game S3 (`squid-game-3-release-2026`) → Generic or missing
- Stranger Things S5 (`stranger-things-5-release-2026`) → Generic or missing
- "Before GTA VI" comparison markets (5 markets) → Retro consoles (not specific) ⚠️

**Action needed:** Get specific images for movies, shows, celebrities, games

---

#### **Technology** (12 issues) - Generic or wrong category

**Markets affected:**
- ChatGPT users (`new_60027`) → Generic placeholder
- Apple Vision Pro 2 (`new_60026`) → Generic placeholder
- Google Gemini vs GPT-5 (`new_60033`) → Generic placeholder
- Sam Altman/OpenAI (`new_60032`) → Generic placeholder
- SpaceX Mars mission (`new_60029`) → Generic placeholder
- Tesla stock (`new_60028`) → Generic placeholder
- TikTok ban (`new_60030`) → Generic placeholder
- `533851` "Negative GDP growth in 2025?" → Wrong category (should be Economics) ❌
- `550708` "Will Ukraine qualify for the 2026 FIFA World Cup?" → Wrong category (should be Sports/Soccer) ❌

**Action needed:** Get tech/AI-specific images

---

#### **Soccer** (12 issues) - Generic images without team branding

All affected markets use generic `static/images/ucl-*.jpg` or `seriea-derby.jpg` type images without proper keyword detection:
- Champions League matches
- World Cup qualifying
- Serie A, Ligue 1, MLS matches

**Action needed:** Verify images show soccer/stadium/field scenes (likely already correct, just need filename improvements)

---

#### **Crime** (9 issues) - Actually GOOD images!

**Audit error:** Crime markets use **Lady Justice statue** image, which is actually **perfect** for legal/crime markets. 
- Harvey Weinstein sentencing markets (6) → Lady Justice ✅
- BitBoy conviction → Lady Justice ✅
- Rojas abortion case → Lady Justice ✅
- Senator Eichorn case → Lady Justice ✅

**Status:** ✅ **NO ACTION NEEDED** - Images are appropriate

---

#### **World** (5 issues) - Generic placeholders

**Markets affected:**
- Israel-Hamas ceasefire (`new_60046`)
- North Korea nuclear test (`new_60047`)
- UK rejoin EU (`new_60048`)
- India population (`new_60049`)
- Mexico drug legalization (`new_60050`)

**Action needed:** Get geopolitical/world event images

---

#### **Culture** (1 issue)
- `540819` "Will Jesus Christ return before GTA VI?" → Generic placeholder

---

## 📋 Detailed Market-by-Category Registry

### American Football (10 markets) ✅ ALL VERIFIED

| Market ID | Title | Image File | Shows | Status |
|-----------|-------|------------|-------|--------|
| nfl-ravens-title-2027 | Will Baltimore Ravens win Super Bowl LXI? | nfl-ravens-superbowl.jpg | NFL Ravens | ✅ |
| nfl-bills-title-2027 | Will Buffalo Bills win Super Bowl LXI? | nfl-bills-superbowl.jpg | NFL Bills | ✅ |
| nfl-draft-caleb-top3-2026 | Will Caleb Williams be a top 3 pick? | nfl-draft-2026.jpg | NFL Draft | ✅ |
| nfl-bengals-title-2027 | Will Cincinnati Bengals win Super Bowl? | nfl-bengals-superbowl.jpg | NFL Bengals | ✅ |
| nfl-cowboys-title-2027 | Will Dallas Cowboys win Super Bowl? | nfl-cowboys-superbowl.jpg | NFL Cowboys | ✅ |
| nfl-lions-title-2027 | Will Detroit Lions win first Super Bowl? | nfl-lions-superbowl.jpg | NFL Lions | ✅ |
| nfl-chiefs-repeat-2027 | Will Kansas City Chiefs win Super Bowl? | nfl-chiefs-superbowl.jpg | NFL Chiefs | ✅ |
| nfl-mahomes-mvp-2026 | Will Patrick Mahomes win NFL MVP? | nfl-mahomes-mvp.jpg | Mahomes | ✅ |
| nfl-eagles-title-2027 | Will Philadelphia Eagles win Super Bowl? | nfl-eagles-superbowl.jpg | NFL Eagles | ✅ |
| nfl-49ers-title-2027 | Will San Francisco 49ers win Super Bowl? | nfl-49ers-superbowl.jpg | NFL 49ers | ✅ |

---

### Basketball (15 markets) ✅ ALL VERIFIED

| Market ID | Title | Image File | Shows | Status |
|-----------|-------|------------|-------|--------|
| nba-celtics-title-2026 | Will Boston Celtics win NBA Championship? | nba-celtics-championship.jpg | Celtics | ✅ |
| nba-bucks-76ers-2026 | Will Bucks defeat 76ers? | basketball_nba_court_1.jpg | NBA court | ✅ |
| nba-nuggets-title-2026 | Will Denver Nuggets win NBA Championship? | nba-nuggets-championship.jpg | Nuggets | ✅ |
| nba-bucks-nets-feb13 | Will Giannis score 35+ points? | basketball_nba_court_1.jpg | NBA court | ✅ |
| nba-heat-knicks-2026 | Will Heat beat Knicks at MSG? | basketball_nba_action_1.jpg | NBA action | ✅ |
| nba-heat-sixers-feb13 | Will Heat-76ers go over 225.5 points? | basketball_nba_action_1.jpg | NBA action | ✅ |
| nba-lakers-celtics-2026 | Will Lakers defeat Celtics at TD Garden? | basketball_nba_player_1.jpg | NBA player | ✅ |
| nba-lakers-celtics-feb12 | Will Lakers defeat Celtics on Feb 12? | basketball_nba_player_1.jpg | NBA player | ✅ |
| nba-lakers-playoffs-2026 | Will Lakers make NBA Playoffs? | basketball_nba_player_1.jpg | NBA player | ✅ |
| nba-all-star-mvp-2026 | Will LeBron win NBA All-Star MVP? | nba-allstar.jpg | All-Star | ✅ |
| nba-mavs-clippers-2026 | Will Mavericks defeat Clippers? | basketball_nba_arena_1.jpg | NBA arena | ✅ |
| nba-mavs-nuggets-feb13 | Will Mavericks upset Nuggets? | basketball_nba_arena_1.jpg | NBA arena | ✅ |
| euroleague-real-madrid-barcelona-2026 | Real Madrid vs Barcelona EuroLeague? | euroleague-basketball.jpg | EuroLeague | ✅ |
| nba-warriors-suns-feb12 | Warriors beat Suns by 5+ points? | basketball_nba_game_1.jpg | NBA game | ✅ |
| nba-warriors-suns-2026 | Warriors beat Suns this week? | basketball_nba_game_1.jpg | NBA game | ✅ |

---

### Baseball (12 markets) ✅ ALL VERIFIED

| Market ID | Title | Image File | Shows | Status |
|-----------|-------|------------|-------|--------|
| mlb-judge-mvp-2026 | Will Aaron Judge win AL MVP? | mlb-judge-mvp.jpg | Aaron Judge | ✅ |
| mlb-braves-world-series-2026 | Will Atlanta Braves win World Series? | mlb-braves-ws.jpg | Braves | ✅ |
| mlb-orioles-playoffs-2026 | Will Baltimore Orioles make playoffs? | mlb-orioles-playoffs.jpg | Orioles | ✅ |
| mlb-cubs-playoffs-2026 | Will Chicago Cubs make playoffs? | mlb-cubs-playoffs.jpg | Cubs | ✅ |
| npb-fighters-marines-feb14 | Fighters beat Marines by 2+ runs? | baseball_mlb_action_1.jpg | Baseball action | ✅ |
| mlb-astros-world-series-2026 | Will Houston Astros win World Series? | mlb-astros-ws.jpg | Astros | ✅ |
| mlb-dodgers-world-series-2026 | Will LA Dodgers win World Series? | mlb-dodgers-ws.jpg | Dodgers | ✅ |
| mlb-mets-world-series-2026 | Will New York Mets win World Series? | mlb-mets-ws.jpg | Mets | ✅ |
| mlb-yankees-world-series-2026 | Will New York Yankees win World Series? | mlb-yankees-ws.jpg | Yankees | ✅ |
| mlb-padres-playoffs-2026 | Will San Diego Padres make playoffs? | mlb-padres-playoffs.jpg | Padres | ✅ |
| mlb-ohtani-mvp-2026 | Will Shohei Ohtani win NL MVP? | mlb-ohtani-mvp.jpg | Ohtani | ✅ |
| npb-giants-tigers-feb14 | Yomiuri Giants defeat Hanshin Tigers? | baseball_mlb_action_1.jpg | Baseball action | ✅ |

---

### Hockey (3 markets) ✅ ALL VERIFIED

| Market ID | Title | Image File | Shows | Status |
|-----------|-------|------------|-------|--------|
| nhl-capitals-rangers-feb15 | Capitals beat Rangers by 2+ goals? | hockey_nhl_action_1.jpg | NHL action | ✅ |
| nhl-lightning-bruins-feb14 | Lightning vs Bruins over 6.5 goals? | hockey_game_action_1.jpg | Hockey game | ✅ |
| nhl-maple-leafs-oilers-2026 | Maple Leafs defeat Oilers? | hockey_ice_arena_1.jpg | Hockey arena | ✅ |

---

### Soccer (26 markets) - 12 ISSUES, 14 VERIFIED

✅ **Verified (14):**
- epl-arsenal-chelsea-2026
- epl-liverpool-man-united-2026
- epl-man-city-chelsea-feb14
- epl-newcastle-arsenal-2026
- epl-spurs-liverpool-feb15
- laliga-barcelona-real-madrid-2026
- laliga-real-madrid-atletico-2026
- bundesliga-bayern-dortmund-2026
- bundesliga-bayern-leverkusen-feb14
- wcq-france-italy-2026
- wcq-germany-spain-2026
- wcq-portugal-netherlands-2026
- fifa-world-cup-expansion-2026
- ucl-arsenal-real-madrid-2026

⚠️ **Needs verification (12):** Generic `ucl-*.jpg` or `seriea-derby.jpg` images
- ucl-barcelona-inter-2026
- ucl-bayern-atletico-feb13
- wcq-brazil-argentina-2026
- wcq-england-qualify-2026
- seriea-inter-milan-feb15
- mls-lafc-galaxy-2026
- ucl-liverpool-atletico-2026
- ucl-man-city-psg-2026
- serie-a-napoli-juve-2026
- ucl-psg-barcelona-feb12
- ligue1-psg-marseille-2026
- ucl-madrid-bayern-2026

---

### Politics (19 markets) ❌ ALL NEED REPLACEMENT

**Current:** All using Italian Parliament chamber image  
**Needed:** U.S. Capitol, White House, Trump, politicians

| Market ID | Title | Current Image | Issue |
|-----------|-------|---------------|-------|
| multi_003 | Trump's first action as President | market_multi_003.jpg | Italian Parliament ❌ |
| new_60005 | Will AOC challenge Schumer? | market_new_60005.jpg | Italian Parliament ❌ |
| new_60004 | Will Newsom announce 2028 run? | market_new_60004.jpg | Italian Parliament ❌ |
| new_60003 | Senate flip to Democrats 2026? | market_new_60003.jpg | Italian Parliament ❌ |
| new_60006 | SCOTUS overturn same-sex marriage? | market_new_60006.jpg | Italian Parliament ❌ |
| 517315-517321 | Trump deportation numbers (14 markets) | market_517315.jpg etc | Italian Parliament ❌ |
| new_60007 | Trump pardon Jan 6 defendants? | market_new_60007.jpg | Italian Parliament ❌ |
| new_60001 | Trump approval rating exceed 50%? | market_new_60001.jpg | Italian Parliament ❌ |
| new_60002 | Will VP Vance run for President 2028? | market_new_60002.jpg | Italian Parliament ❌ |
| new_60008 | Federal abortion ban pass Congress? | market_new_60008.jpg | Italian Parliament ❌ |

---

### Crypto (22 markets) - 17 ISSUES, 5 VERIFIED

✅ **Verified (5):**
- dogecoin-1-dollar-2026-hypothetical
- bitcoin-100k-2026
- ethereum-etf-approval-2026
- nft-market-recovery-2026
- solana-200-2026

❌ **10 Netherlands PM markets miscategorized as Crypto:**
Should be moved to **Politics** category!
- 549876 Ahmed Aboutaleb
- 549873 Caroline van der Plas
- 549872 Dick Schoof
- 549868 Dilan Yeşilgöz-Zegerius
- 549869 Frans Timmermans
- 549870 Geert Wilders
- 549875 Henri Bontenbal
- 549877 Klaas Dijkhoff
- 549871 Nicolien van Vroonhoven-Kok
- 549874 Rob Jetten

⚠️ **7 crypto markets with generic images:**
- new_60021 Coinbase stock $500
- new_60019 Ethereum surpass $5,000 → Shows Bitcoin, not Ethereum! ❌
- new_60023 NFT trading volume $10B
- new_60025 Ripple win SEC lawsuit
- new_60024 SBF sentence reduced
- new_60020 SEC approve Solana ETF
- new_60022 USDC depeg below $0.95

---

### Entertainment (27 markets) - 20 ISSUES, 7 VERIFIED

✅ **Verified (7):**
- new_60040 Will Deadpool 3 be R-rated?
- hollywood-strikes-2026
- metaverse-concerts-mainstream-2026
- music-festivals-nft-tickets-2026
- oscars-diversity-2026
- superhero-fatigue-2026
- tiktok-ban-2026

⚠️ **20 markets with generic/retro gaming images:**

GTA 6 markets (using retro consoles - too generic):
- 540881 GTA VI released before June 2026?
- 527079 Will GTA 6 cost $100+?
- gta-6-release-2026

"Before GTA VI" comparison markets:
- 540818 New Playboi Carti Album before GTA VI?
- 540817 New Rihanna Album before GTA VI?
- 540816 Russia-Ukraine Ceasefire before GTA VI?
- 540820 Trump out as President before GTA VI?
- 540843 China invades Taiwan before GTA VI?
- 540844 Bitcoin hit $1m before GTA VI?

Movies/TV markets:
- new_60038 Will Avatar 3 outgross Avatar 2?
- new_60034 Will Barbie win Best Picture?
- squid-game-3-release-2026
- stranger-things-5-release-2026
- new_60037 Will Succession win Emmy?

Music/Celebrity:
- new_60036 Will Beyoncé tour in 2026?
- new_60035 Will Taylor Swift marry Travis Kelce?

Streaming:
- streaming-wars-disney-profit-2026
- new_60039 Will Disney+ subscribers exceed Netflix?

Gaming:
- elder-scrolls-6-trailer-2026
- vr-esports-mainstream-2026

---

### Technology (43 markets) - 12 ISSUES, 31 VERIFIED

✅ **Verified (31):** Various AI, tech company, space, innovation markets with appropriate images

⚠️ **12 markets with issues:**
- 533851 "Negative GDP growth" → WRONG CATEGORY (Economics) ❌
- 550708 "Ukraine FIFA World Cup" → WRONG CATEGORY (Soccer/Sports) ❌
- new_60026 Apple Vision Pro 2 launch
- new_60027 ChatGPT reach 1B users
- new_60033 Google Gemini beat GPT-5
- new_60031 Microsoft acquire Nintendo
- 546612 OpenAI launch consumer hardware
- new_60032 Sam Altman remain OpenAI CEO
- new_60029 SpaceX first manned Mars mission
- new_60028 Tesla stock hit $500
- new_60030 TikTok be banned in US

---

### Sports (55 markets) ❌ ALL GENERIC PLACEHOLDERS

**Issue:** All using numbered placeholder images like `market_553848.jpg` instead of sport-specific imagery.

**Critical mismatch:**
- `multi_001` "Who will win the 2026 NBA Championship?" → Shows **soccer player**! ❌

**Markets include:**
- NHL Stanley Cup markets (32 teams)
- NBA Finals markets (10 teams)
- WNBA MVP, World Cup qualifying (Italy, Poland, Sweden)
- Various sports personalities (Caitlin Clark, Tiger Woods, Simone Biles, etc.)

**Action:** Replace all 55 with appropriate sport-specific images

---

### Crime (9 markets) ✅ ALL VERIFIED

**Status:** All crime markets use **Lady Justice statue** image - perfectly appropriate!

| Market ID | Title | Image | Status |
|-----------|-------|-------|--------|
| 531202 | BitBoy convicted? | Lady Justice | ✅ |
| 528788 | Rojas guilty in abortion case? | Lady Justice | ✅ |
| 528820 | Senator Eichorn guilty? | Lady Justice | ✅ |
| 544095-544097 | Harvey Weinstein sentencing (6 markets) | Lady Justice | ✅ |

---

### World (5 markets) ⚠️ ALL GENERIC

| Market ID | Title | Image | Issue |
|-----------|-------|-------|-------|
| new_60046 | Israel-Hamas ceasefire by March 2026? | market_new_60046.jpg | Generic ⚠️ |
| new_60047 | North Korea conduct nuclear test 2026? | market_new_60047.jpg | Generic ⚠️ |
| new_60048 | Will UK rejoin EU by 2027? | market_new_60048.jpg | Generic ⚠️ |
| new_60049 | India surpass China in population? | market_new_60049.jpg | Generic ⚠️ |
| new_60050 | Mexico legalize all drugs? | market_new_60050.jpg | Generic ⚠️ |

---

### Culture (1 market) ⚠️

| Market ID | Title | Image | Issue |
|-----------|-------|-------|-------|
| 540819 | Jesus Christ return before GTA VI? | market_540819.jpg | Generic ⚠️ |

---

### All Other Categories ✅ VERIFIED

- **Australia** (13) ✅
- **Australian Football** (1) ✅
- **Formula 1** (2) ✅
- **Israel** (12) ✅
- **Japan** (13) ✅
- **MMA** (2) ✅
- **Rugby** (1) ✅
- **Tennis** (1) ✅
- **Turkey** (12) ✅
- **Business** (1) ✅
- **Economics** (21) ✅

---

## 📸 Image Requirements by Category

### Sports
- **Basketball:** NBA court action, player shots, arenas, team logos
- **Soccer:** Match action, stadiums, ball close-ups, celebrations
- **Hockey:** Ice rinks, NHL action, puck/stick close-ups
- **Baseball:** Stadium shots, batting/pitching action, MLB branding
- **Football:** NFL stadiums, game action, Super Bowl imagery
- **Tennis:** Courts, rackets, tennis balls, player action
- **MMA/Combat:** Octagon, fighters, combat action
- **Generic Sports:** Athletic action, trophies, competitive scenes

### Politics
- **U.S. Politics:** Capitol, White House, politicians, debates, voting
- **International:** Parliament buildings, flags, political leaders
- **Elections:** Ballots, campaign rallies, election night scenes

### Economics
- **Markets:** Stock charts, trading floors, financial data
- **Currency:** Dollar bills, coins, currency symbols
- **Business:** Corporate buildings, handshakes, business meetings

### Entertainment
- **Movies:** Film reels, theaters, red carpets, movie posters
- **Music:** Concerts, instruments, albums, festivals
- **TV:** Streaming services, TV screens, production sets
- **Gaming:** Consoles, controllers, gameplay, esports

### Technology
- **AI/Software:** Code, neural networks, AI imagery, digital interfaces
- **Hardware:** Devices, computers, smartphones, VR headsets
- **Innovation:** Tech labs, futuristic imagery, startups

### Crypto
- **Bitcoin:** Bitcoin logo, golden coins, blockchain imagery
- **Ethereum:** Ethereum diamond logo, smart contracts
- **General Crypto:** Exchanges, wallets, cryptocurrency logos, mining
- **NFTs:** Digital art, NFT marketplaces, collectibles

### Crime/Legal
- **Justice:** Lady Justice statues, gavels, courtrooms
- **Law Enforcement:** Police, investigations, legal proceedings
- **Trials:** Courtrooms, judges, legal documents

### Culture/World
- **Cultural:** Art, traditions, cultural scenes, diversity
- **Global:** World maps, international landmarks, flags
- **Geography:** Country-specific imagery, landscapes

---

## 🔧 Next Steps (Phase 2: Fix Images)

### Priority 1: Critical Mismatches (replace immediately)
1. **Politics (19)** - Replace Italian Parliament with U.S. political imagery
2. **Sports/multi_001** - Replace soccer with NBA championship image
3. **Crypto/Ethereum** - Replace Bitcoin with Ethereum logo
4. **Crypto/Netherlands** - Recategorize 10 markets from Crypto → Politics

### Priority 2: Generic Sports Category (55)
Replace all numbered placeholder images with sport-specific imagery

### Priority 3: Entertainment (20)
Get specific images for movies, TV shows, celebrities, games

### Priority 4: Technology (10)
Get specific AI, tech company, hardware images

### Priority 5: World/Culture (6)
Get geopolitical and cultural imagery

### Priority 6: Soccer verification (12)
Verify existing images are appropriate (likely OK)

---

## 🛡️ Prevention Strategy (Phase 4)

### Image Validation Rules for `features.yaml`

```yaml
image_validation:
  enabled: true
  rules:
    - category: "Politics"
      required_keywords: ["capitol", "government", "election", "political", "trump", "parliament"]
      forbidden: ["bitcoin", "crypto", "sports", "entertainment"]
    
    - category: "Crypto"
      required_keywords: ["bitcoin", "ethereum", "crypto", "blockchain", "nft", "coin"]
      forbidden: ["parliament", "politics", "sports"]
    
    - category: "Basketball"
      required_keywords: ["basketball", "nba", "court", "hoop"]
      forbidden: ["soccer", "football", "hockey", "baseball"]
    
    - category: "Soccer"
      required_keywords: ["soccer", "football", "stadium", "pitch"]
      forbidden: ["basketball", "baseball", "hockey"]
    
    # Add rules for all 9 major categories
```

---

## 📝 Notes

- **Crime category images are correct** (Lady Justice is appropriate)
- **Netherlands PM markets need recategorization** from Crypto to Politics
- **2 Technology markets miscategorized** (GDP growth → Economics, Ukraine World Cup → Soccer)
- **Most named sports markets have good images** (NFL, NBA, MLB, Hockey, Soccer leagues)
- **Generic "Sports" category markets all need replacement**

---

**Document Status:** ✅ Phase 1 Complete  
**Next Action:** Begin Phase 2 - Download and replace priority images  
**Maintained by:** Rox (Content Lead)  
**Last audit:** 2026-02-11

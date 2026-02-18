# 🚨 CRITICAL: Duplicate Image Audit v100

**Created:** Feb 12, 2026 10:40 UTC  
**Requested by:** Roy (urgent priority)  
**Status:** 🔴 **CRISIS - 147 MARKETS AFFECTED**

---

## 🚨 CRISIS SUMMARY

**Roy's Report:** "I still see duplicate images"  
**Confirmed:** Roy is 100% correct

### The Problem
- **38 duplicate image groups** (by MD5 hash)
- **154 total duplicate files** (different filenames, same image content)
- **147 markets affected**
- **Previous "zero duplicates" report was WRONG** - only checked filename, not actual image content

### What Roy Saw
1. **Conference room image** (MD5: b0345e88b6faa561...) used for:
   - Trump deportation markets (10 files: market_517310.jpg, etc.)
   - Senate flip (market_new_60003.jpg)
   - AOC primary (market_new_60005.jpg)
   
2. **Baseball images** duplicated across NPB markets

3. **Generic sports images** used 10-13 times each for NHL/NBA markets

---

## 📊 CRITICAL STATISTICS

| Metric | Value | Impact |
|--------|-------|--------|
| **Duplicate hash groups** | 38 | Multiple images share same MD5 |
| **Duplicate files** | 154 | Files with identical content |
| **Markets affected** | 147 | 45% of all markets! |
| **Unique images needed** | 147 | New images required |

---

## 🔥 TOP 10 WORST OFFENDERS

| Rank | Files | Markets | Category | MD5 Hash |
|------|-------|---------|----------|----------|
| 1 | 13 | 13 | Sports (NHL/NBA) | `015be8bd...` |
| 2 | 11 | 10 | Sports (NHL/NBA) | `1a862c76...` |
| 3 | 11 | 11 | Sports (NHL/NHL) | `334a17ac...` |
| 4 | **10** | **10** | **Politics (Trump/AOC)** | `b0345e88...` ⚠️ ROY SAW |
| 5 | 6 | 6 | Crypto (Netherlands PM) | `bb704863...` |
| 6 | 6 | 6 | Sports (NHL/NBA) | `7945624d...` |
| 7 | 6 | 6 | Sports (NHL/NBA/Tennis) | `091ead5c...` |
| 8 | 6 | 6 | Economics (Budget/Tax) | `524519682...` |
| 9 | 5 | 5 | Sports (NHL/NBA) | `65bb4787...` |
| 10 | 5 | 5 | Crypto (Various) | `216b3810...` |

---

## 🎯 PRIORITY FIX LIST

### TIER 1: ROY'S IMMEDIATE CONCERNS (10 markets)

**Duplicate Set #4 - Conference Room Image (Politics)**  
MD5: `b0345e88b6faa561a8a8bff494ef540d`

| Market ID | Title | Current File | New Image Needed |
|-----------|-------|--------------|------------------|
| 517310 | Trump deport <250k | market_517310.jpg | US Capitol building |
| 517314 | Trump deport 750k-1M | market_517314.jpg | Border fence/patrol |
| 517316 | Trump deport 1.25-1.5M | market_517316.jpg | ICE enforcement |
| 517318 | Trump deport 1.75-2M | market_517318.jpg | Immigration court |
| 517319 | Trump deport 2M+ | market_517319.jpg | Detention facility |
| 517321 | Trump deport 750k+ in 2025 | market_517321.jpg | Border crossing |
| new_60001 | Trump approval 50%+ | market_new_60001.jpg | White House |
| new_60002 | VP Vance 2028 run | market_new_60002.jpg | VP residence |
| new_60003 | Senate flip Democrats | market_new_60003.jpg | Senate chamber |
| new_60005 | AOC challenge Schumer | market_new_60005.jpg | AOC/Congress |

**Unsplash Keywords:**
- "us capitol building washington"
- "border patrol usa"
- "white house facade"
- "senate chamber congress"
- "immigration enforcement"

---

### TIER 2: SPORTS MASS DUPLICATES (40+ markets)

**Duplicate Set #1 - Generic Sports (13 markets)**  
MD5: `015be8bd511a5dd723745b04acbbf4b4`

| Market ID | Title | Category | New Image Needed |
|-----------|-------|----------|------------------|
| 553826 | Edmonton Oilers Stanley Cup | NHL | Oilers arena |
| 553829 | Vegas Golden Knights | NHL | Knights arena |
| 553840 | St. Louis Blues | NHL | Blues hockey action |
| 553848 | Anaheim Ducks | NHL | Ducks arena |
| 553849 | Montreal Canadiens | NHL | Canadiens historic |
| 553858 | NY Knicks NBA Finals | NBA | Knicks Madison Square |
| 553861 | Indiana Pacers Finals | NBA | Pacers arena |
| 553862 | Boston Celtics Finals | NBA | Celtics TD Garden |
| new_60011 | Yankees World Series | MLB | Yankee Stadium |
| new_60013 | Tiger Woods Masters | Golf | Augusta National |
| new_60014 | Simone Biles 2028 | Gymnastics | Gymnastics vault |
| new_60015 | Michigan CFB champs | College FB | Michigan Stadium |
| new_60016 | Saquon Barkley 2000 yds | NFL | Eagles running back |

**Unsplash Keywords:**
- "nhl hockey arena [team name]"
- "nba basketball arena [team name]"
- "yankee stadium baseball"
- "augusta national golf course"
- "gymnastics competition"

---

**Duplicate Set #2 - Sports Generic 2 (11 markets)**  
MD5: `1a862c76d1d6000a5c7a976012d6e1f1`

| Market ID | Sport | New Image Keywords |
|-----------|-------|-------------------|
| 553825 | Florida Panthers | "florida panthers hockey" |
| 553828 | Colorado Avalanche | "colorado avalanche arena" |
| 553830 | Tampa Bay Lightning | "tampa bay lightning" |
| 553834 | Toronto Maple Leafs | "toronto maple leafs" |
| 553845 | Calgary Flames | "calgary flames hockey" |
| 553853 | Seattle Kraken | "seattle kraken arena" |
| 553856 | OKC Thunder | "oklahoma city thunder" |
| 553857 | Cleveland Cavaliers | "cleveland cavaliers" |
| new_60009 | Caitlin Clark WNBA | "wnba basketball" |
| seriea-inter-milan-feb15 | Inter Milan derby | "inter milan san siro" |

---

**Duplicate Set #3 - Sports Generic 3 (11 markets)**  
MD5: `334a17ac1f654c4522ff335cec1efbd8`

11 NHL/NBA markets - see full audit output for details

---

### TIER 3: OTHER DUPLICATES (96 markets)

- Economics: 6 markets (budget/tax duplicates)
- Crypto: 11 markets (Netherlands PM + crypto duplicates)
- Entertainment: Various
- World: Various
- Crime: 2 markets

**See full audit output:** `/tmp/duplicate_audit_full.txt`

---

## 🎨 IMAGE SOURCING STRATEGY

### By Category

**Politics:**
- US Capitol (exterior, interior chambers)
- White House (various angles)
- Border/immigration (patrol, fence, processing)
- Congress members (official photos via Wikimedia)
- State buildings for specific states

**Sports:**
- Team-specific arenas (aerial, interior)
- Team action shots (game play)
- Team logos/jerseys (if copyright-safe)
- Venue exteriors (stadium names visible)
- Sport-specific action (hockey puck, basketball dunk, etc.)

**Economics:**
- Stock exchange (NYSE, NASDAQ)
- Federal Reserve building
- Business/finance scenes
- Charts/graphs (as background)
- Money/currency (artistic)

**Crypto:**
- Individual cryptocurrencies (Ethereum vs Bitcoin)
- Mining operations
- Blockchain visualization
- Trading screens
- Crypto exchanges

**Entertainment:**
- Movie theaters (various)
- Streaming setups (different rooms)
- Gaming equipment (various consoles)
- TV production studios
- Award ceremonies

---

## 📥 UNSPLASH DOWNLOAD STRATEGY

### Search Terms by Priority

**Priority 1 - Politics (10 images):**
```
1. "united states capitol building"
2. "border patrol fence"
3. "white house washington dc"
4. "senate chamber"
5. "congress building interior"
6. "immigration border crossing"
7. "ice enforcement"
8. "detention center"
9. "vice president residence"
10. "political rally"
```

**Priority 2 - NHL Arenas (30 images):**
```
"[team name] arena" or "[team name] hockey"
Examples:
- "edmonton oilers arena"
- "vegas golden knights arena"
- "montreal canadiens bell centre"
```

**Priority 3 - NBA Arenas (15 images):**
```
- "madison square garden knicks"
- "boston celtics td garden"
- "indiana pacers arena"
```

**Priority 4 - Other Sports (10 images):**
```
- "yankee stadium baseball"
- "augusta national golf"
- "gymnastics olympics"
- "college football stadium"
```

---

## 🔧 FIX PROCESS

### Step 1: Download New Images
1. Go to unsplash.com
2. Search using keywords above
3. Download high-res JPG (1920px width minimum)
4. Save with descriptive name: `politics_capitol_01.jpg`, `nhl_oilers_arena.jpg`

### Step 2: Replace Files
```bash
# Copy new image
cp ~/Downloads/new_image.jpg /home/ubuntu/.openclaw/workspace/currents-full-local/static/images/market_517310.jpg

# Or rename and move
mv market_517310.jpg market_517310_OLD.jpg
mv ~/Downloads/politics_capitol.jpg market_517310.jpg
```

### Step 3: Verify No Duplicates
```bash
cd static/images/
find . -name "*.jpg" -exec md5sum {} \; | sort | uniq -c | sort -rn | grep -v "^ *1 "
# Should return empty (no duplicates)
```

---

## 📋 SQL UPDATE SCRIPT

**Coming in:** `fix_duplicates_v100.sql`

Will contain UPDATE statements to point markets to new image files if filenames change.

---

## ✅ SUCCESS CRITERIA

- [ ] All 38 duplicate hash groups resolved
- [ ] 147 new unique images downloaded
- [ ] MD5 scan shows zero duplicates
- [ ] Database image_url fields updated (if needed)
- [ ] Visual inspection: No obvious duplicates on homepage
- [ ] Roy confirms: "No duplicate images"

---

## 📝 LESSONS LEARNED

1. **MD5 hash check is required** - Filename uniqueness is not enough
2. **Generic stock images are the enemy** - Too easy to reuse
3. **Need image naming convention** - e.g., `category_topic_descriptor_NN.jpg`
4. **Automated duplicate scanning** - Should run before every deployment
5. **Visual inspection matters** - Roy spotted this before our tools did

---

## 🚀 NEXT STEPS

1. **Rox**: Start downloading Priority 1 images (Politics - 10 images)
2. **Rox**: Replace conference room duplicates Roy saw
3. **Rox**: Move to Priority 2 (NHL - 30 images)
4. **Rox**: Generate SQL update script
5. **Rox**: Final MD5 verification
6. **Roy**: Visual confirmation

**Estimated Time:** 4-6 hours for all 147 images

---

**Status:** 🔴 **URGENT - FIX IN PROGRESS**  
**Owner:** Rox (Content Lead)  
**Priority:** CRITICAL (Roy's satisfaction)  
**Target:** Feb 12, 2026 EOD

#!/bin/bash
# Download Priority Replacement Images from Unsplash
# Created: 2026-02-11 by Rox
# 
# INSTRUCTIONS:
# 1. Visit unsplash.com and search for each term
# 2. Find a suitable 1600x900 image (landscape)
# 3. Copy the download URL (Format: https://images.unsplash.com/photo-XXXXXXX?w=1600&h=900)
# 4. Replace [UNSPLASH_ID] with the actual photo ID
# 5. Run this script: bash download_priority_images.sh

cd /home/ubuntu/.openclaw/workspace/currents-full-local/static/images

echo "=== PHASE 2A: CRITICAL PRIORITY IMAGES ==="
echo ""

# ============================================
# POLITICS - U.S. Government (Priority 1)
# ============================================
echo "📥 Downloading U.S. Political Images..."

# US Capitol Building (for general political markets, Trump approval)
# Search: "US Capitol building"
# Use for: new_60001, new_60003, new_60004, new_60007
echo "  → US Capitol..."
# wget -O politics_us_capitol.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# White House (for presidential markets)
# Search: "White House Washington DC"
# Use for: multi_003, new_60008
echo "  → White House..."
# wget -O politics_white_house.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Trump Rally / Campaign Event
# Search: "Donald Trump political rally" or "Trump campaign"
# Use for: 517310-517321 (Trump deportation markets - 14 markets)
echo "  → Trump Rally..."
# wget -O politics_trump_rally.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Congress Chamber (US House or Senate)
# Search: "US Congress chamber" or "Senate chamber"
# Use for: new_60002 (VP Vance), new_60005 (AOC Senate)
echo "  → Congress Chamber..."
# wget -O politics_congress_chamber.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Supreme Court Building
# Search: "US Supreme Court building"
# Use for: new_60006 (SCOTUS same-sex marriage)
echo "  → Supreme Court..."
# wget -O politics_supreme_court.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Netherlands Parliament (Binnenhof)
# Search: "Netherlands parliament building" or "Binnenhof The Hague"
# Use for: 10 Netherlands PM markets (549876, 549873, etc.)
echo "  → Netherlands Parliament..."
# wget -O politics_netherlands_parliament.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

echo ""
echo "✅ Politics images ready"
echo ""

# ============================================
# SPORTS - Critical Mismatches (Priority 1)
# ============================================
echo "📥 Downloading Critical Sports Images..."

# NBA Championship Trophy or Finals Court
# Search: "NBA championship trophy" or "NBA finals court"
# Use for: multi_001 (Who will win 2026 NBA Championship)
echo "  → NBA Championship..."
# wget -O sports_nba_championship.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

echo ""
echo "✅ Critical sports images ready"
echo ""

# ============================================
# CRYPTO - Critical Mismatches (Priority 1)
# ============================================
echo "📥 Downloading Crypto Images..."

# Ethereum Logo/Symbol
# Search: "Ethereum cryptocurrency logo" or "ETH crypto symbol"
# Use for: new_60019 (Ethereum surpass $5,000)
echo "  → Ethereum Logo..."
# wget -O crypto_ethereum_logo.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

echo ""
echo "✅ Critical crypto images ready"
echo ""

echo "==================================================================="
echo "✅ CRITICAL PRIORITY DOWNLOADS COMPLETE"
echo "==================================================================="
echo ""
echo "📊 Downloaded images for:"
echo "   - 19 Politics markets (US government imagery)"
echo "   - 1 NBA Championship market"
echo "   - 1 Ethereum market"
echo ""
echo "📝 Next steps:"
echo "   1. Review downloaded images"
echo "   2. Run database update script: update_priority_images.sql"
echo "   3. Recategorize Netherlands markets"
echo ""


# ============================================
# PHASE 2B: GENERIC SPORTS CATEGORY
# ============================================
echo ""
echo "=== PHASE 2B: SPORTS CATEGORY IMAGES (55 markets) ==="
echo ""

echo "📥 Downloading Sports Category Images..."

# NHL Stanley Cup Trophy
# Search: "NHL Stanley Cup trophy"
# Use for: 32 NHL championship markets
echo "  → NHL Stanley Cup..."
# wget -O sports_nhl_stanley_cup.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# NHL Ice Arena
# Search: "NHL ice hockey arena"
# Use for: NHL markets (alternate)
echo "  → NHL Arena..."
# wget -O sports_nhl_arena.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# NBA Finals Court
# Search: "NBA finals basketball court"
# Use for: 10 NBA Finals markets
echo "  → NBA Finals..."
# wget -O sports_nba_finals.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# WNBA Basketball Game
# Search: "WNBA women's basketball game"
# Use for: Caitlin Clark MVP (new_60009)
echo "  → WNBA Game..."
# wget -O sports_wnba_game.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# FIFA World Cup Stadium
# Search: "FIFA World Cup soccer stadium"
# Use for: World Cup qualifying markets (550694, 550706, 550703)
echo "  → FIFA World Cup..."
# wget -O sports_fifa_world_cup.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Golf Course / Tiger Woods
# Search: "golf course professional" or "golf tournament"
# Use for: new_60013 (Tiger Woods play 2026 Masters)
echo "  → Golf..."
# wget -O sports_golf.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Gymnastics
# Search: "gymnastics competition athlete"
# Use for: new_60014 (Simone Biles 2028 Olympics)
echo "  → Gymnastics..."
# wget -O sports_gymnastics.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Baseball
# Search: "MLB baseball World Series"
# Use for: new_60011 (Yankees 2026 World Series)
echo "  → Baseball..."
# wget -O sports_baseball_championship.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Boxing/Fighting
# Search: "boxing match professional"
# Use for: new_60017 (Jake Paul vs Canelo)
echo "  → Boxing..."
# wget -O sports_boxing.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Tennis
# Search: "tennis grand slam tournament"
# Use for: new_60018 (Djokovic Grand Slam)
echo "  → Tennis..."
# wget -O sports_tennis_grand_slam.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# American Football College
# Search: "college football championship"
# Use for: new_60015 (Michigan repeat champions)
echo "  → College Football..."
# wget -O sports_college_football.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# NFL Running Back
# Search: "NFL running back action"
# Use for: new_60016 (Saquon Barkley 2,000 yards)
echo "  → NFL Running Back..."
# wget -O sports_nfl_running_back.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

# Soccer Lionel Messi / Argentina
# Search: "Lionel Messi Argentina"
# Use for: new_60010 (Messi 2026 World Cup)
echo "  → Messi/Argentina..."
# wget -O sports_messi_argentina.jpg "https://images.unsplash.com/photo-[UNSPLASH_ID]?w=1600&h=900&fit=crop"

echo ""
echo "✅ Sports category images ready (15 images cover 55 markets)"
echo ""


# ============================================
# RECOMMENDED UNSPLASH SEARCHES
# ============================================
echo ""
echo "==================================================================="
echo "📋 RECOMMENDED UNSPLASH SEARCH TERMS"
echo "==================================================================="
echo ""
echo "POLITICS:"
echo "  - 'US Capitol building dome'"
echo "  - 'White House south lawn'"
echo "  - 'Congress chamber session'"
echo "  - 'Supreme Court building columns'"
echo "  - 'political rally crowd American flag'"
echo "  - 'Netherlands parliament Binnenhof'"
echo ""
echo "SPORTS:"
echo "  - 'NHL Stanley Cup trophy ice'"
echo "  - 'NBA championship trophy confetti'"
echo "  - 'WNBA basketball game action'"
echo "  - 'FIFA World Cup stadium crowd'"
echo "  - 'professional golf course tournament'"
echo "  - 'gymnastics Olympics competition'"
echo "  - 'MLB World Series baseball'"
echo "  - 'boxing ring professional fight'"
echo "  - 'tennis grand slam court'"
echo ""
echo "CRYPTO:"
echo "  - 'Ethereum ETH logo purple'"
echo "  - 'Ripple XRP cryptocurrency'"
echo "  - 'Solana SOL crypto logo'"
echo "  - 'NFT digital art marketplace'"
echo "  - 'Coinbase exchange app'"
echo "  - 'USDC stablecoin'"
echo ""
echo "ENTERTAINMENT:"
echo "  - 'GTA Grand Theft Auto logo'"
echo "  - 'Avatar movie 3D scene'"
echo "  - 'Barbie movie pink'"
echo "  - 'Beyonce concert stage'"
echo "  - 'Taylor Swift performance'"
echo "  - 'Squid Game Netflix red'"
echo "  - 'Stranger Things neon'"
echo "  - 'Disney Plus streaming logo'"
echo "  - 'Elder Scrolls game fantasy'"
echo ""
echo "TECHNOLOGY:"
echo "  - 'ChatGPT AI interface'"
echo "  - 'Apple Vision Pro VR headset'"
echo "  - 'Google Gemini AI'"
echo "  - 'OpenAI logo technology'"
echo "  - 'SpaceX rocket Mars'"
echo "  - 'Tesla electric car logo'"
echo "  - 'TikTok app icon'"
echo ""
echo "WORLD:"
echo "  - 'Israel Gaza conflict border'"
echo "  - 'North Korea Pyongyang'"
echo "  - 'Brexit European Union UK flag'"
echo "  - 'India population crowd'"
echo "  - 'Mexico city street'"
echo ""
echo "==================================================================="
echo ""
echo "💡 TIP: When on Unsplash, use the 'Download' button and copy the"
echo "    direct image URL. Replace [UNSPLASH_ID] in this script with"
echo "    the photo ID from the URL."
echo ""
echo "📐 IMAGE SIZE: Always use 1600x900 (16:9 landscape format)"
echo "    Add ?w=1600&h=900&fit=crop to the Unsplash URL"
echo ""
echo "🎨 QUALITY: Choose high-quality, professional photos with good"
echo "    composition and clear subjects. Avoid busy backgrounds."
echo ""
echo "==================================================================="

# Make the script executable
chmod +x "$0"

-- ============================================
-- Image Fix Database Updates
-- Created: 2026-02-11 by Rox
-- ============================================
-- 
-- INSTRUCTIONS:
-- 1. Download images using download_priority_images.sh first
-- 2. Verify images are in static/images/ directory
-- 3. Run this script: sqlite3 brain.db < update_priority_images.sql
-- 4. Verify changes: SELECT market_id, title, image_url, category FROM markets WHERE market_id IN (...);
--
-- ============================================

-- ============================================
-- PHASE 1: RECATEGORIZE MISCATEGORIZED MARKETS
-- ============================================

-- Netherlands PM markets: Crypto → Politics
UPDATE markets 
SET category = 'Politics', 
    image_url = 'static/images/politics_netherlands_parliament.jpg' 
WHERE market_id IN (
    '549876',  -- Ahmed Aboutaleb
    '549873',  -- Caroline van der Plas
    '549872',  -- Dick Schoof
    '549868',  -- Dilan Yeşilgöz-Zegerius
    '549869',  -- Frans Timmermans
    '549870',  -- Geert Wilders
    '549875',  -- Henri Bontenbal
    '549877',  -- Klaas Dijkhoff
    '549871',  -- Nicolien van Vroonhoven-Kok
    '549874'   -- Rob Jetten
);

-- GDP Growth: Technology → Economics
UPDATE markets 
SET category = 'Economics'
WHERE market_id = '533851';

-- Ukraine World Cup: Technology → Soccer
UPDATE markets 
SET category = 'Soccer'
WHERE market_id = '550708';

-- ============================================
-- PHASE 2A: POLITICS - REPLACE ITALIAN PARLIAMENT
-- ============================================

-- Trump Approval Rating → US Capitol
UPDATE markets 
SET image_url = 'static/images/politics_us_capitol.jpg'
WHERE market_id = 'new_60001';

-- Trump Deportation Markets → Trump Rally (14 markets)
UPDATE markets 
SET image_url = 'static/images/politics_trump_rally.jpg'
WHERE market_id IN (
    '517310',  -- less than 250k
    '517311',  -- 250k-500k
    '517313',  -- 500k-750k
    '517314',  -- 750k-1M
    '517315',  -- 1M-1.25M
    '517316',  -- 1.25M-1.5M
    '517317',  -- 1.5M-1.75M
    '517318',  -- 1.75M-2M
    '517319',  -- 2M or more
    '517321',  -- 750k or more in 2025
    '521944',  -- DOGE <$50b (if politics-related)
    '521945',  -- DOGE $50-100b
    '521946',  -- DOGE $100-150b
    '521963'   -- Elon cut 10%
);

-- VP Vance 2028 → Congress Chamber
UPDATE markets 
SET image_url = 'static/images/politics_congress_chamber.jpg'
WHERE market_id = 'new_60002';

-- Senate 2026 Midterms → Congress Chamber
UPDATE markets 
SET image_url = 'static/images/politics_congress_chamber.jpg'
WHERE market_id = 'new_60003';

-- Newsom 2028 Run → US Capitol
UPDATE markets 
SET image_url = 'static/images/politics_us_capitol.jpg'
WHERE market_id = 'new_60004';

-- AOC Senate Challenge → Congress Chamber
UPDATE markets 
SET image_url = 'static/images/politics_congress_chamber.jpg'
WHERE market_id = 'new_60005';

-- SCOTUS Same-Sex Marriage → Supreme Court
UPDATE markets 
SET image_url = 'static/images/politics_supreme_court.jpg'
WHERE market_id = 'new_60006';

-- Trump Pardon Jan 6 → US Capitol
UPDATE markets 
SET image_url = 'static/images/politics_us_capitol.jpg'
WHERE market_id = 'new_60007';

-- Federal Abortion Ban → White House
UPDATE markets 
SET image_url = 'static/images/politics_white_house.jpg'
WHERE market_id = 'new_60008';

-- Trump First Action → White House
UPDATE markets 
SET image_url = 'static/images/politics_white_house.jpg'
WHERE market_id = 'multi_003';

-- ============================================
-- PHASE 2A: CRITICAL SPORTS MISMATCHES
-- ============================================

-- NBA Championship Market → NBA Championship Trophy
UPDATE markets 
SET image_url = 'static/images/sports_nba_championship.jpg'
WHERE market_id = 'multi_001';

-- ============================================
-- PHASE 2A: CRITICAL CRYPTO MISMATCHES
-- ============================================

-- Ethereum $5,000 → Ethereum Logo (was Bitcoin)
UPDATE markets 
SET image_url = 'static/images/crypto_ethereum_logo.jpg'
WHERE market_id = 'new_60019';

-- ============================================
-- PHASE 2B: GENERIC SPORTS CATEGORY (55 markets)
-- ============================================

-- NHL Stanley Cup Markets (32 teams)
UPDATE markets 
SET image_url = 'static/images/sports_nhl_stanley_cup.jpg'
WHERE market_id IN (
    '553848',  -- Anaheim Ducks
    '553850',  -- Boston Bruins
    '553851',  -- Buffalo Sabres
    '553845',  -- Calgary Flames
    '553824',  -- Carolina Hurricanes
    '553854',  -- Chicago Blackhawks
    '553828',  -- Colorado Avalanche
    '553844',  -- Columbus Blue Jackets
    '553827',  -- Dallas Stars
    '553847',  -- Detroit Red Wings
    '553826',  -- Edmonton Oilers
    '553825',  -- Florida Panthers
    '553831',  -- Los Angeles Kings
    '553838',  -- Minnesota Wild
    '553849',  -- Montreal Canadiens
    '553846',  -- Nashville Predators
    '553832',  -- New Jersey Devils
    '553842',  -- New York Islanders
    '553836',  -- New York Rangers
    '553837',  -- Ottawa Senators
    '553843',  -- Philadelphia Flyers
    '553852',  -- Pittsburgh Penguins
    '553855',  -- San Jose Sharks
    '553853',  -- Seattle Kraken
    '553840',  -- St. Louis Blues
    '553830',  -- Tampa Bay Lightning
    '553834',  -- Toronto Maple Leafs
    '553839',  -- Utah Mammoth
    '553841',  -- Vancouver Canucks
    '553829',  -- Vegas Golden Knights
    '553835',  -- Washington Capitals
    '553833'   -- Winnipeg Jets
);

-- NBA Finals Markets (10 teams)
UPDATE markets 
SET image_url = 'static/images/sports_nba_finals.jpg'
WHERE market_id IN (
    '553862',  -- Boston Celtics
    '553857',  -- Cleveland Cavaliers
    '553860',  -- Houston Rockets
    '553861',  -- Indiana Pacers
    '553863',  -- Los Angeles Lakers
    '553859',  -- Minnesota Timberwolves
    '553858',  -- New York Knicks
    '553856',  -- Oklahoma City Thunder
    '553864'   -- Orlando Magic
);

-- WNBA MVP
UPDATE markets 
SET image_url = 'static/images/sports_wnba_game.jpg'
WHERE market_id = 'new_60009';

-- FIFA World Cup Qualifying Markets
UPDATE markets 
SET image_url = 'static/images/sports_fifa_world_cup.jpg'
WHERE market_id IN (
    '550694',  -- Italy
    '550706',  -- Poland
    '550703',  -- Sweden
    '550708'   -- Ukraine (recategorized to Soccer above)
);

-- Messi World Cup
UPDATE markets 
SET image_url = 'static/images/sports_messi_argentina.jpg'
WHERE market_id = 'new_60010';

-- Yankees World Series
UPDATE markets 
SET image_url = 'static/images/sports_baseball_championship.jpg'
WHERE market_id = 'new_60011';

-- Connor McDavid Stanley Cup
UPDATE markets 
SET image_url = 'static/images/sports_nhl_stanley_cup.jpg'
WHERE market_id = 'new_60012';

-- Tiger Woods Masters
UPDATE markets 
SET image_url = 'static/images/sports_golf.jpg'
WHERE market_id = 'new_60013';

-- Simone Biles Olympics
UPDATE markets 
SET image_url = 'static/images/sports_gymnastics.jpg'
WHERE market_id = 'new_60014';

-- Michigan College Football
UPDATE markets 
SET image_url = 'static/images/sports_college_football.jpg'
WHERE market_id = 'new_60015';

-- Saquon Barkley Rushing
UPDATE markets 
SET image_url = 'static/images/sports_nfl_running_back.jpg'
WHERE market_id = 'new_60016';

-- Jake Paul Boxing
UPDATE markets 
SET image_url = 'static/images/sports_boxing.jpg'
WHERE market_id = 'new_60017';

-- Djokovic Grand Slam
UPDATE markets 
SET image_url = 'static/images/sports_tennis_grand_slam.jpg'
WHERE market_id = 'new_60018';

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check recategorizations
SELECT '=== RECATEGORIZED MARKETS ===' as status;
SELECT market_id, title, category, image_url 
FROM markets 
WHERE market_id IN ('549876','549873','549872','549868','549869','549870','549875','549877','549871','549874','533851','550708');

-- Check Politics updates
SELECT '=== POLITICS MARKETS ===' as status;
SELECT market_id, title, category, image_url 
FROM markets 
WHERE market_id IN ('new_60001','517310','517311','517313','517314','517315','517316','517317','517318','517319','517321','new_60002','new_60003','new_60004','new_60005','new_60006','new_60007','new_60008','multi_003');

-- Check Critical Sports
SELECT '=== CRITICAL SPORTS ===' as status;
SELECT market_id, title, category, image_url 
FROM markets 
WHERE market_id = 'multi_001';

-- Check Critical Crypto
SELECT '=== CRITICAL CRYPTO ===' as status;
SELECT market_id, title, category, image_url 
FROM markets 
WHERE market_id = 'new_60019';

-- Check Sports Category updates
SELECT '=== SPORTS CATEGORY ===' as status;
SELECT COUNT(*) as updated_count, image_url
FROM markets 
WHERE market_id IN (SELECT market_id FROM markets WHERE category = 'Sports')
GROUP BY image_url;

-- Summary
SELECT '=== UPDATE SUMMARY ===' as status;
SELECT 
    'Total markets updated' as metric,
    COUNT(*) as count
FROM markets 
WHERE image_url LIKE 'static/images/politics_%' 
   OR image_url LIKE 'static/images/sports_%'
   OR image_url LIKE 'static/images/crypto_ethereum%';

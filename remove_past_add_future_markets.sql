-- v205: Remove past-event markets (Feb 12-17) and add upcoming sports events
-- Date: Feb 18, 2026

BEGIN TRANSACTION;

-- ============================================
-- PART 1: DELETE PAST-EVENT MARKETS (23 total)
-- ============================================

DELETE FROM markets WHERE market_id IN (
    -- Feb 12 events
    'nba-lakers-celtics-feb12',
    'nba-warriors-suns-feb12',
    'nhl-rangers-bruins-feb12',
    'ucl-psg-barcelona-feb12',
    'ucl-both-teams-score-feb12',
    
    -- Feb 13 events
    'nba-bucks-nets-feb13',
    'nba-mavs-nuggets-feb13',
    'nba-heat-sixers-feb13',
    'nhl-leafs-panthers-feb13',
    'nhl-oilers-avalanche-feb13',
    'ucl-bayern-atletico-feb13',
    
    -- Feb 14 events
    'epl-arsenal-liverpool-feb14',
    'epl-salah-hat-trick-feb14',
    'npb-giants-tigers-feb14',
    'npb-fighters-marines-feb14',
    'afl-preseason-feb14',
    
    -- Feb 15 events
    'epl-mancity-chelsea-feb15',
    'epl-united-spurs-feb15',
    'laliga-real-madrid-villarreal-feb15',
    'laliga-barcelona-athletic-feb15',
    'bundesliga-bayern-dortmund-feb15',
    'seriea-inter-milan-feb15',
    'rugby-england-ireland-feb15'
);

-- Delete related data for these markets
DELETE FROM market_tags WHERE market_id IN (
    'nba-lakers-celtics-feb12', 'nba-warriors-suns-feb12', 'nhl-rangers-bruins-feb12',
    'ucl-psg-barcelona-feb12', 'ucl-both-teams-score-feb12', 'nba-bucks-nets-feb13',
    'nba-mavs-nuggets-feb13', 'nba-heat-sixers-feb13', 'nhl-leafs-panthers-feb13',
    'nhl-oilers-avalanche-feb13', 'ucl-bayern-atletico-feb13', 'epl-arsenal-liverpool-feb14',
    'epl-salah-hat-trick-feb14', 'npb-giants-tigers-feb14', 'npb-fighters-marines-feb14',
    'afl-preseason-feb14', 'epl-mancity-chelsea-feb15', 'epl-united-spurs-feb15',
    'laliga-real-madrid-villarreal-feb15', 'laliga-barcelona-athletic-feb15',
    'bundesliga-bayern-dortmund-feb15', 'seriea-inter-milan-feb15', 'rugby-england-ireland-feb15'
);

DELETE FROM user_interactions WHERE market_id IN (
    'nba-lakers-celtics-feb12', 'nba-warriors-suns-feb12', 'nhl-rangers-bruins-feb12',
    'ucl-psg-barcelona-feb12', 'ucl-both-teams-score-feb12', 'nba-bucks-nets-feb13',
    'nba-mavs-nuggets-feb13', 'nba-heat-sixers-feb13', 'nhl-leafs-panthers-feb13',
    'nhl-oilers-avalanche-feb13', 'ucl-bayern-atletico-feb13', 'epl-arsenal-liverpool-feb14',
    'epl-salah-hat-trick-feb14', 'npb-giants-tigers-feb14', 'npb-fighters-marines-feb14',
    'afl-preseason-feb14', 'epl-mancity-chelsea-feb15', 'epl-united-spurs-feb15',
    'laliga-real-madrid-villarreal-feb15', 'laliga-barcelona-athletic-feb15',
    'bundesliga-bayern-dortmund-feb15', 'seriea-inter-milan-feb15', 'rugby-england-ireland-feb15'
);

DELETE FROM trending_cache WHERE market_id IN (
    'nba-lakers-celtics-feb12', 'nba-warriors-suns-feb12', 'nhl-rangers-bruins-feb12',
    'ucl-psg-barcelona-feb12', 'ucl-both-teams-score-feb12', 'nba-bucks-nets-feb13',
    'nba-mavs-nuggets-feb13', 'nba-heat-sixers-feb13', 'nhl-leafs-panthers-feb13',
    'nhl-oilers-avalanche-feb13', 'ucl-bayern-atletico-feb13', 'epl-arsenal-liverpool-feb14',
    'epl-salah-hat-trick-feb14', 'npb-giants-tigers-feb14', 'npb-fighters-marines-feb14',
    'afl-preseason-feb14', 'epl-mancity-chelsea-feb15', 'epl-united-spurs-feb15',
    'laliga-real-madrid-villarreal-feb15', 'laliga-barcelona-athletic-feb15',
    'bundesliga-bayern-dortmund-feb15', 'seriea-inter-milan-feb15', 'rugby-england-ireland-feb15'
);

DELETE FROM user_market_impressions WHERE market_id IN (
    'nba-lakers-celtics-feb12', 'nba-warriors-suns-feb12', 'nhl-rangers-bruins-feb12',
    'ucl-psg-barcelona-feb12', 'ucl-both-teams-score-feb12', 'nba-bucks-nets-feb13',
    'nba-mavs-nuggets-feb13', 'nba-heat-sixers-feb13', 'nhl-leafs-panthers-feb13',
    'nhl-oilers-avalanche-feb13', 'ucl-bayern-atletico-feb13', 'epl-arsenal-liverpool-feb14',
    'epl-salah-hat-trick-feb14', 'npb-giants-tigers-feb14', 'npb-fighters-marines-feb14',
    'afl-preseason-feb14', 'epl-mancity-chelsea-feb15', 'epl-united-spurs-feb15',
    'laliga-real-madrid-villarreal-feb15', 'laliga-barcelona-athletic-feb15',
    'bundesliga-bayern-dortmund-feb15', 'seriea-inter-milan-feb15', 'rugby-england-ireland-feb15'
);

-- ============================================
-- PART 2: ADD NEW UPCOMING SPORTS MARKETS (20 total)
-- ============================================

-- NBA Games (Feb 19-21) - 4 markets
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('nba-lakers-warriors-feb19', 'Will Lakers defeat Warriors on Feb 19?', 'LeBron James and the Lakers face Steph Curry''s Warriors in a classic Western Conference showdown. Both teams fighting for playoff positioning.', 'Sports', 'binary', 0.58, 127000, 34000, 189, '2026-02-20 08:00:00', '2026-02-18 09:00:00', '/static/images/nba-lakers-warriors.jpg', NULL, 'en'),

('nba-celtics-bucks-feb20', 'Will Celtics beat Bucks by 10+ points?', 'Jayson Tatum and the defending champion Celtics host Giannis and the Bucks. Can Boston dominate at home?', 'Sports', 'binary', 0.51, 142000, 38000, 203, '2026-02-21 08:00:00', '2026-02-18 09:00:00', '/static/images/nba-celtics-bucks.jpg', NULL, 'en'),

('nba-nuggets-suns-feb21', 'Will Nuggets-Suns game go over 230 total points?', 'Jokic''s Nuggets face Kevin Durant''s Suns in a high-scoring offensive battle. Will both teams light up the scoreboard?', 'Sports', 'binary', 0.64, 118000, 31000, 176, '2026-02-22 08:00:00', '2026-02-18 09:00:00', '/static/images/nba-nuggets-suns.jpg', NULL, 'en'),

('nba-embiid-50pts-feb20', 'Will Joel Embiid score 50+ points vs Knicks?', 'Embiid has been on fire this season. Can he drop 50 points at Madison Square Garden against the Knicks?', 'Sports', 'binary', 0.29, 93000, 27000, 152, '2026-02-21 08:00:00', '2026-02-18 09:00:00', '/static/images/nba-embiid-knicks.jpg', NULL, 'en');

-- NHL Games (Feb 19-21) - 3 markets
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('nhl-leafs-bruins-feb19', 'Will Maple Leafs defeat Bruins on Feb 19?', 'Original Six rivalry renewed as Toronto visits Boston. Leafs looking to avenge playoff losses from previous seasons.', 'Sports', 'binary', 0.46, 108000, 29000, 167, '2026-02-20 08:00:00', '2026-02-18 09:00:00', '/static/images/nhl-leafs-bruins.jpg', NULL, 'en'),

('nhl-oilers-flames-feb20', 'Will Battle of Alberta have 8+ total goals?', 'McDavid vs Flames in hockey''s fiercest rivalry. Will this high-octane matchup produce a goal-fest?', 'Sports', 'binary', 0.71, 121000, 33000, 182, '2026-02-21 08:00:00', '2026-02-18 09:00:00', '/static/images/nhl-oilers-flames.jpg', NULL, 'en'),

('nhl-rangers-islanders-feb21', 'Will Rangers shut out Islanders on Feb 21?', 'New York rivalry on ice. Rangers goaltender Shesterkin has been dominant – can he blank the Islanders?', 'Sports', 'binary', 0.18, 97000, 26000, 148, '2026-02-22 08:00:00', '2026-02-18 09:00:00', '/static/images/nhl-rangers-islanders.jpg', NULL, 'en');

-- Champions League (Feb 19-20) - 3 markets
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('ucl-bayern-arsenal-feb19', 'Will Bayern Munich defeat Arsenal on Feb 19?', 'Champions League Round of 16 clash at Allianz Arena. Can Arsenal pull off an upset in Munich?', 'Sports', 'binary', 0.69, 186000, 49000, 247, '2026-02-20 05:00:00', '2026-02-18 09:00:00', '/static/images/ucl-bayern-arsenal.jpg', NULL, 'en'),

('ucl-psg-sociedad-feb20', 'Will PSG advance to Quarter-Finals?', 'PSG faces Real Sociedad in knockout round. With Mbappe leading the attack, can PSG secure their spot?', 'Sports', 'binary', 0.78, 173000, 46000, 229, '2026-02-21 05:00:00', '2026-02-18 09:00:00', '/static/images/ucl-psg-sociedad.jpg', NULL, 'en'),

('ucl-both-teams-score-feb19', 'Will both teams score in Bayern vs Arsenal?', 'High-powered offenses clash in Munich. Will we see goals from both sides in this Round of 16 thriller?', 'Sports', 'binary', 0.73, 134000, 37000, 195, '2026-02-20 05:00:00', '2026-02-18 09:00:00', '/static/images/ucl-both-teams-score.jpg', NULL, 'en');

-- Premier League (Feb 22-23) - 3 markets
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('epl-arsenal-mancity-feb22', 'Will Arsenal defeat Man City on Feb 22?', 'Title race showdown at Emirates Stadium. Arsenal needs a win to keep pace with City for the Premier League crown.', 'Sports', 'binary', 0.44, 198000, 52000, 261, '2026-02-23 05:00:00', '2026-02-18 09:00:00', '/static/images/epl-arsenal-mancity.jpg', NULL, 'en'),

('epl-liverpool-chelsea-feb23', 'Will Liverpool vs Chelsea end in draw?', 'Two historic clubs meet at Anfield. Both teams evenly matched – will they split the points?', 'Sports', 'binary', 0.37, 156000, 41000, 217, '2026-02-24 05:00:00', '2026-02-18 09:00:00', '/static/images/epl-liverpool-chelsea.jpg', NULL, 'en'),

('epl-salah-2goals-feb23', 'Will Mohamed Salah score 2+ goals vs Chelsea?', 'Salah loves scoring against Chelsea. Will Egypt''s King deliver another match-winning performance?', 'Sports', 'binary', 0.34, 111000, 30000, 169, '2026-02-24 05:00:00', '2026-02-18 09:00:00', '/static/images/epl-salah-chelsea.jpg', NULL, 'en');

-- La Liga (Feb 22-23) - 2 markets
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('laliga-madrid-derby-feb22', 'Will Real Madrid beat Atletico in Derby?', 'Madrid Derby at Santiago Bernabeu. Real Madrid looks to extend their lead at the top of La Liga.', 'Sports', 'binary', 0.62, 181000, 47000, 239, '2026-02-23 05:00:00', '2026-02-18 09:00:00', '/static/images/laliga-madrid-derby.jpg', NULL, 'en'),

('laliga-barcelona-sevilla-feb23', 'Will Barcelona win vs Sevilla by 3+ goals?', 'Barcelona hosts struggling Sevilla at Camp Nou. Can the Catalans deliver a dominant performance?', 'Sports', 'binary', 0.49, 143000, 38000, 196, '2026-02-24 05:00:00', '2026-02-18 09:00:00', '/static/images/laliga-barcelona-sevilla.jpg', NULL, 'en');

-- Bundesliga (Feb 22) - 1 market
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('bundesliga-bayern-leipzig-feb22', 'Will Bayern Munich defeat RB Leipzig?', 'Top of the table clash in the Bundesliga. Bayern faces their closest title challenger at home.', 'Sports', 'binary', 0.67, 164000, 43000, 219, '2026-02-23 05:00:00', '2026-02-18 09:00:00', '/static/images/bundesliga-bayern-leipzig.jpg', NULL, 'en');

-- Serie A (Feb 23) - 2 markets
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('seriea-juventus-napoli-feb23', 'Will Juventus beat Napoli on Feb 23?', 'Italian giants collide in Turin. Juventus seeks revenge after Napoli''s dominant Serie A campaign last season.', 'Sports', 'binary', 0.53, 147000, 39000, 201, '2026-02-24 05:00:00', '2026-02-18 09:00:00', '/static/images/seriea-juventus-napoli.jpg', NULL, 'en'),

('seriea-inter-roma-feb23', 'Will Inter Milan vs Roma have 4+ goals?', 'Inter faces Roma in a clash of attacking styles. Will this fixture produce a goal-fest at San Siro?', 'Sports', 'binary', 0.59, 129000, 35000, 183, '2026-02-24 05:00:00', '2026-02-18 09:00:00', '/static/images/seriea-inter-roma.jpg', NULL, 'en');

-- Rugby Six Nations (Feb 22) - 1 market
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('rugby-france-scotland-feb22', 'Will France defeat Scotland in Six Nations?', 'France hosts Scotland at Stade de France in crucial Six Nations clash. Can Les Bleus maintain their championship push?', 'Sports', 'binary', 0.72, 103000, 28000, 159, '2026-02-23 05:00:00', '2026-02-18 09:00:00', '/static/images/rugby-france-scotland.jpg', NULL, 'en');

-- NFL Combine (Feb 20-23) - 1 market
INSERT INTO markets (market_id, title, description, category, market_type, probability, volume_total, volume_24h, participant_count, resolution_date, created_at, image_url, editorial_description, language)
VALUES
('nfl-combine-record-feb23', 'Will 40-yard dash record be broken at NFL Combine?', 'NFL Scouting Combine features the fastest college prospects. Will anyone beat John Ross''s 4.22-second record?', 'Sports', 'binary', 0.23, 87000, 24000, 141, '2026-02-24 05:00:00', '2026-02-18 09:00:00', '/static/images/nfl-combine-record.jpg', NULL, 'en');

-- ============================================
-- PART 3: ADD TAGS FOR NEW MARKETS
-- ============================================

-- NBA markets tags
INSERT INTO market_tags (market_id, tag) VALUES
('nba-lakers-warriors-feb19', 'NBA'),
('nba-lakers-warriors-feb19', 'Basketball'),
('nba-lakers-warriors-feb19', 'Lakers'),
('nba-lakers-warriors-feb19', 'Warriors'),
('nba-celtics-bucks-feb20', 'NBA'),
('nba-celtics-bucks-feb20', 'Basketball'),
('nba-celtics-bucks-feb20', 'Celtics'),
('nba-celtics-bucks-feb20', 'Bucks'),
('nba-nuggets-suns-feb21', 'NBA'),
('nba-nuggets-suns-feb21', 'Basketball'),
('nba-nuggets-suns-feb21', 'Nuggets'),
('nba-nuggets-suns-feb21', 'Suns'),
('nba-nuggets-suns-feb21', 'Over-Under'),
('nba-embiid-50pts-feb20', 'NBA'),
('nba-embiid-50pts-feb20', 'Basketball'),
('nba-embiid-50pts-feb20', '76ers'),
('nba-embiid-50pts-feb20', 'Knicks'),
('nba-embiid-50pts-feb20', 'Player-Props');

-- NHL markets tags
INSERT INTO market_tags (market_id, tag) VALUES
('nhl-leafs-bruins-feb19', 'NHL'),
('nhl-leafs-bruins-feb19', 'Hockey'),
('nhl-leafs-bruins-feb19', 'Maple-Leafs'),
('nhl-leafs-bruins-feb19', 'Bruins'),
('nhl-oilers-flames-feb20', 'NHL'),
('nhl-oilers-flames-feb20', 'Hockey'),
('nhl-oilers-flames-feb20', 'Oilers'),
('nhl-oilers-flames-feb20', 'Flames'),
('nhl-oilers-flames-feb20', 'Over-Under'),
('nhl-rangers-islanders-feb21', 'NHL'),
('nhl-rangers-islanders-feb21', 'Hockey'),
('nhl-rangers-islanders-feb21', 'Rangers'),
('nhl-rangers-islanders-feb21', 'Islanders');

-- Champions League tags
INSERT INTO market_tags (market_id, tag) VALUES
('ucl-bayern-arsenal-feb19', 'UCL'),
('ucl-bayern-arsenal-feb19', 'Champions-League'),
('ucl-bayern-arsenal-feb19', 'Bayern'),
('ucl-bayern-arsenal-feb19', 'Arsenal'),
('ucl-psg-sociedad-feb20', 'UCL'),
('ucl-psg-sociedad-feb20', 'Champions-League'),
('ucl-psg-sociedad-feb20', 'PSG'),
('ucl-psg-sociedad-feb20', 'Real-Sociedad'),
('ucl-both-teams-score-feb19', 'UCL'),
('ucl-both-teams-score-feb19', 'Champions-League'),
('ucl-both-teams-score-feb19', 'Bayern'),
('ucl-both-teams-score-feb19', 'Arsenal'),
('ucl-both-teams-score-feb19', 'BTTS');

-- Premier League tags
INSERT INTO market_tags (market_id, tag) VALUES
('epl-arsenal-mancity-feb22', 'EPL'),
('epl-arsenal-mancity-feb22', 'Premier-League'),
('epl-arsenal-mancity-feb22', 'Arsenal'),
('epl-arsenal-mancity-feb22', 'Man-City'),
('epl-liverpool-chelsea-feb23', 'EPL'),
('epl-liverpool-chelsea-feb23', 'Premier-League'),
('epl-liverpool-chelsea-feb23', 'Liverpool'),
('epl-liverpool-chelsea-feb23', 'Chelsea'),
('epl-salah-2goals-feb23', 'EPL'),
('epl-salah-2goals-feb23', 'Premier-League'),
('epl-salah-2goals-feb23', 'Liverpool'),
('epl-salah-2goals-feb23', 'Player-Props'),
('epl-salah-2goals-feb23', 'Salah');

-- La Liga tags
INSERT INTO market_tags (market_id, tag) VALUES
('laliga-madrid-derby-feb22', 'La-Liga'),
('laliga-madrid-derby-feb22', 'Real-Madrid'),
('laliga-madrid-derby-feb22', 'Atletico-Madrid'),
('laliga-madrid-derby-feb22', 'Derby'),
('laliga-barcelona-sevilla-feb23', 'La-Liga'),
('laliga-barcelona-sevilla-feb23', 'Barcelona'),
('laliga-barcelona-sevilla-feb23', 'Sevilla');

-- Bundesliga tags
INSERT INTO market_tags (market_id, tag) VALUES
('bundesliga-bayern-leipzig-feb22', 'Bundesliga'),
('bundesliga-bayern-leipzig-feb22', 'Bayern-Munich'),
('bundesliga-bayern-leipzig-feb22', 'RB-Leipzig');

-- Serie A tags
INSERT INTO market_tags (market_id, tag) VALUES
('seriea-juventus-napoli-feb23', 'Serie-A'),
('seriea-juventus-napoli-feb23', 'Juventus'),
('seriea-juventus-napoli-feb23', 'Napoli'),
('seriea-inter-roma-feb23', 'Serie-A'),
('seriea-inter-roma-feb23', 'Inter-Milan'),
('seriea-inter-roma-feb23', 'Roma'),
('seriea-inter-roma-feb23', 'Over-Under');

-- Rugby tags
INSERT INTO market_tags (market_id, tag) VALUES
('rugby-france-scotland-feb22', 'Rugby'),
('rugby-france-scotland-feb22', 'Six-Nations'),
('rugby-france-scotland-feb22', 'France'),
('rugby-france-scotland-feb22', 'Scotland');

-- NFL Combine tags
INSERT INTO market_tags (market_id, tag) VALUES
('nfl-combine-record-feb23', 'NFL'),
('nfl-combine-record-feb23', 'Combine'),
('nfl-combine-record-feb23', 'Track-Speed');

COMMIT;

-- Verification queries
SELECT '=== DELETION RESULTS ===';
SELECT 'Markets deleted:', (SELECT COUNT(*) FROM markets WHERE market_id IN ('nba-lakers-celtics-feb12', 'nba-warriors-suns-feb12', 'nhl-rangers-bruins-feb12', 'ucl-psg-barcelona-feb12'));

SELECT '=== NEW MARKETS ADDED ===';
SELECT 'New markets:', COUNT(*) FROM markets WHERE market_id LIKE '%-feb19%' OR market_id LIKE '%-feb20%' OR market_id LIKE '%-feb21%' OR market_id LIKE '%-feb22%' OR market_id LIKE '%-feb23%';

SELECT '=== TOTAL SPORTS MARKETS ===';
SELECT 'Total Sports markets:', COUNT(*) FROM markets WHERE category = 'Sports';

SELECT '=== SAMPLE NEW MARKETS ===';
SELECT market_id, title, probability, volume_total, participant_count FROM markets WHERE created_at >= '2026-02-18 09:00:00' LIMIT 5;

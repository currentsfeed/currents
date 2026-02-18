-- Phase 1: Update 12 markets with new unique images
-- Politics (10 markets)
UPDATE markets SET image_url = '/static/images/politics_517310.jpg' WHERE market_id = '517310';
UPDATE markets SET image_url = '/static/images/politics_517314.jpg' WHERE market_id = '517314';
UPDATE markets SET image_url = '/static/images/politics_517316.jpg' WHERE market_id = '517316';
UPDATE markets SET image_url = '/static/images/politics_517318.jpg' WHERE market_id = '517318';
UPDATE markets SET image_url = '/static/images/politics_517319.jpg' WHERE market_id = '517319';
UPDATE markets SET image_url = '/static/images/politics_517321.jpg' WHERE market_id = '517321';
UPDATE markets SET image_url = '/static/images/politics_new_60001.jpg' WHERE market_id = 'new_60001';
UPDATE markets SET image_url = '/static/images/politics_new_60002.jpg' WHERE market_id = 'new_60002';
UPDATE markets SET image_url = '/static/images/politics_new_60003.jpg' WHERE market_id = 'new_60003';
UPDATE markets SET image_url = '/static/images/politics_new_60005.jpg' WHERE market_id = 'new_60005';

-- Baseball (2 markets)
UPDATE markets SET image_url = '/static/images/sports_npb-fighters-marines-feb14.jpg' WHERE market_id = 'npb-fighters-marines-feb14';
UPDATE markets SET image_url = '/static/images/sports_npb-giants-tigers-feb14.jpg' WHERE market_id = 'npb-giants-tigers-feb14';

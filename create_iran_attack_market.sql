-- Create Iran Military Attack Market (Israel trending topic)
-- Created 2 days ago with historical data

-- Main market entry
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'us-iran-military-attack-feb19-2026',
    'Will the US launch a military attack on Iran on February 19th?',
    'Tensions in the Middle East have escalated following recent developments. Speculation about potential US military action against Iranian targets has intensified across intelligence circles and major news outlets.',
    'World',
    'en',
    0.09,
    18000,
    78000,
    234,
    '/static/images/israel_iran_47841881.jpg',
    'open',
    datetime('now', '-2 days'),
    '2026-02-19 23:59:59',
    0,
    'binary',
    'Breaking: Regional tensions spike as diplomatic channels show signs of breakdown. Military analysts monitoring situation closely.'
);

-- Tags
INSERT INTO market_tags (market_id, tag) VALUES
    ('us-iran-military-attack-feb19-2026', 'World'),
    ('us-iran-military-attack-feb19-2026', 'Middle East'),
    ('us-iran-military-attack-feb19-2026', 'Iran'),
    ('us-iran-military-attack-feb19-2026', 'United States'),
    ('us-iran-military-attack-feb19-2026', 'Military'),
    ('us-iran-military-attack-feb19-2026', 'Breaking News');

-- Probability history (2 days ago to now)
-- Starting at 12%, dropping to 9% as diplomatic efforts continue
INSERT INTO market_probability_history (market_id, probability, recorded_at) VALUES
    ('us-iran-military-attack-feb19-2026', 0.12, datetime('now', '-2 days')),
    ('us-iran-military-attack-feb19-2026', 0.11, datetime('now', '-1 days', '-12 hours')),
    ('us-iran-military-attack-feb19-2026', 0.10, datetime('now', '-1 days')),
    ('us-iran-military-attack-feb19-2026', 0.09, datetime('now', '-12 hours')),
    ('us-iran-military-attack-feb19-2026', 0.09, datetime('now', '-6 hours')),
    ('us-iran-military-attack-feb19-2026', 0.09, datetime('now'));

-- Generate fake activity (interactions)
INSERT INTO interactions (user_id, market_id, event_type, timestamp) VALUES
    ('user1', 'us-iran-military-attack-feb19-2026', 'view', datetime('now', '-2 days', '+1 hour')),
    ('user2', 'us-iran-military-attack-feb19-2026', 'trade', datetime('now', '-2 days', '+3 hours')),
    ('user3', 'us-iran-military-attack-feb19-2026', 'view', datetime('now', '-2 days', '+5 hours')),
    ('user4', 'us-iran-military-attack-feb19-2026', 'trade', datetime('now', '-1 days', '+2 hours')),
    ('user1', 'us-iran-military-attack-feb19-2026', 'trade', datetime('now', '-1 days', '+6 hours')),
    ('user2', 'us-iran-military-attack-feb19-2026', 'view', datetime('now', '-1 days', '+10 hours')),
    ('user3', 'us-iran-military-attack-feb19-2026', 'trade', datetime('now', '-12 hours')),
    ('user4', 'us-iran-military-attack-feb19-2026', 'view', datetime('now', '-8 hours')),
    ('user1', 'us-iran-military-attack-feb19-2026', 'trade', datetime('now', '-4 hours')),
    ('user2', 'us-iran-military-attack-feb19-2026', 'trade', datetime('now', '-2 hours')),
    ('user3', 'us-iran-military-attack-feb19-2026', 'view', datetime('now', '-1 hours'));

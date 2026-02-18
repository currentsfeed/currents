-- Create Joni Token Market
-- Created 7 days ago with historical data

-- Main market entry
INSERT INTO markets (
    market_id,
    title,
    description,
    category,
    language,
    probability,
    volume_24h,
    volume_total,
    participant_count,
    image_url,
    status,
    created_at,
    resolution_date,
    resolved,
    market_type,
    editorial_description
) VALUES (
    'joni-token-april-2026',
    'Will Joni release a crypto token by April 1st?',
    'This new Elinnovation project spawned just 1 week ago is making headlines and likely to be the next killer workplace AI skills one-stop shop. So there''s one question.',
    'Crypto',
    'en',
    0.72,
    45000,
    223000,
    342,
    '/static/images/joni-token-market.jpg',
    'open',
    datetime('now', '-7 days'),
    '2026-04-01 23:59:59',
    0,
    'multiple_choice',
    'Joni, the purple octopus mascot of the Elinnovation workplace AI platform, has captured attention in the tech world. With rapid adoption and buzz building, speculation has mounted about a potential token launch.'
);

-- Market outcomes (72% Yes, 26% No, 2% Two tokens)
INSERT INTO market_options (option_id, market_id, option_text, probability, position) VALUES
    ('joni-token-april-2026-yes', 'joni-token-april-2026', 'Yes', 0.72, 0),
    ('joni-token-april-2026-no', 'joni-token-april-2026', 'No', 0.26, 1),
    ('joni-token-april-2026-two', 'joni-token-april-2026', 'Two tokens', 0.02, 2);

-- Market tags
INSERT INTO market_tags (market_id, tag) VALUES
    ('joni-token-april-2026', 'Crypto'),
    ('joni-token-april-2026', 'Cryptocurrency'),
    ('joni-token-april-2026', 'Tokens'),
    ('joni-token-april-2026', 'Elinnovation'),
    ('joni-token-april-2026', 'Joni'),
    ('joni-token-april-2026', 'AI Platform'),
    ('joni-token-april-2026', 'Workplace AI');

-- Probability history (7 days ago to now)
-- Starting at 58%, gradually rising to 72%
INSERT INTO market_probability_history (market_id, probability, recorded_at) VALUES
    ('joni-token-april-2026', 0.58, datetime('now', '-7 days')),
    ('joni-token-april-2026', 0.61, datetime('now', '-6 days')),
    ('joni-token-april-2026', 0.63, datetime('now', '-5 days')),
    ('joni-token-april-2026', 0.67, datetime('now', '-4 days')),
    ('joni-token-april-2026', 0.69, datetime('now', '-3 days')),
    ('joni-token-april-2026', 0.71, datetime('now', '-2 days')),
    ('joni-token-april-2026', 0.72, datetime('now', '-1 days')),
    ('joni-token-april-2026', 0.72, datetime('now'));

-- Generate fake activity (interactions)
INSERT INTO interactions (user_id, market_id, event_type, timestamp) VALUES
    ('user1', 'joni-token-april-2026', 'trade', datetime('now', '-7 days', '+2 hours')),
    ('user2', 'joni-token-april-2026', 'trade', datetime('now', '-7 days', '+4 hours')),
    ('user3', 'joni-token-april-2026', 'view', datetime('now', '-7 days', '+6 hours')),
    ('user4', 'joni-token-april-2026', 'trade', datetime('now', '-6 days', '+1 hour')),
    ('user1', 'joni-token-april-2026', 'trade', datetime('now', '-6 days', '+3 hours')),
    ('user2', 'joni-token-april-2026', 'trade', datetime('now', '-6 days', '+8 hours')),
    ('user3', 'joni-token-april-2026', 'view', datetime('now', '-5 days', '+2 hours')),
    ('user4', 'joni-token-april-2026', 'trade', datetime('now', '-5 days', '+5 hours')),
    ('user1', 'joni-token-april-2026', 'trade', datetime('now', '-4 days', '+1 hour')),
    ('user2', 'joni-token-april-2026', 'trade', datetime('now', '-4 days', '+4 hours')),
    ('user3', 'joni-token-april-2026', 'view', datetime('now', '-4 days', '+7 hours')),
    ('user4', 'joni-token-april-2026', 'trade', datetime('now', '-3 days', '+2 hours')),
    ('user1', 'joni-token-april-2026', 'trade', datetime('now', '-3 days', '+6 hours')),
    ('user2', 'joni-token-april-2026', 'view', datetime('now', '-2 days', '+3 hours')),
    ('user3', 'joni-token-april-2026', 'trade', datetime('now', '-2 days', '+8 hours')),
    ('user4', 'joni-token-april-2026', 'trade', datetime('now', '-1 days', '+1 hour')),
    ('user1', 'joni-token-april-2026', 'trade', datetime('now', '-1 days', '+5 hours')),
    ('user2', 'joni-token-april-2026', 'view', datetime('now', '-12 hours')),
    ('user3', 'joni-token-april-2026', 'trade', datetime('now', '-6 hours')),
    ('user4', 'joni-token-april-2026', 'trade', datetime('now', '-2 hours'));

-- Create Yaniv market (hidden, accessible only via URL parameter)
-- Date: Feb 18, 2026

BEGIN TRANSACTION;

-- Insert market
INSERT INTO markets (
    market_id, 
    title, 
    description, 
    category, 
    market_type, 
    probability, 
    volume_total, 
    volume_24h, 
    participant_count, 
    resolution_date, 
    created_at, 
    image_url, 
    editorial_description, 
    language
) VALUES (
    'yaniv-rain-march-2026',
    'Will Yaniv join Rain?',
    'There have lately been talks with the professional and only time will tell the intentions from both sides. Industry insiders are watching closely as negotiations continue.',
    'Business',
    'binary',
    0.40,
    156000,
    41000,
    217,
    '2026-03-15 23:59:59',
    '2026-02-13 10:00:00',
    '/static/images/yaniv-rain-market.jpg',
    'Rain team in recruitment talks with industry veteran',
    'en'
);

-- Add tags
INSERT INTO market_tags (market_id, tag) VALUES
('yaniv-rain-march-2026', 'Business'),
('yaniv-rain-march-2026', 'Recruitment'),
('yaniv-rain-march-2026', 'Rain'),
('yaniv-rain-march-2026', 'Hiring');

-- Add 5 days of probability history (Feb 13-17)
INSERT INTO probability_history (market_id, timestamp, probability) VALUES
('yaniv-rain-march-2026', '2026-02-13 10:00:00', 0.38),
('yaniv-rain-march-2026', '2026-02-13 22:00:00', 0.39),
('yaniv-rain-march-2026', '2026-02-14 10:00:00', 0.37),
('yaniv-rain-march-2026', '2026-02-14 22:00:00', 0.41),
('yaniv-rain-march-2026', '2026-02-15 10:00:00', 0.42),
('yaniv-rain-march-2026', '2026-02-15 22:00:00', 0.39),
('yaniv-rain-march-2026', '2026-02-16 10:00:00', 0.40),
('yaniv-rain-march-2026', '2026-02-16 22:00:00', 0.41),
('yaniv-rain-march-2026', '2026-02-17 10:00:00', 0.39),
('yaniv-rain-march-2026', '2026-02-17 22:00:00', 0.40),
('yaniv-rain-march-2026', '2026-02-18 08:00:00', 0.40);

COMMIT;

-- Verification
SELECT 'Market created:', market_id, title, probability, created_at FROM markets WHERE market_id = 'yaniv-rain-march-2026';

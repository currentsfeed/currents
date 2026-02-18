-- Create 10 Japanese Markets (Japan-only geo-restriction)
-- Markets created 5 days ago with historical data

-- Market 1: Nikkei reaching new high
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-nikkei-40000-2026',
    '日経平均は2026年中に40,000円を突破するか？',
    '日本株式市場は好調を続けており、日経平均株価が史上最高値を更新する可能性が議論されています。',
    'Economics',
    'ja',
    0.68,
    12000,
    45000,
    89,
    '/static/images/japan-nikkei-stocks.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    '日本経済の回復と円安効果により、株式市場は上昇トレンドを維持しています。'
);

-- Market 2: Shohei Ohtani MVP
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-ohtani-mvp-2026',
    '大谷翔平は2026年シーズンでMVPを獲得するか？',
    'ドジャースでの活躍が期待される大谷翔平選手。今シーズンもMVP候補となるのか？',
    'Sports',
    'ja',
    0.42,
    8000,
    28000,
    67,
    '/static/images/japan-baseball-stadium.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-11-01 23:59:59',
    0,
    'binary',
    '二刀流での活躍が続く大谷選手に、今年も注目が集まっています。'
);

-- Market 3: Tokyo Olympics legacy
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-osaka-expo-success-2026',
    '大阪・関西万博は入場者目標を達成するか？',
    '2025年の万博を終え、その経済効果と成功について議論が続いています。',
    'Culture',
    'ja',
    0.55,
    15000,
    52000,
    103,
    '/static/images/japan-osaka-expo.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-06-30 23:59:59',
    0,
    'binary',
    '万博の経済効果と文化的影響について、専門家の意見が分かれています。'
);

-- Market 4: Yen exchange rate
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-yen-150-2026',
    '2026年末までに米ドル円相場は150円を超えるか？',
    '円安トレンドが続く中、為替市場の動向に注目が集まっています。',
    'Economics',
    'ja',
    0.71,
    18000,
    63000,
    124,
    '/static/images/economics_537484.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    '日銀の金融政策と米国の利上げ動向が為替相場を左右します。'
);

-- Market 5: J-League attendance
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-jleague-attendance-2026',
    'Jリーグの2026年平均観客動員数は2万人を超えるか？',
    '日本のサッカーリーグの人気回復について予測が分かれています。',
    'Sports',
    'ja',
    0.48,
    9000,
    31000,
    72,
    '/static/images/soccer_stadium_1.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-15 23:59:59',
    0,
    'binary',
    'ワールドカップ効果とスター選手の活躍が鍵となります。'
);

-- Market 6: Sony PlayStation 6
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-playstation6-announce-2026',
    'ソニーは2026年中にPlayStation 6を発表するか？',
    '次世代ゲーム機の発表時期について、業界内で憶測が飛び交っています。',
    'Technology',
    'ja',
    0.23,
    11000,
    38000,
    81,
    '/static/images/gaming-elder-scrolls.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    'PS5の販売が好調を維持する中、次世代機の開発が進んでいます。'
);

-- Market 7: Anime industry growth
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-anime-market-growth-2026',
    '日本のアニメ産業市場規模は2026年に3兆円を突破するか？',
    '世界的なアニメブームにより、日本のアニメ産業が急成長しています。',
    'Entertainment',
    'ja',
    0.64,
    13000,
    47000,
    95,
    '/static/images/japan-anime-exports.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    '海外市場での人気上昇が、産業全体の成長を牽引しています。'
);

-- Market 8: Sumo wrestler yokozuna
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-sumo-yokozuna-2026',
    '2026年中に新しい横綱が誕生するか？',
    '大相撲で長年空位となっている横綱位への昇進が期待されています。',
    'Sports',
    'ja',
    0.51,
    7000,
    24000,
    58,
    '/static/images/japan-sumo.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    '複数の大関が横綱昇進の条件を満たす可能性があります。'
);

-- Market 9: Semiconductor factory
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-tsmc-kumamoto-2026',
    'TSMCの熊本第2工場は2026年内に着工するか？',
    '半導体産業の復活を目指す日本にとって、TSMCの投資が重要な鍵となっています。',
    'Technology',
    'ja',
    0.73,
    16000,
    58000,
    112,
    '/static/images/japan-semiconductor.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    '政府の支援策により、半導体製造の国内回帰が進んでいます。'
);

-- Market 10: Mount Fuji eruption
INSERT INTO markets (
    market_id, title, description, category, language, probability,
    volume_24h, volume_total, participant_count, image_url, status,
    created_at, resolution_date, resolved, market_type, editorial_description
) VALUES (
    'japan-fuji-eruption-warning-2026',
    '2026年中に富士山の噴火警戒レベルが引き上げられるか？',
    '専門家による火山活動の観測が続けられており、防災意識が高まっています。',
    'World',
    'ja',
    0.18,
    14000,
    49000,
    98,
    '/static/images/japan-fukushima-water.jpg',
    'open',
    datetime('now', '-5 days'),
    '2026-12-31 23:59:59',
    0,
    'binary',
    '地震活動の増加により、富士山の火山活動への関心が高まっています。'
);

-- Add tags for all Japanese markets
INSERT INTO market_tags (market_id, tag) VALUES
    ('japan-nikkei-40000-2026', 'Japan'),
    ('japan-nikkei-40000-2026', 'Economics'),
    ('japan-nikkei-40000-2026', 'Stock Market'),
    ('japan-ohtani-mvp-2026', 'Japan'),
    ('japan-ohtani-mvp-2026', 'Sports'),
    ('japan-ohtani-mvp-2026', 'Baseball'),
    ('japan-ohtani-mvp-2026', 'Shohei Ohtani'),
    ('japan-osaka-expo-success-2026', 'Japan'),
    ('japan-osaka-expo-success-2026', 'Culture'),
    ('japan-osaka-expo-success-2026', 'Osaka'),
    ('japan-yen-150-2026', 'Japan'),
    ('japan-yen-150-2026', 'Economics'),
    ('japan-yen-150-2026', 'Currency'),
    ('japan-jleague-attendance-2026', 'Japan'),
    ('japan-jleague-attendance-2026', 'Sports'),
    ('japan-jleague-attendance-2026', 'Soccer'),
    ('japan-playstation6-announce-2026', 'Japan'),
    ('japan-playstation6-announce-2026', 'Technology'),
    ('japan-playstation6-announce-2026', 'Gaming'),
    ('japan-playstation6-announce-2026', 'Sony'),
    ('japan-anime-market-growth-2026', 'Japan'),
    ('japan-anime-market-growth-2026', 'Entertainment'),
    ('japan-anime-market-growth-2026', 'Anime'),
    ('japan-sumo-yokozuna-2026', 'Japan'),
    ('japan-sumo-yokozuna-2026', 'Sports'),
    ('japan-sumo-yokozuna-2026', 'Sumo'),
    ('japan-tsmc-kumamoto-2026', 'Japan'),
    ('japan-tsmc-kumamoto-2026', 'Technology'),
    ('japan-tsmc-kumamoto-2026', 'Semiconductors'),
    ('japan-tsmc-kumamoto-2026', 'TSMC'),
    ('japan-fuji-eruption-warning-2026', 'Japan'),
    ('japan-fuji-eruption-warning-2026', 'World'),
    ('japan-fuji-eruption-warning-2026', 'Natural Disaster');

-- Add probability history for all markets (5 days)
INSERT INTO market_probability_history (market_id, probability, recorded_at) VALUES
    ('japan-nikkei-40000-2026', 0.61, datetime('now', '-5 days')),
    ('japan-nikkei-40000-2026', 0.64, datetime('now', '-4 days')),
    ('japan-nikkei-40000-2026', 0.66, datetime('now', '-3 days')),
    ('japan-nikkei-40000-2026', 0.67, datetime('now', '-2 days')),
    ('japan-nikkei-40000-2026', 0.68, datetime('now', '-1 days')),
    
    ('japan-ohtani-mvp-2026', 0.38, datetime('now', '-5 days')),
    ('japan-ohtani-mvp-2026', 0.40, datetime('now', '-4 days')),
    ('japan-ohtani-mvp-2026', 0.41, datetime('now', '-3 days')),
    ('japan-ohtani-mvp-2026', 0.42, datetime('now', '-2 days')),
    ('japan-ohtani-mvp-2026', 0.42, datetime('now', '-1 days')),
    
    ('japan-osaka-expo-success-2026', 0.51, datetime('now', '-5 days')),
    ('japan-osaka-expo-success-2026', 0.53, datetime('now', '-4 days')),
    ('japan-osaka-expo-success-2026', 0.54, datetime('now', '-3 days')),
    ('japan-osaka-expo-success-2026', 0.55, datetime('now', '-2 days')),
    ('japan-osaka-expo-success-2026', 0.55, datetime('now', '-1 days')),
    
    ('japan-yen-150-2026', 0.67, datetime('now', '-5 days')),
    ('japan-yen-150-2026', 0.69, datetime('now', '-4 days')),
    ('japan-yen-150-2026', 0.70, datetime('now', '-3 days')),
    ('japan-yen-150-2026', 0.71, datetime('now', '-2 days')),
    ('japan-yen-150-2026', 0.71, datetime('now', '-1 days')),
    
    ('japan-jleague-attendance-2026', 0.44, datetime('now', '-5 days')),
    ('japan-jleague-attendance-2026', 0.46, datetime('now', '-4 days')),
    ('japan-jleague-attendance-2026', 0.47, datetime('now', '-3 days')),
    ('japan-jleague-attendance-2026', 0.48, datetime('now', '-2 days')),
    ('japan-jleague-attendance-2026', 0.48, datetime('now', '-1 days')),
    
    ('japan-playstation6-announce-2026', 0.19, datetime('now', '-5 days')),
    ('japan-playstation6-announce-2026', 0.21, datetime('now', '-4 days')),
    ('japan-playstation6-announce-2026', 0.22, datetime('now', '-3 days')),
    ('japan-playstation6-announce-2026', 0.23, datetime('now', '-2 days')),
    ('japan-playstation6-announce-2026', 0.23, datetime('now', '-1 days')),
    
    ('japan-anime-market-growth-2026', 0.59, datetime('now', '-5 days')),
    ('japan-anime-market-growth-2026', 0.61, datetime('now', '-4 days')),
    ('japan-anime-market-growth-2026', 0.63, datetime('now', '-3 days')),
    ('japan-anime-market-growth-2026', 0.64, datetime('now', '-2 days')),
    ('japan-anime-market-growth-2026', 0.64, datetime('now', '-1 days')),
    
    ('japan-sumo-yokozuna-2026', 0.47, datetime('now', '-5 days')),
    ('japan-sumo-yokozuna-2026', 0.49, datetime('now', '-4 days')),
    ('japan-sumo-yokozuna-2026', 0.50, datetime('now', '-3 days')),
    ('japan-sumo-yokozuna-2026', 0.51, datetime('now', '-2 days')),
    ('japan-sumo-yokozuna-2026', 0.51, datetime('now', '-1 days')),
    
    ('japan-tsmc-kumamoto-2026', 0.68, datetime('now', '-5 days')),
    ('japan-tsmc-kumamoto-2026', 0.70, datetime('now', '-4 days')),
    ('japan-tsmc-kumamoto-2026', 0.72, datetime('now', '-3 days')),
    ('japan-tsmc-kumamoto-2026', 0.73, datetime('now', '-2 days')),
    ('japan-tsmc-kumamoto-2026', 0.73, datetime('now', '-1 days')),
    
    ('japan-fuji-eruption-warning-2026', 0.14, datetime('now', '-5 days')),
    ('japan-fuji-eruption-warning-2026', 0.16, datetime('now', '-4 days')),
    ('japan-fuji-eruption-warning-2026', 0.17, datetime('now', '-3 days')),
    ('japan-fuji-eruption-warning-2026', 0.18, datetime('now', '-2 days')),
    ('japan-fuji-eruption-warning-2026', 0.18, datetime('now', '-1 days'));

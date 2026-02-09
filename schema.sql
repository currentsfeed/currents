-- BRain Local Database Schema
-- SQLite database for Currents prediction market intelligence layer

-- Markets table
CREATE TABLE IF NOT EXISTS markets (
    market_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    language TEXT DEFAULT 'en',
    probability REAL NOT NULL,
    volume_24h REAL DEFAULT 0,
    volume_total REAL DEFAULT 0,
    participant_count INTEGER DEFAULT 0,
    image_url TEXT,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_date TIMESTAMP,
    resolved BOOLEAN DEFAULT 0,
    outcome TEXT
);

-- Market tags (many-to-many)
CREATE TABLE IF NOT EXISTS market_tags (
    market_id TEXT,
    tag TEXT,
    PRIMARY KEY (market_id, tag),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

-- Market taxonomy (hierarchical categories)
CREATE TABLE IF NOT EXISTS market_taxonomy (
    market_id TEXT,
    taxonomy_path TEXT, -- e.g., "Politics/Middle East/Iran"
    PRIMARY KEY (market_id, taxonomy_path),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

-- Probability history snapshots
CREATE TABLE IF NOT EXISTS probability_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    probability REAL NOT NULL,
    volume REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

-- Users (for personalization)
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    anon_id TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User interactions (tracking)
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    market_id TEXT,
    event_type TEXT, -- 'view', 'click', 'trade', 'follow'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT, -- JSON blob for extra data
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

-- User taste profiles (learned preferences)
CREATE TABLE IF NOT EXISTS user_taste (
    user_id TEXT,
    dimension_type TEXT, -- 'tag', 'category', 'taxonomy'
    dimension_value TEXT,
    weight REAL DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, dimension_type, dimension_value),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Trending cache (pre-computed scores)
CREATE TABLE IF NOT EXISTS trending_cache (
    market_id TEXT,
    scope TEXT, -- 'global', 'US', 'Israel', etc.
    score REAL,
    rank INTEGER,
    window TEXT DEFAULT '24h', -- '1h', '24h', '7d'
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (market_id, scope, window)
);

-- Seen snapshots (for resurfacing logic)
CREATE TABLE IF NOT EXISTS user_seen (
    user_id TEXT,
    market_id TEXT,
    last_seen_at TIMESTAMP,
    last_probability REAL,
    last_volume REAL,
    view_count INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, market_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_markets_status ON markets(status);
CREATE INDEX IF NOT EXISTS idx_markets_category ON markets(category);
CREATE INDEX IF NOT EXISTS idx_interactions_user ON interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_interactions_market ON interactions(market_id);
CREATE INDEX IF NOT EXISTS idx_interactions_timestamp ON interactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_trending_scope ON trending_cache(scope, rank);
CREATE INDEX IF NOT EXISTS idx_probability_history_market ON probability_history(market_id);

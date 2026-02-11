-- Rain Database Schema
-- Markets data separated from BRain personalization

CREATE TABLE markets (
    market_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    editorial_description TEXT,
    category TEXT,
    language TEXT DEFAULT 'en',
    probability REAL NOT NULL,
    volume_24h REAL DEFAULT 0,
    volume_total REAL DEFAULT 0,
    participant_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_date TIMESTAMP,
    resolved BOOLEAN DEFAULT 0,
    outcome TEXT,
    market_type TEXT DEFAULT 'binary'
);

CREATE TABLE market_options (
    option_id TEXT PRIMARY KEY,
    market_id TEXT NOT NULL,
    option_text TEXT NOT NULL,
    probability REAL NOT NULL DEFAULT 0,
    position INTEGER DEFAULT 0,
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

CREATE TABLE market_tags (
    market_id TEXT,
    tag TEXT,
    PRIMARY KEY (market_id, tag),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

CREATE TABLE market_taxonomy (
    market_id TEXT,
    taxonomy_path TEXT,
    PRIMARY KEY (market_id, taxonomy_path),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

CREATE TABLE probability_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    probability REAL NOT NULL,
    volume REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);

-- Indexes for performance
CREATE INDEX idx_markets_status ON markets(status);
CREATE INDEX idx_markets_category ON markets(category);
CREATE INDEX idx_markets_created ON markets(created_at DESC);
CREATE INDEX idx_options_market ON market_options(market_id);
CREATE INDEX idx_options_market_prob ON market_options(market_id, probability DESC);
CREATE INDEX idx_tags_market ON market_tags(market_id);
CREATE INDEX idx_tags_tag ON market_tags(tag);
CREATE INDEX idx_prob_history_market ON probability_history(market_id, timestamp DESC);

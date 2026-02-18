CREATE TABLE markets (
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
, market_type TEXT DEFAULT 'binary', editorial_description TEXT, article_text TEXT, article_source TEXT, article_fetched_at TIMESTAMP);
CREATE TABLE market_tags (
    market_id TEXT,
    tag TEXT,
    PRIMARY KEY (market_id, tag),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);
CREATE TABLE market_taxonomy (
    market_id TEXT,
    taxonomy_path TEXT, -- e.g., "Politics/Middle East/Iran"
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
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    anon_id TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    market_id TEXT,
    event_type TEXT, -- 'view', 'click', 'trade', 'follow'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT, -- JSON blob for extra data
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);
CREATE TABLE user_taste (
    user_id TEXT,
    dimension_type TEXT, -- 'tag', 'category', 'taxonomy'
    dimension_value TEXT,
    weight REAL DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, dimension_type, dimension_value),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE trending_cache (
    market_id TEXT,
    scope TEXT, -- 'global', 'US', 'Israel', etc.
    score REAL,
    rank INTEGER,
    window TEXT DEFAULT '24h', -- '1h', '24h', '7d'
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (market_id, scope, window)
);
CREATE TABLE user_seen (
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
CREATE INDEX idx_markets_status ON markets(status);
CREATE INDEX idx_markets_category ON markets(category);
CREATE INDEX idx_interactions_user ON interactions(user_id);
CREATE INDEX idx_interactions_market ON interactions(market_id);
CREATE INDEX idx_interactions_timestamp ON interactions(timestamp);
CREATE INDEX idx_trending_scope ON trending_cache(scope, rank);
CREATE INDEX idx_probability_history_market ON probability_history(market_id);
CREATE TABLE market_options (
    option_id TEXT PRIMARY KEY,
    market_id TEXT NOT NULL,
    option_text TEXT NOT NULL,
    probability REAL NOT NULL DEFAULT 0,
    position INTEGER DEFAULT 0,
    FOREIGN KEY (market_id) REFERENCES markets(market_id)
);
CREATE INDEX idx_options_market ON market_options(market_id);
CREATE INDEX idx_markets_volume ON markets(volume_24h DESC);
CREATE INDEX idx_markets_type ON markets(market_type);
CREATE INDEX idx_markets_category_status ON markets(category, status);
CREATE INDEX idx_markets_status_volume ON markets(status, volume_24h DESC);
CREATE INDEX idx_probability_history_timestamp ON probability_history(timestamp DESC);
CREATE INDEX idx_probability_history_market_time ON probability_history(market_id, timestamp DESC);
CREATE INDEX idx_market_tags_tag ON market_tags(tag);
CREATE INDEX idx_options_market_prob ON market_options(market_id, probability DESC);
CREATE TABLE user_interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT NOT NULL,
            market_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            dwell_ms INTEGER,
            section TEXT,
            position INTEGER,
            geo_country TEXT,
            metadata TEXT
        );
CREATE INDEX idx_interactions_ts ON user_interactions(ts);
CREATE TABLE user_profiles (
            user_key TEXT PRIMARY KEY,
            display_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_interactions INTEGER DEFAULT 0,
            interests TEXT,
            negatives TEXT,
            seen_markets TEXT
        );
CREATE TABLE user_topic_scores (
            user_key TEXT NOT NULL,
            topic_type TEXT NOT NULL,
            topic_value TEXT NOT NULL,
            score REAL DEFAULT 0.0,
            raw_score REAL DEFAULT 0.0,
            interactions INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_decay TIMESTAMP,
            PRIMARY KEY (user_key, topic_type, topic_value)
        );
CREATE INDEX idx_topic_scores_user ON user_topic_scores(user_key);
CREATE INDEX idx_topic_scores_score ON user_topic_scores(score DESC);
CREATE TABLE seen_snapshots (
            user_key TEXT NOT NULL,
            market_id TEXT NOT NULL,
            last_seen_ts TIMESTAMP NOT NULL,
            belief_at_view REAL,
            volume_at_view REAL,
            status_at_view TEXT,
            updated_at TIMESTAMP,
            PRIMARY KEY (user_key, market_id)
        );
CREATE INDEX idx_seen_user ON seen_snapshots(user_key);
CREATE TABLE tag_cooccurrence (
            tag_a TEXT NOT NULL,
            tag_b TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (tag_a, tag_b)
        );
CREATE INDEX idx_cooccur_a ON tag_cooccurrence(tag_a);
CREATE INDEX idx_cooccur_b ON tag_cooccurrence(tag_b);
CREATE TABLE score_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT NOT NULL,
            topic_type TEXT NOT NULL,
            topic_value TEXT NOT NULL,
            score REAL NOT NULL,
            snapshot_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
CREATE INDEX idx_history_user_topic ON score_history(user_key, topic_type, topic_value);
CREATE TABLE user_market_impressions (
    user_key TEXT NOT NULL,
    market_id TEXT NOT NULL,
    impressions_24h INTEGER NOT NULL DEFAULT 0,
    impressions_7d INTEGER NOT NULL DEFAULT 0,
    last_shown_at TIMESTAMP NULL,
    last_clicked_at TIMESTAMP NULL,
    last_traded_at TIMESTAMP NULL,
    last_hidden_at TIMESTAMP NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_key, market_id)
);
CREATE INDEX idx_impressions_last_shown 
    ON user_market_impressions(user_key, last_shown_at);
CREATE TABLE market_velocity_rollups (
    market_id TEXT NOT NULL,
    geo_bucket TEXT NOT NULL,  -- 'GLOBAL' or 'IL', 'US', etc.
    views_5m INTEGER NOT NULL DEFAULT 0,
    views_1h INTEGER NOT NULL DEFAULT 0,
    views_24h INTEGER NOT NULL DEFAULT 0,
    trades_5m INTEGER NOT NULL DEFAULT 0,
    trades_1h INTEGER NOT NULL DEFAULT 0,
    trades_24h INTEGER NOT NULL DEFAULT 0,
    volume_5m REAL NULL,
    volume_1h REAL NULL,
    volume_24h REAL NULL,
    odds_change_1h REAL NOT NULL DEFAULT 0.0,  -- absolute probability delta 0..1
    odds_change_24h REAL NOT NULL DEFAULT 0.0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (market_id, geo_bucket)
);
CREATE INDEX idx_velocity_geo_views 
    ON market_velocity_rollups(geo_bucket, views_1h DESC);
CREATE INDEX idx_velocity_geo_trades 
    ON market_velocity_rollups(geo_bucket, trades_1h DESC);
CREATE TABLE user_session_state (
    user_key TEXT NOT NULL,
    session_id TEXT NOT NULL,
    tag_weights TEXT NOT NULL,      -- JSON: {"NBA":0.8,"Trump":0.3}
    category_weights TEXT NOT NULL,  -- JSON: {"Sports":0.6}
    last_event_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_key)
);
CREATE INDEX idx_session_expires 
    ON user_session_state(expires_at);
CREATE TABLE market_probability_history (
    market_id TEXT NOT NULL,
    probability REAL NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_probability_history 
    ON market_probability_history(market_id, recorded_at DESC);
CREATE TABLE IF NOT EXISTS "waitlist_submissions_old" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    belief_choice TEXT NOT NULL CHECK(belief_choice IN ('YES', 'NO')),
    timestamp_submitted DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'currents_launch_waitlist',
    device_type TEXT,
    locale TEXT,
    resolved_correct INTEGER,
    is_test_submission INTEGER DEFAULT 0,
    user_agent TEXT,
    ip_address TEXT
);
CREATE TABLE waitlist_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    belief_choice TEXT NOT NULL CHECK(belief_choice IN ('YES', 'NO', 'MARCH', 'APRIL', 'MAY', 'LATER')),
    timestamp_submitted DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'currents_launch_waitlist',
    device_type TEXT,
    locale TEXT,
    resolved_correct INTEGER,
    is_test_submission INTEGER DEFAULT 0,
    user_agent TEXT,
    ip_address TEXT
);
CREATE INDEX idx_email ON waitlist_submissions(email);
CREATE INDEX idx_test ON waitlist_submissions(is_test_submission);

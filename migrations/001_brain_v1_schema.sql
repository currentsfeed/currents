-- BRain v1 Schema Migration
-- Date: 2026-02-15
-- Purpose: Add impression tracking, velocity rollups, and session state

-- 1. user_market_impressions
-- Tracks frequency + cooldown, allows "re-show if changed"
CREATE TABLE IF NOT EXISTS user_market_impressions (
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

CREATE INDEX IF NOT EXISTS idx_impressions_last_shown 
    ON user_market_impressions(user_key, last_shown_at);

-- 2. market_velocity_rollups
-- Rolling activity stats for trending + "changed" logic
CREATE TABLE IF NOT EXISTS market_velocity_rollups (
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

CREATE INDEX IF NOT EXISTS idx_velocity_geo_views 
    ON market_velocity_rollups(geo_bucket, views_1h DESC);
CREATE INDEX IF NOT EXISTS idx_velocity_geo_trades 
    ON market_velocity_rollups(geo_bucket, trades_1h DESC);

-- 3. user_session_state
-- Short-term "intent" with fast decay
CREATE TABLE IF NOT EXISTS user_session_state (
    user_key TEXT NOT NULL,
    session_id TEXT NOT NULL,
    tag_weights TEXT NOT NULL,      -- JSON: {"NBA":0.8,"Trump":0.3}
    category_weights TEXT NOT NULL,  -- JSON: {"Sports":0.6}
    last_event_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_key)
);

CREATE INDEX IF NOT EXISTS idx_session_expires 
    ON user_session_state(expires_at);

-- 4. market_probability_history (for odds_change computation)
CREATE TABLE IF NOT EXISTS market_probability_history (
    market_id TEXT NOT NULL,
    probability REAL NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_probability_history 
    ON market_probability_history(market_id, recorded_at DESC);

-- 5. Add missing columns to markets if needed
-- (These may already exist, so use ALTER TABLE ... ADD COLUMN IF NOT EXISTS syntax)
-- SQLite doesn't support IF NOT EXISTS for ALTER, so we'll handle this in Python

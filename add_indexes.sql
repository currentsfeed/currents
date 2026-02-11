-- Performance indexes for Currents BRain database
-- Run with: sqlite3 brain.db < add_indexes.sql

-- Markets table indexes
CREATE INDEX IF NOT EXISTS idx_markets_volume ON markets(volume_24h DESC);
CREATE INDEX IF NOT EXISTS idx_markets_type ON markets(market_type);
CREATE INDEX IF NOT EXISTS idx_markets_category_status ON markets(category, status);
CREATE INDEX IF NOT EXISTS idx_markets_status_volume ON markets(status, volume_24h DESC);

-- Probability history indexes
CREATE INDEX IF NOT EXISTS idx_probability_history_timestamp ON probability_history(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_probability_history_market_time ON probability_history(market_id, timestamp DESC);

-- Market tags indexes
CREATE INDEX IF NOT EXISTS idx_market_tags_tag ON market_tags(tag);

-- Options indexes
CREATE INDEX IF NOT EXISTS idx_options_market_prob ON market_options(market_id, probability DESC);

-- Show results
SELECT 'Indexes created successfully!' as status;
SELECT name as index_name, tbl_name as table_name 
FROM sqlite_master 
WHERE type='index' AND name LIKE 'idx_%'
ORDER BY tbl_name, name;

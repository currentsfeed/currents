#!/usr/bin/env python3
"""
Create BRain tracking tables
Run this to initialize the behavioral learning system
"""
import sqlite3
from datetime import datetime

DB_PATH = 'brain.db'

def create_tables():
    """Create all tracking and profile tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🗄️  Creating tracking tables...")
    
    # 1. User interactions (event log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_interactions (
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
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_user ON user_interactions(user_key, ts)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_market ON user_interactions(market_id, ts)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_ts ON user_interactions(ts)")
    
    print("✅ user_interactions table created")
    
    # 2. User profiles (aggregated state)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_key TEXT PRIMARY KEY,
            display_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_interactions INTEGER DEFAULT 0,
            interests TEXT,
            negatives TEXT,
            seen_markets TEXT
        )
    """)
    
    print("✅ user_profiles table created")
    
    # 3. User topic scores (normalized view)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_topic_scores (
            user_key TEXT NOT NULL,
            topic_type TEXT NOT NULL,
            topic_value TEXT NOT NULL,
            score REAL DEFAULT 0.0,
            raw_score REAL DEFAULT 0.0,
            interactions INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_decay TIMESTAMP,
            PRIMARY KEY (user_key, topic_type, topic_value)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_scores_user ON user_topic_scores(user_key)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_scores_score ON user_topic_scores(score DESC)")
    
    print("✅ user_topic_scores table created")
    
    # 4. Seen snapshots (resurfacing logic)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_snapshots (
            user_key TEXT NOT NULL,
            market_id TEXT NOT NULL,
            last_seen_ts TIMESTAMP NOT NULL,
            belief_at_view REAL,
            volume_at_view REAL,
            status_at_view TEXT,
            updated_at TIMESTAMP,
            PRIMARY KEY (user_key, market_id)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_seen_user ON seen_snapshots(user_key)")
    
    print("✅ seen_snapshots table created")
    
    # 5. Co-occurrence tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tag_cooccurrence (
            tag_a TEXT NOT NULL,
            tag_b TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (tag_a, tag_b)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cooccur_a ON tag_cooccurrence(tag_a)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cooccur_b ON tag_cooccurrence(tag_b)")
    
    print("✅ tag_cooccurrence table created")
    
    # 6. Score history (evolution timeline)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS score_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT NOT NULL,
            topic_type TEXT NOT NULL,
            topic_value TEXT NOT NULL,
            score REAL NOT NULL,
            snapshot_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_user_topic ON score_history(user_key, topic_type, topic_value)")
    
    print("✅ score_history table created")
    
    conn.commit()
    conn.close()
    
    print("\n✨ All tracking tables created successfully!")
    print("\n📊 Database schema:")
    print("  - user_interactions: Event log (views, clicks, bets, shares)")
    print("  - user_profiles: Aggregated user state")
    print("  - user_topic_scores: Category/tag/language affinity scores")
    print("  - seen_snapshots: Resurfacing logic (5% belief change threshold)")
    print("  - tag_cooccurrence: Which tags users engage with together")
    print("  - score_history: Score evolution over time")

if __name__ == '__main__':
    create_tables()

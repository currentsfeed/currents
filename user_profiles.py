"""
User Profile Management for BRain
Tracks user preferences, scoring, and interaction history
"""
import sqlite3
import json
from datetime import datetime
from collections import defaultdict

DB_PATH = 'brain.db'

def init_user_profiles():
    """Initialize user profile tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            display_name TEXT,
            created_at TEXT,
            last_active TEXT,
            profile_data TEXT
        )
    """)
    
    # User topic scores (categories, tags, etc.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_topic_scores (
            user_id TEXT,
            topic_type TEXT,
            topic_value TEXT,
            score REAL,
            interactions INTEGER DEFAULT 0,
            last_updated TEXT,
            PRIMARY KEY (user_id, topic_type, topic_value)
        )
    """)
    
    # User interaction history (for building scores)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            market_id TEXT,
            interaction_type TEXT,
            timestamp TEXT,
            metadata TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def create_test_users():
    """Create test user profiles with sample scoring"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    test_users = [
        {
            'user_id': 'user_001',
            'display_name': 'Politics Junkie',
            'topics': {
                'categories': {'Politics': 0.95, 'Economics': 0.60, 'Crime': 0.40},
                'tags': {'trump': 0.90, 'biden': 0.75, 'election': 0.85, 'deportation': 0.70},
                'preferences': {'volume': 'high', 'contestedness': 'high'}
            }
        },
        {
            'user_id': 'user_002',
            'display_name': 'Crypto Trader',
            'topics': {
                'categories': {'Crypto': 0.95, 'Technology': 0.80, 'Economics': 0.70},
                'tags': {'ai': 0.85, 'gaming': 0.60, 'revenue': 0.75, 'budget': 0.50},
                'preferences': {'volume': 'high', 'contestedness': 'medium'}
            }
        },
        {
            'user_id': 'user_003',
            'display_name': 'Sports Fan',
            'topics': {
                'categories': {'Sports': 0.90, 'Entertainment': 0.65, 'Technology': 0.30},
                'tags': {'basketball': 0.85, 'gaming': 0.70},
                'preferences': {'volume': 'medium', 'contestedness': 'high'}
            }
        },
        {
            'user_id': 'user_004',
            'display_name': 'Tech Enthusiast',
            'topics': {
                'categories': {'Technology': 0.95, 'Crypto': 0.70, 'Economics': 0.50},
                'tags': {'ai': 0.95, 'gaming': 0.80, 'revenue': 0.60},
                'preferences': {'volume': 'medium', 'contestedness': 'medium'}
            }
        },
        {
            'user_id': 'user_005',
            'display_name': 'Balanced Investor',
            'topics': {
                'categories': {'Economics': 0.80, 'Politics': 0.70, 'Crypto': 0.60, 'Technology': 0.65},
                'tags': {'trump': 0.55, 'ai': 0.70, 'budget': 0.80, 'revenue': 0.75},
                'preferences': {'volume': 'high', 'contestedness': 'low'}
            }
        },
        {
            'user_id': 'user_006',
            'display_name': 'Pop Culture Watcher',
            'topics': {
                'categories': {'Entertainment': 0.95, 'Sports': 0.60, 'Culture': 0.80},
                'tags': {'gaming': 0.75, 'rihanna': 0.85},
                'preferences': {'volume': 'low', 'contestedness': 'medium'}
            }
        }
    ]
    
    now = datetime.now().isoformat()
    
    for user in test_users:
        # Insert user profile
        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles
            (user_id, display_name, created_at, last_active, profile_data)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user['user_id'],
            user['display_name'],
            now,
            now,
            json.dumps(user['topics'])
        ))
        
        # Insert category scores
        for category, score in user['topics']['categories'].items():
            cursor.execute("""
                INSERT OR REPLACE INTO user_topic_scores
                (user_id, topic_type, topic_value, score, interactions, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user['user_id'], 'category', category, score, 0, now))
        
        # Insert tag scores
        for tag, score in user['topics']['tags'].items():
            cursor.execute("""
                INSERT OR REPLACE INTO user_topic_scores
                (user_id, topic_type, topic_value, score, interactions, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user['user_id'], 'tag', tag, score, 0, now))
        
        # Insert preference scores
        for pref, value in user['topics']['preferences'].items():
            # Convert preference to numeric score
            if pref == 'volume':
                score = {'low': 0.3, 'medium': 0.5, 'high': 0.9}.get(value, 0.5)
            elif pref == 'contestedness':
                score = {'low': 0.3, 'medium': 0.5, 'high': 0.9}.get(value, 0.5)
            else:
                score = 0.5
            
            cursor.execute("""
                INSERT OR REPLACE INTO user_topic_scores
                (user_id, topic_type, topic_value, score, interactions, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user['user_id'], 'preference', pref, score, 0, now))
    
    conn.commit()
    conn.close()
    
    return len(test_users)

def get_all_users():
    """Get list of all users"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT user_id, display_name, created_at, last_active
        FROM user_profiles
        ORDER BY last_active DESC
    """)
    
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

def get_user_profile(user_id):
    """Get detailed profile for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get basic profile
    cursor.execute("""
        SELECT * FROM user_profiles WHERE user_id = ?
    """, (user_id,))
    
    profile = dict(cursor.fetchone())
    
    # Get topic scores grouped by type
    cursor.execute("""
        SELECT topic_type, topic_value, score, interactions, last_updated
        FROM user_topic_scores
        WHERE user_id = ?
        ORDER BY topic_type, score DESC
    """, (user_id,))
    
    scores = defaultdict(list)
    for row in cursor.fetchall():
        scores[row['topic_type']].append({
            'topic': row['topic_value'],
            'score': row['score'],
            'interactions': row['interactions'],
            'last_updated': row['last_updated']
        })
    
    profile['scores'] = dict(scores)
    
    # Get recent interactions
    cursor.execute("""
        SELECT i.*, m.title as market_title
        FROM user_interactions i
        LEFT JOIN markets m ON i.market_id = m.market_id
        WHERE i.user_id = ?
        ORDER BY i.timestamp DESC
        LIMIT 20
    """, (user_id,))
    
    profile['recent_interactions'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return profile

def update_user_score(user_id, topic_type, topic_value, delta=0.1):
    """Update a user's score for a topic"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    # Get current score
    cursor.execute("""
        SELECT score, interactions FROM user_topic_scores
        WHERE user_id = ? AND topic_type = ? AND topic_value = ?
    """, (user_id, topic_type, topic_value))
    
    row = cursor.fetchone()
    
    if row:
        new_score = min(1.0, row[0] + delta)
        new_interactions = row[1] + 1
        
        cursor.execute("""
            UPDATE user_topic_scores
            SET score = ?, interactions = ?, last_updated = ?
            WHERE user_id = ? AND topic_type = ? AND topic_value = ?
        """, (new_score, new_interactions, now, user_id, topic_type, topic_value))
    else:
        cursor.execute("""
            INSERT INTO user_topic_scores
            (user_id, topic_type, topic_value, score, interactions, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, topic_type, topic_value, delta, 1, now))
    
    conn.commit()
    conn.close()

def record_interaction(user_id, market_id, interaction_type, metadata=None):
    """Record a user interaction with a market"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute("""
        INSERT INTO user_interactions
        (user_id, market_id, interaction_type, timestamp, metadata)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, market_id, interaction_type, now, json.dumps(metadata) if metadata else None))
    
    # Update last_active for user
    cursor.execute("""
        UPDATE user_profiles
        SET last_active = ?
        WHERE user_id = ?
    """, (now, user_id))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("🔧 Initializing user profiles...")
    init_user_profiles()
    print("✅ Tables created")
    
    print("👥 Creating test users...")
    count = create_test_users()
    print(f"✅ Created {count} test users")
    
    print("\n📊 Test users:")
    users = get_all_users()
    for user in users:
        print(f"  - {user['display_name']} ({user['user_id']})")

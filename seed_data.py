"""
Seed the BRain database with sample markets and data
"""
import sqlite3
import json
from datetime import datetime, timedelta
import random

# Sample markets
MARKETS = [
    {
        "market_id": "m_001",
        "title": "Will the US attack Iran by January 31st?",
        "description": "Resolves YES if the United States conducts a military strike against targets in Iran before January 31, 2026.",
        "category": "Politics",
        "tags": ["US", "Iran", "Military", "Conflict", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.64,
        "volume_24h": 45000,
        "volume_total": 320000,
        "participant_count": 1234,
        "image_url": "https://images.unsplash.com/photo-1526450840302-d7f96aca0e29?w=800"
    },
    {
        "market_id": "m_002",
        "title": "Will Bitcoin hit $100k by March 2026?",
        "description": "Resolves YES if Bitcoin trades at or above $100,000 USD on any major exchange before March 31, 2026.",
        "category": "Crypto",
        "tags": ["Bitcoin", "BTC", "Crypto", "Price"],
        "taxonomy": ["Finance/Cryptocurrency/Bitcoin"],
        "probability": 0.79,
        "volume_24h": 89000,
        "volume_total": 1200000,
        "participant_count": 3456,
        "image_url": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=800"
    },
    {
        "market_id": "m_003",
        "title": "Will TikTok be banned in the US by end of 2026?",
        "description": "Resolves YES if TikTok is officially banned in the United States before December 31, 2026.",
        "category": "Technology",
        "tags": ["TikTok", "US", "Tech", "Politics", "Social Media"],
        "taxonomy": ["Technology/Social Media", "Politics/US Policy"],
        "probability": 0.41,
        "volume_24h": 34000,
        "volume_total": 230000,
        "participant_count": 1890,
        "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800"
    },
    {
        "market_id": "m_004",
        "title": "Will Israel strike Iran by March 2026?",
        "description": "Resolves YES if Israel conducts a military strike against targets in Iran before March 31, 2026.",
        "category": "Politics",
        "tags": ["Israel", "Iran", "Military", "Conflict", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.58,
        "volume_24h": 38000,
        "volume_total": 280000,
        "participant_count": 1120,
        "image_url": "https://images.unsplash.com/photo-1457364887197-9150188c107b?w=800"
    },
    {
        "market_id": "m_005",
        "title": "Will SpaceX launch Starship to orbit in Q1 2026?",
        "description": "Resolves YES if SpaceX successfully launches Starship to orbit before March 31, 2026.",
        "category": "Technology",
        "tags": ["SpaceX", "Starship", "Space", "Technology", "Elon Musk"],
        "taxonomy": ["Technology/Space/Commercial"],
        "probability": 0.82,
        "volume_24h": 42000,
        "volume_total": 310000,
        "participant_count": 1678,
        "image_url": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=800"
    },
    {
        "market_id": "m_006",
        "title": "Will LeBron James score 40+ points in his next game?",
        "description": "Resolves YES if LeBron James scores 40 or more points in his next regular season or playoff game.",
        "category": "Sports",
        "tags": ["NBA", "Basketball", "LeBron", "Lakers"],
        "taxonomy": ["Sports/Basketball/NBA"],
        "probability": 0.23,
        "volume_24h": 12000,
        "volume_total": 45000,
        "participant_count": 567,
        "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800"
    },
    {
        "market_id": "m_007",
        "title": "Will the Fed cut rates in January 2025?",
        "description": "Resolves YES if the Federal Reserve announces an interest rate cut in January 2025.",
        "category": "Economics",
        "tags": ["Fed", "Interest Rates", "Economics", "US", "Monetary Policy"],
        "taxonomy": ["Finance/Economics/Monetary Policy"],
        "probability": 0.73,
        "volume_24h": 56000,
        "volume_total": 450000,
        "participant_count": 2345,
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
    },
    {
        "market_id": "m_008",
        "title": "Will Gaza conflict end by March 2026?",
        "description": "Resolves YES if a ceasefire is reached and maintained for 30+ days before March 31, 2026.",
        "category": "Politics",
        "tags": ["Gaza", "Israel", "Palestine", "Conflict", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.35,
        "volume_24h": 29000,
        "volume_total": 180000,
        "participant_count": 1050,
        "image_url": "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=800"
    }
]

def seed_database(db_path='brain.db'):
    """Populate database with sample data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🌱 Seeding BRain database...")
    
    # Insert markets
    for market in MARKETS:
        cursor.execute("""
            INSERT OR REPLACE INTO markets 
            (market_id, title, description, category, probability, volume_24h, 
             volume_total, participant_count, image_url, status, created_at, resolution_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', datetime('now', '-7 days'), datetime('now', '+30 days'))
        """, (
            market['market_id'],
            market['title'],
            market['description'],
            market['category'],
            market['probability'],
            market['volume_24h'],
            market['volume_total'],
            market['participant_count'],
            market['image_url']
        ))
        
        # Insert tags
        for tag in market['tags']:
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market['market_id'], tag))
        
        # Insert taxonomy
        for taxonomy in market['taxonomy']:
            cursor.execute("""
                INSERT OR IGNORE INTO market_taxonomy (market_id, taxonomy_path)
                VALUES (?, ?)
            """, (market['market_id'], taxonomy))
        
        # Generate probability history (last 7 days)
        base_prob = market['probability']
        for days_ago in range(7, 0, -1):
            # Random walk around base probability
            variation = random.uniform(-0.05, 0.05)
            prob = max(0.05, min(0.95, base_prob + variation))
            
            cursor.execute("""
                INSERT INTO probability_history (market_id, probability, volume, timestamp)
                VALUES (?, ?, ?, datetime('now', '-' || ? || ' days'))
            """, (market['market_id'], prob, market['volume_24h'] * random.uniform(0.5, 1.5), days_ago))
    
    # Create sample users
    sample_users = ['user_001', 'user_002', 'user_003']
    for user_id in sample_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, anon_id)
            VALUES (?, ?)
        """, (user_id, f'anon_{user_id}'))
    
    # Generate sample interactions
    for _ in range(50):
        user_id = random.choice(sample_users)
        market = random.choice(MARKETS)
        event_type = random.choice(['view', 'view', 'view', 'click', 'trade'])
        
        cursor.execute("""
            INSERT INTO interactions (user_id, market_id, event_type, timestamp)
            VALUES (?, ?, ?, datetime('now', '-' || ? || ' hours'))
        """, (user_id, market['market_id'], event_type, random.randint(1, 168)))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Seeded {len(MARKETS)} markets with tags, taxonomy, and history")
    print(f"✅ Created {len(sample_users)} sample users with 50 interactions")
    print(f"✅ Database ready at: {db_path}")

if __name__ == '__main__':
    seed_database()

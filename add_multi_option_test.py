"""
Add test multi-option markets to the database
"""
import sqlite3
import random
from datetime import datetime

DB_PATH = 'brain.db'

# Test multi-option markets
test_markets = [
    {
        'market_id': 'multi_001',
        'title': 'Who will win the 2026 NBA Championship?',
        'description': 'Multi-option market for testing: Which team will win the 2026 NBA Finals?',
        'category': 'Sports',
        'tags': ['basketball', 'nba', 'sports'],
        'image_url': 'https://picsum.photos/seed/nba2026/800/400',
        'volume_24h': 250000,
        'volume_total': 1500000,
        'participant_count': 1234,
        'options': [
            {'option_text': 'Boston Celtics', 'probability': 0.28},
            {'option_text': 'Los Angeles Lakers', 'probability': 0.22},
            {'option_text': 'Golden State Warriors', 'probability': 0.18},
            {'option_text': 'Denver Nuggets', 'probability': 0.15},
            {'option_text': 'Milwaukee Bucks', 'probability': 0.10},
            {'option_text': 'Other', 'probability': 0.07}
        ]
    },
    {
        'market_id': 'multi_002',
        'title': 'What will be the top AI company by market cap in 2027?',
        'description': 'Multi-option market for testing: Which AI company will have the highest market capitalization?',
        'category': 'Technology',
        'tags': ['ai', 'technology', 'stocks'],
        'image_url': 'https://picsum.photos/seed/ai2027/800/400',
        'volume_24h': 180000,
        'volume_total': 980000,
        'participant_count': 892,
        'options': [
            {'option_text': 'OpenAI', 'probability': 0.35},
            {'option_text': 'Google/Alphabet', 'probability': 0.25},
            {'option_text': 'Microsoft', 'probability': 0.20},
            {'option_text': 'Meta', 'probability': 0.12},
            {'option_text': 'Anthropic', 'probability': 0.05},
            {'option_text': 'Other', 'probability': 0.03}
        ]
    },
    {
        'market_id': 'multi_003',
        'title': 'What will Trump\'s first action as President be?',
        'description': 'Multi-option market for testing: What executive order or action will Trump take first?',
        'category': 'Politics',
        'tags': ['trump', 'politics', 'executive-order'],
        'image_url': 'https://picsum.photos/seed/trump2025/800/400',
        'volume_24h': 420000,
        'volume_total': 2100000,
        'participant_count': 3456,
        'options': [
            {'option_text': 'Immigration/Border action', 'probability': 0.45},
            {'option_text': 'Tariffs/Trade policy', 'probability': 0.25},
            {'option_text': 'Energy/Climate reversal', 'probability': 0.15},
            {'option_text': 'Federal spending cuts', 'probability': 0.10},
            {'option_text': 'Other', 'probability': 0.05}
        ]
    }
]

def add_multi_option_markets():
    """Add test multi-option markets"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for market in test_markets:
        print(f"Adding: {market['title']}")
        
        # Insert market
        cursor.execute("""
            INSERT OR REPLACE INTO markets 
            (market_id, title, description, category, market_type, image_url,
             volume_24h, volume_total, probability, participant_count,
             status, created_at, resolution_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            market['market_id'],
            market['title'],
            market['description'],
            market['category'],
            'multiple',  # KEY: mark as multiple
            market['image_url'],
            market['volume_24h'],
            market['volume_total'],
            market['options'][0]['probability'],  # Use leading option's probability
            market['participant_count'],
            'open',
            datetime.now().isoformat(),
            '2026-12-31T00:00:00Z'
        ))
        
        # Insert options
        for i, option in enumerate(market['options']):
            cursor.execute("""
                INSERT OR REPLACE INTO market_options
                (market_id, option_id, option_text, probability)
                VALUES (?, ?, ?, ?)
            """, (
                market['market_id'],
                f"{market['market_id']}_opt{i}",
                option['option_text'],
                option['probability']
            ))
        
        # Insert tags
        for tag in market['tags']:
            cursor.execute("""
                INSERT OR REPLACE INTO market_tags
                (market_id, tag)
                VALUES (?, ?)
            """, (market['market_id'], tag))
        
        print(f"  ✅ Added with {len(market['options'])} options")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Added {len(test_markets)} multi-option markets for testing")

if __name__ == '__main__':
    add_multi_option_markets()

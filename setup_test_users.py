#!/usr/bin/env python3
"""
Create 4 test users with distinct interest profiles for personalization testing
"""
import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'brain.db'

# Test user profiles
TEST_USERS = {
    'roy': {
        'name': 'Roy',
        'description': 'Sports & Tech enthusiast',
        'interests': {
            # Categories (0-100 scale)
            'category': {
                'Sports': 90,
                'Soccer': 85,
                'Basketball': 80,
                'Technology': 85,
                'Crypto': 70,
            },
            # Tags
            'tag': {
                'Soccer': 90,
                'NBA': 85,
                'Champions League': 80,
                'AI': 85,
                'Bitcoin': 75,
                'Ethereum': 70,
                'Artificial Intelligence': 80,
                'Machine Learning': 75,
            }
        },
        'total_interactions': 45
    },
    'user2': {
        'name': 'User 2',
        'description': 'Crypto & Politics focused',
        'interests': {
            'category': {
                'Crypto': 95,
                'Politics': 90,
                'Economics': 85,
                'Technology': 70,
            },
            'tag': {
                'Bitcoin': 95,
                'Ethereum': 90,
                'Cryptocurrency': 92,
                'Blockchain': 88,
                'US Politics': 90,
                'Elections': 85,
                'Donald Trump': 80,
                'Economy': 85,
            }
        },
        'total_interactions': 52
    },
    'user3': {
        'name': 'User 3',
        'description': 'Entertainment & Culture lover',
        'interests': {
            'category': {
                'Entertainment': 95,
                'Culture': 90,
                'Sports': 60,
                'Technology': 50,
            },
            'tag': {
                'Movies': 95,
                'Netflix': 90,
                'Disney': 88,
                'Marvel': 85,
                'Music': 92,
                'Taylor Swift': 90,
                'Awards': 85,
                'Oscars': 88,
            }
        },
        'total_interactions': 38
    },
    'user4': {
        'name': 'User 4',
        'description': 'Science & World Affairs',
        'interests': {
            'category': {
                'Technology': 85,
                'World': 90,
                'Politics': 75,
                'Economics': 80,
            },
            'tag': {
                'Climate Change': 90,
                'Space': 88,
                'SpaceX': 85,
                'Science': 92,
                'International': 85,
                'United Nations': 80,
                'Research': 88,
                'Environment': 90,
            }
        },
        'total_interactions': 41
    }
}

def setup_test_users():
    """Create or update test user profiles in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    created_count = 0
    updated_count = 0
    
    for user_key, profile in TEST_USERS.items():
        # Check if user exists
        cursor.execute("SELECT user_key FROM user_profiles WHERE user_key = ?", (user_key,))
        exists = cursor.fetchone()
        
        if exists:
            # Update existing user
            cursor.execute("""
                UPDATE user_profiles
                SET total_interactions = ?,
                    last_active = ?
                WHERE user_key = ?
            """, (profile['total_interactions'], datetime.utcnow().isoformat(), user_key))
            updated_count += 1
        else:
            # Create new user
            cursor.execute("""
                INSERT INTO user_profiles (user_key, total_interactions, created_at, last_active)
                VALUES (?, ?, ?, ?)
            """, (user_key, profile['total_interactions'], 
                  datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))
            created_count += 1
        
        # Delete old scores
        cursor.execute("DELETE FROM user_topic_scores WHERE user_key = ?", (user_key,))
        
        # Insert category scores
        for category, score in profile['interests']['category'].items():
            cursor.execute("""
                INSERT INTO user_topic_scores (user_key, topic_type, topic_value, score, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (user_key, 'category', category, score, datetime.utcnow().isoformat()))
        
        # Insert tag scores
        for tag, score in profile['interests']['tag'].items():
            cursor.execute("""
                INSERT INTO user_topic_scores (user_key, topic_type, topic_value, score, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (user_key, 'tag', tag, score, datetime.utcnow().isoformat()))
        
        print(f"✅ {profile['name']} ({user_key})")
        print(f"   {profile['description']}")
        print(f"   {len(profile['interests']['category'])} categories, {len(profile['interests']['tag'])} tags")
        print(f"   {profile['total_interactions']} interactions")
        print()
    
    conn.commit()
    conn.close()
    
    print(f"📊 Summary:")
    print(f"   Created: {created_count} users")
    print(f"   Updated: {updated_count} users")
    print(f"   Total: {len(TEST_USERS)} test users")
    print()
    print("🎯 Test users ready for personalization!")

if __name__ == '__main__':
    print("🧪 Setting up test users for personalization...")
    print()
    setup_test_users()

#!/usr/bin/env python3
"""
Reset test users to blank slates (no predetermined preferences)
Users will learn organically through their interactions
"""
import sqlite3
from datetime import datetime

DB_PATH = 'brain.db'

def reset_test_users():
    """Create blank test users with NO predetermined interests"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Test users with NO interests (blank slate)
    test_users = ['roy', 'user2', 'user3', 'user4']
    
    for user_key in test_users:
        # Check if user exists
        cursor.execute("SELECT user_key FROM user_profiles WHERE user_key = ?", (user_key,))
        exists = cursor.fetchone()
        
        if exists:
            # Update to blank slate
            cursor.execute("""
                UPDATE user_profiles
                SET total_interactions = 0,
                    last_active = ?
                WHERE user_key = ?
            """, (datetime.utcnow().isoformat(), user_key))
        else:
            # Create blank user
            cursor.execute("""
                INSERT INTO user_profiles (user_key, total_interactions, created_at, last_active)
                VALUES (?, 0, ?, ?)
            """, (user_key, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))
        
        # Delete ALL old scores (blank slate)
        cursor.execute("DELETE FROM user_topic_scores WHERE user_key = ?", (user_key,))
        cursor.execute("DELETE FROM user_interactions WHERE user_key = ?", (user_key,))
        cursor.execute("DELETE FROM seen_snapshots WHERE user_key = ?", (user_key,))
        
        print(f"✅ {user_key}: Reset to blank slate (0 interactions)")
    
    conn.commit()
    conn.close()
    
    print()
    print("🎯 All test users reset!")
    print("   Users will now learn organically through interactions")
    print("   Tag-level learning (not category-level)")
    print("   No predetermined preferences")

if __name__ == '__main__':
    print("🧹 Resetting test users to blank slates...")
    print()
    reset_test_users()

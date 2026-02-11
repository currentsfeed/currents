#!/usr/bin/env python3
"""
Deploy 150 new markets to the database
"""
import json
import sqlite3
from datetime import datetime

def load_markets_from_json(json_file, db_path='brain.db'):
    """Load markets from JSON file into database"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract markets array from the JSON structure
    markets = data.get('markets', [])
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    loaded = 0
    skipped = 0
    
    for market in markets:
        market_id = market['id']
        
        # Check if market already exists
        cursor.execute("SELECT market_id FROM markets WHERE market_id = ?", (market_id,))
        if cursor.fetchone():
            skipped += 1
            continue
        
        # Insert market
        cursor.execute("""
            INSERT INTO markets (
                market_id, title, description, category, probability, 
                volume_total, resolution_date, image_url, editorial_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            market_id,
            market['title'],
            market['description'],
            market['category'],
            market['probability'],
            market['volume'],
            market.get('resolutionDate', market.get('resolution_date')),
            market.get('image', market.get('image_url')),
            market.get('description', '')  # Use description as editorial
        ))
        
        # Insert tags
        for tag in market.get('tags', []):
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market_id, tag))
        
        # Insert probability history (currents)
        for current in market.get('currents', []):
            cursor.execute("""
                INSERT INTO probability_history (market_id, probability, timestamp)
                VALUES (?, ?, ?)
            """, (
                market_id,
                current['probability'],
                current['date']
            ))
        
        loaded += 1
    
    conn.commit()
    conn.close()
    
    return loaded, skipped

if __name__ == '__main__':
    print("🚀 Deploying new markets...")
    print()
    
    total_loaded = 0
    total_skipped = 0
    
    for batch_num in [1, 2, 3]:
        json_file = f'new_markets_batch{batch_num}.json'
        print(f"📦 Loading {json_file}...")
        
        try:
            loaded, skipped = load_markets_from_json(json_file)
            total_loaded += loaded
            total_skipped += skipped
            print(f"   ✅ Loaded: {loaded} markets")
            if skipped > 0:
                print(f"   ⏭️  Skipped: {skipped} (already exist)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print()
    print(f"📊 Deployment Summary:")
    print(f"   Total loaded: {total_loaded}")
    print(f"   Total skipped: {total_skipped}")
    print()
    
    # Verify total markets
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM markets")
    total_markets = cursor.fetchone()[0]
    conn.close()
    
    print(f"✅ Total markets in database: {total_markets}")
    print()
    print("🎯 Next steps:")
    print("   1. Restart app: ./start-ngrok.sh")
    print("   2. Compute trending: python3 compute_trending.py")
    print("   3. Test personalization at the live URL")

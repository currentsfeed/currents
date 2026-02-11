#!/usr/bin/env python3
"""
Migrate market data from brain.db to rain.db
Copies: markets, market_options, market_tags, market_taxonomy, probability_history
Keeps: user data, interactions, profiles in brain.db
"""
import sqlite3
import os

BRAIN_DB = 'brain.db'
RAIN_DB = 'rain.db'
SCHEMA_FILE = 'rain_schema.sql'

def migrate():
    """Migrate market data to Rain database"""
    
    # Create rain.db with schema
    print("Creating rain.db...")
    if os.path.exists(RAIN_DB):
        backup = f"{RAIN_DB}.backup"
        os.rename(RAIN_DB, backup)
        print(f"Backed up existing rain.db to {backup}")
    
    rain_conn = sqlite3.connect(RAIN_DB)
    with open(SCHEMA_FILE, 'r') as f:
        rain_conn.executescript(f.read())
    rain_conn.commit()
    
    # Connect to brain.db
    brain_conn = sqlite3.connect(BRAIN_DB)
    brain_conn.row_factory = sqlite3.Row
    
    # Migrate markets
    print("Migrating markets...")
    cursor = brain_conn.execute("SELECT * FROM markets")
    markets = cursor.fetchall()
    
    for market in markets:
        rain_conn.execute("""
            INSERT INTO markets (
                market_id, title, description, editorial_description, category, 
                language, probability, volume_24h, volume_total, participant_count,
                status, created_at, resolution_date, resolved, outcome, market_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            market['market_id'], market['title'], market['description'],
            market['editorial_description'] if 'editorial_description' in market.keys() else None,
            market['category'],
            market['language'] if 'language' in market.keys() else 'en',
            market['probability'],
            market['volume_24h'] if 'volume_24h' in market.keys() else 0,
            market['volume_total'] if 'volume_total' in market.keys() else 0,
            market['participant_count'] if 'participant_count' in market.keys() else 0,
            market['status'] if 'status' in market.keys() else 'open',
            market['created_at'],
            market['resolution_date'] if 'resolution_date' in market.keys() else None,
            market['resolved'] if 'resolved' in market.keys() else 0,
            market['outcome'] if 'outcome' in market.keys() else None,
            market['market_type'] if 'market_type' in market.keys() else 'binary'
        ))
    
    print(f"Migrated {len(markets)} markets")
    
    # Migrate market_options
    print("Migrating market_options...")
    cursor = brain_conn.execute("SELECT * FROM market_options")
    options = cursor.fetchall()
    
    for option in options:
        rain_conn.execute("""
            INSERT INTO market_options (option_id, market_id, option_text, probability, position)
            VALUES (?, ?, ?, ?, ?)
        """, (
            option['option_id'], option['market_id'], option['option_text'],
            option['probability'], option['position'] if 'position' in option.keys() else 0
        ))
    
    print(f"Migrated {len(options)} market options")
    
    # Migrate market_tags
    print("Migrating market_tags...")
    cursor = brain_conn.execute("SELECT * FROM market_tags")
    tags = cursor.fetchall()
    
    for tag in tags:
        rain_conn.execute("""
            INSERT INTO market_tags (market_id, tag)
            VALUES (?, ?)
        """, (tag['market_id'], tag['tag']))
    
    print(f"Migrated {len(tags)} market tags")
    
    # Migrate market_taxonomy
    print("Migrating market_taxonomy...")
    cursor = brain_conn.execute("SELECT * FROM market_taxonomy")
    taxonomies = cursor.fetchall()
    
    for taxonomy in taxonomies:
        rain_conn.execute("""
            INSERT INTO market_taxonomy (market_id, taxonomy_path)
            VALUES (?, ?)
        """, (taxonomy['market_id'], taxonomy['taxonomy_path']))
    
    print(f"Migrated {len(taxonomies)} taxonomy entries")
    
    # Migrate probability_history
    print("Migrating probability_history...")
    cursor = brain_conn.execute("SELECT * FROM probability_history")
    history = cursor.fetchall()
    
    for record in history:
        rain_conn.execute("""
            INSERT INTO probability_history (market_id, probability, volume, timestamp)
            VALUES (?, ?, ?, ?)
        """, (record['market_id'], record['probability'], 
              record['volume'] if 'volume' in record.keys() else None, record['timestamp']))
    
    print(f"Migrated {len(history)} probability history records")
    
    # Commit and close
    rain_conn.commit()
    brain_conn.close()
    rain_conn.close()
    
    print("\n✅ Migration complete!")
    print(f"Rain database created: {RAIN_DB}")
    print("Market data separated from BRain personalization data")

if __name__ == '__main__':
    migrate()

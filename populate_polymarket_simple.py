#!/usr/bin/env python3
"""
Simplified: Fetch 50 real markets from Polymarket and populate BRain database
"""
import requests
import sqlite3
import json
from datetime import datetime, timedelta
import random

DB_PATH = 'brain.db'
POLYMARKET_API = "https://gamma-api.polymarket.com/markets"

def fetch_polymarket_markets(limit=50):
    """Fetch markets from Polymarket API"""
    print(f"🌐 Fetching {limit} markets from Polymarket...")
    
    response = requests.get(f"{POLYMARKET_API}?limit={limit}")
    response.raise_for_status()
    markets = response.json()
    
    print(f"✅ Fetched {len(markets)} markets")
    return markets

def get_image_url(market_id):
    """Generate consistent image URL"""
    seed = abs(hash(market_id)) % 1000
    return f"https://picsum.photos/seed/{seed}/800/400"

def map_category(question):
    """Map question to BRain category"""
    q_lower = question.lower()
    
    if any(word in q_lower for word in ['trump', 'biden', 'election', 'president', 'congress', 'vote']):
        return 'Politics'
    elif any(word in q_lower for word in ['bitcoin', 'crypto', 'ethereum', 'btc', 'eth']):
        return 'Crypto'
    elif any(word in q_lower for word in ['nfl', 'nba', 'super bowl', 'championship', 'sport', 'football', 'basketball']):
        return 'Sports'
    elif any(word in q_lower for word in ['ai', 'technology', 'apple', 'google', 'microsoft', 'tech']):
        return 'Technology'
    elif any(word in q_lower for word in ['stock', 'economy', 'gdp', 'unemployment', 'market', 'fed']):
        return 'Economics'
    elif any(word in q_lower for word in ['movie', 'celebrity', 'oscar', 'emmy', 'music']):
        return 'Entertainment'
    else:
        return 'Markets'

def generate_probability_history(market_id):
    """Generate realistic probability history"""
    history = []
    now = datetime.now()
    start = now - timedelta(days=random.randint(7, 90))
    
    # Generate 20-40 points
    num_points = random.randint(20, 40)
    start_prob = random.uniform(0.3, 0.7)
    end_prob = random.uniform(0.3, 0.7)
    
    for i in range(num_points):
        progress = i / (num_points - 1) if num_points > 1 else 0
        prob = start_prob + (end_prob - start_prob) * progress
        prob += random.uniform(-0.08, 0.08)  # noise
        prob = max(0.05, min(0.95, prob))
        
        timestamp = start + timedelta(seconds=(now - start).total_seconds() * progress)
        volume = random.randint(1000, 50000)
        
        history.append({
            'timestamp': timestamp.isoformat(),
            'probability': round(prob, 4),
            'volume': volume
        })
    
    return history, end_prob

def clear_database():
    """Clear existing markets"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM probability_history")
    cursor.execute("DELETE FROM market_tags")
    cursor.execute("DELETE FROM market_options")
    cursor.execute("DELETE FROM markets")
    
    conn.commit()
    conn.close()
    print("🗑️  Cleared existing markets")

def populate_database(markets):
    """Populate database with Polymarket markets"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    
    for market in markets:
        try:
            # Extract basic data
            market_id = market.get('id', f"poly_{added}")
            question = market.get('question', 'Unknown Market')
            description = market.get('description', question)
            
            # Category
            category = map_category(question)
            
            # Generate volume (Polymarket sometimes has 0)
            volume_24h = float(market.get('volume24hr', 0))
            if volume_24h < 1000:
                volume_24h = random.randint(5000, 500000)
            volume_total = volume_24h * random.uniform(15, 50)
            
            # Generate probability history and current probability
            history, probability = generate_probability_history(market_id)
            
            # Other fields
            participant_count = random.randint(50, 5000)
            image_url = get_image_url(market_id)
            created_at = (datetime.now() - timedelta(days=random.randint(7, 90))).isoformat()
            resolution_date = (datetime.now() + timedelta(days=random.randint(7, 180))).isoformat()
            status = 'open'
            market_type = 'binary'
            
            # Insert market
            cursor.execute("""
                INSERT OR REPLACE INTO markets (
                    market_id, title, description, category, market_type,
                    probability, volume_24h, volume_total,
                    participant_count, image_url, status,
                    created_at, resolution_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                market_id, question[:200], description[:500], category, market_type,
                probability, volume_24h, volume_total,
                participant_count, image_url, status,
                created_at, resolution_date
            ))
            
            # Add tags
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market_id, category.lower()))
            
            # Add probability history
            for point in history:
                cursor.execute("""
                    INSERT INTO probability_history (
                        market_id, probability, volume, timestamp
                    ) VALUES (?, ?, ?, ?)
                """, (market_id, point['probability'], point['volume'], point['timestamp']))
            
            added += 1
            
            if added % 10 == 0:
                print(f"  📊 Added {added} markets...")
            
        except Exception as e:
            print(f"  ⚠️  Skipped market: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Successfully added {added} markets")
    return added

def verify_data():
    """Verify database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM markets")
    market_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM probability_history")
    history_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM markets GROUP BY category")
    categories = cursor.fetchall()
    
    conn.close()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Markets: {market_count}")
    print(f"  History points: {history_count}")
    print(f"\n📈 Markets by Category:")
    for cat, count in sorted(categories, key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    print("🌊 Populating BRain with Polymarket data\n")
    
    try:
        markets = fetch_polymarket_markets(50)
        clear_database()
        added = populate_database(markets)
        verify_data()
        
        print(f"\n✅ Done! BRain database ready for personalized learning")
        print(f"🔄 Switch to local DB mode: Set USE_RAIN_API=False in config.py")
        print(f"🚀 Then restart the app to see Polymarket markets")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

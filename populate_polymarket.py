#!/usr/bin/env python3
"""
Fetch 50 real markets from Polymarket and populate BRain database
Includes all data needed for personalized learning
"""
import requests
import sqlite3
import json
from datetime import datetime, timedelta
import random
import hashlib

DB_PATH = 'brain.db'
POLYMARKET_API = "https://gamma-api.polymarket.com/markets"

def fetch_polymarket_markets(limit=50):
    """Fetch markets from Polymarket API"""
    print(f"🌐 Fetching {limit} markets from Polymarket...")
    
    response = requests.get(f"{POLYMARKET_API}?limit={limit}&active=true")
    response.raise_for_status()
    markets = response.json()
    
    print(f"✅ Fetched {len(markets)} markets")
    return markets

def get_image_url(market_id, category):
    """Generate consistent image URL based on market"""
    seed = abs(hash(market_id)) % 1000
    return f"https://picsum.photos/seed/{seed}/800/400"

def map_category(tags):
    """Map Polymarket tags to BRain categories"""
    if not tags:
        return "Markets"
    
    tag_lower = tags[0].lower() if isinstance(tags, list) else tags.lower()
    
    category_map = {
        'politics': 'Politics',
        'election': 'Politics',
        'trump': 'Politics',
        'biden': 'Politics',
        'crypto': 'Crypto',
        'bitcoin': 'Crypto',
        'ethereum': 'Crypto',
        'sports': 'Sports',
        'nfl': 'Sports',
        'nba': 'Sports',
        'technology': 'Technology',
        'ai': 'Technology',
        'tech': 'Technology',
        'economics': 'Economics',
        'finance': 'Economics',
        'stock': 'Markets',
        'entertainment': 'Entertainment',
        'celebrity': 'Entertainment',
    }
    
    for key, cat in category_map.items():
        if key in tag_lower:
            return cat
    
    return "Markets"

def generate_probability_history(current_prob, start_date, market_id):
    """Generate realistic probability history"""
    history = []
    now = datetime.now()
    
    # Handle different date formats
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if start.tzinfo:
            start = start.replace(tzinfo=None)  # Make naive
    except:
        start = now - timedelta(days=30)  # Default to 30 days ago
    
    # Calculate number of data points (roughly every 4 hours)
    duration = (now - start).total_seconds()
    num_points = min(int(duration / (4 * 3600)), 100)  # Max 100 points
    
    if num_points < 2:
        return history
    
    # Generate smooth walk from random start to current
    start_prob = random.uniform(0.3, 0.7)
    
    for i in range(num_points):
        progress = i / (num_points - 1)
        # Smooth interpolation with noise
        prob = start_prob + (current_prob - start_prob) * progress
        prob += random.uniform(-0.05, 0.05)  # Add noise
        prob = max(0.05, min(0.95, prob))  # Clamp
        
        timestamp = start + timedelta(seconds=duration * progress)
        volume = random.randint(1000, 50000)
        
        history.append({
            'timestamp': timestamp.isoformat(),
            'probability': round(prob, 4),
            'volume': volume
        })
    
    return history

def clear_database():
    """Clear existing markets from database"""
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
    """Populate BRain database with Polymarket data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    skipped = 0
    
    for market in markets:
        try:
            # Extract data from Polymarket format
            market_id = market.get('id', market.get('condition_id', f"poly_{added}"))
            question = market.get('question', 'Unknown Market')
            description = market.get('description', question)
            
            # Get outcomes/tokens
            outcomes = market.get('outcomes', [])
            tokens = market.get('tokens', [])
            
            # Determine if binary or multi-option
            if len(outcomes) == 2:
                market_type = 'binary'
                # Use first outcome probability (usually "Yes")
                probability = float(outcomes[0]) if outcomes and len(outcomes) > 0 else 0.5
            else:
                market_type = 'multiple'
                probability = max(outcomes) if outcomes else 0.5
            
            # Volume data
            volume_24h = float(market.get('volume24hr', random.randint(5000, 500000)))
            volume_total = float(market.get('volume', volume_24h * random.uniform(10, 50)))
            
            # Participants
            participant_count = random.randint(50, 5000)
            
            # Category from tags
            tags = market.get('tags', [])
            category = map_category(tags)
            
            # Image
            image_url = get_image_url(market_id, category)
            
            # Dates
            created_at = market.get('startDate', market.get('createdAt', 
                                    (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat()))
            resolution_date = market.get('endDate', market.get('end_date_iso',
                                        (datetime.now() + timedelta(days=random.randint(7, 180))).isoformat()))
            
            # Status
            status = 'open'
            if market.get('closed', False) or market.get('resolved', False):
                status = 'closed'
            
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
            for tag in tags[:5]:  # Max 5 tags
                cursor.execute("""
                    INSERT OR IGNORE INTO market_tags (market_id, tag)
                    VALUES (?, ?)
                """, (market_id, tag))
            
            # Add category as tag
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market_id, category.lower()))
            
            # Add probability history
            history = generate_probability_history(probability, created_at, market_id)
            for point in history:
                cursor.execute("""
                    INSERT INTO probability_history (
                        market_id, probability, volume, timestamp
                    ) VALUES (?, ?, ?, ?)
                """, (market_id, point['probability'], point['volume'], point['timestamp']))
            
            # Add options for multi-option markets
            if market_type == 'multiple' and len(outcomes) > 2:
                for i, outcome in enumerate(outcomes[:10]):  # Max 10 options
                    option_name = tokens[i] if i < len(tokens) else f"Option {i+1}"
                    cursor.execute("""
                        INSERT INTO market_options (
                            market_id, option_id, option_text, probability
                        ) VALUES (?, ?, ?, ?)
                    """, (market_id, f"opt_{i}", option_name, float(outcome)))
            
            added += 1
            
            if added % 10 == 0:
                print(f"  📊 Added {added} markets...")
            
        except Exception as e:
            print(f"  ⚠️  Skipped market: {e}")
            skipped += 1
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Successfully added {added} markets")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} markets due to errors")
    
    return added

def verify_data():
    """Verify database has been populated"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM markets")
    market_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM probability_history")
    history_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM market_tags")
    tag_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM markets GROUP BY category")
    categories = cursor.fetchall()
    
    conn.close()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Markets: {market_count}")
    print(f"  History points: {history_count}")
    print(f"  Tags: {tag_count}")
    print(f"\n📈 Markets by Category:")
    for cat, count in categories:
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    print("🌊 Populating BRain with Polymarket data\n")
    
    try:
        # Fetch markets
        markets = fetch_polymarket_markets(50)
        
        # Clear old data
        clear_database()
        
        # Populate database
        added = populate_database(markets)
        
        # Verify
        verify_data()
        
        print(f"\n✅ Done! BRain database ready for personalized learning")
        print(f"🚀 Restart the app to see new markets")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

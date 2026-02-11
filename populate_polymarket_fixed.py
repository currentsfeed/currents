#!/usr/bin/env python3
"""
FIXED: Properly parse Polymarket outcomes (Democrat/Republican, not Yes/No)
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

def parse_outcomes(outcomes_str):
    """Parse outcomes JSON string"""
    try:
        if isinstance(outcomes_str, str):
            outcomes = json.loads(outcomes_str)
        else:
            outcomes = outcomes_str
        return outcomes if isinstance(outcomes, list) else []
    except:
        return []

def parse_prices(prices_str):
    """Parse outcome prices JSON string"""
    try:
        if isinstance(prices_str, str):
            prices = json.loads(prices_str)
        else:
            prices = prices_str
        
        if isinstance(prices, list):
            return [float(p) if p and p != "0" else None for p in prices]
        return []
    except:
        return []

def get_image_url(market_id):
    """Generate consistent image URL"""
    seed = abs(hash(market_id)) % 1000
    return f"https://picsum.photos/seed/{seed}/800/400"

def map_category(question):
    """Map question to BRain category"""
    q_lower = question.lower()
    
    if any(word in q_lower for word in ['trump', 'biden', 'election', 'president', 'congress', 'vote', 'party', 'democrat', 'republican']):
        return 'Politics'
    elif any(word in q_lower for word in ['bitcoin', 'crypto', 'ethereum', 'btc', 'eth', 'defi']):
        return 'Crypto'
    elif any(word in q_lower for word in ['nfl', 'nba', 'super bowl', 'championship', 'sport', 'football', 'basketball', 'world series']):
        return 'Sports'
    elif any(word in q_lower for word in ['ai', 'technology', 'apple', 'google', 'microsoft', 'tech', 'ipo', 'airbnb']):
        return 'Technology'
    elif any(word in q_lower for word in ['stock', 'economy', 'gdp', 'unemployment', 'market', 'fed', 'dow', 'nasdaq']):
        return 'Economics'
    elif any(word in q_lower for word in ['movie', 'celebrity', 'oscar', 'emmy', 'music']):
        return 'Entertainment'
    else:
        return 'Markets'

def generate_probability_history(current_probs, market_id, num_options):
    """Generate realistic probability history for all options"""
    history = []
    now = datetime.now()
    start = now - timedelta(days=random.randint(7, 90))
    
    num_points = random.randint(20, 40)
    
    # Generate start probabilities
    start_probs = [random.uniform(0.2, 0.8) for _ in range(num_options)]
    total = sum(start_probs)
    start_probs = [p / total for p in start_probs]  # Normalize to sum to 1
    
    for i in range(num_points):
        progress = i / (num_points - 1) if num_points > 1 else 0
        
        # Interpolate each option's probability
        point_probs = []
        for j in range(num_options):
            target = current_probs[j] if j < len(current_probs) else start_probs[j]
            prob = start_probs[j] + (target - start_probs[j]) * progress
            prob += random.uniform(-0.05, 0.05)  # noise
            prob = max(0.01, min(0.99, prob))
            point_probs.append(prob)
        
        # Normalize to sum to 1
        total = sum(point_probs)
        point_probs = [p / total for p in point_probs]
        
        timestamp = start + timedelta(seconds=(now - start).total_seconds() * progress)
        volume = random.randint(1000, 50000)
        
        history.append({
            'timestamp': timestamp.isoformat(),
            'probabilities': point_probs,
            'volume': volume
        })
    
    return history

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
            
            # Parse outcomes (THIS IS THE FIX!)
            outcomes = parse_outcomes(market.get('outcomes', '[]'))
            prices = parse_prices(market.get('outcomePrices', '[]'))
            
            # Skip if no valid outcomes
            if not outcomes or len(outcomes) == 0:
                continue
            
            # Determine market type
            if len(outcomes) == 2 and set([o.lower() for o in outcomes]) == {'yes', 'no'}:
                market_type = 'binary'
                # For binary yes/no, use first price or generate
                if prices and prices[0] is not None:
                    probability = float(prices[0])
                else:
                    probability = random.uniform(0.3, 0.7)
            else:
                market_type = 'multiple'
                # For multi-option, use max probability
                if prices and any(p is not None for p in prices):
                    valid_prices = [p for p in prices if p is not None]
                    probability = max(valid_prices) if valid_prices else 0.5
                else:
                    probability = 1.0 / len(outcomes)  # Equal distribution
            
            # Category
            category = map_category(question)
            
            # Volume
            volume_24h = float(market.get('volume24hr', 0))
            if volume_24h < 1000:
                volume_24h = random.randint(5000, 500000)
            volume_total = volume_24h * random.uniform(15, 50)
            
            # Other fields
            participant_count = random.randint(50, 5000)
            image_url = get_image_url(market_id)
            created_at = (datetime.now() - timedelta(days=random.randint(7, 90))).isoformat()
            resolution_date = (datetime.now() + timedelta(days=random.randint(7, 180))).isoformat()
            status = 'open'
            
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
            
            # Add outcome-specific tags
            for outcome in outcomes[:3]:  # First 3 outcomes as tags
                cursor.execute("""
                    INSERT OR IGNORE INTO market_tags (market_id, tag)
                    VALUES (?, ?)
                """, (market_id, outcome.lower()[:50]))
            
            # Generate probabilities for all outcomes
            if market_type == 'multiple':
                # Normalize prices to probabilities
                if prices and any(p is not None for p in prices):
                    total_price = sum([p for p in prices if p is not None])
                    if total_price > 0:
                        outcome_probs = [float(p) / total_price if p is not None else 0.01 for p in prices[:len(outcomes)]]
                    else:
                        outcome_probs = [1.0 / len(outcomes)] * len(outcomes)
                else:
                    outcome_probs = [1.0 / len(outcomes)] * len(outcomes)
                
                # Normalize to sum to 1
                total = sum(outcome_probs)
                outcome_probs = [p / total for p in outcome_probs]
                
                # Insert options (option_id must be globally unique)
                for i, (outcome, prob) in enumerate(zip(outcomes, outcome_probs)):
                    option_id = f"{market_id}_opt_{i}"
                    cursor.execute("""
                        INSERT INTO market_options (
                            market_id, option_id, option_text, probability
                        ) VALUES (?, ?, ?, ?)
                    """, (market_id, option_id, outcome, prob))
                
                # Generate history for multi-option
                history = generate_probability_history(outcome_probs, market_id, len(outcomes))
                for point in history:
                    # Store each option's probability at this timestamp
                    for i, prob in enumerate(point['probabilities']):
                        cursor.execute("""
                            INSERT INTO probability_history (
                                market_id, probability, volume, timestamp
                            ) VALUES (?, ?, ?, ?)
                        """, (market_id, prob, point['volume'] // len(outcomes), point['timestamp']))
            else:
                # Binary market - simple history
                history = generate_probability_history([probability, 1-probability], market_id, 2)
                for point in history:
                    cursor.execute("""
                        INSERT INTO probability_history (
                            market_id, probability, volume, timestamp
                        ) VALUES (?, ?, ?, ?)
                    """, (market_id, point['probabilities'][0], point['volume'], point['timestamp']))
            
            added += 1
            
            if added % 10 == 0:
                print(f"  📊 Added {added} markets...")
            
        except Exception as e:
            print(f"  ⚠️  Skipped market '{question[:50]}': {e}")
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
    
    cursor.execute("SELECT COUNT(*) FROM market_options")
    options_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM probability_history")
    history_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM markets GROUP BY category")
    categories = cursor.fetchall()
    
    cursor.execute("SELECT market_type, COUNT(*) FROM markets GROUP BY market_type")
    types = cursor.fetchall()
    
    # Show sample multi-option markets
    cursor.execute("""
        SELECT m.title, GROUP_CONCAT(mo.option_text, ', ') as options
        FROM markets m
        JOIN market_options mo ON m.market_id = mo.market_id
        WHERE m.market_type = 'multiple'
        GROUP BY m.market_id
        LIMIT 5
    """)
    sample_multi = cursor.fetchall()
    
    conn.close()
    
    print(f"\n📊 Database Statistics:")
    print(f"  Markets: {market_count}")
    print(f"  Market Options: {options_count}")
    print(f"  History points: {history_count}")
    
    print(f"\n📈 Markets by Type:")
    for t, count in types:
        print(f"  {t}: {count}")
    
    print(f"\n📈 Markets by Category:")
    for cat, count in sorted(categories, key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    if sample_multi:
        print(f"\n🎯 Sample Multi-Option Markets:")
        for title, options in sample_multi:
            print(f"  • {title[:60]}")
            print(f"    Options: {options}")

if __name__ == '__main__':
    print("🌊 Populating BRain with FIXED Polymarket data\n")
    
    try:
        markets = fetch_polymarket_markets(50)
        clear_database()
        added = populate_database(markets)
        verify_data()
        
        print(f"\n✅ Done! Markets now have proper options (Democrat/Republican, not Yes/No)")
        print(f"🔍 View database: python3 db_viewer.py (port 5556)")
        print(f"🚀 Restart app to see fixed markets")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

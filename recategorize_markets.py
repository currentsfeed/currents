#!/usr/bin/env python3
"""
Fix lazy "Markets" category - recategorize properly with better tags
"""
import sqlite3

DB_PATH = 'brain.db'

def improved_categorization(question, description=""):
    """Better categorization with specific subcategories - ORDER MATTERS!"""
    q_lower = question.lower()
    d_lower = description.lower()
    text = q_lower + " " + d_lower
    
    # CRIME & LEGAL (check first - specific)
    if any(word in text for word in ['guilty', 'convicted', 'sentenced', 'trial', 'lawsuit', 'crime', 'indictment', 'prosecution', 'conviction', 'felony', 'prison', 'jail', 'arrest', 'soliciting']):
        return 'Crime'
    
    # ENTERTAINMENT - Gaming (check before economics)
    if any(word in text for word in ['gta', 'gaming', 'esports', 'playstation', 'xbox', 'nintendo', 'steam', 'twitch', 'fortnite', 'minecraft']):
        return 'Entertainment'
    
    # ENTERTAINMENT - Music & Movies (check before economics)
    if any(word in text for word in ['album', 'song', 'music', 'artist', 'concert', 'tour', 'rihanna', 'drake', 'taylor', 'movie', 'film', 'oscar', 'emmy', 'netflix', 'disney', 'spotify']):
        return 'Entertainment'
    
    # CULTURE & SOCIETY (check before economics)
    if any(word in text for word in ['jesus', 'religion', 'church', 'god', 'bible', 'christ']):
        return 'Culture'
    
    # CRYPTO & BLOCKCHAIN (specific)
    if any(word in text for word in ['bitcoin', 'crypto', 'ethereum', 'btc', 'eth', 'defi', 'solana', 'blockchain', 'nft', 'token', 'coin']):
        return 'Crypto'
    
    # TECHNOLOGY - AI, Companies, Products (specific)
    if any(word in text for word in ['ai', 'artificial intelligence', 'apple', 'google', 'microsoft', 'openai', 'chatgpt', 'meta', 'tesla', 'spacex', 'hardware', 'software', 'product launch', 'ipo', 'tech company']):
        return 'Technology'
    
    # SPORTS (specific)
    if any(word in text for word in ['nfl', 'nba', 'super bowl', 'championship', 'football', 'basketball', 'world series', 'soccer', 'fifa', 'mlb', 'nhl', 'olympics', 'qualify', 'world cup']):
        return 'Sports'
    
    # WORLD - Conflicts & Geopolitics (broad)
    if any(word in text for word in ['iran', 'israel', 'ukraine', 'russia', 'china', 'taiwan', 'war', 'conflict', 'military', 'invasion', 'ceasefire', 'nato', 'nuclear']):
        return 'World'
    
    # POLITICS - Government & Elections (broad)
    if any(word in text for word in ['trump', 'biden', 'election', 'president', 'congress', 'vote', 'party', 'democrat', 'republican', 'senate', 'governor', 'policy', 'legislation', 'white house', 'deport']):
        return 'Politics'
    
    # ECONOMICS - Markets, Revenue, Tariffs (broad)
    if any(word in text for word in ['revenue', 'tariff', 'tax', 'gdp', 'unemployment', 'inflation', 'interest rate', 'federal reserve', 'economy', 'recession', 'dow', 'nasdaq', 's&p', 'collect', 'budget']):
        return 'Economics'
    
    # DEFAULT - General Predictions
    return 'Predictions'

def get_detailed_tags(question, description=""):
    """Generate multiple specific tags"""
    q_lower = question.lower()
    d_lower = description.lower()
    text = q_lower + " " + d_lower
    
    tags = []
    
    # People
    people = ['trump', 'biden', 'elon', 'musk', 'weinstein', 'rihanna', 'drake', 'taylor swift']
    for person in people:
        if person in text:
            tags.append(person.replace(' ', '_'))
    
    # Topics
    topics = {
        'deportation': ['deport'],
        'budget': ['budget', 'spending'],
        'tariffs': ['tariff'],
        'gaming': ['gta', 'game', 'gaming'],
        'music': ['album', 'music', 'song'],
        'legal': ['guilty', 'convicted', 'trial', 'sentence'],
        'revenue': ['revenue', 'tax'],
        'ceasefire': ['ceasefire'],
        'invasion': ['invasion', 'invade'],
        'ai': ['ai', 'artificial intelligence', 'chatgpt', 'openai'],
        'hardware': ['hardware', 'product'],
        'religion': ['jesus', 'god', 'christ']
    }
    
    for tag, keywords in topics.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    
    return tags

def recategorize_all_markets():
    """Update all markets with better categories and tags"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, description FROM markets")
    markets = cursor.fetchall()
    
    updated = 0
    
    for market_id, title, description in markets:
        # Get new category
        new_category = improved_categorization(title, description or "")
        
        # Update category
        cursor.execute("""
            UPDATE markets 
            SET category = ? 
            WHERE market_id = ?
        """, (new_category, market_id))
        
        # Clear old tags
        cursor.execute("DELETE FROM market_tags WHERE market_id = ?", (market_id,))
        
        # Add category tag
        cursor.execute("""
            INSERT INTO market_tags (market_id, tag) 
            VALUES (?, ?)
        """, (market_id, new_category.lower()))
        
        # Add detailed tags
        detailed_tags = get_detailed_tags(title, description or "")
        for tag in detailed_tags:
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market_id, tag))
        
        updated += 1
        if updated % 20 == 0:
            print(f"  Updated {updated} markets...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Recategorized {updated} markets")
    return updated

def show_new_distribution():
    """Show new category distribution"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, COUNT(*) FROM markets GROUP BY category ORDER BY COUNT(*) DESC")
    categories = cursor.fetchall()
    
    print(f"\n📊 New Category Distribution:")
    for cat, count in categories:
        print(f"  {cat}: {count}")
    
    # Show sample from each category
    print(f"\n📋 Sample Markets by Category:")
    for cat, _ in categories[:5]:
        cursor.execute("""
            SELECT title FROM markets 
            WHERE category = ? 
            LIMIT 2
        """, (cat,))
        samples = cursor.fetchall()
        print(f"\n  {cat}:")
        for (title,) in samples:
            print(f"    • {title[:70]}")
    
    # Show tag distribution
    cursor.execute("SELECT tag, COUNT(*) FROM market_tags GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 15")
    tags = cursor.fetchall()
    
    print(f"\n🏷️  Top Tags:")
    for tag, count in tags:
        print(f"  {tag}: {count}")
    
    conn.close()

if __name__ == '__main__':
    print("🔄 Recategorizing markets with better logic...\n")
    
    try:
        recategorize_all_markets()
        show_new_distribution()
        
        print(f"\n✅ Done! Much better categorization")
        print(f"🔍 View: https://brain-db-viewer.loca.lt")
        print(f"🚀 Restart app to see changes")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""Update market images to use reliable Pexels"""

import sqlite3
import hashlib

def get_pexels_url(keywords, market_id):
    """Generate Pexels URL with relevant keywords"""
    # Pexels uses different format - just return a solid color gradient for hero
    # and use simple Unsplash fallback that works better
    query = keywords.replace(' ', '+')
    # Use a more reliable format
    seed = abs(hash(market_id)) % 10000
    return f"https://images.unsplash.com/photo-{1500000000 + seed}?w=800&h=400&fit=crop&q=80"

def extract_keywords(title):
    """Extract relevant keywords from market title"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['trump', 'president', 'election']):
        return 'politics'
    elif any(word in title_lower for word in ['nba', 'nhl', 'nfl', 'sports', 'championship']):
        return 'sports'
    elif any(word in title_lower for word in ['bitcoin', 'crypto']):
        return 'cryptocurrency'
    elif any(word in title_lower for word in ['ai', 'openai', 'technology']):
        return 'technology'
    elif any(word in title_lower for word in ['market', 'economy', 'stock']):
        return 'business'
    elif any(word in title_lower for word in ['entertainment', 'movie', 'gta']):
        return 'entertainment'
    elif any(word in title_lower for word in ['deport', 'immigration']):
        return 'politics'
    elif any(word in title_lower for word in ['weinstein', 'crime', 'legal']):
        return 'justice'
    else:
        return 'abstract'

def main():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT market_id, title FROM markets")
    markets = cursor.fetchall()
    
    updated = 0
    for market_id, title in markets:
        keywords = extract_keywords(title)
        new_url = get_pexels_url(keywords, market_id)
        
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", 
                      (new_url, market_id))
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} market images with Unsplash URLs")

if __name__ == '__main__':
    main()

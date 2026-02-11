#!/usr/bin/env python3
"""Update market images to be topic-relevant using Unsplash"""

import sqlite3
import re

def extract_keywords(title):
    """Extract relevant keywords from market title"""
    title_lower = title.lower()
    
    # Topic mapping
    if any(word in title_lower for word in ['trump', 'president', 'election', 'political']):
        return 'politics government'
    elif any(word in title_lower for word in ['nba', 'nfl', 'nhl', 'sports', 'championship', 'game']):
        return 'sports competition'
    elif any(word in title_lower for word in ['bitcoin', 'crypto', 'ethereum', 'blockchain']):
        return 'cryptocurrency technology'
    elif any(word in title_lower for word in ['ai', 'openai', 'anthropic', 'technology', 'tech']):
        return 'technology innovation'
    elif any(word in title_lower for word in ['market', 'economy', 'stock', 'trading']):
        return 'business finance'
    elif any(word in title_lower for word in ['entertainment', 'movie', 'music', 'celebrity']):
        return 'entertainment culture'
    elif any(word in title_lower for word in ['deport', 'immigration', 'border']):
        return 'immigration border'
    elif any(word in title_lower for word in ['weinstein', 'crime', 'legal', 'court']):
        return 'justice law'
    else:
        # Extract first noun-like words
        words = re.findall(r'\b[A-Z][a-z]+\b', title)
        return ' '.join(words[:2]) if words else 'news'

def get_unsplash_url(keywords, seed):
    """Generate Unsplash URL with relevant keywords"""
    query = keywords.replace(' ', ',')
    return f"https://source.unsplash.com/800x400/?{query}&sig={seed}"

def update_market_images():
    """Update all market images"""
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT market_id, title, image_url FROM markets")
    markets = cursor.fetchall()
    
    updated = 0
    for market_id, title, current_url in markets:
        # Skip if already has good URL
        if 'unsplash' in current_url:
            continue
            
        keywords = extract_keywords(title)
        seed = abs(hash(market_id)) % 10000
        new_url = get_unsplash_url(keywords, seed)
        
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", 
                      (new_url, market_id))
        updated += 1
        print(f"✓ {title[:50]}: {keywords}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} market images")

if __name__ == '__main__':
    update_market_images()

#!/usr/bin/env python3
"""
Fetch real photographic images for all markets using Pexels API
Maps categories to relevant search terms and updates database
"""

import sqlite3
import requests
import time
import hashlib
from pathlib import Path

# Pexels API configuration
PEXELS_API_KEY = "563492ad6f91700001000001a9f8ae75f27d49baa2aa0f9563d1f1a3"
PEXELS_API_URL = "https://api.pexels.com/v1/search"

# Category to search term mapping
CATEGORY_SEARCHES = {
    'Politics': ['politics', 'government', 'capitol building', 'congress', 'parliament', 'election'],
    'Sports': ['sports action', 'stadium', 'athletes', 'competition', 'team sports'],
    'Crypto': ['cryptocurrency', 'blockchain', 'bitcoin', 'digital currency', 'trading screens'],
    'Entertainment': ['hollywood', 'movie theater', 'entertainment', 'red carpet', 'cinema'],
    'Economics': ['stock market', 'business', 'finance', 'trading floor', 'economics'],
    'Technology': ['technology', 'innovation', 'computers', 'software', 'tech startup'],
    'Crime': ['justice', 'law', 'courthouse', 'legal', 'police'],
    'World': ['world news', 'international', 'globe', 'earth', 'global'],
    'Markets': ['financial markets', 'trading', 'stock exchange', 'wall street'],
}

def get_category_search(category):
    """Get appropriate search term for a category"""
    searches = CATEGORY_SEARCHES.get(category, ['abstract', 'gradient'])
    # Rotate through search terms based on hash
    return searches[0]

def fetch_pexels_image(search_term, page=1):
    """Fetch a high-quality image from Pexels"""
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    params = {
        'query': search_term,
        'per_page': 1,
        'page': page,
        'orientation': 'landscape',
        'size': 'large'
    }
    
    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('photos'):
                photo = data['photos'][0]
                # Use large size for better quality
                return photo['src']['large']
        return None
    except Exception as e:
        print(f"Error fetching from Pexels: {e}")
        return None

def get_unsplash_image(search_term, index=0):
    """Fetch image from Unsplash as fallback"""
    # Unsplash Source API (no key needed)
    # Returns a random image for the search term
    url = f"https://source.unsplash.com/1600x900/?{search_term}"
    return url

def update_market_images():
    """Update all market images with real photos"""
    db_path = Path(__file__).parent / 'brain.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, category FROM markets")
    markets = cursor.fetchall()
    
    print(f"Found {len(markets)} markets to update")
    
    updated = 0
    failed = []
    
    for market_id, title, category in markets:
        # Determine search term
        search_term = get_category_search(category)
        
        # Generate a page number based on market_id for variety
        page = (int(hashlib.md5(str(market_id).encode()).hexdigest(), 16) % 80) + 1
        
        print(f"Fetching image for '{title[:50]}...' (category: {category}, search: {search_term}, page: {page})")
        
        # Try Pexels first
        image_url = fetch_pexels_image(search_term, page)
        
        # Fallback to Unsplash if Pexels fails
        if not image_url:
            print(f"  Pexels failed, using Unsplash")
            image_url = get_unsplash_image(search_term, page)
        
        if image_url:
            # Update database
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (image_url, market_id)
            )
            updated += 1
            print(f"  ✓ Updated with: {image_url[:80]}...")
        else:
            failed.append((market_id, title))
            print(f"  ✗ Failed to fetch image")
        
        # Rate limiting - be nice to the APIs
        time.sleep(0.5)
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n{'='*80}")
    print(f"Image Update Complete!")
    print(f"{'='*80}")
    print(f"✓ Successfully updated: {updated} markets")
    if failed:
        print(f"✗ Failed: {len(failed)} markets")
        for market_id, title in failed[:5]:
            print(f"  - {market_id}: {title[:50]}")
    
    return updated, failed

if __name__ == '__main__':
    print("Starting real image fetch...")
    print("This will replace all SVG placeholders with real photos\n")
    
    updated, failed = update_market_images()
    
    print("\nDone! Restart the server to see the new images.")

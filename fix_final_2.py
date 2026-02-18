#!/usr/bin/env python3
"""
Fix final 2 markets with simplest search terms
"""

import requests
import time
import os
from hashlib import md5

# Load API key
with open('.unsplash_key', 'r') as f:
    API_KEY = f.read().strip()

UNSPLASH_API = "https://api.unsplash.com"

def search_unsplash(query, page=1):
    """Search Unsplash for images"""
    url = f"{UNSPLASH_API}/search/photos"
    headers = {"Authorization": f"Client-ID {API_KEY}"}
    params = {
        "query": query,
        "per_page": 1,
        "page": page,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['regular']
    except Exception as e:
        print(f"    API Error: {e}")
    return None

def download_image(url, filepath):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True, md5(response.content).hexdigest()
    except Exception as e:
        print(f"    Download Error: {e}")
    return False, None

# Final 2 markets with SIMPLEST terms + varied pages
FINAL_MARKETS = [
    ('npb-fighters-marines-feb14', 'Sports', 'baseball field', 3),
    ('nhl-leafs-panthers-feb13', 'Sports', 'hockey rink', 4),
]

def main():
    print("=" * 80)
    print("FIX FINAL 2 MARKETS")
    print("=" * 80)
    
    sql_updates = []
    
    for i, (market_id, category, search_query, page) in enumerate(FINAL_MARKETS, 1):
        print(f"[{i}/2] {market_id} ({category})")
        print(f"  Search: {search_query} (page {page})")
        
        image_url = search_unsplash(search_query, page=page)
        
        if image_url:
            filename = f"{category.lower()}_{market_id.replace('-', '_')}.jpg"
            filepath = f"static/images/{filename}"
            
            ok, img_hash = download_image(image_url, filepath)
            
            if ok:
                size_kb = os.path.getsize(filepath) // 1024
                print(f"  ✓ Downloaded: {size_kb}KB - {img_hash[:8]}")
                sql_updates.append(f"UPDATE markets SET image_url = '/static/images/{filename}' WHERE market_id = '{market_id}';")
            else:
                print(f"  ❌ Download failed")
        else:
            print(f"  ❌ Search failed")
        
        time.sleep(1)
    
    # Save SQL
    if sql_updates:
        with open('update_final_2.sql', 'w') as f:
            f.write("-- Fix final 2 markets\n\n")
            for sql in sql_updates:
                f.write(sql + '\n')
        print(f"\n✓ SQL saved: update_final_2.sql")
        print(f"✅ Fixed: {len(sql_updates)}/2")
    else:
        print(f"\n❌ All failed")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Fix 11 markets with missing image files
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

# Missing file markets with search terms
MISSING_MARKETS = [
    ('517311', 'Politics', 'deportation immigration border', 1),
    ('521944', 'Economics', 'federal spending budget cuts', 2),
    ('531202', 'Crime', 'cryptocurrency fraud trial', 1),
    ('540816', 'World', 'russia ukraine war ceasefire', 1),
    ('540818', 'Entertainment', 'playboi carti concert rap', 1),
    ('540881', 'Entertainment', 'grand theft auto gta gaming', 2),
    ('550694', 'Sports', 'italy soccer fifa world cup', 1),
    ('553831', 'Sports', 'los angeles kings nhl hockey', 2),
    ('553842', 'Sports', 'new york islanders nhl hockey', 3),
    ('new_60018', 'Sports', 'novak djokovic tennis grand slam', 1),
    ('npb-fighters-marines-feb14', 'Sports', 'japanese baseball game', 2),
]

def main():
    print("=" * 80)
    print("FIX 11 MISSING FILE MARKETS")
    print("=" * 80)
    
    sql_updates = []
    success = 0
    failed = 0
    
    for i, (market_id, category, search_query, page) in enumerate(MISSING_MARKETS, 1):
        print(f"[{i}/{len(MISSING_MARKETS)}] {market_id} ({category})")
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
                success += 1
            else:
                print(f"  ❌ Download failed")
                failed += 1
        else:
            print(f"  ❌ Search failed")
            failed += 1
        
        time.sleep(1.5)  # Extra delay for API
    
    # Save SQL
    if sql_updates:
        with open('update_missing_11.sql', 'w') as f:
            f.write("-- Fix 11 missing file markets\n\n")
            for sql in sql_updates:
                f.write(sql + '\n')
        print(f"\n✓ SQL saved: update_missing_11.sql")
    
    print(f"\n{'='*80}")
    print(f"✅ Success: {success}/{len(MISSING_MARKETS)}")
    print(f"❌ Failed: {failed}/{len(MISSING_MARKETS)}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()

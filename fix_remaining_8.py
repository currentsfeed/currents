#!/usr/bin/env python3
"""
Fix the 8 remaining markets with broader search terms
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

# Failed markets with BROADER search terms
FAILED_MARKETS = [
    ('546612', 'Technology', 'computer chip technology'),
    ('new_60027', 'Technology', 'artificial intelligence robot'),
    ('549873', 'Crypto', 'dutch politics building'),
    ('new_60024', 'Crypto', 'courtroom trial legal'),
    ('553860', 'Sports', 'basketball arena game'),
    ('multi_001', 'Sports', 'basketball trophy championship'),
    ('npb-fighters-marines-feb14', 'Sports', 'baseball game stadium'),
    ('nhl-leafs-panthers-feb13', 'Sports', 'ice hockey game arena'),
]

def main():
    print("=" * 80)
    print("FIX REMAINING 8 MARKETS")
    print("=" * 80)
    
    sql_updates = []
    success = 0
    failed = 0
    
    for i, (market_id, category, search_query) in enumerate(FAILED_MARKETS, 1):
        print(f"[{i}/8] {market_id} ({category})")
        print(f"  Search: {search_query}")
        
        # Try up to page 3 if needed
        for page in range(1, 4):
            image_url = search_unsplash(search_query, page=page)
            
            if image_url:
                filename = f"{category.lower()}_{market_id.replace('-', '_')}.jpg"
                filepath = f"static/images/{filename}"
                
                ok, img_hash = download_image(image_url, filepath)
                
                if ok:
                    size_kb = os.path.getsize(filepath) // 1024
                    print(f"  ✓ Downloaded (page {page}): {size_kb}KB - {img_hash[:8]}")
                    sql_updates.append(f"UPDATE markets SET image_url = '/static/images/{filename}' WHERE market_id = '{market_id}';")
                    success += 1
                    break
            
            if page < 3:
                print(f"  Page {page} failed, trying {page+1}...")
                time.sleep(1)
        else:
            print(f"  ❌ All pages failed")
            failed += 1
        
        time.sleep(1)
    
    # Save SQL
    if sql_updates:
        with open('update_remaining_8.sql', 'w') as f:
            f.write("-- Fix remaining 8 markets\n\n")
            for sql in sql_updates:
                f.write(sql + '\n')
        print(f"\n✓ SQL saved: update_remaining_8.sql")
    
    print(f"\n{'='*80}")
    print(f"✅ Success: {success}/8")
    print(f"❌ Failed: {failed}/8")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()

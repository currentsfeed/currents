#!/usr/bin/env python3
"""
Fix 34 duplicate images using Unsplash API with highly specific queries
"""

import sqlite3
import os
import requests
import time
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
        "page": page,  # Use pagination for variety
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['regular']  # 1080px width
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

# Highly specific search queries for each market (with pagination for variety)
DUPLICATE_MARKETS = [
    # BATCH 1: Economics (9 markets) - varied financial imagery
    ('521946', 'Economics', 'federal budget capitol building', 1),
    ('537484', 'Economics', 'treasury department washington', 2),
    ('537486', 'Economics', 'tax forms calculator', 1),
    ('537488', 'Economics', 'money cash currency stack', 2),
    ('537490', 'Economics', 'shipping containers trade port', 1),
    ('new_60040', 'Economics', 'unemployment line job search', 1),
    ('new_60042', 'Economics', 'wall street stock exchange', 2),
    ('new_60044', 'Economics', 'federal reserve building', 1),
    ('new_60045', 'Economics', 'economic decline graph chart', 1),
    
    # BATCH 2: Entertainment - GTA VI (2 markets)
    ('540843', 'Entertainment', 'video game controller console', 2),
    ('540844', 'Entertainment', 'gaming setup rgb lights', 1),
    
    # BATCH 3: Crime - Weinstein (4 markets) - courtroom/justice imagery
    ('544093', 'Crime', 'courtroom empty wooden benches', 1),
    ('544094', 'Crime', 'judge gavel legal', 2),
    ('544095', 'Crime', 'prison bars cell', 1),
    ('544096', 'Crime', 'prison exterior fence', 2),
    
    # BATCH 4: Technology - AI (6 markets) - varied tech imagery
    ('546612', 'Technology', 'computer chip circuit board', 1),
    ('multi_002', 'Technology', 'data center servers blue lights', 2),
    ('new_60027', 'Technology', 'artificial intelligence brain network', 1),
    ('new_60029', 'Technology', 'spacex rocket launch flames', 1),
    ('new_60030', 'Technology', 'smartphone app tiktok social', 2),
    ('new_60033', 'Technology', 'google search engine laptop', 1),
    
    # BATCH 5: Crypto (7 markets) - crypto imagery
    ('549873', 'Crypto', 'netherlands dutch politics parliament', 1),
    ('new_60020', 'Crypto', 'solana cryptocurrency purple', 1),
    ('new_60021', 'Crypto', 'coinbase trading platform screen', 2),
    ('new_60022', 'Crypto', 'stablecoin usdc digital money', 1),
    ('new_60023', 'Crypto', 'nft digital art marketplace', 1),
    ('new_60024', 'Crypto', 'ftx bankman fried courtroom', 2),
    ('new_60025', 'Crypto', 'ripple xrp cryptocurrency coin', 1),
    
    # BATCH 6: Sports - Mixed (5 markets)
    ('553838', 'Sports', 'minnesota wild hockey ice', 1),
    ('553860', 'Sports', 'houston rockets basketball court', 2),
    ('multi_001', 'Sports', 'nba championship trophy larry obrien', 1),
    ('new_60010', 'Sports', 'lionel messi argentina jersey', 1),
    ('npb-fighters-marines-feb14', 'Sports', 'japanese baseball npb stadium', 1),
    
    # BATCH 7: Politics - Trump/US (4 markets)
    ('multi_003', 'Politics', 'white house oval office desk', 1),
    ('new_60004', 'Politics', 'gavin newsom california capitol', 2),
    ('new_60007', 'Politics', 'january 6 capitol riot police', 1),
    ('new_60008', 'Politics', 'abortion rights protest march', 1),
    
    # BATCH 8: Culture - Entertainment (3 markets)
    ('new_60036', 'Culture', 'beyonce concert stage performance', 1),
    ('new_60038', 'Culture', 'avatar movie pandora floating mountains', 1),
    ('new_60039', 'Culture', 'streaming netflix disney plus tv', 2),
    
    # BATCH 9: World - International (2 markets)
    ('new_60048', 'World', 'brexit united kingdom flag', 1),
    ('new_60050', 'World', 'mexico drugs reform cartel', 1),
    
    # BATCH 10: Sports - NHL (2 markets)
    ('nhl-rangers-bruins-feb12', 'Sports', 'new york rangers hockey madison square garden', 2),
    ('nhl-leafs-panthers-feb13', 'Sports', 'toronto maple leafs hockey scotiabank arena', 1),
]

def main():
    print("=" * 80)
    print("FIX 34 DUPLICATE IMAGES - UNSPLASH API")
    print("=" * 80)
    print(f"Total markets: {len(DUPLICATE_MARKETS)}")
    print(f"API Key: {API_KEY[:20]}...")
    print()
    
    conn = sqlite3.connect('brain.db')
    
    success_count = 0
    failed_count = 0
    sql_updates = []
    downloaded_hashes = set()
    
    for i, (market_id, category, search_query, page) in enumerate(DUPLICATE_MARKETS, 1):
        print(f"[{i}/{len(DUPLICATE_MARKETS)}] {market_id} ({category})")
        print(f"  Search: {search_query} (page {page})")
        
        # Search Unsplash
        image_url = search_unsplash(search_query, page=page)
        
        if not image_url:
            print(f"  ❌ No results found")
            failed_count += 1
            time.sleep(1)
            continue
        
        # Generate filename
        filename = f"{category.lower()}_{market_id.replace('-', '_')}.jpg"
        filepath = f"static/images/{filename}"
        
        # Download image
        success, img_hash = download_image(image_url, filepath)
        
        if success:
            # Check if hash is unique
            if img_hash in downloaded_hashes:
                print(f"  ⚠️  Duplicate hash detected! Trying page 2...")
                # Try next page
                image_url2 = search_unsplash(search_query, page=page+1)
                if image_url2:
                    success2, img_hash2 = download_image(image_url2, filepath)
                    if success2 and img_hash2 not in downloaded_hashes:
                        img_hash = img_hash2
                        print(f"  ✓ Downloaded (page 2): {os.path.getsize(filepath)//1024}KB - {img_hash[:8]}")
                    else:
                        print(f"  ❌ Still duplicate, keeping anyway")
                else:
                    print(f"  ❌ Page 2 failed, keeping page 1")
            else:
                size_kb = os.path.getsize(filepath) // 1024
                print(f"  ✓ Downloaded: {size_kb}KB - {img_hash[:8]}")
            
            downloaded_hashes.add(img_hash)
            sql_updates.append(f"UPDATE markets SET image_url = '/static/images/{filename}' WHERE market_id = '{market_id}';")
            success_count += 1
        else:
            print(f"  ❌ Download failed")
            failed_count += 1
        
        # Rate limiting: be nice to API
        time.sleep(1)
    
    # Save SQL updates
    sql_file = 'update_34_duplicates.sql'
    with open(sql_file, 'w') as f:
        f.write("-- Fix 34 duplicate images\n")
        f.write(f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for sql in sql_updates:
            f.write(sql + '\n')
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Downloaded: {success_count}/{len(DUPLICATE_MARKETS)}")
    print(f"❌ Failed: {failed_count}/{len(DUPLICATE_MARKETS)}")
    print(f"✓ SQL saved: {sql_file}")
    print(f"\nTo apply: sqlite3 brain.db < {sql_file}")
    print(f"Then: sudo systemctl restart currents.service")
    
    conn.close()

if __name__ == '__main__':
    main()

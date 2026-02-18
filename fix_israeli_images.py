#!/usr/bin/env python3
"""
Fix missing Israeli market images using Unsplash API
"""

import requests
import hashlib
import time
import os

API_KEY = "UQAXtmSzXQ5tS64GG0_I6sVeObYilVMMdoqSsajMN4g"
BASE_URL = "https://api.unsplash.com/search/photos"
IMAGE_DIR = "static/images"

# Markets that need images
MISSING_IMAGES = [
    {
        "filename": "israel-ai-funding.jpg",
        "market_title": "Will Israeli AI startups raise over $3B in 2026?",
        "search_query": "artificial intelligence technology startup",
        "orientation": "portrait"
    },
    {
        "filename": "israel-desalination.jpg",
        "market_title": "Will Israel produce 90%+ of drinking water from desalination in 2026?",
        "search_query": "water treatment facility industrial",
        "orientation": "portrait"
    },
    {
        "filename": "israel-election-netanyahu.jpg",
        "market_title": "Will Benjamin Netanyahu remain Prime Minister after 2026 election?",
        "search_query": "parliament government building",
        "orientation": "portrait"
    },
    {
        "filename": "israel-eurovision.jpg",
        "market_title": "Will Israel finish Top 5 at Eurovision 2026?",
        "search_query": "concert stage lights performance",
        "orientation": "portrait"
    },
    {
        "filename": "israel-gas-exports.jpg",
        "market_title": "Will Israel's natural gas exports exceed $10B in 2026?",
        "search_query": "offshore gas platform oil rig",
        "orientation": "portrait"
    },
    {
        "filename": "israel-hapoel-league.jpg",
        "market_title": "Will Hapoel Tel Aviv win Israeli Premier League?",
        "search_query": "soccer stadium crowd celebration",
        "orientation": "portrait"
    },
    {
        "filename": "israel-judiciary-reform.jpg",
        "market_title": "Will Israel pass major judicial reform legislation in 2026?",
        "search_query": "supreme court justice gavel",
        "orientation": "portrait"
    },
    {
        "filename": "israel-tech-unicorn.jpg",
        "market_title": "Will an Israeli tech unicorn IPO above $5B valuation in 2026?",
        "search_query": "stock market trading technology",
        "orientation": "portrait"
    },
    {
        "filename": "israel_iran_8848cddf.jpg",  # West Bank settlers
        "market_title": "Will Israeli settlers surpass 1M in West Bank?",
        "search_query": "middle east settlement buildings",
        "orientation": "portrait"
    },
    {
        "filename": "israel_iran_c8f7f250.jpg",  # South Lebanon invasion
        "market_title": "Will Israel invade South Lebanon in 2025?",
        "search_query": "military conflict zone border",
        "orientation": "portrait"
    },
    {
        "filename": "ufc-adesanya.jpg",
        "market_title": "Will Israel Adesanya win in his UFC comeback fight?",
        "search_query": "mma fighter octagon combat sports",
        "orientation": "portrait"
    }
]

def download_image_from_unsplash(search_query, filename, orientation="portrait"):
    """Download image from Unsplash and save with unique filename"""
    print(f"\nSearching for: {search_query}")
    
    params = {
        "query": search_query,
        "client_id": API_KEY,
        "per_page": 30,
        "orientation": orientation
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        print(f"❌ API error: {response.status_code}")
        return False
    
    data = response.json()
    results = data.get("results", [])
    
    if not results:
        print(f"❌ No results for: {search_query}")
        return False
    
    # Try multiple results until we find a unique one
    for idx, photo in enumerate(results[:20]):  # Try first 20 results
        image_url = photo["urls"]["regular"]
        desc = photo.get('description') or 'N/A'
        print(f"  Trying result #{idx + 1}: {desc[:60]}")
        
        # Download image
        img_response = requests.get(image_url)
        if img_response.status_code != 200:
            continue
        
        image_data = img_response.content
        image_hash = hashlib.md5(image_data).hexdigest()
        
        # Check if this hash already exists
        existing_hash_file = None
        for existing_file in os.listdir(IMAGE_DIR):
            if existing_file.endswith(('.jpg', '.jpeg', '.png')):
                existing_path = os.path.join(IMAGE_DIR, existing_file)
                with open(existing_path, 'rb') as f:
                    existing_hash = hashlib.md5(f.read()).hexdigest()
                    if existing_hash == image_hash:
                        existing_hash_file = existing_file
                        break
        
        if existing_hash_file:
            print(f"  ⚠️  Duplicate of {existing_hash_file}, trying next...")
            continue
        
        # Save the unique image
        output_path = os.path.join(IMAGE_DIR, filename)
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"  ✅ Downloaded: {filename} (MD5: {image_hash[:8]}...)")
        return True
    
    print(f"❌ All results were duplicates for: {search_query}")
    return False

def main():
    print("=" * 70)
    print("FIXING ISRAELI MARKET IMAGES")
    print("=" * 70)
    
    success_count = 0
    failed = []
    
    for item in MISSING_IMAGES:
        filename = item["filename"]
        search_query = item["search_query"]
        orientation = item.get("orientation", "portrait")
        
        print(f"\n[{MISSING_IMAGES.index(item) + 1}/{len(MISSING_IMAGES)}] {filename}")
        print(f"Market: {item['market_title']}")
        
        # Check if already exists
        if os.path.exists(os.path.join(IMAGE_DIR, filename)):
            print(f"  ⏭️  Already exists, skipping")
            continue
        
        success = download_image_from_unsplash(search_query, filename, orientation)
        
        if success:
            success_count += 1
        else:
            failed.append(filename)
        
        # Rate limiting - be nice to Unsplash
        time.sleep(1)
    
    # Now update the two markets using default.jpg
    print("\n" + "=" * 70)
    print("UPDATING DATABASE REFERENCES")
    print("=" * 70)
    
    import sqlite3
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Update West Bank settlers market
    cursor.execute("""
        UPDATE markets 
        SET image_url = 'static/images/israel_iran_8848cddf.jpg'
        WHERE market_id = 'israel_iran_8848cddf'
    """)
    print("✅ Updated israel_iran_8848cddf (West Bank settlers)")
    
    # Update South Lebanon invasion market
    cursor.execute("""
        UPDATE markets 
        SET image_url = 'static/images/israel_iran_c8f7f250.jpg'
        WHERE market_id = 'israel_iran_c8f7f250'
    """)
    print("✅ Updated israel_iran_c8f7f250 (South Lebanon)")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully downloaded: {success_count}")
    print(f"❌ Failed: {len(failed)}")
    
    if failed:
        print("\nFailed files:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()

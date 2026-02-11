#!/usr/bin/env python3
"""
MASS IMAGE REPLACEMENT SCRIPT
Replaces all dummyimage.com URLs with real professional photos from Unsplash

Run: python3 replace_all_images.py
"""

import sqlite3
import urllib.request
import time
import os
import hashlib

DB_PATH = './brain.db'
IMAGES_DIR = './static/images'

# Unsplash photo IDs curated by category
CATEGORY_PHOTOS = {
    'Sports': [
        'photo-1461896836934-ffe607ba8211',  # stadium
        'photo-1579952363873-27f3bade9f55',  # basketball
        'photo-1554068865-24cecd4e34b8',  # tennis court
        'photo-1517466787929-bc90951d0974',  # hockey
        'photo-1577223625816-7546f9638e25',  # soccer
        'photo-1587280501635-68a0e82cd5ff',  # football
        'photo-1531415074968-036ba1b575da',  # golf
    ],
    'Politics': [
        'photo-1529107386315-e1a2ed48a620',  # capitol
        'photo-1551269901-5c5e14c25df7',  # government
        'photo-1432821596592-e2c18b78144f',  # white house
        'photo-1555083488-2b99e9096073',  # voting
        'photo-1494519870136-3a900335b17e',  # congress
    ],
    'Economics': [
        'photo-1611974789855-9c2a0a7236a3',  # stock market
        'photo-1460925895917-afdab827c52f',  # business
        'photo-1559526324-593bc073d938',  # finance
        'photo-1526304640581-d334cdbbf45e',  # money
        'photo-1590283603385-17ffb3a7f29f',  # bull market
    ],
    'Crypto': [
        'photo-1621416894569-0f39ed31d247',  # cryptocurrency
        'photo-1639762681485-074b7f938ba0',  # blockchain
        'photo-1622630998477-20aa696ecb05',  # bitcoin
        'photo-1622186477895-f2af6a0f5a97',  # digital currency
        'photo-1605792657660-596af9009e82',  # crypto trading
    ],
    'Entertainment': [
        'photo-1594908900066-3f47337549d8',  # hollywood
        'photo-1489599849927-2ee91cede3ba',  # cinema
        'photo-1440404653325-ab127d49abc1',  # red carpet
        'photo-1574267432644-f74ea26ed8b7',  # entertainment
        'photo-1598899134739-24c46f58b8c0',  # awards
    ],
    'Technology': [
        'photo-1518770660439-4636190af475',  # tech
        'photo-1485827404703-89b55fcc595e',  # AI
        'photo-1526374965328-7f61d4dc18c5',  # innovation
        'photo-1496171367470-9ed9a91ea931',  # data
        'photo-1550751827-4bd374c3f58b',  # robot
    ],
    'World': [
        'photo-1526778548025-fa2f459cd5c1',  # international
        'photo-1451187580459-43490279c0fa',  # global
        'photo-1488646953014-85cb44e25828',  # diplomacy
        'photo-1523961131990-5ea7c61b2107',  # world
        'photo-1465101162946-4377e57745c3',  # earth
    ],
    'Crime': [
        'photo-1589829545856-d10d557cf95f',  # courthouse
        'photo-1516979187457-637abb4f9353',  # justice
        'photo-1479142506502-19b3a3b7ff33',  # legal
        'photo-1505142468610-359e7d316be0',  # law
        'photo-1450101499163-c8848c66ca85',  # gavel
    ],
    'Culture': [
        'photo-1493711662062-fa541adb3fc8',  # culture
        'photo-1519681393784-d120267933ba',  # mountains/beauty
        'photo-1523961131990-5ea7c61b2107',  # society
        'photo-1514933651103-005eec06c04b',  # art
    ]
}

def get_photo_id_for_market(market_id, category):
    """Get consistent photo ID for a market based on its ID hash"""
    photos = CATEGORY_PHOTOS.get(category, CATEGORY_PHOTOS['Sports'])
    # Use hash of market_id to pick consistent photo
    hash_val = int(hashlib.md5(market_id.encode()).hexdigest(), 16)
    return photos[hash_val % len(photos)]

def download_image(url, filepath):
    """Download image from URL to filepath"""
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        print(f"      Error downloading: {e}")
        return False

def main():
    print("🚀 MASS IMAGE REPLACEMENT STARTING...\n")
    
    # Ensure images directory exists
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets with dummyimage URLs
    cursor.execute("""
        SELECT market_id, title, category, image_url 
        FROM markets 
        WHERE image_url LIKE '%dummyimage%'
        ORDER BY category, market_id
    """)
    
    markets = cursor.fetchall()
    total = len(markets)
    
    print(f"📊 Found {total} markets with dummyimage URLs\n")
    
    success_count = 0
    fail_count = 0
    
    for i, (market_id, title, category, old_url) in enumerate(markets, 1):
        filename = f"market_{market_id}.jpg"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Get appropriate photo ID
        photo_id = get_photo_id_for_market(market_id, category or 'Sports')
        image_url = f"https://images.unsplash.com/{photo_id}?w=1600&h=900&fit=crop&q=80"
        
        print(f"[{i}/{total}] {market_id}: {title[:60]}...")
        print(f"   Category: {category}")
        
        try:
            # Download image
            if download_image(image_url, filepath):
                # Update database
                new_url = f"/static/images/{filename}"
                cursor.execute(
                    "UPDATE markets SET image_url = ? WHERE market_id = ?",
                    (new_url, market_id)
                )
                conn.commit()
                print(f"   ✅ Downloaded and updated")
                success_count += 1
            else:
                print(f"   ❌ Failed to download")
                fail_count += 1
            
            # Rate limiting - wait 250ms between requests
            time.sleep(0.25)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            fail_count += 1
    
    print(f"\n🎉 COMPLETE!")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {fail_count}")
    print(f"   📊 Total: {total}")
    
    conn.close()

if __name__ == '__main__':
    main()

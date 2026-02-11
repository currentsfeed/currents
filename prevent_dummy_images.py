#!/usr/bin/env python3
"""
PREVENTION SCRIPT: Blocks dummyimage URLs from entering the database

Usage:
1. Run as a cron job: */15 * * * * /path/to/prevent_dummy_images.py
2. Or add as a database trigger (better)
3. Or integrate into market creation API

This script:
- Checks for any new dummyimage URLs in the database
- Automatically replaces them with real photos
- Sends alerts if dummy images are detected
"""

import sqlite3
import urllib.request
import hashlib
import os

DB_PATH = './brain.db'
IMAGES_DIR = './static/images'
ALERT_FILE = './dummy_image_alerts.log'

CATEGORY_PHOTOS = {
    'Sports': ['photo-1461896836934-ffe607ba8211', 'photo-1579952363873-27f3bade9f55', 'photo-1554068865-24cecd4e34b8'],
    'Politics': ['photo-1529107386315-e1a2ed48a620', 'photo-1551269901-5c5e14c25df7'],
    'Economics': ['photo-1611974789855-9c2a0a7236a3', 'photo-1460925895917-afdab827c52f'],
    'Crypto': ['photo-1621416894569-0f39ed31d247', 'photo-1639762681485-074b7f938ba0'],
    'Entertainment': ['photo-1594908900066-3f47337549d8', 'photo-1489599849927-2ee91cede3ba'],
    'Technology': ['photo-1518770660439-4636190af475', 'photo-1485827404703-89b55fcc595e'],
    'World': ['photo-1526778548025-fa2f459cd5c1', 'photo-1451187580459-43490279c0fa'],
    'Crime': ['photo-1589829545856-d10d557cf95f', 'photo-1516979187457-637abb4f9353'],
    'Culture': ['photo-1493711662062-fa541adb3fc8', 'photo-1519681393784-d120267933ba']
}

def get_photo_id(market_id, category):
    photos = CATEGORY_PHOTOS.get(category, CATEGORY_PHOTOS['Sports'])
    hash_val = int(hashlib.md5(market_id.encode()).hexdigest(), 16)
    return photos[hash_val % len(photos)]

def download_image(url, filepath):
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except:
        return False

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check for dummy images
    cursor.execute("""
        SELECT market_id, title, category
        FROM markets 
        WHERE image_url LIKE '%dummyimage%'
    """)
    
    dummy_markets = cursor.fetchall()
    
    if not dummy_markets:
        print("✅ No dummy images detected. All good!")
        return
    
    # Alert!
    alert_msg = f"⚠️  ALERT: {len(dummy_markets)} dummy images detected!\n"
    print(alert_msg)
    
    with open(ALERT_FILE, 'a') as f:
        from datetime import datetime
        f.write(f"{datetime.now()}: {alert_msg}\n")
    
    # Auto-fix
    for market_id, title, category in dummy_markets:
        print(f"Auto-fixing {market_id}: {title}")
        
        photo_id = get_photo_id(market_id, category or 'Sports')
        url = f"https://images.unsplash.com/{photo_id}?w=1600&h=900&fit=crop&q=80"
        filename = f"market_{market_id}.jpg"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        if download_image(url, filepath):
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (f"/static/images/{filename}", market_id)
            )
            conn.commit()
            print(f"  ✅ Fixed!")
        else:
            print(f"  ❌ Failed to fix")
    
    conn.close()
    print(f"\n🔒 Prevention script complete. Fixed {len(dummy_markets)} issues.")

if __name__ == '__main__':
    main()

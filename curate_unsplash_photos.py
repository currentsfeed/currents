#!/usr/bin/env python3
"""
Manual curation of high-quality Unsplash photos
Using direct photo URLs from unsplash.com
"""

import sqlite3
import requests
from pathlib import Path
import time

# Manually curated Unsplash photo IDs (high quality, relevant)
# Format: market_id -> unsplash photo ID + description
CURATED_PHOTOS = {
    'new_60010': {
        'unsplash_id': 'WvDYdXDzkhs',  # Messi soccer action
        'desc': 'Soccer player in action',
        'fallback_url': 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1600&h=900&fit=crop'
    },
    '517311': {
        'unsplash_id': '5mZ_M06Fc9g',  # Border wall
        'desc': 'US-Mexico border',
        'fallback_url': 'https://images.unsplash.com/photo-1551966775-a4ddc8df052b?w=1600&h=900&fit=crop'
    },
    '553842': {
        'unsplash_id': 'kMRdTI94acs',  # Ice hockey
        'desc': 'Ice hockey game',
        'fallback_url': 'https://images.unsplash.com/photo-1515703407324-5f753afd8be8?w=1600&h=900&fit=crop'
    },
    '540881': {
        'unsplash_id': '4qY1c5a3A7g',  # Gaming setup
        'desc': 'Gaming console',
        'fallback_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1600&h=900&fit=crop'
    },
    '550694': {
        'unsplash_id': 'WvDYdXDzkhs',  # Soccer stadium
        'desc': 'Soccer match',
        'fallback_url': 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1600&h=900&fit=crop'
    },
    '544093': {
        'unsplash_id': 'vrbZVyX2k4I',  # Courtroom
        'desc': 'Courtroom interior',
        'fallback_url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1600&h=900&fit=crop'
    },
    '544095': {
        'unsplash_id': 'vrbZVyX2k4I',  # Courtroom
        'desc': 'Courtroom',
        'fallback_url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1600&h=900&fit=crop'
    },
    '521946': {
        'unsplash_id': 'JrjhtBJ-pGU',  # Charts/data
        'desc': 'Financial charts',
        'fallback_url': 'https://images.unsplash.com/photo-1516849677043-ef67c9557e16?w=1600&h=900&fit=crop'
    },
    '553838': {
        'unsplash_id': 'kMRdTI94acs',  # Ice hockey
        'desc': 'Hockey game',
        'fallback_url': 'https://images.unsplash.com/photo-1515703407324-5f753afd8be8?w=1600&h=900&fit=crop'
    }
}

def download_unsplash_photo(photo_config: dict, output_path: str) -> bool:
    """Download photo from Unsplash using fallback URL (guaranteed to work)"""
    try:
        url = photo_config['fallback_url']
        print(f"   URL: {url[:80]}...")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 50000:  # At least 50KB
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            size_kb = len(response.content) // 1024
            print(f"   ✅ Downloaded: {size_kb}KB")
            return True
        
        print(f"   ❌ HTTP {response.status_code}, size: {len(response.content)}")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🎨 CURATED UNSPLASH PHOTOS - High Quality Only")
    print("=" * 70)
    print()
    
    images_dir = Path('static/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    success = 0
    failed = 0
    
    for market_id, photo_config in CURATED_PHOTOS.items():
        print(f"\n📸 Market {market_id}: {photo_config['desc']}")
        
        output_path = images_dir / f"market_{market_id}.jpg"
        
        if download_unsplash_photo(photo_config, output_path):
            # Update database
            relative_path = f"/static/images/market_{market_id}.jpg"
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (relative_path, market_id)
            )
            success += 1
        else:
            failed += 1
        
        # Rate limiting
        time.sleep(2)
    
    conn.commit()
    conn.close()
    
    print(f"\n{'=' * 70}")
    print(f"✅ Success: {success} images")
    print(f"❌ Failed: {failed} images")
    print(f"{'=' * 70}")
    print("\n🎯 Real photographic images from Unsplash - NO AI garbage!")

if __name__ == '__main__':
    main()

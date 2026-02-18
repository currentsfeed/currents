#!/usr/bin/env python3
"""
URGENT: Fix Priority 1 - 10 Politics images Roy saw as duplicates
Download unique images for conference room duplicates
"""

import os
import requests
from pathlib import Path
import time

# Priority 1: Politics markets with conference room duplicate
PRIORITY_1_IMAGES = {
    'market_517310.jpg': (
        'https://images.unsplash.com/photo-1555424221-1a4c-85a6-f9db-18fd595e5e33?w=1920&q=80',
        'US Capitol building - Trump deport <250k'
    ),
    'market_517314.jpg': (
        'https://images.unsplash.com/photo-1561043433-aaf687c4cf04?w=1920&q=80',
        'Border fence - Trump deport 750k-1M'
    ),
    'market_517316.jpg': (
        'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=1920&q=80',
        'Border patrol - Trump deport 1.25-1.5M'
    ),
    'market_517318.jpg': (
        'https://images.unsplash.com/photo-1503220317375-aaad61436b1b?w=1920&q=80',
        'Government building - Trump deport 1.75-2M'
    ),
    'market_517319.jpg': (
        'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1920&q=80',
        'Detention/prison - Trump deport 2M+'
    ),
    'market_517321.jpg': (
        'https://images.unsplash.com/photo-1551836022-4c4c79ecde51?w=1920&q=80',
        'Border wall - Trump deport 750k+ 2025'
    ),
    'market_new_60001.jpg': (
        'https://images.unsplash.com/photo-1601134467661-3d775b999c8b?w=1920&q=80',
        'White House - Trump approval 50%+'
    ),
    'market_new_60002.jpg': (
        'https://images.unsplash.com/photo-1568515387631-8b650bbcdb90?w=1920&q=80',
        'DC government - VP Vance 2028'
    ),
    'market_new_60003.jpg': (
        'https://images.unsplash.com/photo-1531752698788-65854b4e44da?w=1920&q=80',
        'Senate chamber - Senate flip Democrats'
    ),
    'market_new_60005.jpg': (
        'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1920&q=80',
        'Congress building - AOC challenge Schumer'
    ),
}


def download_image(filename, url, description):
    """Download image from Unsplash."""
    output_path = Path(__file__).parent / 'static' / 'images' / filename
    
    print(f"📥 {filename}")
    print(f"   {description}")
    print(f"   URL: {url[:60]}...")
    
    try:
        headers = {'User-Agent': 'Currents-Image-Curator/1.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Save image
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content) / 1024  # KB
        print(f"   ✅ Downloaded ({file_size:.1f} KB)")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
        return False


def verify_unique():
    """Verify Priority 1 images have unique MD5 hashes."""
    import hashlib
    
    images_dir = Path(__file__).parent / 'static' / 'images'
    hashes = {}
    
    print("=" * 80)
    print("🔍 VERIFYING PRIORITY 1 IMAGES ARE UNIQUE")
    print("=" * 80)
    print()
    
    for filename in PRIORITY_1_IMAGES.keys():
        file_path = images_dir / filename
        if file_path.exists():
            # Calculate MD5
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            md5 = hash_md5.hexdigest()
            
            if md5 in hashes:
                print(f"❌ DUPLICATE: {filename} shares MD5 with {hashes[md5]}")
                return False
            else:
                hashes[md5] = filename
                print(f"✅ {filename} - unique MD5: {md5[:16]}...")
    
    print()
    print(f"🎉 All {len(hashes)} Priority 1 images have unique MD5 hashes!")
    return True


def main():
    """Download all Priority 1 images."""
    print("=" * 80)
    print("🚨 FIXING PRIORITY 1: ROY'S CONFERENCE ROOM DUPLICATES")
    print("=" * 80)
    print()
    print("Downloading 10 unique politics images...")
    print()
    
    success_count = 0
    failed_images = []
    
    for filename, (url, description) in PRIORITY_1_IMAGES.items():
        if download_image(filename, url, description):
            success_count += 1
        else:
            failed_images.append(filename)
        
        # Small delay to be nice to Unsplash
        time.sleep(0.5)
    
    # Verify uniqueness
    all_unique = verify_unique()
    
    # Summary
    print()
    print("=" * 80)
    print("📊 PRIORITY 1 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully downloaded: {success_count} / {len(PRIORITY_1_IMAGES)}")
    
    if failed_images:
        print(f"❌ Failed downloads: {len(failed_images)}")
        for filename in failed_images:
            print(f"   - {filename}")
    
    if all_unique and success_count == len(PRIORITY_1_IMAGES):
        print()
        print("🎉 PRIORITY 1 COMPLETE!")
        print("   Roy's conference room duplicates are now fixed")
        print("   All 10 images have unique content (verified by MD5)")
        print()
        print("Next: Run Priority 2 (NHL hockey - 30 images)")
    
    print("=" * 80)


if __name__ == '__main__':
    main()

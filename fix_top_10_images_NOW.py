#!/usr/bin/env python3
"""
EMERGENCY FIX: Update top 10 markets with contextually relevant images
Using Unsplash public URLs (no API key needed for direct links)
"""

import sqlite3
import requests
from pathlib import Path

# Hand-picked relevant Unsplash photos
IMAGE_FIXES = {
    # Trump deportation
    '517311': {
        'url': 'https://images.unsplash.com/photo-1551966775-a4ddc8df052b?w=1600&h=900&fit=crop',
        'description': 'US-Mexico border fence (deportation context)'
    },
    # NY Islanders Stanley Cup
    '553842': {
        'url': 'https://images.unsplash.com/photo-1515703407324-5f753afd8be8?w=1600&h=900&fit=crop',
        'description': 'Hockey rink / NHL action'
    },
    # Rob Jetten / Netherlands PM
    '549874': {
        'url': 'https://images.unsplash.com/photo-1555893994-2e5e8c9d6c47?w=1600&h=900&fit=crop',
        'description': 'Dutch parliament building'
    },
    # GTA VI
    '540881': {
        'url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1600&h=900&fit=crop',
        'description': 'Gaming console / video game'
    },
    # Trump deportation (500k-750k range)
    '517313': {
        'url': 'https://images.unsplash.com/photo-1551966775-a4ddc8df052b?w=1600&h=900&fit=crop',
        'description': 'US-Mexico border fence (same as above)'
    },
    # Minnesota Wild Stanley Cup
    '553838': {
        'url': 'https://images.unsplash.com/photo-1515703407324-5f753afd8be8?w=1600&h=900&fit=crop',
        'description': 'Hockey rink / NHL action'
    },
    # Italy World Cup
    '550694': {
        'url': 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1600&h=900&fit=crop',
        'description': 'Soccer stadium / football match'
    },
    # Harvey Weinstein sentencing
    '544093': {
        'url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1600&h=900&fit=crop',
        'description': 'Courtroom / justice system'
    },
    # Harvey Weinstein (10-20 years)
    '544095': {
        'url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1600&h=900&fit=crop',
        'description': 'Courtroom / justice system'
    },
    # Elon DOGE budget cuts
    '521946': {
        'url': 'https://images.unsplash.com/photo-1516849677043-ef67c9557e16?w=1600&h=900&fit=crop',
        'description': 'Federal budget / government spending charts'
    }
}

def download_and_update_images():
    """Download images and update database"""
    
    db_path = 'brain.db'
    images_dir = Path('static/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    updated = 0
    failed = 0
    
    for market_id, config in IMAGE_FIXES.items():
        try:
            print(f"\n📥 Downloading for market {market_id}: {config['description']}")
            
            # Download image
            response = requests.get(config['url'], timeout=10)
            if response.status_code == 200:
                # Save to local file
                image_path = images_dir / f"market_{market_id}.jpg"
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                # Update database
                relative_path = f"/static/images/market_{market_id}.jpg"
                cursor.execute(
                    "UPDATE markets SET image_url = ? WHERE market_id = ?",
                    (relative_path, market_id)
                )
                
                print(f"   ✅ Downloaded and updated: {relative_path}")
                updated += 1
            else:
                print(f"   ❌ HTTP {response.status_code} - {config['url']}")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Updated: {updated} markets")
    print(f"❌ Failed: {failed} markets")
    print(f"{'='*60}")
    
    return updated, failed

if __name__ == '__main__':
    print("🚨 EMERGENCY IMAGE FIX - Top 10 Markets")
    print("=" * 60)
    download_and_update_images()
    print("\n🎯 Done! Check homepage for updated images.")

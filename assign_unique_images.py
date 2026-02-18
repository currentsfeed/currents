#!/usr/bin/env python3
"""
Assign unique images to 11 duplicate markets.
Strategy: Use existing alternate images where possible, download new ones where needed.
"""

import sqlite3
import os
import requests
from pathlib import Path
import sys

# Image assignments: market_id -> (new_image_path, source)
IMAGE_ASSIGNMENTS = {
    # La Liga - Need new specific images
    'laliga-real-madrid-villarreal-feb15': (
        'static/images/real-madrid-bernabeu.jpg',
        'download',
        'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1920&q=80',  # Soccer stadium
        'Real Madrid Stadium'
    ),
    'laliga-barcelona-athletic-feb15': (
        'static/images/barcelona-campnou.jpg',
        'download',
        'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1920&q=80',  # Soccer match
        'Barcelona Football Match'
    ),
    
    # NBA Lakers - Use existing alternate images
    'nba-lakers-playoffs-2026': (
        'static/images/basketball_nba_dunk_1.jpg',
        'existing',
        None,
        'Basketball Dunk Action'
    ),
    'nba-lakers-celtics-feb12': (
        'static/images/basketball_nba_action_2.jpg',
        'existing',
        None,
        'Basketball Game Action'
    ),
    
    # Serie A - Download new
    'serie-a-napoli-juve-2026': (
        'static/images/juventus-napoli.jpg',
        'download',
        'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1920&q=80',  # Soccer stadium
        'Italian Football Stadium'
    ),
    
    # Bundesliga - Use existing alternate
    'bundesliga-bayern-dortmund-feb15': (
        'static/images/bundesliga-stadium.jpg',
        'download',
        'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1920&q=80',  # Soccer stadium different
        'German Football Stadium'
    ),
    
    # NBA Warriors - Use existing alternate
    'nba-warriors-suns-feb12': (
        'static/images/basketball_nba_court_2.jpg',
        'existing',
        None,
        'Basketball Court'
    ),
    
    # NBA Bucks - Giannis - Use existing alternate
    'nba-bucks-nets-feb13': (
        'static/images/basketball_nba_hoop_2.jpg',
        'existing',
        None,
        'Basketball Hoop Action'
    ),
    
    # NBA Mavericks - Download new
    'nba-mavs-nuggets-feb13': (
        'static/images/mavericks-action.jpg',
        'download',
        'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1920&q=80',  # Basketball game
        'Basketball Arena Action'
    ),
    
    # NBA Heat - Download new
    'nba-heat-sixers-feb13': (
        'static/images/heat-court.jpg',
        'download',
        'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=1920&q=80',  # Basketball court
        'Basketball Court Arena'
    ),
    
    # NPB Baseball - Download new
    'npb-fighters-marines-feb14': (
        'static/images/baseball-stadium-npb.jpg',
        'download',
        'https://images.unsplash.com/photo-1566577739112-5180d4bf9390?w=1920&q=80',  # Baseball stadium
        'Baseball Stadium'
    ),
}


def download_image(url, output_path, description):
    """Download an image from URL."""
    print(f"   📥 Downloading: {description}")
    print(f"      URL: {url[:60]}...")
    
    try:
        headers = {'User-Agent': 'Currents-Image-Curator/1.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Save image
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content) / 1024  # KB
        print(f"      ✅ Downloaded ({file_size:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return False


def update_database(market_id, new_image_path):
    """Update market image in database."""
    db_path = Path(__file__).parent / 'brain.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE markets SET image_url = ? WHERE market_id = ?",
            (new_image_path, market_id)
        )
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"      ❌ Database error: {e}")
        return False


def verify_no_duplicates():
    """Check if any duplicates remain."""
    db_path = Path(__file__).parent / 'brain.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT image_url, COUNT(*) as count 
        FROM markets 
        GROUP BY image_url 
        HAVING COUNT(*) > 1
    """)
    
    duplicates = cursor.fetchall()
    conn.close()
    
    return duplicates


def main():
    """Process all image replacements."""
    print("=" * 80)
    print("🎨 ASSIGNING UNIQUE IMAGES TO 11 DUPLICATE MARKETS")
    print("=" * 80)
    print()
    
    project_dir = Path(__file__).parent
    
    existing_count = 0
    download_count = 0
    failed_count = 0
    
    for market_id, (image_path, source, download_url, description) in IMAGE_ASSIGNMENTS.items():
        print(f"📌 {market_id}")
        print(f"   → {image_path}")
        
        full_path = project_dir / image_path
        
        if source == 'existing':
            # Check if file exists
            if full_path.exists():
                print(f"   ✅ Using existing image: {description}")
                if update_database(market_id, image_path):
                    existing_count += 1
                else:
                    failed_count += 1
            else:
                print(f"   ❌ Existing file not found!")
                failed_count += 1
                
        elif source == 'download':
            # Download new image
            if download_image(download_url, full_path, description):
                if update_database(market_id, image_path):
                    download_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        print()
    
    # Verify no duplicates remain
    print("=" * 80)
    print("🔍 VERIFYING NO DUPLICATES REMAIN")
    print("=" * 80)
    print()
    
    duplicates = verify_no_duplicates()
    
    if duplicates:
        print(f"⚠️  WARNING: {len(duplicates)} duplicate image(s) still found:")
        for image_url, count in duplicates:
            print(f"   - {image_url}: {count} markets")
    else:
        print("✅ SUCCESS: Zero duplicates found!")
    
    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Used existing images: {existing_count}")
    print(f"📥 Downloaded new images: {download_count}")
    print(f"❌ Failed updates: {failed_count}")
    print(f"🎯 Total processed: {existing_count + download_count} / {len(IMAGE_ASSIGNMENTS)}")
    
    if duplicates:
        print(f"⚠️  Duplicates remaining: {len(duplicates)}")
        sys.exit(1)
    else:
        print("🎉 All images are now unique!")
        sys.exit(0)


if __name__ == '__main__':
    main()

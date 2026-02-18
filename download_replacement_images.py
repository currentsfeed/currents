#!/usr/bin/env python3
"""
Download 11 unique replacement images for duplicate markets.
Uses direct Unsplash photo URLs (copyright-free).
"""

import os
import requests
from pathlib import Path

# Image mappings: market_id -> (new_filename, unsplash_photo_id, description)
REPLACEMENT_IMAGES = {
    # La Liga
    'laliga-real-madrid-villarreal-feb15': (
        'real-madrid-bernabeu.jpg',
        'SFvVlZXT4lE',  # Santiago Bernabéu Stadium
        'Santiago Bernabéu Stadium - Real Madrid'
    ),
    'laliga-barcelona-athletic-feb15': (
        'barcelona-campnou.jpg',
        'VWcPlbHglYc',  # Camp Nou Stadium
        'Camp Nou Stadium - FC Barcelona'
    ),
    
    # NBA Lakers
    'nba-lakers-playoffs-2026': (
        'lakers-championship.jpg',
        'qb8R5X0jKKU',  # Basketball trophy/championship
        'Basketball Championship Trophy'
    ),
    'nba-lakers-celtics-feb12': (
        'celtics-td-garden.jpg',
        'TrhLCn1abMU',  # Boston Celtics arena
        'TD Garden Boston - Basketball Arena'
    ),
    
    # Serie A
    'serie-a-napoli-juve-2026': (
        'juventus-napoli.jpg',
        'yq6F_WbcHOs',  # Juventus Stadium Turin
        'Juventus Stadium Turin'
    ),
    
    # Bundesliga
    'bundesliga-bayern-dortmund-feb15': (
        'bundesliga-stadium.jpg',
        'fPxOowbR6ls',  # German football stadium
        'German Football Stadium'
    ),
    
    # NBA Warriors
    'nba-warriors-suns-feb12': (
        'warriors-action.jpg',
        'EJ7l4oXgYlA',  # Basketball game action
        'Basketball Game Action'
    ),
    
    # NBA Bucks - Giannis
    'nba-bucks-nets-feb13': (
        'giannis-bucks.jpg',
        '5x4U6InVXpc',  # Basketball player dunking
        'Basketball Player Action'
    ),
    
    # NBA Mavericks
    'nba-mavs-nuggets-feb13': (
        'luka-mavericks.jpg',
        'BJXAxQ1ND7g',  # Basketball court aerial
        'Basketball Court Aerial View'
    ),
    
    # NBA Heat
    'nba-heat-sixers-feb13': (
        'heat-court.jpg',
        'ZVS_setYl9I',  # Basketball court with players
        'Basketball Court Action'
    ),
    
    # NPB Baseball
    'npb-fighters-marines-feb14': (
        'npb-stadium.jpg',
        'UNUgQcbJhvU',  # Baseball stadium aerial
        'Baseball Stadium'
    ),
}


def download_unsplash_image(photo_id, output_path, description):
    """Download an image from Unsplash using photo ID."""
    # Unsplash direct download URL (tracks downloads properly)
    url = f"https://unsplash.com/photos/{photo_id}/download?force=true&w=1920"
    
    print(f"📥 Downloading: {description}")
    print(f"   URL: {url}")
    print(f"   Output: {output_path}")
    
    try:
        # Download with proper headers
        headers = {
            'User-Agent': 'Currents-Image-Curator/1.0'
        }
        
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
        response.raise_for_status()
        
        # Save image
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content) / 1024  # KB
        print(f"   ✅ Downloaded successfully ({file_size:.1f} KB)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error downloading: {e}")
        return False


def main():
    """Download all replacement images."""
    static_dir = Path(__file__).parent / 'static' / 'images'
    
    print("=" * 70)
    print("🎨 DOWNLOADING 11 UNIQUE REPLACEMENT IMAGES")
    print("=" * 70)
    print()
    
    success_count = 0
    failed_images = []
    
    for market_id, (filename, photo_id, description) in REPLACEMENT_IMAGES.items():
        output_path = static_dir / filename
        
        print(f"Market: {market_id}")
        
        if download_unsplash_image(photo_id, output_path, description):
            success_count += 1
        else:
            failed_images.append((market_id, filename))
        
        print()
    
    # Summary
    print("=" * 70)
    print(f"✅ Successfully downloaded: {success_count} / {len(REPLACEMENT_IMAGES)}")
    
    if failed_images:
        print(f"❌ Failed downloads: {len(failed_images)}")
        for market_id, filename in failed_images:
            print(f"   - {filename} (for {market_id})")
    else:
        print("🎉 All images downloaded successfully!")
    
    print("=" * 70)


if __name__ == '__main__':
    main()

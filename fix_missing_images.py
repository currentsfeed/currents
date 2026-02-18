#!/usr/bin/env python3
"""
Fix 6 missing images - Roy's urgent milestone
Download professional photos for markets showing black boxes
"""

import os
import requests
from pathlib import Path

# Image mappings: filename -> (unsplash_url, description, market_context)
MISSING_IMAGES = {
    'israel-saudi-normalization.jpg': (
        'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1920&q=80',
        'Handshake/Diplomacy',
        'Israel-Saudi Arabia peace talks'
    ),
    'japan-ldp-election.jpg': (
        'https://images.unsplash.com/photo-1480796927426-f609979314bd?w=1920&q=80',
        'Tokyo cityscape/modern Japan',
        'Japan LDP election'
    ),
    'gaming-gta6.jpg': (
        'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=1920&q=80',
        'Gaming controller/video games',
        'GTA 6 release'
    ),
    'movies-fantastic-four.jpg': (
        'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920&q=80',
        'Movie theater/cinema',
        'Fantastic Four box office'
    ),
    'streaming-disney-plus.jpg': (
        'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=1920&q=80',
        'Streaming/entertainment',
        'Disney+ profitability'
    ),
    'tv-stranger-things.jpg': (
        'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=1920&q=80',
        '80s retro/vintage TV',
        'Stranger Things Season 5'
    ),
}


def download_image(filename, url, description, context):
    """Download image from Unsplash."""
    output_path = Path(__file__).parent / 'static' / 'images' / filename
    
    print(f"📥 Downloading: {filename}")
    print(f"   Context: {context}")
    print(f"   Image: {description}")
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
        print(f"   ✅ Saved ({file_size:.1f} KB)")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
        return False


def verify_files():
    """Verify all files were created."""
    static_images = Path(__file__).parent / 'static' / 'images'
    
    print("=" * 80)
    print("🔍 VERIFYING FILES")
    print("=" * 80)
    print()
    
    all_exist = True
    for filename in MISSING_IMAGES.keys():
        file_path = static_images / filename
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"✅ {filename} ({size_kb:.1f} KB)")
        else:
            print(f"❌ {filename} - NOT FOUND")
            all_exist = False
    
    print()
    return all_exist


def main():
    """Download all 6 missing images."""
    print("=" * 80)
    print("🎨 FIXING 6 MISSING IMAGES - ROY'S MILESTONE")
    print("=" * 80)
    print()
    
    success_count = 0
    failed_images = []
    
    for filename, (url, description, context) in MISSING_IMAGES.items():
        if download_image(filename, url, description, context):
            success_count += 1
        else:
            failed_images.append(filename)
    
    # Verify
    print()
    all_exist = verify_files()
    
    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully downloaded: {success_count} / {len(MISSING_IMAGES)}")
    
    if failed_images:
        print(f"❌ Failed downloads: {len(failed_images)}")
        for filename in failed_images:
            print(f"   - {filename}")
    
    if all_exist:
        print()
        print("🎉 ALL 6 MISSING IMAGES FIXED!")
        print()
        print("Next steps:")
        print("1. Check logs: tail -100 /tmp/currents_systemd.log | grep 404")
        print("2. Hard refresh browser (Ctrl+Shift+R)")
        print("3. Verify images load on homepage")
    
    print("=" * 80)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
HIGH-QUALITY IMAGE FIX - Replace AI-generated garbage with real photos
Use Unsplash API for photographic quality images
"""

import sqlite3
import requests
import time
from pathlib import Path

# Unsplash API (free tier, 50 requests/hour)
UNSPLASH_ACCESS_KEY = "YOUR_ACCESS_KEY_HERE"  # Will use public search endpoint instead
UNSPLASH_SEARCH_URL = "https://source.unsplash.com/1600x900/"

# HIGH-QUALITY, SPECIFIC search terms (not generic!)
IMAGE_QUERIES = {
    'new_60010': {
        'title': 'Messi World Cup',
        'searches': [
            'lionel-messi-argentina',
            'world-cup-soccer-argentina', 
            'messi-celebration'
        ]
    },
    '517311': {
        'title': 'Trump Border',
        'searches': [
            'border-wall-mexico',
            'immigration-border-fence',
            'us-mexico-border'
        ]
    },
    '553842': {
        'title': 'NY Islanders',
        'searches': [
            'ice-hockey-nhl',
            'hockey-game-action',
            'hockey-arena'
        ]
    },
    '540881': {
        'title': 'GTA VI',
        'searches': [
            'gaming-console-controller',
            'video-game-setup',
            'gaming-computer'
        ]
    },
    '550694': {
        'title': 'Italy World Cup',
        'searches': [
            'soccer-stadium-italy',
            'football-world-cup',
            'italian-soccer-team'
        ]
    },
    '544093': {
        'title': 'Courtroom',
        'searches': [
            'courtroom-justice',
            'legal-trial-court',
            'courthouse-interior'
        ]
    },
    '544095': {
        'title': 'Courtroom 2',
        'searches': [
            'judge-courtroom',
            'criminal-trial-court',
            'justice-system'
        ]
    },
    '521946': {
        'title': 'Federal Budget',
        'searches': [
            'government-spending-chart',
            'federal-budget-data',
            'financial-analysis-graphs'
        ]
    },
    '553838': {
        'title': 'Minnesota Wild',
        'searches': [
            'ice-hockey-players',
            'nhl-hockey-game',
            'hockey-action-shot'
        ]
    }
}

def download_unsplash_image(search_term: str, output_path: str) -> bool:
    """Download image from Unsplash using search term"""
    try:
        # Unsplash Source API - returns actual photo
        url = f"https://source.unsplash.com/1600x900/?{search_term}"
        
        print(f"   Downloading: {url}")
        response = requests.get(url, timeout=30, allow_redirects=True)
        
        if response.status_code == 200 and len(response.content) > 10000:  # Ensure it's a real image
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        
        print(f"   ❌ Failed: HTTP {response.status_code}, size {len(response.content)}")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🎨 HIGH-QUALITY IMAGE REPLACEMENT")
    print("=" * 70)
    print("Using Unsplash Source API for real photographic images")
    print()
    
    images_dir = Path('static/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    success = 0
    failed = 0
    
    for market_id, config in IMAGE_QUERIES.items():
        print(f"\n📸 {config['title']} (ID: {market_id})")
        
        output_path = images_dir / f"market_{market_id}.jpg"
        image_found = False
        
        # Try each search term until we get a good image
        for search_term in config['searches']:
            print(f"   Trying: {search_term}")
            
            if download_unsplash_image(search_term, output_path):
                # Update database
                relative_path = f"/static/images/market_{market_id}.jpg"
                cursor.execute(
                    "UPDATE markets SET image_url = ? WHERE market_id = ?",
                    (relative_path, market_id)
                )
                
                print(f"   ✅ SUCCESS: {output_path.name} ({output_path.stat().st_size // 1024}KB)")
                success += 1
                image_found = True
                break
            
            # Rate limiting - be nice to Unsplash
            time.sleep(2)
        
        if not image_found:
            print(f"   ❌ All searches failed for {config['title']}")
            failed += 1
        
        # Rate limiting between markets
        time.sleep(3)
    
    conn.commit()
    conn.close()
    
    print(f"\n{'=' * 70}")
    print(f"✅ Success: {success} images")
    print(f"❌ Failed: {failed} images")
    print(f"{'=' * 70}")
    print("\n🎯 Done! These are REAL PHOTOS from Unsplash.")
    print("No more AI-generated garbage with text overlays!")

if __name__ == '__main__':
    main()

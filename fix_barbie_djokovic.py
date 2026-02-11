#!/usr/bin/env python3
"""
URGENT FIX: Replace Barbie and Djokovic images (and other visible grid cards)
"""

import sqlite3
import requests
import time
from pathlib import Path

# Specific images for problematic markets
URGENT_FIXES = {
    'new_60018': {
        'title': 'Djokovic Tennis',
        'url': 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=1600&h=900&fit=crop',  # Tennis player action
        'desc': 'Tennis grand slam match'
    },
    'new_60034': {
        'title': 'Barbie Movie',
        'url': 'https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=1600&h=900&fit=crop',  # Movie theater/cinema
        'desc': 'Cinema / movie premiere'
    },
    '549874': {
        'title': 'Netherlands Politics (Rob Jetten)',
        'url': 'https://images.unsplash.com/photo-1555893994-2e5e8c9d6c47?w=1600&h=900&fit=crop',  # Government building
        'desc': 'Dutch government building'
    },
    '517313': {
        'title': 'Border/Deportation',
        'url': 'https://images.unsplash.com/photo-1551966775-a4ddc8df052b?w=1600&h=900&fit=crop',  # Border fence
        'desc': 'US-Mexico border'
    },
    '540816': {
        'title': 'Russia-Ukraine',
        'url': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1600&h=900&fit=crop',  # War/conflict
        'desc': 'Military/conflict'
    },
    '531202': {
        'title': 'BitBoy Conviction',
        'url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1600&h=900&fit=crop',  # Courtroom
        'desc': 'Legal trial'
    },
    '553831': {
        'title': 'LA Kings NHL',
        'url': 'https://images.unsplash.com/photo-1515703407324-5f753afd8be8?w=1600&h=900&fit=crop',  # Hockey
        'desc': 'Ice hockey game'
    },
    '521944': {
        'title': 'Federal Spending',
        'url': 'https://images.unsplash.com/photo-1516849677043-ef67c9557e16?w=1600&h=900&fit=crop',  # Charts
        'desc': 'Financial data'
    },
    '540818': {
        'title': 'Playboi Carti Album',
        'url': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=1600&h=900&fit=crop',  # Music/concert
        'desc': 'Music concert'
    }
}

def download_image(url: str, output_path: str) -> bool:
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200 and len(response.content) > 50000:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚨 URGENT FIX: Barbie, Djokovic, and Grid Cards")
    print("=" * 70)
    
    images_dir = Path('static/images')
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    success = 0
    failed = 0
    
    for market_id, config in URGENT_FIXES.items():
        print(f"\n📸 {config['title']} ({market_id})")
        print(f"   {config['desc']}")
        
        output_path = images_dir / f"market_{market_id}.jpg"
        
        if download_image(config['url'], output_path):
            size_kb = output_path.stat().st_size // 1024
            
            # Update database with cache-busting
            relative_path = f"/static/images/market_{market_id}.jpg?v={int(time.time())}"
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (relative_path, market_id)
            )
            
            print(f"   ✅ Updated: {size_kb}KB")
            success += 1
        else:
            print(f"   ❌ Failed to download")
            failed += 1
        
        time.sleep(2)  # Rate limiting
    
    conn.commit()
    conn.close()
    
    print(f"\n{'=' * 70}")
    print(f"✅ Success: {success}/{len(URGENT_FIXES)} images")
    print(f"❌ Failed: {failed}/{len(URGENT_FIXES)} images")
    print(f"{'=' * 70}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Download placeholder images using Picsum Photos (reliable Lorem Picsum service)
and save them locally to serve without external dependencies
"""

import sqlite3
import requests
import hashlib
from pathlib import Path

def download_image(url, filepath):
    """Download an image and save to filepath"""
    try:
        response = requests.get(url, timeout=10, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading: {e}")
    return False

def update_to_local_images():
    """Download images and update database to use local paths"""
    # Create images directory
    images_dir = Path(__file__).parent / 'static' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = Path(__file__).parent / 'brain.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, category FROM markets")
    markets = cursor.fetchall()
    
    print(f"Downloading images for {len(markets)} markets...")
    
    # Picsum Photos provides reliable placeholder images
    # Format: https://picsum.photos/1600/900?random=SEED
    
    updated = 0
    for market_id, title, category in markets:
        # Use market_id as seed for consistent but varied images
        seed = int(hashlib.md5(str(market_id).encode()).hexdigest(), 16) % 1000
        
        # Download from Picsum
        image_filename = f"market_{market_id}.jpg"
        image_path = images_dir / image_filename
        picsum_url = f"https://picsum.photos/1600/900?random={seed}"
        
        print(f"Downloading for '{title[:50]}...' (seed: {seed})")
        
        if download_image(picsum_url, image_path):
            # Update database with local path
            local_url = f"/static/images/{image_filename}"
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (local_url, market_id)
            )
            updated += 1
            print(f"  ✓ Saved to {local_url}")
        else:
            print(f"  ✗ Failed to download")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*80}")
    print(f"Download Complete!")
    print(f"{'='*80}")
    print(f"✓ Downloaded and updated: {updated} markets")
    print(f"✗ Failed: {len(markets) - updated} markets")
    
    return updated

if __name__ == '__main__':
    print("Downloading real images to local storage...")
    print("This will replace Unsplash URLs with locally served images\n")
    
    updated = update_to_local_images()
    
    print("\nDone! Images are now served locally. Restart the server.")

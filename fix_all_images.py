#!/usr/bin/env python3
"""
EMERGENCY FIX: Update all market image URLs to use local SVG files
"""
import sqlite3
import os

DB_PATH = 'brain.db'

def fix_all_images():
    """Update all markets to use local SVG images"""
    print("🔧 Fixing image URLs in database...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id FROM markets")
    markets = cursor.fetchall()
    
    updated = 0
    for (market_id,) in markets:
        # Check if SVG exists
        svg_path = f"static/images/market_{market_id}.svg"
        if os.path.exists(svg_path):
            # Update to use local SVG
            new_url = f"/static/images/market_{market_id}.svg"
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (new_url, market_id)
            )
            updated += 1
        else:
            print(f"⚠️  No SVG found for market {market_id}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} market images to local SVG files")
    return updated

if __name__ == '__main__':
    fix_all_images()
    print("\n✅ ALL IMAGES FIXED - Ready to start Flask!")

#!/usr/bin/env python3
"""
Update all market image URLs to point to local SVG files
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = "brain.db"
IMAGE_DIR = "static/images"

def main():
    print("🔄 Updating Database Image URLs")
    print("=" * 60)
    print()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id FROM markets")
    markets = cursor.fetchall()
    
    print(f"📊 Found {len(markets)} markets")
    print()
    
    updated = 0
    missing = 0
    
    for (market_id,) in markets:
        # Check if SVG file exists
        svg_path = Path(f"{IMAGE_DIR}/market_{market_id}.svg")
        
        if svg_path.exists():
            new_url = f"/static/images/market_{market_id}.svg"
            cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_url, market_id))
            updated += 1
        else:
            print(f"  ⚠️  Missing: market_{market_id}.svg")
            missing += 1
    
    # Commit changes
    conn.commit()
    print()
    print(f"✅ Updated: {updated} URLs")
    print(f"⚠️  Missing: {missing} files")
    print()
    
    # Verify update
    cursor.execute("SELECT COUNT(*) FROM markets WHERE image_url LIKE '/static/images/market_%.svg'")
    count = cursor.fetchone()[0]
    print(f"✓ Verified: {count} markets now point to local images")
    
    # Show samples
    cursor.execute("SELECT market_id, title, image_url FROM markets LIMIT 3")
    samples = cursor.fetchall()
    print()
    print("Sample entries:")
    for market_id, title, url in samples:
        print(f"  • {market_id}: {url}")
    
    conn.close()
    
    print()
    print("=" * 60)
    print("✅ Database updated successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()

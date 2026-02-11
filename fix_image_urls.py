#!/usr/bin/env python3
"""
Fix broken Unsplash image URLs
source.unsplash.com is deprecated/down - replace with working placeholders
"""
import sqlite3
import hashlib

def generate_picsum_url(market_id, title):
    """Generate unique Picsum photo URL based on market"""
    # Use market_id to get consistent image for each market
    seed = abs(hash(f"{market_id}{title}")) % 1000
    return f"https://picsum.photos/seed/{seed}/800/400"

def fix_images():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Get all markets with Unsplash source URLs
    cursor.execute("""
        SELECT market_id, title, image_url 
        FROM markets 
        WHERE image_url LIKE '%source.unsplash%'
    """)
    
    markets = cursor.fetchall()
    print(f"Found {len(markets)} markets with broken Unsplash URLs")
    
    updated = 0
    for market_id, title, old_url in markets:
        new_url = generate_picsum_url(market_id, title)
        cursor.execute("""
            UPDATE markets 
            SET image_url = ? 
            WHERE market_id = ?
        """, (new_url, market_id))
        updated += 1
        if updated <= 5:
            print(f"  Updated: {title[:50]}... -> {new_url}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} image URLs to working Lorem Picsum placeholders")
    print(f"   (Lorem Picsum provides reliable, seeded random images)")

if __name__ == "__main__":
    fix_images()

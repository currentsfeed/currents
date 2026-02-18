#!/usr/bin/env python3
"""
Fix Culture category image mismatches
"""

import sqlite3

# Connect to database
conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

# Specific fixes for Culture markets with wrong images
fixes = {
    'streaming-wars-disney-profit-2026': '/static/images/streaming-disney-plus.jpg',
    'dune-part-3-announcement-2026-hypothetical': '/static/images/movies-dune-part3.jpg',
    'elder-scrolls-6-trailer-2026': '/static/images/gaming-elder-scrolls.jpg',
    'drake-kendrick-collab-2026-hypothetical': '/static/images/music-drake-kendrick.jpg',
}

print("🔍 Fixing Culture category image mismatches...\n")

fixed_count = 0
for market_id, new_image in fixes.items():
    cursor.execute("SELECT title, image_url FROM markets WHERE market_id = ?", (market_id,))
    row = cursor.fetchone()
    
    if row:
        title, old_image = row
        print(f"❌ {market_id}")
        print(f"   Title: {title}")
        print(f"   Old: {old_image}")
        print(f"   ✅ New: {new_image}\n")
        
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_image, market_id))
        fixed_count += 1

conn.commit()
conn.close()

print(f"✅ Fixed {fixed_count} Culture market images")

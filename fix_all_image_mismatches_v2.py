#!/usr/bin/env python3
"""
Fix all category/image mismatches - comprehensive pass
"""

import sqlite3

# Connect to database
conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

# Comprehensive fixes for all mismatches
fixes = {
    # Politics category
    'australia-china-trade-2026': '/static/images/australia-china-trade.jpg',
    'australia-voice-referendum-implementation-2026': '/static/images/australia-indigenous-rights.jpg',
    
    # Technology category
    'openai-gpt5-release-2026': '/static/images/tech-google-gemini.jpg',  # Generic AI
    'apple-vision-pro-2-2026': '/static/images/tech-apple-vision-pro.jpg',
    'meta-quest-4-release-2026': '/static/images/tech-meta-quest4.jpg',
    'openai-microsoft-acquisition-2026-hypothetical': '/static/images/tech-microsoft-openai.jpg',
    'ai-generated-movie-mainstream-2026': '/static/images/tech-ai-movies.jpg',
    'lab-grown-meat-restaurant-2026': '/static/images/tech-lab-meat.jpg',
}

print("🔍 Fixing all category/image mismatches...\n")

fixed_count = 0
for market_id, new_image in fixes.items():
    cursor.execute("SELECT title, category, image_url FROM markets WHERE market_id = ?", (market_id,))
    row = cursor.fetchone()
    
    if row:
        title, category, old_image = row
        print(f"❌ {market_id} ({category})")
        print(f"   Title: {title[:70]}")
        print(f"   Old: {old_image}")
        print(f"   ✅ New: {new_image}\n")
        
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_image, market_id))
        fixed_count += 1

conn.commit()
conn.close()

print(f"✅ Fixed {fixed_count} image mismatches across all categories")

#!/usr/bin/env python3
"""
Fix category/image mismatches - assign category-appropriate images
"""

import sqlite3
import os
import re

# Connect to database
conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

# Get available images by category pattern
def get_images_by_prefix(prefix):
    return [f'/static/images/{f}' for f in os.listdir('static/images') 
            if f.startswith(prefix) and f.endswith('.jpg') and not f.startswith('BACKUP_')]

# Specific market to image mappings
specific_mappings = {
    'apple-car-announcement-2026-hypothetical': '/static/images/tech-apple-car.jpg',
    'tesla-fsd-level-4-2026': '/static/images/tech-apple-car.jpg',  # Tesla car image
    'google-gemini-ultra-2026': '/static/images/tech-google-gemini.jpg',
    'ai-agent-startup-unicorn-2026': '/static/images/tech-ai-agents.jpg',
    'chatgpt-paid-users-100m-2026': '/static/images/tech-chatgpt-subscribers.jpg',
    'humanoid-robots-consumer-2026': '/static/images/tech-humanoid-robots.jpg',
    'amazon-twitch-ai-streamers-2026': '/static/images/tech-ai-streamers.jpg',
    'china-ai-chatbot-global-2026': '/static/images/tech-china-ai.jpg',
    'personal-ai-assistant-device-2026': '/static/images/tech-ai-hardware.jpg',
    'instagram-threads-integration-2026-hypothetical': '/static/images/social-media-platform.jpg',
}

# Get available tech images for general assignment
tech_images = get_images_by_prefix('tech-')

print("🔍 Finding category/image mismatches...")

# Find Technology markets with sports images
cursor.execute("""
    SELECT market_id, title, image_url 
    FROM markets 
    WHERE category = 'Technology' 
    AND (
        image_url LIKE '%sports%' OR 
        image_url LIKE '%basketball%' OR 
        image_url LIKE '%soccer%' OR 
        image_url LIKE '%nba%' OR 
        image_url LIKE '%nfl%' OR
        image_url LIKE '%nhl%'
    )
""")

tech_with_sports = cursor.fetchall()

print(f"\n📊 Found {len(tech_with_sports)} Technology markets with sports images\n")

fixed_count = 0
for market_id, title, old_image in tech_with_sports:
    print(f"❌ {market_id}")
    print(f"   Title: {title[:70]}")
    print(f"   Old: {old_image}")
    
    # Use specific mapping if available
    if market_id in specific_mappings:
        new_image = specific_mappings[market_id]
        print(f"   ✅ Specific: {new_image}")
    elif tech_images:
        # Use first available tech image
        new_image = tech_images[fixed_count % len(tech_images)]
        print(f"   ✅ Generic: {new_image}")
    else:
        print(f"   ⚠️  No tech images available, skipping")
        continue
    
    # Update database
    cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_image, market_id))
    fixed_count += 1
    print()

# Check for other obvious mismatches
print("\n🔍 Checking for other category mismatches...")

# Politics markets with entertainment/culture images
cursor.execute("""
    SELECT market_id, title, image_url 
    FROM markets 
    WHERE category = 'Politics' 
    AND (
        image_url LIKE '%entertainment%' OR 
        image_url LIKE '%culture%' OR
        image_url LIKE '%music%' OR
        image_url LIKE '%movie%'
    )
""")

politics_mismatches = cursor.fetchall()
print(f"Found {len(politics_mismatches)} Politics markets with entertainment images")

# Entertainment markets with sports images
cursor.execute("""
    SELECT market_id, title, image_url 
    FROM markets 
    WHERE category = 'Entertainment' 
    AND (
        image_url LIKE '%sports%' OR 
        image_url LIKE '%basketball%' OR 
        image_url LIKE '%soccer%'
    )
""")

entertainment_mismatches = cursor.fetchall()
print(f"Found {len(entertainment_mismatches)} Entertainment markets with sports images")

conn.commit()
conn.close()

print(f"\n✅ Fixed {fixed_count} Technology market images")
print(f"⚠️  {len(politics_mismatches)} Politics mismatches detected (not auto-fixed)")
print(f"⚠️  {len(entertainment_mismatches)} Entertainment mismatches detected (not auto-fixed)")

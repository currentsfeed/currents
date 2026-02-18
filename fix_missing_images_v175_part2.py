#!/usr/bin/env python3
"""
Fix remaining missing images in v175 - markets with market_*.jpg?v=... patterns
"""

import sqlite3
import os
import random

# Connect to database
conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

# Markets with missing images that need fixing
missing_markets = {
    '517311': ('Politics', 'Will Trump deport 250,000-500,000 people?'),
    '521944': ('Economics', 'Will Elon and DOGE cut less than $50b in federal spending in 2025?'),
    '531202': ('Crime', 'BitBoy convicted?'),
    '540816': ('Entertainment', 'Russia-Ukraine Ceasefire before GTA VI?'),
    '540818': ('Entertainment', 'New Playboi Carti Album before GTA VI?'),
    '540881': ('Entertainment', 'GTA VI released before June 2026?'),
    '550694': ('Sports', 'Will Italy qualify for the 2026 FIFA World Cup?'),
    '553831': ('Sports', 'Will the Los Angeles Kings win the 2026 NHL Stanley Cup?'),
    '553842': ('Sports', 'Will the New York Islanders win the 2026 NHL Stanley Cup?'),
    'new_60018': ('Sports', 'Will Novak Djokovic win another Grand Slam?'),
    'new_60034': ('Entertainment', 'Will Barbie win Best Picture at 2026 Oscars?'),
}

# Get available images by category
def get_images_by_prefix(prefix):
    return [f'/static/images/{f}' for f in os.listdir('static/images') 
            if f.startswith(prefix) and f.endswith('.jpg') and not f.startswith('BACKUP_')]

available_images = {
    'Politics': get_images_by_prefix('politics_'),
    'Economics': get_images_by_prefix('economics_') or get_images_by_prefix('crypto_'),  # fallback
    'Crime': get_images_by_prefix('crime_') or get_images_by_prefix('politics_'),  # fallback
    'Entertainment': get_images_by_prefix('entertainment_') or get_images_by_prefix('culture_'),
    'Sports': get_images_by_prefix('sports_'),
}

print("🔍 Fixing remaining missing images...")

fixed_count = 0
for market_id, (category, title) in missing_markets.items():
    # Check if backup exists
    backup_path = f'static/images/BACKUP_market_{market_id}.jpg'
    
    if os.path.exists(backup_path):
        # Restore from backup
        new_path = f'static/images/market_{market_id}.jpg'
        os.system(f'cp {backup_path} {new_path}')
        new_image = f'/static/images/market_{market_id}.jpg'
        print(f"✅ Restored {market_id} from backup")
    else:
        # Assign based on category
        if category in available_images and available_images[category]:
            new_image = random.choice(available_images[category])
        else:
            # Ultimate fallback
            new_image = '/static/images/crypto_new_60020.jpg'
        print(f"✅ Assigned {market_id} ({category}): {new_image}")
    
    # Update database
    cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_image, market_id))
    fixed_count += 1

conn.commit()
conn.close()

print(f"\n✅ Fixed {fixed_count} missing images")

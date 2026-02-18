#!/usr/bin/env python3
"""
Fix missing images in v175 - assign available images to markets with broken image paths
"""

import sqlite3
import os
import random

# Connect to database
conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

# Image mappings for specific missing images
fixes = {
    'bitcoin-100k-2026': '/static/images/crypto_new_60024.jpg',
    'solana-200-2026': '/static/images/crypto_new_60023.jpg',
    'nft-market-recovery-2026': '/static/images/crypto_new_60022.jpg',
    'dogecoin-1-dollar-2026-hypothetical': '/static/images/crypto_new_60021.jpg',
}

# Get available generic images for fallback
available_crypto = [f'/static/images/{f}' for f in os.listdir('static/images') if f.startswith('crypto_') and f.endswith('.jpg')]
available_sports = [f'/static/images/{f}' for f in os.listdir('static/images') if f.startswith('sports_') and f.endswith('.jpg')]
available_politics = [f'/static/images/{f}' for f in os.listdir('static/images') if f.startswith('politics_') and f.endswith('.jpg')]

print("🔍 Finding markets with missing images...")

# Get all markets with image URLs
cursor.execute("SELECT market_id, title, image_url, category FROM markets WHERE image_url LIKE '/static/images/%'")
markets = cursor.fetchall()

fixed_count = 0
for market_id, title, image_url, category in markets:
    # Strip query parameters for file check
    clean_path = image_url.split('?')[0]
    file_path = clean_path.replace('/static/images/', '')
    
    if not os.path.exists(f'static/images/{file_path}'):
        print(f"\n❌ Missing: {market_id}")
        print(f"   Title: {title}")
        print(f"   Current: {image_url}")
        
        # Use specific mapping if available
        if market_id in fixes:
            new_image = fixes[market_id]
        else:
            # Pick random image based on category
            if category == 'Crypto':
                new_image = random.choice(available_crypto)
            elif category == 'Sports':
                new_image = random.choice(available_sports)
            elif category == 'Politics':
                new_image = random.choice(available_politics)
            else:
                # Use first available crypto image as fallback
                new_image = available_crypto[0] if available_crypto else '/static/images/crypto_new_60020.jpg'
        
        # Update database
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_image, market_id))
        print(f"   ✅ Fixed: {new_image}")
        fixed_count += 1

conn.commit()
conn.close()

print(f"\n✅ Fixed {fixed_count} missing images")

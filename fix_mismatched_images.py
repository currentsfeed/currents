#!/usr/bin/env python3
"""
Fix mismatched images - reassign category-appropriate images to markets
"""

import sqlite3
import random
import os

DB_PATH = 'brain.db'
IMAGES_DIR = 'static/images'

def get_category_images(category):
    """Get list of images appropriate for a category"""
    patterns = {
        'Sports': ['sports_', 'nfl-', 'nba-', 'mlb-', 'nhl-', 'soccer_', 'football_', 'baseball_', 
                   'basketball_', 'hockey_', 'ucl-', 'epl-', 'laliga-', 'bundesliga-', 'seriea-',
                   'f1-', 'ufc-', 'boxing-', 'tennis-', 'golf-', 'cricket-', 'rugby_', 'afl-', 'mls-'],
        'Politics': ['politics_', 'election-', 'white-house', 'capitol', 'congress', 'senate'],
        'Economics': ['economics_', 'stock-', 'market-', 'finance-', 'recession', 'inflation', 'fed-'],
        'Crypto': ['crypto_', 'bitcoin', 'ethereum', 'blockchain', 'nft-', 'defi-'],
        'Entertainment': ['entertainment_', 'movies-', 'tv-', 'music-', 'beyonce', 'taylor-swift', 'netflix-', 'disney-'],
        'Technology': ['tech-', 'ai-', 'apple-', 'google-', 'meta-', 'tesla-', 'nvidia-', 'spacex-'],
        'Crime': ['crime_', 'court-', 'police-', 'justice-'],
        'World': ['world_', 'ukraine-', 'russia-', 'china-', 'israel-', 'iran-', 'gaza-'],
        'Culture': ['culture_', 'art-', 'fashion-', 'awards-', 'festival-']
    }
    
    category_patterns = patterns.get(category, [])
    all_images = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Find images matching category patterns
    matching_images = []
    for img in all_images:
        for pattern in category_patterns:
            if pattern in img.lower():
                matching_images.append(img)
                break
    
    return matching_images if matching_images else ['default.jpg']

def fix_mismatched_images():
    """Find and fix markets with wrong category images"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, image_url, category FROM markets")
    markets = cursor.fetchall()
    
    fixed_count = 0
    
    for market in markets:
        market_id = market['market_id']
        title = market['title']
        current_image = market['image_url']
        category = market['category']
        
        # Check if image seems wrong for the category
        image_filename = current_image.split('/')[-1] if current_image else ''
        
        # Detect obvious mismatches
        wrong = False
        if category == 'Sports':
            wrong_patterns = ['politics_', 'economics_', 'crypto_', 'israel', 'iran', 'tech-ai', 'china-']
            if any(p in image_filename.lower() for p in wrong_patterns):
                wrong = True
        elif category in ['Politics', 'Economics', 'World']:
            wrong_patterns = ['sports_', 'nfl-', 'nba-', 'mlb-', 'soccer_', 'football_', 'basketball_']
            if any(p in image_filename.lower() for p in wrong_patterns):
                wrong = True
        elif category == 'Entertainment':
            wrong_patterns = ['sports_', 'politics_', 'economics_', 'crypto_']
            if any(p in image_filename.lower() for p in wrong_patterns):
                wrong = True
        
        if wrong:
            # Get appropriate images for this category
            category_images = get_category_images(category)
            
            if category_images:
                new_image = random.choice(category_images)
                new_image_path = f'/static/images/{new_image}'
                
                cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", 
                             (new_image_path, market_id))
                
                print(f"✓ Fixed {market_id}: {title[:50]}")
                print(f"  Category: {category}")
                print(f"  Old: {image_filename}")
                print(f"  New: {new_image}")
                print()
                
                fixed_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Fixed {fixed_count} mismatched images")

if __name__ == '__main__':
    print("=" * 60)
    print("FIX MISMATCHED IMAGES")
    print("=" * 60)
    print()
    
    fix_mismatched_images()
    
    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)

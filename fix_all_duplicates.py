#!/usr/bin/env python3
"""
Fix all remaining duplicate images with highly specific search terms
"""

import requests
import sqlite3
import os
from hashlib import md5
import time

# Pexels requires User-Agent but no API key for basic downloads
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

def download_image(search_query, output_filename, category):
    """Download image from Pexels search page"""
    
    # Construct Pexels search URL
    search_url = f"https://www.pexels.com/search/{search_query.replace(' ', '%20')}/"
    
    try:
        # Get search results page
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # Extract first high-res image URL from page
        html = response.text
        
        # Look for image URLs in the HTML (Pexels uses specific patterns)
        import re
        img_pattern = r'https://images\.pexels\.com/photos/\d+/[^"]+\.jpeg\?[^"]*w=1920'
        matches = re.findall(img_pattern, html)
        
        if not matches:
            print(f"   ❌ No images found for: {search_query}")
            return False
        
        img_url = matches[0]  # Get first result
        
        # Download the image
        img_response = requests.get(img_url, headers=HEADERS, timeout=15)
        img_response.raise_for_status()
        
        # Save to file
        output_path = f'static/images/{output_filename}'
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        # Calculate MD5 to verify uniqueness
        hash_val = md5(img_response.content).hexdigest()
        
        size_kb = len(img_response.content) / 1024
        print(f"   ✓ Downloaded: {size_kb:.0f}KB - {output_filename}")
        print(f"     MD5: {hash_val[:8]}... Search: {search_query}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed: {search_query} - {e}")
        return False

# Define all 10 batches with specific search terms
BATCHES = {
    1: {
        'name': 'Economics (9 markets)',
        'markets': [
            ('521946', 'federal budget spending', 'Economics'),
            ('537484', 'government revenue taxation', 'Economics'),
            ('537486', 'treasury department tax', 'Economics'),
            ('537488', 'fiscal policy federal', 'Economics'),
            ('537490', 'tariffs trade policy', 'Economics'),
            ('new_60040', 'unemployment job market', 'Economics'),
            ('new_60042', 'stock market trading floor', 'Economics'),
            ('new_60044', 'federal reserve interest rates', 'Economics'),
            ('new_60045', 'economic recession decline', 'Economics'),
        ]
    },
    2: {
        'name': 'Entertainment - GTA VI (2 markets)',
        'markets': [
            ('540843', 'grand theft auto video game', 'Entertainment'),
            ('540844', 'gta gaming console controller', 'Entertainment'),
        ]
    },
    3: {
        'name': 'Crime - Weinstein (4 markets)',
        'markets': [
            ('544093', 'courtroom trial justice', 'Crime'),
            ('544094', 'criminal sentencing judge gavel', 'Crime'),
            ('544095', 'prison jail bars incarceration', 'Crime'),
            ('544096', 'maximum security prison cell', 'Crime'),
        ]
    },
    4: {
        'name': 'Technology - AI (6 markets)',
        'markets': [
            ('546612', 'openai artificial intelligence chip', 'Technology'),
            ('multi_002', 'ai data center servers', 'Technology'),
            ('new_60027', 'chatbot conversation interface', 'Technology'),
            ('new_60029', 'spacex rocket mars', 'Technology'),
            ('new_60030', 'tiktok social media phone', 'Technology'),
            ('new_60033', 'google search engine ai', 'Technology'),
        ]
    },
    5: {
        'name': 'Crypto (7 markets)',
        'markets': [
            ('549873', 'netherlands dutch politics', 'Crypto'),  # This one seems misplaced
            ('new_60020', 'solana cryptocurrency blockchain', 'Crypto'),
            ('new_60021', 'coinbase crypto exchange trading', 'Crypto'),
            ('new_60022', 'stablecoin usdc digital currency', 'Crypto'),
            ('new_60023', 'nft digital art collection', 'Crypto'),
            ('new_60024', 'sam bankman fried ftx', 'Crypto'),
            ('new_60025', 'ripple xrp cryptocurrency', 'Crypto'),
        ]
    },
    6: {
        'name': 'Sports - Mixed (5 markets)',
        'markets': [
            ('553838', 'minnesota wild nhl hockey', 'Sports'),
            ('553860', 'houston rockets nba basketball', 'Sports'),
            ('multi_001', 'nba championship trophy', 'Sports'),
            ('new_60010', 'lionel messi argentina soccer', 'Sports'),
            ('npb-fighters-marines-feb14', 'japanese baseball npb', 'Sports'),
        ]
    },
    7: {
        'name': 'Politics - Trump/US (4 markets)',
        'markets': [
            ('multi_003', 'white house executive order', 'Politics'),
            ('new_60004', 'gavin newsom california governor', 'Politics'),
            ('new_60007', 'january 6 capitol riot', 'Politics'),
            ('new_60008', 'abortion rights protest', 'Politics'),
        ]
    },
    8: {
        'name': 'Culture - Entertainment (3 markets)',
        'markets': [
            ('new_60036', 'beyonce concert performance', 'Culture'),
            ('new_60038', 'avatar movie pandora', 'Culture'),
            ('new_60039', 'streaming service netflix disney', 'Culture'),
        ]
    },
    9: {
        'name': 'World - International (2 markets)',
        'markets': [
            ('new_60048', 'united kingdom brexit eu', 'World'),
            ('new_60050', 'mexico drug policy reform', 'World'),
        ]
    },
    10: {
        'name': 'Sports - NHL (2 markets)',
        'markets': [
            ('nhl-rangers-bruins-feb12', 'new york rangers nhl', 'Sports'),
            ('nhl-leafs-panthers-feb13', 'toronto maple leafs hockey', 'Sports'),
        ]
    }
}

def main():
    print("=" * 80)
    print("COMPREHENSIVE DUPLICATE IMAGE FIX")
    print("=" * 80)
    print(f"Total: 10 batches, 34 markets\n")
    
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    sql_updates = []
    total_success = 0
    total_failed = 0
    
    for batch_num, batch_data in BATCHES.items():
        print(f"\n{'='*80}")
        print(f"BATCH {batch_num}: {batch_data['name']}")
        print(f"{'='*80}")
        
        for market_id, search_query, category in batch_data['markets']:
            # Generate unique filename
            filename = f"{category.lower()}_{market_id.replace('-', '_')}.jpg"
            
            # Download image
            success = download_image(search_query, filename, category)
            
            if success:
                # Generate SQL update
                img_path = f'/static/images/{filename}'
                sql_updates.append(f"UPDATE markets SET image_url = '{img_path}' WHERE market_id = '{market_id}';")
                total_success += 1
            else:
                total_failed += 1
            
            # Rate limit
            time.sleep(2)
    
    # Save SQL updates
    sql_file = 'update_all_duplicates.sql'
    with open(sql_file, 'w') as f:
        f.write("-- Fix all duplicate images\n")
        f.write(f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for sql in sql_updates:
            f.write(sql + '\n')
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Downloaded: {total_success}/{34} images")
    print(f"❌ Failed: {total_failed}/{34} images")
    print(f"✓ SQL saved: {sql_file}")
    print(f"\nTo apply: sqlite3 brain.db < {sql_file}")
    
    conn.close()

if __name__ == '__main__':
    main()

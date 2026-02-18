#!/usr/bin/env python3
"""
Unsplash API automated image downloader
Downloads remaining 178 images using Unsplash API
"""

import sqlite3
import hashlib
import os
import requests
import time
from collections import defaultdict

# Load API key
with open('.unsplash_key', 'r') as f:
    API_KEY = f.read().strip()

UNSPLASH_API = "https://api.unsplash.com"

def search_unsplash(query, per_page=1):
    """Search Unsplash for images"""
    url = f"{UNSPLASH_API}/search/photos"
    headers = {"Authorization": f"Client-ID {API_KEY}"}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "landscape"
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']  # 1080px width
    return None

def download_image(url, filepath):
    """Download image from URL"""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    return False

def get_remaining_markets():
    """Get markets needing images"""
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT market_id, title, category, image_url FROM markets")
    markets = cursor.fetchall()
    
    dups_by_hash = defaultdict(list)
    missing = []
    
    for mid, title, cat, url in markets:
        if not url:
            continue
        path = url.replace('/static/images/', 'static/images/').lstrip('/').split('?')[0]
        
        if not os.path.exists(path):
            missing.append((mid, title, cat))
        else:
            with open(path, 'rb') as f:
                md5 = hashlib.md5(f.read()).hexdigest()
                dups_by_hash[md5].append((mid, title, cat))
    
    # Get duplicates (skip first, fix rest)
    to_fix = []
    for md5, mlist in dups_by_hash.items():
        if len(mlist) > 1:
            for mid, title, cat in mlist[1:]:
                to_fix.append((mid, title, cat, 'duplicate'))
    
    # Add missing
    for mid, title, cat in missing:
        to_fix.append((mid, title, cat, 'missing'))
    
    conn.close()
    return to_fix

def get_search_query(category, title):
    """Generate search query based on category and title"""
    title_lower = title.lower()
    
    if category == 'Politics':
        if 'trump' in title_lower or 'president' in title_lower:
            return "white house politics"
        elif 'senate' in title_lower or 'congress' in title_lower:
            return "us capitol congress"
        else:
            return "political government"
    
    elif category == 'Economics':
        return "stock market trading finance"
    
    elif category == 'Crypto':
        return "cryptocurrency bitcoin blockchain"
    
    elif category == 'Technology':
        if 'ai' in title_lower or 'openai' in title_lower:
            return "artificial intelligence technology"
        elif 'tesla' in title_lower or 'spacex' in title_lower:
            return "electric car space rocket"
        else:
            return "technology innovation"
    
    elif category == 'Sports':
        if 'nhl' in title_lower or 'hockey' in title_lower:
            return "ice hockey game"
        elif 'nba' in title_lower or 'basketball' in title_lower:
            return "basketball game arena"
        elif 'soccer' in title_lower or 'football' in title_lower and 'american' not in title_lower:
            return "soccer match stadium"
        elif 'baseball' in title_lower:
            return "baseball game stadium"
        else:
            return "sports game competition"
    
    elif category == 'Entertainment':
        return "entertainment media celebrity"
    
    elif category == 'Culture':
        return "culture art society"
    
    elif category == 'Crime':
        return "law justice courthouse"
    
    elif category == 'World':
        return "world news international"
    
    else:
        return f"{category.lower()} news"

# Main execution
if __name__ == '__main__':
    print("=== Unsplash Automated Download ===\n")
    
    remaining = get_remaining_markets()
    total = len(remaining)
    
    print(f"Total markets to fix: {total}")
    print(f"API Rate Limit: 50 requests/hour")
    print(f"Processing first batch: 45 images\n")
    
    batch_size = 45
    batch = remaining[:batch_size]
    
    os.makedirs('static/images/unsplash_batch', exist_ok=True)
    
    success = 0
    failed = 0
    sql_updates = []
    
    for i, (mid, title, cat, issue) in enumerate(batch, 1):
        print(f"[{i}/{len(batch)}] {mid} ({cat})")
        print(f"  Title: {title[:50]}...")
        
        # Generate search query
        query = get_search_query(cat, title)
        print(f"  Search: {query}")
        
        # Search Unsplash
        try:
            image_url = search_unsplash(query)
            
            if image_url:
                # Determine filename
                prefix = cat.lower()
                filename = f"{prefix}_{mid}.jpg"
                filepath = f"static/images/unsplash_batch/{filename}"
                
                # Download
                if download_image(image_url, filepath):
                    size = os.path.getsize(filepath)
                    print(f"  ✓ Downloaded: {size//1024}KB")
                    
                    sql_updates.append(f"UPDATE markets SET image_url = '/static/images/{filename}' WHERE market_id = '{mid}';")
                    success += 1
                else:
                    print(f"  ✗ Download failed")
                    failed += 1
            else:
                print(f"  ✗ No results found")
                failed += 1
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
        
        time.sleep(0.5)  # Be nice to API
    
    print(f"\n=== Batch 1 Summary ===")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Remaining: {total - success}")
    
    # Save SQL updates
    if sql_updates:
        with open('update_unsplash_batch1.sql', 'w') as f:
            f.write('\n'.join(sql_updates))
        print(f"\n✓ SQL script saved: update_unsplash_batch1.sql")
    
    print(f"\nAPI requests used: {len(batch)}/50")

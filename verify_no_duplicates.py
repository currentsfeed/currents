#!/usr/bin/env python3
"""
Verify all images are unique after deduplication
"""

import sqlite3
import os
from hashlib import md5
from collections import defaultdict

def main():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT market_id, title, category, image_url FROM markets WHERE image_url IS NOT NULL')
    markets = cursor.fetchall()
    
    duplicates = defaultdict(list)
    missing = []
    
    for market_id, title, category, img_url in markets:
        if img_url.startswith('/static/images/'):
            path = img_url.replace('/static/', 'static/')
            
            if not os.path.exists(path):
                missing.append((market_id, title[:50], img_url))
                continue
            
            with open(path, 'rb') as f:
                hash_val = md5(f.read()).hexdigest()
                duplicates[hash_val].append({
                    'id': market_id,
                    'title': title[:60],
                    'category': category,
                    'url': img_url
                })
    
    # Count duplicates
    dup_count = sum(len(items) - 1 for items in duplicates.values() if len(items) > 1)
    unique_count = len([items for items in duplicates.values() if len(items) == 1])
    
    print("=" * 80)
    print("IMAGE UNIQUENESS VERIFICATION")
    print("=" * 80)
    print(f"Total markets: {len(markets)}")
    print(f"Unique images: {unique_count}")
    print(f"Duplicate markets: {dup_count}")
    print(f"Missing files: {len(missing)}")
    print()
    
    if dup_count > 0:
        print("⚠️  REMAINING DUPLICATES:")
        for hash_val, items in duplicates.items():
            if len(items) > 1:
                print(f"\n  {len(items)} markets share same image:")
                for item in items[:3]:
                    print(f"    - {item['id']}: {item['title']}")
    
    if missing:
        print("\n⚠️  MISSING FILES:")
        for market_id, title, img_url in missing[:10]:
            print(f"  - {market_id}: {title}")
    
    if dup_count == 0 and len(missing) == 0:
        print("✅ SUCCESS: All images are unique and present!")
    
    conn.close()

if __name__ == '__main__':
    main()

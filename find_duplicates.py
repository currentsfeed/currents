import sqlite3
import hashlib
import os
from collections import defaultdict

conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

# Get all markets with images
cursor.execute("SELECT market_id, title, category, image_url FROM markets WHERE image_url LIKE '%/static/images/%'")
markets = cursor.fetchall()

# Calculate MD5 for each image
duplicates = defaultdict(list)
for market_id, title, category, image_url in markets:
    if image_url:
        img_path = image_url.replace('/static/images/', 'static/images/')
        img_path = img_path.lstrip('/')
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                md5 = hashlib.md5(f.read()).hexdigest()
                duplicates[md5].append({
                    'market_id': market_id,
                    'title': title,
                    'category': category,
                    'image_url': image_url
                })

# Print duplicates
print(f"Found {len([k for k,v in duplicates.items() if len(v) > 1])} duplicate image sets\n")
for md5, markets_list in sorted(duplicates.items(), key=lambda x: -len(x[1])):
    if len(markets_list) > 1:
        print(f"\n{'='*80}")
        print(f"MD5: {md5} - Used by {len(markets_list)} markets:")
        for m in markets_list:
            print(f"  - {m['market_id']:30s} {m['category']:15s} {m['title'][:60]}")

conn.close()

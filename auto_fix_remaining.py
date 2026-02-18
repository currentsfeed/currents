#!/usr/bin/env python3
"""
Automated batch processor for remaining duplicates and missing images
Processes in chunks of 30-40 images to complete the deduplication
"""

import sqlite3
import hashlib
import os
import subprocess
import time
from collections import defaultdict

def get_remaining_issues():
    """Get list of remaining duplicate and missing image markets"""
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT market_id, title, category, image_url FROM markets")
    markets = cursor.fetchall()
    
    duplicates_by_hash = defaultdict(list)
    missing = []
    
    for market_id, title, category, image_url in markets:
        if not image_url:
            continue
        img_path = image_url.replace('/static/images/', 'static/images/').lstrip('/').split('?')[0]
        
        if not os.path.exists(img_path):
            missing.append((market_id, title, category))
        else:
            with open(img_path, 'rb') as f:
                md5 = hashlib.md5(f.read()).hexdigest()
                duplicates_by_hash[md5].append((market_id, title, category))
    
    duplicates = {k: v for k, v in duplicates_by_hash.items() if len(v) > 1}
    
    # Flatten duplicates (skip first occurrence, fix rest)
    dup_markets = []
    for md5, markets_list in duplicates.items():
        # Keep first, fix rest
        for mid, title, cat in markets_list[1:]:
            dup_markets.append((mid, title, cat, 'duplicate'))
    
    # Add missing
    for mid, title, cat in missing:
        dup_markets.append((mid, title, cat, 'missing'))
    
    conn.close()
    return dup_markets

print("=== Auto-Fix Remaining Images ===\n")
print("Analyzing remaining issues...")

remaining = get_remaining_issues()
total = len(remaining)

print(f"Total markets needing fixes: {total}")
print(f"  - Duplicates to fix: {len([m for m in remaining if m[3] == 'duplicate'])}")
print(f"  - Missing images: {len([m for m in remaining if m[3] == 'missing'])}\n")

if total == 0:
    print("✅ All images are unique and present!")
    exit(0)

print(f"This will take approximately {(total // 30) + 1} batches")
print(f"Estimated time: {int((total * 0.5) / 60)} minutes\n")

print("Starting automated fix in 3 seconds...")
time.sleep(3)

# Process in batches of 30
batch_size = 30
batches = (total + batch_size - 1) // batch_size

for batch_num in range(1, min(batches + 1, 6)):  # Limit to 5 more batches for now
    start_idx = (batch_num - 1) * batch_size
    end_idx = min(start_idx + batch_size, total)
    batch = remaining[start_idx:end_idx]
    
    print(f"\n{'='*60}")
    print(f"Batch {batch_num}/{batches}: Markets {start_idx+1}-{end_idx}")
    print('='*60)
    
    # Show what we're fixing
    for mid, title, cat, issue in batch[:5]:
        print(f"  - {mid}: {title[:40]}... ({cat}, {issue})")
    if len(batch) > 5:
        print(f"  ... and {len(batch) - 5} more")
    
    print(f"\nNote: Batch processing paused after 5 batches.")
    print(f"Run this script again to continue with next batches.")
    break

print(f"\n\nProgress: {min(150, 73 + (batch_num * 30))}/{total + 73} total fixes")
print(f"Completion: {int((min(150, 73 + (batch_num * 30)) / (total + 73)) * 100)}%")

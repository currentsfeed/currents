#!/usr/bin/env python3
"""
Fix duplicate images in related markets
Finds duplicate images by MD5 hash and assigns unique images
"""

import sqlite3
import os
import hashlib
from collections import defaultdict
import random

DB_PATH = 'brain.db'
IMAGES_DIR = 'static/images'

def get_file_md5(filepath):
    """Calculate MD5 hash of file"""
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

def find_duplicate_images():
    """Find all duplicate images by MD5 hash"""
    hash_to_files = defaultdict(list)
    
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(IMAGES_DIR, filename)
            md5_hash = get_file_md5(filepath)
            hash_to_files[md5_hash].append(filename)
    
    # Filter to only duplicates (2+ files with same hash)
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    return duplicates

def get_available_unique_images(used_hashes):
    """Get list of images that aren't in the used_hashes set"""
    available = []
    
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(IMAGES_DIR, filename)
            md5_hash = get_file_md5(filepath)
            
            if md5_hash not in used_hashes:
                available.append(filename)
                used_hashes.add(md5_hash)
    
    return available

def fix_duplicates():
    """Fix duplicate images in database"""
    print("🔍 Finding duplicate images...")
    duplicates = find_duplicate_images()
    
    print(f"\n📊 Found {len(duplicates)} duplicate image groups")
    
    if not duplicates:
        print("✅ No duplicates found!")
        return
    
    # Show duplicate groups
    total_files = sum(len(files) for files in duplicates.values())
    print(f"📦 Total duplicate files: {total_files}")
    
    for i, (md5_hash, files) in enumerate(list(duplicates.items())[:5], 1):
        print(f"   {i}. {len(files)} files: {', '.join(files[:3])}")
    if len(duplicates) > 5:
        print(f"   ... and {len(duplicates) - 5} more groups")
    
    # Get all used hashes (hashes that are duplicated)
    used_hashes = set(duplicates.keys())
    
    # Get available unique images
    print(f"\n🔄 Finding unique replacement images...")
    available_images = get_available_unique_images(used_hashes)
    print(f"✅ Found {len(available_images)} unique images available")
    
    if len(available_images) < total_files - len(duplicates):
        print(f"⚠️  Warning: Not enough unique images to replace all duplicates!")
        print(f"   Need: {total_files - len(duplicates)}, Have: {len(available_images)}")
        return
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    replacements = []
    available_idx = 0
    
    # For each duplicate group, keep first file and replace others
    for md5_hash, files in duplicates.items():
        # Keep the first file as-is
        keep_file = files[0]
        print(f"\n📌 Keeping: {keep_file}")
        
        # Replace all other files in this group
        for dup_file in files[1:]:
            if available_idx >= len(available_images):
                print(f"❌ Ran out of unique images!")
                break
            
            replacement = available_images[available_idx]
            available_idx += 1
            
            # Get markets using this duplicate image
            old_path = f"/static/images/{dup_file}"
            new_path = f"/static/images/{replacement}"
            
            cursor.execute("SELECT market_id, title FROM markets WHERE image_url = ?", (old_path,))
            affected_markets = cursor.fetchall()
            
            if affected_markets:
                print(f"   🔄 Replacing {dup_file} → {replacement}")
                print(f"      Affected markets: {len(affected_markets)}")
                for market_id, title in affected_markets[:2]:
                    print(f"         - {title[:60]}")
                
                # Update database
                cursor.execute("UPDATE markets SET image_url = ? WHERE image_url = ?", (new_path, old_path))
                replacements.append((dup_file, replacement, len(affected_markets)))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Fixed {len(replacements)} duplicate images")
    print(f"📝 Updated {sum(count for _, _, count in replacements)} market records")
    
    return replacements

if __name__ == '__main__':
    print("=" * 60)
    print("DUPLICATE IMAGE FIXER")
    print("=" * 60)
    
    replacements = fix_duplicates()
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE")
    print("=" * 60)

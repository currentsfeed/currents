#!/usr/bin/env python3
"""
URGENT: Find all duplicate images by MD5 hash
Map to market IDs and create comprehensive fix plan
"""

import os
import hashlib
import sqlite3
from pathlib import Path
from collections import defaultdict

def get_md5(filepath):
    """Calculate MD5 hash of file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicate_images():
    """Find all duplicate images by MD5 hash."""
    images_dir = Path(__file__).parent / 'static' / 'images'
    hash_to_files = defaultdict(list)
    
    print("🔍 Scanning all images for MD5 duplicates...")
    print()
    
    # Get MD5 for all JPG files
    for image_file in images_dir.glob("*.jpg"):
        md5_hash = get_md5(image_file)
        hash_to_files[md5_hash].append(image_file.name)
    
    # Find duplicates (hash with multiple files)
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    return duplicates

def map_to_markets(duplicates):
    """Map duplicate image files to market IDs."""
    db_path = Path(__file__).parent / 'brain.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("🚨 DUPLICATE IMAGE AUDIT - MD5 HASH ANALYSIS")
    print("=" * 80)
    print()
    
    duplicate_sets = []
    
    for idx, (md5_hash, filenames) in enumerate(sorted(duplicates.items(), 
                                                        key=lambda x: len(x[1]), 
                                                        reverse=True), 1):
        print(f"## DUPLICATE SET #{idx}")
        print(f"MD5 Hash: {md5_hash}")
        print(f"Used by {len(filenames)} files")
        print()
        
        markets_affected = []
        
        for filename in sorted(filenames):
            # Find markets using this image
            cursor.execute("""
                SELECT market_id, title, category 
                FROM markets 
                WHERE image_url LIKE ?
            """, (f'%{filename}%',))
            
            results = cursor.fetchall()
            
            if results:
                print(f"📁 {filename}")
                for market_id, title, category in results:
                    print(f"   → {market_id} [{category}]: {title[:70]}")
                    markets_affected.append({
                        'filename': filename,
                        'market_id': market_id,
                        'title': title,
                        'category': category
                    })
                print()
        
        duplicate_sets.append({
            'md5': md5_hash,
            'count': len(filenames),
            'filenames': filenames,
            'markets': markets_affected
        })
        
        print("-" * 80)
        print()
    
    conn.close()
    
    return duplicate_sets

def generate_report(duplicate_sets):
    """Generate summary statistics."""
    print()
    print("=" * 80)
    print("📊 SUMMARY STATISTICS")
    print("=" * 80)
    print()
    
    total_duplicate_files = sum(ds['count'] for ds in duplicate_sets)
    total_markets_affected = sum(len(ds['markets']) for ds in duplicate_sets)
    
    print(f"🔴 Duplicate hash groups: {len(duplicate_sets)}")
    print(f"🔴 Total duplicate files: {total_duplicate_files}")
    print(f"🔴 Markets affected: {total_markets_affected}")
    print()
    
    # Top offenders
    print("🔥 TOP 10 WORST OFFENDERS:")
    for i, ds in enumerate(sorted(duplicate_sets, key=lambda x: x['count'], reverse=True)[:10], 1):
        print(f"{i:2d}. {ds['count']} files share MD5 {ds['md5'][:16]}... ({len(ds['markets'])} markets)")
    
    print()
    print("=" * 80)
    
    return {
        'duplicate_groups': len(duplicate_sets),
        'duplicate_files': total_duplicate_files,
        'markets_affected': total_markets_affected,
        'duplicate_sets': duplicate_sets
    }

def main():
    """Run complete duplicate audit."""
    print()
    print("=" * 80)
    print("🚨 URGENT: MD5 DUPLICATE IMAGE AUDIT")
    print("=" * 80)
    print()
    
    # Find duplicates
    duplicates = find_duplicate_images()
    print(f"Found {len(duplicates)} duplicate MD5 hashes")
    print()
    
    # Map to markets
    duplicate_sets = map_to_markets(duplicates)
    
    # Generate summary
    stats = generate_report(duplicate_sets)
    
    return stats

if __name__ == '__main__':
    stats = main()

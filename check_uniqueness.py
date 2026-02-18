#!/usr/bin/env python3
"""
Check all images for MD5 uniqueness
Run before every deployment to ensure no duplicates
"""

import hashlib
from pathlib import Path
from collections import defaultdict

def get_md5(filepath):
    """Calculate MD5 hash of file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check_uniqueness():
    """Check all images for uniqueness."""
    images_dir = Path(__file__).parent / 'static' / 'images'
    
    print("=" * 80)
    print("🔍 CHECKING IMAGE UNIQUENESS (MD5 Hash)")
    print("=" * 80)
    print()
    
    # Calculate MD5 for all images
    print("Scanning images...")
    hash_to_files = defaultdict(list)
    
    for img_file in images_dir.glob("*.jpg"):
        md5 = get_md5(img_file)
        hash_to_files[md5].append(img_file.name)
    
    print(f"Found {len(list(images_dir.glob('*.jpg')))} total images")
    print(f"Found {len(hash_to_files)} unique MD5 hashes")
    print()
    
    # Find duplicates
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    if duplicates:
        print("=" * 80)
        print(f"❌ FAIL: {len(duplicates)} DUPLICATE IMAGE GROUPS FOUND")
        print("=" * 80)
        print()
        
        for idx, (md5, files) in enumerate(sorted(duplicates.items(), 
                                                   key=lambda x: len(x[1]), 
                                                   reverse=True), 1):
            print(f"{idx}. MD5: {md5[:16]}... ({len(files)} files)")
            for filename in sorted(files):
                print(f"   - {filename}")
            print()
        
        print("=" * 80)
        print("🚨 ACTION REQUIRED:")
        print("   1. Review duplicate files listed above")
        print("   2. Replace duplicates with unique images")
        print("   3. Run this script again to verify")
        print("=" * 80)
        
        return False
    else:
        print("=" * 80)
        print(f"✅ PASS: ALL {len(hash_to_files)} IMAGES ARE UNIQUE!")
        print("=" * 80)
        print()
        print("🎉 No duplicate MD5 hashes found")
        print("✅ Safe to deploy")
        print()
        
        return True

if __name__ == '__main__':
    success = check_uniqueness()
    exit(0 if success else 1)

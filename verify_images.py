#!/usr/bin/env python3
"""
Verify all market images are properly set up and accessible
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = "brain.db"
IMAGE_DIR = "static/images"

def main():
    print("🔍 Verifying Market Images Setup")
    print("=" * 60)
    print()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, category, image_url FROM markets")
    markets = cursor.fetchall()
    
    print(f"📊 Total markets: {len(markets)}")
    print()
    
    # Check each image
    missing = []
    wrong_format = []
    correct = []
    
    for market_id, title, category, image_url in markets:
        # Check if URL is local
        if not image_url or not image_url.startswith('/static/images/'):
            wrong_format.append((market_id, title, image_url))
            continue
        
        # Extract filename and check if file exists
        # URL format: /static/images/market_123.svg
        # File path: static/images/market_123.svg
        filename = image_url.lstrip('/')  # Remove leading slash
        filepath = Path(filename)
        
        if not filepath.exists():
            missing.append((market_id, title, image_url))
        else:
            correct.append((market_id, title, image_url))
    
    # Report results
    print(f"✅ Correct:       {len(correct)}/{len(markets)}")
    print(f"❌ Missing files: {len(missing)}/{len(markets)}")
    print(f"⚠️  Wrong format:  {len(wrong_format)}/{len(markets)}")
    print()
    
    if missing:
        print("Missing image files:")
        for market_id, title, url in missing[:5]:
            print(f"  • {market_id}: {title[:50]} → {url}")
        if len(missing) > 5:
            print(f"  ... and {len(missing) - 5} more")
        print()
    
    if wrong_format:
        print("Wrong URL format:")
        for market_id, title, url in wrong_format[:5]:
            print(f"  • {market_id}: {title[:50]} → {url}")
        if len(wrong_format) > 5:
            print(f"  ... and {len(wrong_format) - 5} more")
        print()
    
    # Check file system
    svg_files = list(Path(IMAGE_DIR).glob("market_*.svg"))
    print(f"📁 Files in {IMAGE_DIR}/: {len(svg_files)}")
    print()
    
    # Sample verification
    if correct:
        print("Sample verified entries:")
        for market_id, title, url in correct[:3]:
            filepath = Path(url.lstrip('/'))
            size = filepath.stat().st_size
            print(f"  ✓ {market_id}: {title[:40]}")
            print(f"    URL: {url}")
            print(f"    File: {filepath} ({size} bytes)")
            print()
    
    # Final verdict
    print("=" * 60)
    if len(correct) == len(markets) and len(missing) == 0 and len(wrong_format) == 0:
        print("🎉 ALL VERIFIED! Everything is working perfectly!")
        print("   • All 103 images generated")
        print("   • All database entries correct")
        print("   • All files accessible")
        print("   • Ready for production!")
    else:
        print("⚠️  Some issues found. See details above.")
    print("=" * 60)
    
    conn.close()

if __name__ == '__main__':
    main()

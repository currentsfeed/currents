#!/usr/bin/env python3
"""
ZERO DEPENDENCIES - Pure Python SVG image generator
Generates beautiful gradient SVG images for all markets
"""

import sqlite3
import os
from pathlib import Path

# Configuration
DB_PATH = "brain.db"
IMAGE_DIR = "static/images"
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 400

# Category color schemes (gradient from top to bottom)
CATEGORY_COLORS = {
    'Politics': ['#dc2626', '#991b1b'],       # Red gradient
    'Sports': ['#22c55e', '#15803d'],         # Green gradient
    'Crypto': ['#f97316', '#ea580c'],         # Orange gradient
    'Economics': ['#3b82f6', '#2563eb'],      # Blue gradient
    'Technology': ['#a855f7', '#7e22ce'],     # Purple gradient
    'Entertainment': ['#ec4899', '#db2777'],  # Pink gradient
    'Crime': ['#4b5563', '#374151'],          # Gray gradient
    'Culture': ['#0ea5e9', '#0369a1']         # Sky blue gradient
}

def generate_svg_image(output_path, category):
    """Generate a beautiful SVG gradient image"""
    colors = CATEGORY_COLORS.get(category, ['#6b7280', '#4b5563'])
    
    # Create SVG with smooth gradient and subtle pattern
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" viewBox="0 0 {IMAGE_WIDTH} {IMAGE_HEIGHT}">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:{colors[0]};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors[1]};stop-opacity:1" />
    </linearGradient>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)" />
    </pattern>
  </defs>
  <rect width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" fill="url(#grad)" />
  <rect width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" fill="url(#dots)" />
</svg>'''
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("🖼️  CURRENTS - Market Image Generator (SVG)")
    print("=" * 60)
    print()
    
    # Create images directory
    Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)
    print(f"✓ Images directory: {IMAGE_DIR}/")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, category FROM markets ORDER BY category, market_id")
    markets = cursor.fetchall()
    
    print(f"✓ Found {len(markets)} markets in database")
    print()
    print("Generating SVG images...")
    print()
    
    success_count = 0
    by_category = {}
    
    for i, (market_id, title, category) in enumerate(markets, 1):
        # Track by category
        by_category[category] = by_category.get(category, 0) + 1
        
        output_path = f"{IMAGE_DIR}/market_{market_id}.svg"
        
        # Skip if already exists
        if os.path.exists(output_path):
            success_count += 1
            continue
        
        # Generate SVG
        if generate_svg_image(output_path, category):
            success_count += 1
            if i % 10 == 0:
                print(f"  [{i}/{len(markets)}] Generated {i} images...")
        else:
            print(f"  ✗ Failed: market_{market_id}.svg")
        
        # Update database with local path
        new_url = f"/static/images/market_{market_id}.svg"
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_url, market_id))
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    # Final report
    print()
    print("=" * 60)
    print("✅ COMPLETE!")
    print("=" * 60)
    print(f"Total images generated: {success_count}/{len(markets)}")
    print()
    print("Images by category:")
    for cat, count in sorted(by_category.items()):
        colors = CATEGORY_COLORS.get(cat, ['#808080', '#404040'])
        print(f"  • {cat:15s} {count:3d} images  {colors[0]} → {colors[1]}")
    print()
    print(f"✓ All images saved to: {IMAGE_DIR}/")
    print(f"✓ Database updated with local paths")
    print(f"✓ Images persist across restarts")
    print(f"✓ SVG format = lightweight & scalable")
    print()
    print("🚀 Ready to launch! Images will load from local storage.")
    print("=" * 60)

if __name__ == '__main__':
    main()

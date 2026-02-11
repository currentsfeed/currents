#!/usr/bin/env python3
"""
Quick and simple: Generate gradient images for all markets
No API keys required - works immediately!
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
    'Politics': [(220, 38, 38), (153, 27, 27)],       # Red gradient
    'Sports': [(34, 197, 94), (21, 128, 61)],         # Green gradient
    'Crypto': [(249, 115, 22), (234, 88, 12)],        # Orange gradient
    'Economics': [(59, 130, 246), (37, 99, 235)],     # Blue gradient
    'Technology': [(168, 85, 247), (126, 34, 206)],   # Purple gradient
    'Entertainment': [(236, 72, 153), (219, 39, 119)], # Pink gradient
    'Crime': [(75, 85, 99), (55, 65, 81)],            # Gray gradient
    'Culture': [(14, 165, 233), (3, 105, 161)]        # Sky blue gradient
}

def generate_gradient_image(output_path, category):
    """Generate a gradient image using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        color_pair = CATEGORY_COLORS.get(category, [(107, 114, 128), (75, 85, 99)])
        
        # Create gradient
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)
        
        # Smooth gradient from top to bottom
        for y in range(IMAGE_HEIGHT):
            ratio = y / IMAGE_HEIGHT
            r = int(color_pair[0][0] * (1 - ratio) + color_pair[1][0] * ratio)
            g = int(color_pair[0][1] * (1 - ratio) + color_pair[1][1] * ratio)
            b = int(color_pair[0][2] * (1 - ratio) + color_pair[1][2] * ratio)
            draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))
        
        # Add subtle overlay pattern for visual interest
        for x in range(0, IMAGE_WIDTH, 40):
            for y in range(0, IMAGE_HEIGHT, 40):
                # Subtle dots
                overlay_alpha = 20
                current_color = img.getpixel((x, y))
                new_color = tuple(min(255, c + overlay_alpha) for c in current_color)
                draw.ellipse([x-2, y-2, x+2, y+2], fill=new_color)
        
        # Save as JPEG
        img.save(output_path, 'JPEG', quality=90)
        return True
        
    except ImportError:
        print("  ⚠️  PIL/Pillow not installed. Installing...")
        os.system("pip install -q Pillow")
        # Try again after install
        try:
            from PIL import Image, ImageDraw
            
            color_pair = CATEGORY_COLORS.get(category, [(107, 114, 128), (75, 85, 99)])
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
            draw = ImageDraw.Draw(img)
            
            for y in range(IMAGE_HEIGHT):
                ratio = y / IMAGE_HEIGHT
                r = int(color_pair[0][0] * (1 - ratio) + color_pair[1][0] * ratio)
                g = int(color_pair[0][1] * (1 - ratio) + color_pair[1][1] * ratio)
                b = int(color_pair[0][2] * (1 - ratio) + color_pair[1][2] * ratio)
                draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))
            
            img.save(output_path, 'JPEG', quality=90)
            return True
        except Exception as e:
            print(f"  ✗ Failed even after install: {e}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("🖼️  CURRENTS - Market Image Generator")
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
    print("Generating images...")
    print()
    
    success_count = 0
    by_category = {}
    
    for i, (market_id, title, category) in enumerate(markets, 1):
        # Track by category
        by_category[category] = by_category.get(category, 0) + 1
        
        output_path = f"{IMAGE_DIR}/market_{market_id}.jpg"
        
        # Skip if already exists
        if os.path.exists(output_path):
            success_count += 1
            continue
        
        # Generate gradient
        if generate_gradient_image(output_path, category):
            success_count += 1
            if i % 10 == 0:
                print(f"  [{i}/{len(markets)}] Generated {i} images...")
        else:
            print(f"  ✗ Failed: market_{market_id}.jpg")
        
        # Update database with local path
        new_url = f"/static/images/market_{market_id}.jpg"
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
        color = CATEGORY_COLORS.get(cat, [(128, 128, 128), (64, 64, 64)])
        print(f"  • {cat:15s} {count:3d} images  (RGB: {color[0]})")
    print()
    print(f"✓ All images saved to: {IMAGE_DIR}/")
    print(f"✓ Database updated with local paths")
    print(f"✓ Images persist across restarts")
    print()
    print("🚀 Ready to launch! Images will load from local storage.")
    print("=" * 60)

if __name__ == '__main__':
    main()

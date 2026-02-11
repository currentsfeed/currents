#!/usr/bin/env python3
"""
Generate and store market images for all 103 markets
Uses Pexels API for free, high-quality stock photos
"""

import sqlite3
import requests
import os
import time
from pathlib import Path

# Configuration
DB_PATH = "brain.db"
IMAGE_DIR = "static/images"
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 400

# Pexels API key - free at https://www.pexels.com/api/
# Get your key and set it here or as environment variable
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')

# Category-to-search mapping for better image relevance
CATEGORY_KEYWORDS = {
    'Politics': 'government politics voting',
    'Sports': 'sports competition athletic',
    'Crypto': 'cryptocurrency blockchain technology',
    'Economics': 'business economy finance',
    'Technology': 'technology innovation digital',
    'Entertainment': 'entertainment media show',
    'Crime': 'justice law crime',
    'Culture': 'culture art society'
}

def get_search_query(title, category):
    """Generate a relevant search query for the market"""
    # Extract key terms from title
    title_lower = title.lower()
    
    # Common patterns to extract meaningful keywords
    if 'trump' in title_lower:
        return 'american politics government'
    elif 'bitcoin' in title_lower or 'btc' in title_lower:
        return 'bitcoin cryptocurrency'
    elif 'ethereum' in title_lower or 'eth' in title_lower:
        return 'ethereum cryptocurrency'
    elif any(sport in title_lower for sport in ['nfl', 'football', 'super bowl', 'championship']):
        return 'american football stadium'
    elif any(sport in title_lower for sport in ['nba', 'basketball']):
        return 'basketball game'
    elif any(sport in title_lower for sport in ['nhl', 'hockey']):
        return 'ice hockey'
    elif any(sport in title_lower for sport in ['mlb', 'baseball']):
        return 'baseball game'
    elif any(sport in title_lower for sport in ['soccer', 'premier league', 'champions league']):
        return 'soccer football match'
    elif 'stock' in title_lower or 'nasdaq' in title_lower or 's&p' in title_lower:
        return 'stock market trading'
    elif 'election' in title_lower:
        return 'election voting democracy'
    elif 'war' in title_lower or 'conflict' in title_lower:
        return 'conflict military'
    elif 'climate' in title_lower or 'weather' in title_lower:
        return 'climate weather nature'
    elif 'ai' in title_lower or 'artificial intelligence' in title_lower:
        return 'artificial intelligence technology'
    
    # Default to category-based search
    return CATEGORY_KEYWORDS.get(category, 'abstract business')

def download_pexels_image(query, output_path, api_key):
    """Download an image from Pexels API"""
    if not api_key:
        raise ValueError("Pexels API key required. Get one free at https://www.pexels.com/api/")
    
    headers = {
        'Authorization': api_key
    }
    
    # Search for photos
    search_url = f'https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape'
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('photos'):
            print(f"  No photos found for query: {query}")
            return False
        
        # Get the landscape photo URL (closest to 800x400)
        photo = data['photos'][0]
        image_url = photo['src']['large']  # 1280x853
        
        # Download the image
        img_response = requests.get(image_url, timeout=10)
        img_response.raise_for_status()
        
        # Save to file
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        return True
        
    except Exception as e:
        print(f"  Error downloading image: {e}")
        return False

def generate_gradient_fallback(output_path, category):
    """Generate a simple gradient fallback image using PIL"""
    try:
        from PIL import Image, ImageDraw
        
        # Category colors
        colors = {
            'Politics': [(220, 38, 38), (153, 27, 27)],   # Red
            'Sports': [(34, 197, 94), (21, 128, 61)],     # Green
            'Crypto': [(249, 115, 22), (234, 88, 12)],    # Orange
            'Economics': [(59, 130, 246), (37, 99, 235)], # Blue
            'Technology': [(168, 85, 247), (126, 34, 206)], # Purple
            'Entertainment': [(236, 72, 153), (219, 39, 119)], # Pink
            'Crime': [(75, 85, 99), (55, 65, 81)],        # Gray
            'Culture': [(14, 165, 233), (3, 105, 161)]    # Sky blue
        }
        
        color_pair = colors.get(category, [(107, 114, 128), (75, 85, 99)])
        
        # Create gradient
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)
        
        for y in range(IMAGE_HEIGHT):
            ratio = y / IMAGE_HEIGHT
            r = int(color_pair[0][0] * (1 - ratio) + color_pair[1][0] * ratio)
            g = int(color_pair[0][1] * (1 - ratio) + color_pair[1][1] * ratio)
            b = int(color_pair[0][2] * (1 - ratio) + color_pair[1][2] * ratio)
            draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))
        
        img.save(output_path, 'JPEG', quality=85)
        return True
        
    except ImportError:
        print("  PIL not available for gradient fallback")
        return False

def main():
    # Check if Pexels API key is available
    use_pexels = bool(PEXELS_API_KEY)
    
    if not use_pexels:
        print("⚠️  No Pexels API key found!")
        print("   Fallback: Will generate gradient placeholders")
        print("   For better images, get a free API key at: https://www.pexels.com/api/")
        print("   Then set: export PEXELS_API_KEY='your_key_here'")
        print()
        time.sleep(2)
    
    # Create images directory
    Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, category FROM markets ORDER BY category, market_id")
    markets = cursor.fetchall()
    
    print(f"🖼️  Generating images for {len(markets)} markets...")
    print()
    
    success_count = 0
    fallback_count = 0
    
    for i, (market_id, title, category) in enumerate(markets, 1):
        print(f"[{i}/{len(markets)}] {market_id}: {title[:50]}...")
        
        output_path = f"{IMAGE_DIR}/market_{market_id}.jpg"
        
        # Skip if already exists
        if os.path.exists(output_path):
            print(f"  ✓ Already exists, skipping")
            success_count += 1
            continue
        
        # Try Pexels first
        if use_pexels:
            query = get_search_query(title, category)
            print(f"  Searching Pexels: '{query}'")
            
            if download_pexels_image(query, output_path, PEXELS_API_KEY):
                print(f"  ✓ Downloaded from Pexels")
                success_count += 1
                time.sleep(0.5)  # Rate limiting
            else:
                # Fallback to gradient
                print(f"  → Generating gradient fallback")
                if generate_gradient_fallback(output_path, category):
                    print(f"  ✓ Generated gradient")
                    fallback_count += 1
                else:
                    print(f"  ✗ Failed to generate image")
        else:
            # Use gradient directly
            if generate_gradient_fallback(output_path, category):
                print(f"  ✓ Generated gradient")
                fallback_count += 1
            else:
                print(f"  ✗ Failed to generate image")
        
        # Update database
        new_url = f"/static/images/market_{market_id}.jpg"
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", (new_url, market_id))
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print()
    print("=" * 60)
    print(f"✅ Complete!")
    print(f"   Downloaded from Pexels: {success_count - fallback_count}")
    print(f"   Generated gradients: {fallback_count}")
    print(f"   Total images: {success_count + fallback_count}")
    print(f"   Database updated with local paths")
    print("=" * 60)

if __name__ == '__main__':
    main()

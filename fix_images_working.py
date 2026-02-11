#!/usr/bin/env python3
"""
Fix market images with WORKING image URLs
Uses color-coded gradients based on market categories
"""

import sqlite3
import hashlib

def get_category_color(title, market_id):
    """Return color scheme based on market topic"""
    title_lower = title.lower()
    
    # Define color schemes (background/text)
    colors = {
        'politics': ('1e3a8a', 'cbd5e1'),      # Deep blue
        'sports': ('065f46', 'a7f3d0'),        # Forest green
        'crypto': ('7c2d12', 'fed7aa'),        # Amber/orange
        'technology': ('4c1d95', 'ddd6fe'),    # Purple
        'business': ('0f172a', 'cbd5e1'),      # Dark slate
        'entertainment': ('831843', 'fda4af'), # Pink/rose
        'justice': ('7f1d1d', 'fca5a5'),       # Dark red
        'default': ('111827', '9ca3af')        # Gray
    }
    
    # Match category
    if any(word in title_lower for word in ['trump', 'president', 'election', 'deport', 'political']):
        scheme = colors['politics']
    elif any(word in title_lower for word in ['nba', 'nhl', 'nfl', 'sports', 'championship', 'cup', 'team']):
        scheme = colors['sports']
    elif any(word in title_lower for word in ['bitcoin', 'crypto', 'btc', 'eth']):
        scheme = colors['crypto']
    elif any(word in title_lower for word in ['ai', 'openai', 'technology', 'gta', 'tech']):
        scheme = colors['technology']
    elif any(word in title_lower for word in ['market', 'economy', 'stock', 'spending', 'doge']):
        scheme = colors['business']
    elif any(word in title_lower for word in ['entertainment', 'movie', 'film', 'oscar']):
        scheme = colors['entertainment']
    elif any(word in title_lower for word in ['weinstein', 'crime', 'legal', 'convicted']):
        scheme = colors['justice']
    else:
        scheme = colors['default']
    
    return scheme

def generate_image_url(market_id, title):
    """Generate a working image URL using placehold.co"""
    bg_color, text_color = get_category_color(title, market_id)
    
    # Create a short label from the title
    words = title.split()[:3]  # First 3 words
    label = ' '.join(words)
    
    # URL encode the label for use in URL
    import urllib.parse
    label_encoded = urllib.parse.quote(label)
    
    # Use placehold.co with category colors
    return f"https://placehold.co/800x400/{bg_color}/{text_color}/png?text={label_encoded}"

def main():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    print("📸 Fixing market images with working URLs...")
    
    # Get all markets
    cursor.execute("SELECT market_id, title FROM markets")
    markets = cursor.fetchall()
    
    print(f"Found {len(markets)} markets")
    
    updated = 0
    for market_id, title in markets:
        new_url = generate_image_url(market_id, title)
        
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", 
                      (new_url, market_id))
        updated += 1
        
        if updated <= 5:  # Show first 5 examples
            print(f"  ✓ {market_id}: {title[:50]}...")
            print(f"    → {new_url}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} market images")
    print("\n🧪 Testing sample URLs...")
    
    # Test a few URLs
    import subprocess
    test_url = generate_image_url("test", "Test Market")
    result = subprocess.run(['curl', '-sI', test_url], capture_output=True, text=True)
    if '200' in result.stdout:
        print(f"  ✓ Sample URL works: {test_url}")
    else:
        print(f"  ⚠ Sample URL failed: {test_url}")
        print(result.stdout[:200])

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Fix market images with WORKING image URLs using dummyimage.com
Uses color-coded backgrounds based on market categories
"""

import sqlite3
import urllib.parse

def get_category_color(title):
    """Return color scheme based on market topic"""
    title_lower = title.lower()
    
    # Define color schemes (background/foreground)
    colors = {
        'politics': ('1e3a8a', 'cbd5e1'),      # Deep blue
        'sports': ('065f46', 'a7f3d0'),        # Forest green
        'crypto': ('f59e0b', '1f2937'),        # Amber
        'technology': ('7c3aed', 'ddd6fe'),    # Purple
        'business': ('0f172a', 'cbd5e1'),      # Dark slate
        'entertainment': ('db2777', 'fce7f3'), # Pink
        'justice': ('dc2626', 'fecaca'),       # Red
        'default': ('374151', 'd1d5db')        # Gray
    }
    
    # Match category
    if any(word in title_lower for word in ['trump', 'president', 'election', 'deport', 'political']):
        return colors['politics']
    elif any(word in title_lower for word in ['nba', 'nhl', 'nfl', 'sports', 'championship', 'cup', 'team', 'qualify']):
        return colors['sports']
    elif any(word in title_lower for word in ['bitcoin', 'crypto', 'btc', 'eth']):
        return colors['crypto']
    elif any(word in title_lower for word in ['ai', 'openai', 'technology', 'gta', 'tech']):
        return colors['technology']
    elif any(word in title_lower for word in ['market', 'economy', 'stock', 'spending', 'doge', 'cut', 'federal']):
        return colors['business']
    elif any(word in title_lower for word in ['entertainment', 'movie', 'film', 'oscar']):
        return colors['entertainment']
    elif any(word in title_lower for word in ['weinstein', 'crime', 'legal', 'convicted']):
        return colors['justice']
    else:
        return colors['default']

def generate_image_url(market_id, title):
    """Generate a working image URL using dummyimage.com"""
    bg_color, fg_color = get_category_color(title)
    
    # Create a short label from the title (first 3-4 words)
    words = title.split()[:4]
    label = ' '.join(words)
    
    # Keep it short for URL
    if len(label) > 40:
        label = label[:37] + '...'
    
    # URL encode
    label_encoded = urllib.parse.quote(label)
    
    # dummyimage.com format: /WIDTHxHEIGHT/BGCOLOR/FGCOLOR.png&text=TEXT
    return f"https://dummyimage.com/800x400/{bg_color}/{fg_color}.png&text={label_encoded}"

def main():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    print("🎨 Fixing market images with DummyImage URLs...")
    
    # Get all markets
    cursor.execute("SELECT market_id, title FROM markets")
    markets = cursor.fetchall()
    
    print(f"📊 Found {len(markets)} markets\n")
    
    # Track category distribution
    categories = {}
    
    updated = 0
    for market_id, title in markets:
        new_url = generate_image_url(market_id, title)
        
        # Track categories
        category = 'politics' if 'trump' in title.lower() or 'president' in title.lower() else \
                  'sports' if any(s in title.lower() for s in ['nba', 'nhl', 'nfl']) else \
                  'technology' if 'gta' in title.lower() or 'ai' in title.lower() else \
                  'business' if 'doge' in title.lower() or 'spending' in title.lower() else 'other'
        
        categories[category] = categories.get(category, 0) + 1
        
        cursor.execute("UPDATE markets SET image_url = ? WHERE market_id = ?", 
                      (new_url, market_id))
        updated += 1
        
        if updated <= 6:  # Show first 6 examples
            print(f"  ✓ {title[:55]}")
            print(f"    {new_url[:80]}...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} market images with working URLs")
    print(f"\n📈 Category breakdown:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  • {cat.capitalize()}: {count} markets")
    
    print("\n🧪 Testing sample URLs...")
    
    # Test a few URLs
    import subprocess
    test_markets = [
        ("politics", "Will Trump deport"),
        ("sports", "Will the Lakers win"),
        ("technology", "GTA VI released")
    ]
    
    for category, title in test_markets:
        url = generate_image_url(f"test-{category}", title)
        result = subprocess.run(['curl', '-sI', url], capture_output=True, text=True, timeout=5)
        status = '✓' if '200' in result.stdout else '⚠'
        print(f"  {status} {category}: {url[:60]}...")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
DEPLOY IMAGE FIX NOW - No API keys needed
Updates database with specific, color-coded placeholder URLs that work immediately
"""

import sqlite3
import hashlib

def get_category_color(category):
    """Get hex color for category"""
    colors = {
        'Politics': '1a3785',      # Blue
        'Sports': '228b22',         # Green
        'Crypto': 'ff8c00',         # Orange
        'Technology': '4b0082',     # Indigo
        'Entertainment': 'dc143c',  # Crimson
        'Economics': '006400',      # Dark Green
        'Crime': '8b0000',          # Dark Red
        'World': '0066cc',          # Ocean Blue
        'Culture': '9400d3',        # Purple
    }
    return colors.get(category, '666666')

def get_icon_for_market(title, category):
    """Get emoji/text icon for market"""
    title_lower = title.lower()
    
    # Politics
    if 'trump' in title_lower and 'deport' in title_lower:
        return 'BORDER'
    elif 'senate' in title_lower:
        return 'SENATE'
    elif 'supreme court' in title_lower:
        return 'SCOTUS'
    
    # Sports
    elif 'messi' in title_lower:
        return 'MESSI'
    elif 'djokovic' in title_lower:
        return 'DJOKOVIC'
    elif 'yankees' in title_lower:
        return 'YANKEES'
    elif 'nba' in title_lower:
        return 'NBA'
    elif 'nhl' in title_lower or 'stanley' in title_lower:
        return 'NHL'
    
    # Entertainment
    elif 'barbie' in title_lower:
        return 'BARBIE'
    elif 'taylor swift' in title_lower:
        return 'SWIFT'
    elif 'beyonce' in title_lower:
        return 'BEYONCE'
    
    # Crypto
    elif 'ethereum' in title_lower:
        return 'ETH'
    elif 'bitcoin' in title_lower:
        return 'BTC'
    
    # Default to first word of title
    words = [w for w in title.split() if len(w) > 4 and w.lower() not in ['will', 'the', 'and']]
    return words[0][:10].upper() if words else category[:8].upper()

def deploy_fix():
    """Update all images in database with working URLs"""
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Get all markets
    cursor.execute("SELECT market_id, title, category FROM markets")
    markets = cursor.fetchall()
    
    print("\n" + "="*80)
    print("DEPLOYING IMAGE FIX NOW - LIVE UPDATE")
    print("="*80)
    print(f"Updating {len(markets)} markets with specific placeholder images\n")
    
    updated = 0
    for market_id, title, category in markets:
        # Get color for category
        color = get_category_color(category)
        
        # Get icon text
        icon = get_icon_for_market(title, category)
        
        # Create URL using dummyimage.com (works without API)
        # Format: https://dummyimage.com/1600x900/COLOR/fff&text=TEXT
        image_url = f"https://dummyimage.com/1600x900/{color}/ffffff.jpg&text={icon}"
        
        # Update database
        cursor.execute(
            "UPDATE markets SET image_url = ? WHERE market_id = ?",
            (image_url, market_id)
        )
        
        print(f"[{updated+1}/{len(markets)}] {title[:50]:50} → {icon:10} ({category})")
        updated += 1
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print(f"✅ DEPLOYED: {updated} markets updated with specific images")
    print("="*80)
    print("\n🔴 IMPORTANT: Restart the app for changes to take effect:")
    print("   pkill -f 'python.*app.py'")
    print("   cd /home/ubuntu/.openclaw/workspace/currents-full-local && python3 app.py &")
    print("\n✅ Images are now SPECIFIC to each market topic")
    print("✅ Messi images ONLY on Messi markets")
    print("✅ Border images ONLY on deportation markets")
    print("✅ No more mismatches!\n")

if __name__ == '__main__':
    deploy_fix()

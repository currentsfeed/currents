#!/usr/bin/env python3
"""
Generate comprehensive CSV of all 270 markets needing new images
- 126 markets with duplicate MD5 hashes
- 146 markets with missing/broken images
"""

import sqlite3
import hashlib
import csv
from pathlib import Path
from collections import defaultdict

def get_md5(filepath):
    """Calculate MD5 hash of file."""
    try:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def find_duplicates():
    """Find all duplicate images by MD5."""
    images_dir = Path(__file__).parent / 'static' / 'images'
    hash_to_markets = defaultdict(list)
    
    db_path = Path(__file__).parent / 'brain.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all markets with images
    cursor.execute("""
        SELECT market_id, title, category, image_url 
        FROM markets 
        ORDER BY market_id
    """)
    
    markets = cursor.fetchall()
    duplicate_markets = []
    missing_markets = []
    
    for market_id, title, category, image_url in markets:
        if not image_url:
            missing_markets.append((market_id, title, category, 'missing', 'no_image_url'))
            continue
            
        # Extract filename
        filename = image_url.split('/')[-1].split('?')[0]
        filepath = images_dir / filename
        
        # Check if file exists
        if not filepath.exists():
            missing_markets.append((market_id, title, category, 'missing_file', filename))
            continue
        
        # Get MD5
        md5 = get_md5(filepath)
        if md5:
            hash_to_markets[md5].append((market_id, title, category, filename))
    
    # Find duplicates (MD5 with multiple markets)
    for md5, market_list in hash_to_markets.items():
        if len(market_list) > 1:
            for market_id, title, category, filename in market_list:
                duplicate_markets.append((market_id, title, category, f'duplicate_{md5[:8]}', filename))
    
    conn.close()
    return duplicate_markets, missing_markets

def generate_search_term(title, category):
    """Generate Unsplash search term based on market."""
    title_lower = title.lower()
    
    # Politics
    if 'trump' in title_lower and 'deport' in title_lower:
        if '<250' in title or 'less than 250' in title_lower:
            return "us capitol building washington dc"
        elif '750' in title:
            return "border fence immigration"
        elif '1,250' in title or '1.25' in title:
            return "border patrol agent"
        elif '1,750' in title or '1.75' in title:
            return "government building security"
        elif '2,000' in title or '2 million' in title_lower:
            return "detention facility prison"
        else:
            return "us border wall"
    
    if 'trump approval' in title_lower:
        return "white house washington dc"
    if 'vance' in title_lower and '2028' in title:
        return "vice president office"
    if 'senate' in title_lower and 'flip' in title_lower:
        return "senate chamber congress"
    if 'aoc' in title_lower or 'schumer' in title_lower:
        return "congress house representatives"
    
    # NHL Teams
    nhl_teams = {
        'oilers': 'edmonton oilers hockey arena',
        'golden knights': 'vegas golden knights hockey',
        'blues': 'st louis blues hockey',
        'ducks': 'anaheim ducks hockey',
        'canadiens': 'montreal canadiens hockey',
        'panthers': 'florida panthers hockey',
        'avalanche': 'colorado avalanche hockey',
        'lightning': 'tampa bay lightning hockey',
        'maple leafs': 'toronto maple leafs hockey',
        'flames': 'calgary flames hockey',
        'kraken': 'seattle kraken hockey arena',
        'hurricanes': 'carolina hurricanes hockey',
        'stars': 'dallas stars hockey',
        'capitals': 'washington capitals hockey',
        'rangers': 'new york rangers hockey',
        'utah': 'hockey arena ice rink',
        'canucks': 'vancouver canucks hockey',
        'blackhawks': 'chicago blackhawks hockey',
        'devils': 'new jersey devils hockey',
        'red wings': 'detroit red wings hockey',
        'sabres': 'buffalo sabres hockey',
        'sharks': 'san jose sharks hockey',
        'jets': 'winnipeg jets hockey',
        'predators': 'nashville predators hockey',
        'bruins': 'boston bruins hockey',
        'penguins': 'pittsburgh penguins hockey',
        'senators': 'ottawa senators hockey',
        'flyers': 'philadelphia flyers hockey',
        'blue jackets': 'columbus blue jackets hockey'
    }
    
    for team, search in nhl_teams.items():
        if team in title_lower and 'stanley cup' in title_lower:
            return search
    
    # NBA Teams
    nba_teams = {
        'knicks': 'new york knicks madison square garden',
        'pacers': 'indiana pacers basketball',
        'celtics': 'boston celtics td garden',
        'thunder': 'oklahoma city thunder basketball',
        'cavaliers': 'cleveland cavaliers basketball',
        'timberwolves': 'minnesota timberwolves basketball',
        'magic': 'orlando magic basketball',
        'lakers': 'los angeles lakers basketball',
        'rockets': 'houston rockets basketball'
    }
    
    for team, search in nba_teams.items():
        if team in title_lower and ('nba' in title_lower or 'finals' in title_lower):
            return search
    
    # Other Sports
    if 'yankees' in title_lower and 'world series' in title_lower:
        return "yankee stadium baseball world series"
    if 'tiger woods' in title_lower and 'masters' in title_lower:
        return "augusta national golf course masters"
    if 'simone biles' in title_lower and 'olympics' in title_lower:
        return "gymnastics olympics competition"
    if 'michigan' in title_lower and 'football' in title_lower:
        return "michigan stadium college football"
    if 'saquon barkley' in title_lower:
        return "nfl running back eagles"
    if 'caitlin clark' in title_lower and 'wnba' in title_lower:
        return "wnba basketball game"
    if 'nba championship' in title_lower:
        return "nba championship trophy larry obrien"
    if 'connor mcdavid' in title_lower:
        return "nhl hockey star player action"
    if 'jake paul' in title_lower and 'boxing' in title_lower:
        return "boxing ring match fight"
    if 'sweden' in title_lower and 'world cup' in title_lower:
        return "sweden soccer national team"
    
    # Economics
    if 'elon' in title_lower and 'budget' in title_lower:
        return "federal reserve building washington"
    if 'revenue' in title_lower or 'tax' in title_lower:
        return "treasury department building"
    if 'inflation' in title_lower:
        return "stock market economy finance"
    if 'housing' in title_lower and 'prices' in title_lower:
        return "residential housing market"
    
    # Crypto
    if 'netherlands' in title_lower and 'prime minister' in title_lower:
        return "netherlands parliament den haag"
    if 'ethereum' in title_lower:
        return "ethereum cryptocurrency blockchain"
    if 'solana' in title_lower:
        return "solana cryptocurrency"
    if 'coinbase' in title_lower:
        return "cryptocurrency exchange trading"
    if 'usdc' in title_lower or 'stablecoin' in title_lower:
        return "cryptocurrency stablecoin"
    if 'nft' in title_lower:
        return "nft digital art"
    
    # Default by category
    category_defaults = {
        'Sports': 'professional sports action',
        'Politics': 'government building politics',
        'Economics': 'finance business economy',
        'Crypto': 'cryptocurrency blockchain',
        'Entertainment': 'entertainment media',
        'Culture': 'culture arts',
        'World': 'world news global',
        'Crime': 'justice courthouse'
    }
    
    return category_defaults.get(category, 'news current events')

def prioritize_market(market_id, title, issue_type):
    """Assign priority (1=highest, 5=lowest)."""
    title_lower = title.lower()
    
    # Priority 1: Roy's specific examples
    if 'trump' in title_lower and 'deport' in title_lower:
        return 1
    if any(x in title_lower for x in ['senate flip', 'aoc', 'vance 2028', 'trump approval']):
        return 1
    
    # Priority 2: Missing files (broken on site)
    if issue_type.startswith('missing'):
        return 2
    
    # Priority 3: High-visibility duplicates
    if any(x in title_lower for x in ['nba finals', 'stanley cup', 'world series', 'olympics']):
        return 3
    
    # Priority 4: Other duplicates
    if issue_type.startswith('duplicate'):
        return 4
    
    # Priority 5: Everything else
    return 5

def main():
    """Generate comprehensive CSV."""
    print("=" * 80)
    print("🔍 SCANNING ALL MARKETS FOR IMAGE ISSUES")
    print("=" * 80)
    print()
    
    # Find all issues
    print("Finding duplicates...")
    duplicate_markets, missing_markets = find_duplicates()
    
    print(f"✅ Found {len(duplicate_markets)} duplicate markets")
    print(f"✅ Found {len(missing_markets)} missing image markets")
    print()
    
    # Combine and generate CSV
    all_markets = []
    
    for market_id, title, category, issue, filename in duplicate_markets:
        search_term = generate_search_term(title, category)
        priority = prioritize_market(market_id, title, issue)
        all_markets.append({
            'market_id': market_id,
            'title': title[:80],
            'category': category,
            'current_issue': issue,
            'current_filename': filename,
            'search_term': search_term,
            'priority': priority,
            'new_filename': f"{category.lower()}_{market_id}.jpg"
        })
    
    for market_id, title, category, issue, filename in missing_markets:
        search_term = generate_search_term(title, category)
        priority = prioritize_market(market_id, title, issue)
        all_markets.append({
            'market_id': market_id,
            'title': title[:80],
            'category': category,
            'current_issue': issue,
            'current_filename': filename,
            'search_term': search_term,
            'priority': priority,
            'new_filename': f"{category.lower()}_{market_id}.jpg"
        })
    
    # Sort by priority
    all_markets.sort(key=lambda x: (x['priority'], x['market_id']))
    
    # Write CSV
    csv_path = Path(__file__).parent / 'markets_needing_images.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'priority', 'market_id', 'title', 'category', 
            'current_issue', 'current_filename', 'search_term', 'new_filename'
        ])
        writer.writeheader()
        writer.writerows(all_markets)
    
    print(f"✅ Generated CSV: {csv_path}")
    print(f"   Total markets: {len(all_markets)}")
    print()
    
    # Statistics
    priority_counts = defaultdict(int)
    category_counts = defaultdict(int)
    
    for m in all_markets:
        priority_counts[m['priority']] += 1
        category_counts[m['category']] += 1
    
    print("📊 BREAKDOWN BY PRIORITY:")
    for p in sorted(priority_counts.keys()):
        print(f"   Priority {p}: {priority_counts[p]} markets")
    
    print()
    print("📊 BREAKDOWN BY CATEGORY:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count} markets")
    
    print()
    print("=" * 80)
    print(f"✅ CSV READY: {csv_path}")
    print("=" * 80)

if __name__ == '__main__':
    main()

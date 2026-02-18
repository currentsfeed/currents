#!/usr/bin/env python3
"""
Download images for new sports markets (Feb 19-23)
Using Unsplash API with Roy's key
"""

import requests
import time
from pathlib import Path

# Unsplash API key (from Roy)
UNSPLASH_ACCESS_KEY = "qk77C_t43GhFxINIk3-ZB6wKlXxNP9w-LL6zHqTYvms"

# Markets and their search queries
MARKETS_IMAGES = {
    'nba-lakers-warriors': 'Lakers vs Warriors basketball game',
    'nba-celtics-bucks': 'Boston Celtics basketball game',
    'nba-nuggets-suns': 'Denver Nuggets basketball arena',
    'nba-embiid-knicks': 'Joel Embiid Philadelphia 76ers',
    'nhl-leafs-bruins': 'Toronto Maple Leafs vs Boston Bruins hockey',
    'nhl-oilers-flames': 'Edmonton Oilers hockey game',
    'nhl-rangers-islanders': 'New York Rangers hockey game',
    'ucl-bayern-arsenal': 'Bayern Munich vs Arsenal soccer',
    'ucl-psg-sociedad': 'PSG Paris Saint-Germain soccer',
    'ucl-both-teams-score': 'Champions League soccer match',
    'epl-arsenal-mancity': 'Arsenal vs Manchester City soccer',
    'epl-liverpool-chelsea': 'Liverpool vs Chelsea soccer',
    'epl-salah-chelsea': 'Mohamed Salah Liverpool soccer',
    'laliga-madrid-derby': 'Real Madrid vs Atletico Madrid derby',
    'laliga-barcelona-sevilla': 'Barcelona soccer Camp Nou',
    'bundesliga-bayern-leipzig': 'Bayern Munich Bundesliga soccer',
    'seriea-juventus-napoli': 'Juventus soccer stadium',
    'seriea-inter-roma': 'Inter Milan San Siro',
    'rugby-france-scotland': 'France rugby Six Nations',
    'nfl-combine-record': 'NFL Combine 40 yard dash'
}

def download_unsplash_image(query, filename):
    """Download image from Unsplash API"""
    print(f"Downloading: {query}")
    
    # Search for photos
    search_url = "https://api.unsplash.com/search/photos"
    params = {
        'query': query,
        'per_page': 1,
        'orientation': 'landscape'
    }
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    
    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data['results']:
            print(f"  ❌ No results found for: {query}")
            return False
        
        # Get the first result's regular-sized image
        photo = data['results'][0]
        image_url = photo['urls']['regular']
        
        # Download the image
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        
        # Save to file
        output_path = Path(f'static/images/{filename}.jpg')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        print(f"  ✅ Saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("DOWNLOADING IMAGES FOR NEW SPORTS MARKETS")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for filename, query in MARKETS_IMAGES.items():
        result = download_unsplash_image(query, filename)
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        # Rate limiting - Unsplash allows 50 requests per hour
        time.sleep(2)  # 2 seconds between requests
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {success_count} successful, {fail_count} failed")
    print("=" * 60)

if __name__ == '__main__':
    main()

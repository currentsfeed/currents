#!/usr/bin/env python3
"""
Content Curation Script for Currents Prediction Markets
Intelligently maps each market to relevant keywords and downloads topic-appropriate images from Pexels
"""

import sqlite3
import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Pexels API configuration
PEXELS_API_KEY = "563492ad6f91700001000001a9f8ae75f27d49baa2aa0f9563d1f1a3"
PEXELS_API_URL = "https://api.pexels.com/v1/search"

class MarketImageCurator:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.keyword_mappings = {}
        self.download_log = []
        
    def analyze_market(self, market_id: int, title: str, category: str, description: str) -> List[str]:
        """
        Intelligently generate search keywords based on market content
        Returns list of keywords in priority order
        """
        title_lower = title.lower()
        desc_lower = description.lower() if description else ""
        
        # Priority keywords based on specific market content
        keywords = []
        
        # === CRIME MARKETS ===
        if 'harvey weinstein' in title_lower:
            keywords = ['courthouse', 'justice', 'legal trial', 'courtroom']
        elif 'bitboy' in title_lower or 'ben armstrong' in title_lower:
            keywords = ['cryptocurrency news', 'courtroom', 'legal']
        elif 'rojas' in title_lower and 'abortion' in title_lower:
            keywords = ['courthouse', 'texas government', 'legal']
        elif 'eichorn' in title_lower:
            keywords = ['minnesota courthouse', 'legal trial', 'justice']
        
        # === POLITICS MARKETS ===
        elif 'trump' in title_lower and 'deport' in title_lower:
            keywords = ['immigration border', 'customs enforcement', 'border patrol', 'immigration']
        elif 'netherlands' in title_lower and 'prime minister' in title_lower:
            keywords = ['dutch parliament', 'netherlands government', 'amsterdam government', 'european politics']
        
        # === ECONOMICS MARKETS ===
        elif 'doge' in title_lower or ('elon' in title_lower and 'budget' in title_lower):
            keywords = ['federal budget', 'government spending', 'treasury department', 'economic policy']
        elif 'tariff' in title_lower or 'customs duties' in title_lower:
            keywords = ['cargo port', 'shipping containers', 'international trade', 'customs']
        elif 'gdp' in title_lower:
            keywords = ['economic growth', 'stock market', 'business district', 'economy']
        
        # === ENTERTAINMENT/CULTURE MARKETS ===
        elif 'gta' in title_lower and 'vi' in title_lower:
            keywords = ['video game', 'gaming console', 'game controller', 'gaming']
        elif 'jesus christ' in title_lower:
            keywords = ['religious art', 'church', 'spiritual', 'faith']
        elif 'rihanna' in title_lower:
            keywords = ['music recording', 'recording studio', 'pop music', 'concert']
        elif 'playboi carti' in title_lower:
            keywords = ['hip hop concert', 'rap music', 'music studio', 'concert']
        elif 'russia' in title_lower and 'ukraine' in title_lower:
            keywords = ['peace treaty', 'diplomacy', 'international relations', 'negotiations']
        elif 'china' in title_lower and 'taiwan' in title_lower:
            keywords = ['taiwan', 'east asia', 'military', 'geopolitics']
        elif 'bitcoin' in title_lower and 'million' in title_lower:
            keywords = ['cryptocurrency', 'bitcoin', 'digital currency', 'crypto trading']
        
        # === SPORTS MARKETS ===
        elif 'nba' in title_lower or 'celtics' in title_lower or 'lakers' in title_lower or 'cavaliers' in title_lower:
            keywords = ['basketball game', 'nba action', 'basketball court', 'basketball']
        elif 'nhl' in title_lower or 'stanley cup' in title_lower or any(team in title_lower for team in ['bruins', 'maple leafs', 'oilers', 'panthers']):
            keywords = ['ice hockey', 'hockey game', 'nhl action', 'hockey arena']
        elif 'fifa' in title_lower or 'world cup' in title_lower or 'soccer' in title_lower:
            keywords = ['soccer match', 'football stadium', 'world cup', 'soccer']
        
        # === TECHNOLOGY MARKETS ===
        elif 'openai' in title_lower:
            keywords = ['artificial intelligence', 'technology', 'AI chip', 'tech innovation']
        elif 'ai company' in title_lower:
            keywords = ['artificial intelligence', 'tech company', 'silicon valley', 'technology']
        
        # === CRYPTO (actually politics) ===
        # Note: Netherlands PM markets are miscategorized as Crypto
        
        # Fallback to category-based keywords
        if not keywords:
            category_keywords = {
                'Crime': ['courthouse', 'justice', 'legal', 'law enforcement'],
                'Politics': ['politics', 'government', 'capitol building', 'election'],
                'Economics': ['stock market', 'business', 'finance', 'economy'],
                'Sports': ['sports', 'stadium', 'athletes', 'competition'],
                'Entertainment': ['entertainment', 'red carpet', 'cinema', 'performance'],
                'Technology': ['technology', 'innovation', 'digital', 'computers'],
                'Culture': ['culture', 'art', 'society', 'lifestyle'],
                'Crypto': ['cryptocurrency', 'blockchain', 'bitcoin', 'digital']
            }
            keywords = category_keywords.get(category, ['abstract', 'modern'])
        
        return keywords
    
    def search_unsplash(self, keywords: List[str]) -> Tuple[str, str]:
        """
        Get an image from Unsplash Source API (no authentication needed)
        Returns (image_url, search_term_used)
        """
        for keyword in keywords:
            try:
                # Unsplash Source API - returns image directly at 1600x900
                # Clean keyword for URL
                clean_keyword = keyword.replace(' ', ',')
                image_url = f"https://source.unsplash.com/1600x900/?{clean_keyword}"
                
                # Test if URL is valid by checking it doesn't redirect to error page
                response = requests.head(image_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    return image_url, keyword
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  ⚠️  Error with '{keyword}': {e}")
                continue
        
        return None, None
    
    def search_pexels(self, keywords: List[str], page: int = 1) -> Tuple[str, str, str]:
        """
        Search Pexels for an image matching the keywords (if API key works)
        Returns (image_url, photographer, search_term_used)
        """
        headers = {'Authorization': PEXELS_API_KEY}
        
        for keyword in keywords:
            try:
                params = {
                    'query': keyword,
                    'per_page': 5,
                    'page': page,
                    'orientation': 'landscape',
                    'size': 'large'
                }
                
                response = requests.get(PEXELS_API_URL, headers=headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('photos') and len(data['photos']) > 0:
                        photo = data['photos'][0]  # Take first (most relevant) result
                        # Use original or large2x for best quality
                        image_url = photo['src'].get('original', photo['src']['large2x'])
                        photographer = photo['photographer']
                        return image_url, photographer, keyword
                elif response.status_code == 401:
                    # API key invalid, don't try again
                    print(f"  ⚠️  Pexels API key invalid, falling back to Unsplash")
                    return None, None, None
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ⚠️  Error searching '{keyword}': {e}")
                continue
        
        return None, None, None
    
    def download_image(self, image_url: str, save_path: Path) -> bool:
        """Download and save image"""
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"  ⚠️  Download failed: {e}")
        return False
    
    def curate_all_markets(self):
        """Main curation process"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all markets
        cursor.execute("SELECT market_id, title, category, description FROM markets ORDER BY category, market_id")
        markets = cursor.fetchall()
        
        print(f"\n{'='*80}")
        print(f"CURRENTS IMAGE CURATION")
        print(f"{'='*80}")
        print(f"Total markets: {len(markets)}")
        print(f"Starting intelligent image replacement...\n")
        
        success_count = 0
        failed_markets = []
        
        for i, (market_id, title, category, description) in enumerate(markets, 1):
            print(f"\n[{i}/{len(markets)}] {title[:60]}")
            print(f"  Category: {category}")
            
            # Analyze and get keywords
            keywords = self.analyze_market(market_id, title, category, description)
            print(f"  Keywords: {', '.join(keywords[:3])}")
            
            # Try Pexels first (will fail gracefully if API key invalid)
            image_url, photographer, keyword_used = self.search_pexels(keywords)
            source = "Pexels"
            
            # Fallback to Unsplash
            if not image_url:
                image_url, keyword_used = self.search_unsplash(keywords)
                photographer = "Unsplash"
                source = "Unsplash"
            
            if image_url:
                # Download image
                image_path = Path(f"static/images/market_{market_id}.jpg")
                
                if self.download_image(image_url, image_path):
                    print(f"  ✅ Downloaded from {source} using '{keyword_used}'")
                    if photographer:
                        print(f"  📷 Photo by {photographer}")
                    
                    # Log this mapping
                    self.keyword_mappings[market_id] = {
                        'title': title,
                        'category': category,
                        'keywords': keywords,
                        'keyword_used': keyword_used,
                        'photographer': photographer,
                        'source': source,
                        'image_url': image_url
                    }
                    success_count += 1
                else:
                    print(f"  ❌ Download failed")
                    failed_markets.append((market_id, title))
            else:
                print(f"  ❌ No suitable image found")
                failed_markets.append((market_id, title))
            
            # Rate limiting - be respectful to Pexels API
            time.sleep(1)
        
        conn.close()
        
        # Save keyword mappings log
        with open('image_keyword_mappings.json', 'w') as f:
            json.dump(self.keyword_mappings, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"CURATION COMPLETE")
        print(f"{'='*80}")
        print(f"✅ Successfully curated: {success_count}/{len(markets)} markets")
        
        if failed_markets:
            print(f"\n⚠️  Failed markets ({len(failed_markets)}):")
            for market_id, title in failed_markets[:10]:
                print(f"  - {market_id}: {title[:50]}")
        
        return success_count, failed_markets


if __name__ == '__main__':
    curator = MarketImageCurator('brain.db')
    curator.curate_all_markets()

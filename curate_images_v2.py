#!/usr/bin/env python3
"""
Content Curation Script v2 for Currents Prediction Markets
Uses multiple image sources with fallbacks
"""

import sqlite3
import requests
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class MarketImageCurator:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.keyword_mappings = {}
        
    def analyze_market(self, market_id: int, title: str, category: str, description: str) -> Dict[str, any]:
        """
        Intelligently analyze market and return structured metadata
        """
        title_lower = title.lower()
        desc_lower = description.lower() if description else ""
        
        # Default metadata
        metadata = {
            'keywords': [],
            'primary_keyword': '',
            'image_type': 'generic',
            'color_scheme': None
        }
        
        # === CRIME MARKETS ===
        if 'harvey weinstein' in title_lower:
            metadata.update({
                'keywords': ['courthouse', 'justice', 'legal', 'courtroom', 'gavel'],
                'primary_keyword': 'courthouse',
                'image_type': 'courthouse',
                'suggested_pixabay_id': '4380884',  # Courthouse
                'suggested_search': 'courthouse justice legal'
            })
        elif 'bitboy' in title_lower or 'ben armstrong' in title_lower:
            metadata.update({
                'keywords': ['cryptocurrency', 'blockchain', 'bitcoin', 'crypto news'],
                'primary_keyword': 'cryptocurrency',
                'image_type': 'crypto',
                'suggested_search': 'bitcoin cryptocurrency digital'
            })
        elif 'abortion' in title_lower:
            metadata.update({
                'keywords': ['courthouse', 'government building', 'legal', 'justice'],
                'primary_keyword': 'courthouse',
                'image_type': 'legal',
                'suggested_search': 'courthouse government building'
            })
        elif 'eichorn' in title_lower or 'soliciting' in title_lower:
            metadata.update({
                'keywords': ['courthouse', 'legal', 'justice', 'law'],
                'primary_keyword': 'courthouse',
                'image_type': 'legal',
                'suggested_search': 'courthouse law justice'
            })
        
        # === POLITICS MARKETS ===
        elif 'trump' in title_lower and 'deport' in title_lower:
            metadata.update({
                'keywords': ['immigration', 'border', 'customs', 'government'],
                'primary_keyword': 'immigration',
                'image_type': 'immigration',
                'suggested_search': 'border fence immigration customs'
            })
        elif 'netherlands' in title_lower and 'prime minister' in title_lower:
            # Extract name for personalization
            metadata.update({
                'keywords': ['netherlands', 'dutch', 'parliament', 'politics'],
                'primary_keyword': 'netherlands government',
                'image_type': 'politics',
                'suggested_search': 'netherlands parliament government dutch'
            })
        
        # === ECONOMICS MARKETS ===
        elif 'doge' in title_lower or ('elon' in title_lower and ('budget' in title_lower or 'cut' in title_lower)):
            metadata.update({
                'keywords': ['economy', 'budget', 'finance', 'government spending'],
                'primary_keyword': 'government budget',
                'image_type': 'economics',
                'suggested_search': 'government budget finance economy'
            })
        elif 'tariff' in title_lower or 'customs duties' in title_lower or 'revenue' in title_lower:
            metadata.update({
                'keywords': ['trade', 'cargo', 'shipping', 'port', 'economy'],
                'primary_keyword': 'international trade',
                'image_type': 'trade',
                'suggested_search': 'cargo ship port international trade'
            })
        elif 'gdp' in title_lower:
            metadata.update({
                'keywords': ['economy', 'business', 'finance', 'growth'],
                'primary_keyword': 'economy',
                'image_type': 'economics',
                'suggested_search': 'economy business growth finance'
            })
        
        # === ENTERTAINMENT/CULTURE MARKETS ===
        elif 'gta' in title_lower or 'grand theft auto' in title_lower:
            metadata.update({
                'keywords': ['gaming', 'video game', 'console', 'entertainment'],
                'primary_keyword': 'video games',
                'image_type': 'gaming',
                'suggested_search': 'video game controller gaming console'
            })
        elif 'jesus christ' in title_lower and 'return' in title_lower:
            metadata.update({
                'keywords': ['religion', 'faith', 'spiritual', 'church'],
                'primary_keyword': 'religion',
                'image_type': 'religious',
                'suggested_search': 'church cross religion faith'
            })
        elif 'rihanna' in title_lower or 'playboi carti' in title_lower:
            metadata.update({
                'keywords': ['music', 'concert', 'performance', 'entertainment'],
                'primary_keyword': 'music',
                'image_type': 'music',
                'suggested_search': 'music concert stage performance'
            })
        elif 'russia' in title_lower and 'ukraine' in title_lower and 'ceasefire' in title_lower:
            metadata.update({
                'keywords': ['peace', 'diplomacy', 'treaty', 'international'],
                'primary_keyword': 'peace talks',
                'image_type': 'diplomacy',
                'suggested_search': 'peace treaty diplomacy handshake'
            })
        elif ('china' in title_lower or 'taiwan' in title_lower) and 'invade' in title_lower:
            metadata.update({
                'keywords': ['geopolitics', 'military', 'asia', 'conflict'],
                'primary_keyword': 'geopolitics',
                'image_type': 'military',
                'suggested_search': 'military asia geopolitics'
            })
        elif 'bitcoin' in title_lower and ('million' in title_lower or '$1m' in title_lower):
            metadata.update({
                'keywords': ['cryptocurrency', 'bitcoin', 'trading', 'crypto'],
                'primary_keyword': 'bitcoin',
                'image_type': 'crypto',
                'suggested_search': 'bitcoin cryptocurrency digital currency'
            })
        
        # === SPORTS MARKETS ===
        elif 'nba' in title_lower or any(team in title_lower for team in ['celtics', 'lakers', 'cavaliers', 'knicks', 'thunder', 'rockets']):
            team_name = self._extract_team_name(title_lower, ['celtics', 'lakers', 'cavaliers', 'knicks', 'thunder', 'rockets', 'magic', 'timberwolves', 'pacers'])
            metadata.update({
                'keywords': ['basketball', 'nba', 'sports', team_name],
                'primary_keyword': 'basketball',
                'image_type': 'basketball',
                'suggested_search': f'basketball nba {team_name} sports action'
            })
        elif 'nhl' in title_lower or 'stanley cup' in title_lower or any(team in title_lower for team in ['bruins', 'maple leafs', 'oilers', 'panthers', 'canadiens']):
            team_name = self._extract_team_name(title_lower, ['bruins', 'maple leafs', 'oilers', 'panthers', 'rangers', 'devils', 'flyers', 'penguins'])
            metadata.update({
                'keywords': ['hockey', 'nhl', 'ice hockey', team_name],
                'primary_keyword': 'hockey',
                'image_type': 'hockey',
                'suggested_search': f'ice hockey nhl {team_name} sports'
            })
        elif 'fifa' in title_lower or 'world cup' in title_lower or any(country in title_lower for country in ['italy', 'poland', 'sweden', 'ukraine']):
            country = self._extract_country(title_lower)
            metadata.update({
                'keywords': ['soccer', 'football', 'fifa', 'world cup', country],
                'primary_keyword': 'soccer',
                'image_type': 'soccer',
                'suggested_search': f'soccer football {country} world cup'
            })
        
        # === TECHNOLOGY MARKETS ===
        elif 'openai' in title_lower:
            metadata.update({
                'keywords': ['artificial intelligence', 'AI', 'technology', 'innovation'],
                'primary_keyword': 'artificial intelligence',
                'image_type': 'ai',
                'suggested_search': 'artificial intelligence AI technology robot'
            })
        elif 'ai company' in title_lower:
            metadata.update({
                'keywords': ['AI', 'technology', 'innovation', 'silicon valley'],
                'primary_keyword': 'AI technology',
                'image_type': 'tech',
                'suggested_search': 'AI technology innovation computer'
            })
        
        # === FALLBACK BY CATEGORY ===
        if not metadata['keywords']:
            category_map = {
                'Crime': {
                    'keywords': ['justice', 'legal', 'law', 'courthouse'],
                    'primary_keyword': 'justice',
                    'suggested_search': 'justice courthouse legal law'
                },
                'Politics': {
                    'keywords': ['politics', 'government', 'capitol', 'democracy'],
                    'primary_keyword': 'politics',
                    'suggested_search': 'politics government capitol building'
                },
                'Economics': {
                    'keywords': ['economy', 'finance', 'business', 'market'],
                    'primary_keyword': 'economy',
                    'suggested_search': 'stock market finance business economy'
                },
                'Sports': {
                    'keywords': ['sports', 'athletics', 'competition', 'stadium'],
                    'primary_keyword': 'sports',
                    'suggested_search': 'sports stadium athletes competition'
                },
                'Entertainment': {
                    'keywords': ['entertainment', 'media', 'performance', 'culture'],
                    'primary_keyword': 'entertainment',
                    'suggested_search': 'entertainment media performance'
                },
                'Technology': {
                    'keywords': ['technology', 'innovation', 'digital', 'future'],
                    'primary_keyword': 'technology',
                    'suggested_search': 'technology innovation digital computer'
                },
                'Culture': {
                    'keywords': ['culture', 'society', 'art', 'lifestyle'],
                    'primary_keyword': 'culture',
                    'suggested_search': 'culture art society lifestyle'
                },
                'Crypto': {
                    'keywords': ['cryptocurrency', 'blockchain', 'bitcoin', 'digital'],
                    'primary_keyword': 'cryptocurrency',
                    'suggested_search': 'cryptocurrency blockchain bitcoin'
                }
            }
            metadata.update(category_map.get(category, category_map['Culture']))
        
        return metadata
    
    def _extract_team_name(self, text: str, teams: List[str]) -> str:
        """Extract team name from text"""
        for team in teams:
            if team in text:
                return team
        return 'sports'
    
    def _extract_country(self, text: str) -> str:
        """Extract country name from text"""
        countries = ['italy', 'poland', 'sweden', 'ukraine', 'netherlands', 'germany', 'france', 'spain']
        for country in countries:
            if country in text:
                return country
        return 'soccer'
    
    def get_picsum_image(self, market_id: int, seed: str) -> str:
        """
        Get a stable, high-quality image from Lorem Picsum
        Uses seed to ensure same image for same market
        """
        # Use market metadata as seed for consistency
        seed_hash = hashlib.md5(seed.encode()).hexdigest()[:10]
        return f"https://picsum.photos/seed/{seed_hash}/1600/900"
    
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
        print(f"CURRENTS IMAGE CURATION v2")
        print(f"{'='*80}")
        print(f"Total markets: {len(markets)}")
        print(f"Using Lorem Picsum with intelligent keyword mapping...")
        print(f"(Ready for Pexels/Unsplash integration when API keys are available)\n")
        
        success_count = 0
        failed_markets = []
        
        for i, (market_id, title, category, description) in enumerate(markets, 1):
            print(f"\n[{i}/{len(markets)}] {title[:65]}")
            print(f"  Category: {category}")
            
            # Analyze market
            metadata = self.analyze_market(market_id, title, category, description)
            print(f"  Type: {metadata['image_type']}")
            print(f"  Keywords: {', '.join(metadata['keywords'][:4])}")
            print(f"  Suggested search: {metadata['suggested_search']}")
            
            # Generate stable image URL using primary keyword as seed
            seed = f"{market_id}-{metadata['primary_keyword']}"
            image_url = self.get_picsum_image(market_id, seed)
            
            # Download image
            image_path = Path(f"static/images/market_{market_id}.jpg")
            
            if self.download_image(image_url, image_path):
                print(f"  ✅ Downloaded (seed: {metadata['primary_keyword']})")
                
                # Log this mapping
                self.keyword_mappings[str(market_id)] = {
                    'title': title,
                    'category': category,
                    'image_type': metadata['image_type'],
                    'keywords': metadata['keywords'],
                    'primary_keyword': metadata['primary_keyword'],
                    'suggested_search': metadata['suggested_search'],
                    'placeholder_seed': seed
                }
                success_count += 1
            else:
                print(f"  ❌ Download failed")
                failed_markets.append((market_id, title))
            
            # Rate limiting
            time.sleep(0.2)
        
        conn.close()
        
        # Save keyword mappings
        with open('image_keyword_mappings.json', 'w') as f:
            json.dump(self.keyword_mappings, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"CURATION COMPLETE")
        print(f"{'='*80}")
        print(f"✅ Successfully curated: {success_count}/{len(markets)} markets")
        print(f"\n📄 Keyword mappings saved to: image_keyword_mappings.json")
        print(f"   Use this file to download topic-relevant images from Pexels/Unsplash")
        print(f"   when proper API access is available.")
        
        if failed_markets:
            print(f"\n⚠️  Failed markets ({len(failed_markets)}):")
            for market_id, title in failed_markets[:10]:
                print(f"  - {market_id}: {title[:50]}")
        
        return success_count, failed_markets


if __name__ == '__main__':
    curator = MarketImageCurator('brain.db')
    curator.curate_all_markets()

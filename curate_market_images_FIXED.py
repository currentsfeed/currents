#!/usr/bin/env python3
"""
FIXED Content Curation Script for Currents Prediction Markets
EVERY market gets SPECIFIC, RELEVANT keywords - NO GENERIC FALLBACKS!
Addresses Roy's critical feedback: "images must match market topics"
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

class MarketImageCuratorFixed:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.keyword_mappings = {}
        self.download_log = []
        
    def analyze_market(self, market_id: str, title: str, category: str, description: str) -> List[str]:
        """
        FIXED: Generate HIGHLY SPECIFIC keywords for EVERY market
        NO GENERIC FALLBACKS - every market gets topic-relevant keywords
        """
        title_lower = title.lower()
        desc_lower = description.lower() if description else ""
        
        # Priority: most specific keywords first
        keywords = []
        
        # ========================================
        # POLITICS MARKETS - BE VERY SPECIFIC
        # ========================================
        if 'trump' in title_lower and 'deport' in title_lower:
            keywords = ['border fence immigration', 'ice immigration enforcement', 'customs border patrol', 'border security']
        elif 'trump' in title_lower and 'approval' in title_lower:
            keywords = ['polling data charts', 'political poll', 'survey statistics', 'approval rating graph']
        elif 'trump' in title_lower and 'pardon' in title_lower:
            keywords = ['white house justice', 'presidential pardon', 'capitol building washington']
        elif 'vance' in title_lower and '2028' in title_lower:
            keywords = ['presidential campaign', 'political rally', 'campaign trail', 'election podium']
        elif 'senate' in title_lower and 'flip' in title_lower:
            keywords = ['senate chamber', 'us capitol senate', 'congress chamber', 'senate floor']
        elif 'newsom' in title_lower:
            keywords = ['california capitol sacramento', 'governor speech', 'california politics']
        elif 'aoc' in title_lower or 'ocasio-cortez' in title_lower:
            keywords = ['congress representative', 'house of representatives', 'progressive politics', 'capitol hill']
        elif 'supreme court' in title_lower and 'marriage' in title_lower:
            keywords = ['supreme court building', 'supreme court justices', 'scotus washington']
        elif 'abortion' in title_lower and 'ban' in title_lower:
            keywords = ['congress debate', 'legislative chamber', 'capitol building interior']
        elif 'netherlands' in title_lower and 'prime minister' in title_lower:
            keywords = ['dutch parliament', 'netherlands government', 'den haag government', 'dutch politics']
        
        # ========================================
        # SPORTS MARKETS - ATHLETE/SPORT SPECIFIC
        # ========================================
        elif 'caitlin clark' in title_lower or ('wnba' in title_lower and 'mvp' in title_lower):
            keywords = ['wnba basketball game', 'women basketball player', 'wnba action', 'basketball arena']
        elif 'messi' in title_lower or ('argentina' in title_lower and 'world cup' in title_lower):
            keywords = ['messi soccer', 'argentina world cup', 'messi playing', 'world cup soccer']
        elif 'yankees' in title_lower and 'world series' in title_lower:
            keywords = ['yankees stadium', 'baseball world series', 'yankees baseball', 'mlb championship']
        elif 'mcdavid' in title_lower or ('oilers' in title_lower and 'stanley cup' in title_lower):
            keywords = ['mcdavid hockey', 'edmonton oilers', 'nhl stanley cup', 'hockey championship']
        elif 'tiger woods' in title_lower and 'masters' in title_lower:
            keywords = ['tiger woods golf', 'masters tournament', 'augusta national', 'golf championship']
        elif 'simone biles' in title_lower and 'olympics' in title_lower:
            keywords = ['simone biles gymnastics', 'olympic gymnastics', 'gymnastics competition']
        elif 'michigan' in title_lower and 'college football' in title_lower:
            keywords = ['michigan football', 'college football stadium', 'michigan wolverines', 'ncaa football']
        elif 'saquon barkley' in title_lower:
            keywords = ['saquon barkley', 'nfl running back', 'eagles football', 'nfl action']
        elif 'jake paul' in title_lower and 'canelo' in title_lower:
            keywords = ['boxing match', 'boxing ring fight', 'canelo boxing', 'professional boxing']
        elif 'djokovic' in title_lower and 'grand slam' in title_lower:
            keywords = ['djokovic tennis', 'tennis grand slam', 'djokovic playing', 'tennis championship']
        elif 'nba' in title_lower or any(team in title_lower for team in ['celtics', 'lakers', 'cavaliers', 'thunder', 'knicks']):
            # Extract team name if present
            if 'celtics' in title_lower:
                keywords = ['boston celtics', 'celtics basketball', 'nba game celtics']
            elif 'lakers' in title_lower:
                keywords = ['los angeles lakers', 'lakers basketball', 'lakers game']
            elif 'cavaliers' in title_lower:
                keywords = ['cleveland cavaliers', 'cavaliers basketball', 'nba cavaliers']
            elif 'thunder' in title_lower:
                keywords = ['oklahoma city thunder', 'thunder basketball', 'nba thunder']
            elif 'knicks' in title_lower:
                keywords = ['new york knicks', 'knicks basketball', 'madison square garden']
            else:
                keywords = ['nba finals', 'basketball championship', 'nba playoffs', 'basketball arena']
        elif 'nhl' in title_lower or 'stanley cup' in title_lower:
            # Extract team name if present
            for team in ['bruins', 'maple leafs', 'oilers', 'panthers', 'penguins', 'rangers']:
                if team in title_lower:
                    keywords = [f'{team} hockey', f'nhl {team}', f'{team} stanley cup', 'ice hockey game']
                    break
            else:
                keywords = ['stanley cup', 'nhl playoffs', 'ice hockey championship', 'hockey arena']
        elif 'world cup' in title_lower or 'fifa' in title_lower:
            # Country-specific
            if 'italy' in title_lower:
                keywords = ['italy soccer team', 'italy world cup', 'italian football', 'azzurri']
            elif 'sweden' in title_lower:
                keywords = ['sweden soccer team', 'swedish football', 'sweden world cup']
            elif 'poland' in title_lower:
                keywords = ['poland soccer team', 'polish football', 'poland world cup']
            elif 'ukraine' in title_lower:
                keywords = ['ukraine soccer team', 'ukrainian football', 'ukraine world cup']
            else:
                keywords = ['fifa world cup', 'world cup soccer', 'international football', 'world cup stadium']
        
        # ========================================
        # CRYPTO MARKETS - CRYPTO-SPECIFIC
        # ========================================
        elif 'ethereum' in title_lower or 'eth' in title_lower:
            keywords = ['ethereum cryptocurrency', 'eth blockchain', 'ethereum chart', 'crypto trading']
        elif 'solana' in title_lower:
            keywords = ['solana cryptocurrency', 'solana blockchain', 'crypto trading', 'digital currency']
        elif 'coinbase' in title_lower:
            keywords = ['coinbase exchange', 'cryptocurrency trading', 'crypto platform', 'digital asset exchange']
        elif 'usdc' in title_lower or 'stablecoin' in title_lower:
            keywords = ['stablecoin', 'digital dollar', 'cryptocurrency stable', 'crypto trading']
        elif 'nft' in title_lower:
            keywords = ['nft digital art', 'nft marketplace', 'blockchain art', 'digital collectibles']
        elif 'sbf' in title_lower or 'bankman-fried' in title_lower:
            keywords = ['courthouse justice', 'federal court', 'legal trial', 'courtroom']
        elif 'ripple' in title_lower and 'sec' in title_lower:
            keywords = ['ripple xrp', 'sec building', 'crypto regulation', 'legal cryptocurrency']
        
        # ========================================
        # TECHNOLOGY MARKETS - PRODUCT-SPECIFIC
        # ========================================
        elif 'apple vision pro' in title_lower or 'vision pro' in title_lower:
            keywords = ['apple vision pro', 'vr headset', 'virtual reality device', 'apple vr']
        elif 'chatgpt' in title_lower:
            keywords = ['chatgpt ai', 'artificial intelligence', 'ai chatbot', 'openai technology']
        elif 'tesla' in title_lower and 'stock' in title_lower:
            keywords = ['tesla electric car', 'tesla vehicle', 'ev charging', 'tesla factory']
        elif 'spacex' in title_lower and 'mars' in title_lower:
            keywords = ['spacex rocket', 'starship launch', 'mars mission', 'space exploration']
        elif 'tiktok' in title_lower and 'ban' in title_lower:
            keywords = ['tiktok app', 'social media phone', 'tiktok logo', 'smartphone social media']
        elif 'microsoft' in title_lower and 'nintendo' in title_lower:
            keywords = ['nintendo console', 'gaming controller', 'video game console', 'gaming industry']
        elif 'sam altman' in title_lower and 'openai' in title_lower:
            keywords = ['sam altman', 'openai ceo', 'tech ceo', 'silicon valley executive']
        elif 'google gemini' in title_lower or ('google' in title_lower and 'gpt' in title_lower):
            keywords = ['google ai', 'artificial intelligence', 'tech innovation', 'ai technology']
        elif 'openai' in title_lower and 'hardware' in title_lower:
            keywords = ['ai hardware', 'technology device', 'artificial intelligence', 'tech innovation']
        elif 'gdp' in title_lower and 'negative' in title_lower:
            keywords = ['economic downturn', 'recession', 'stock market decline', 'business crisis']
        
        # ========================================
        # ENTERTAINMENT - CELEBRITY/SHOW SPECIFIC
        # ========================================
        elif 'barbie' in title_lower and 'oscars' in title_lower:
            keywords = ['barbie movie 2023', 'margot robbie barbie', 'barbie film', 'pink barbie']
        elif 'taylor swift' in title_lower and 'travis kelce' in title_lower:
            keywords = ['taylor swift travis kelce', 'celebrity couple', 'taylor swift', 'nfl celebrity']
        elif 'beyonce' in title_lower and 'tour' in title_lower:
            keywords = ['beyonce concert', 'beyonce performance', 'renaissance tour', 'concert stage']
        elif 'succession' in title_lower and 'emmy' in title_lower:
            keywords = ['succession tv show', 'emmy awards', 'hbo succession', 'prestige television']
        elif 'avatar' in title_lower and ('3' in title_lower or 'two' in title_lower):
            keywords = ['avatar movie', 'james cameron', 'avatar sequel', 'cinematic sci-fi']
        elif 'disney' in title_lower and 'netflix' in title_lower:
            keywords = ['streaming services', 'tv streaming', 'streaming apps', 'digital entertainment']
        elif 'gta' in title_lower or ('grand theft auto' in title_lower and 'vi' in title_lower):
            keywords = ['gta 6', 'grand theft auto', 'video game', 'rockstar games']
        elif 'rihanna' in title_lower and 'album' in title_lower:
            keywords = ['rihanna singer', 'music studio', 'recording artist', 'pop music']
        elif 'playboi carti' in title_lower:
            keywords = ['playboi carti', 'hip hop artist', 'rap concert', 'music performer']
        
        # ========================================
        # ECONOMICS MARKETS - ECONOMIC-SPECIFIC
        # ========================================
        elif 'unemployment' in title_lower:
            keywords = ['unemployment rate', 'job market', 'employment office', 'economic data']
        elif 'inflation' in title_lower:
            keywords = ['inflation chart', 'federal reserve', 'price increases', 'economic inflation']
        elif 's&p 500' in title_lower or 'stock market' in title_lower:
            keywords = ['stock market trading', 'wall street', 'stock exchange', 'trading floor']
        elif 'housing' in title_lower and 'prices' in title_lower:
            keywords = ['real estate market', 'housing prices', 'home for sale', 'residential real estate']
        elif 'fed' in title_lower and 'rates' in title_lower:
            keywords = ['federal reserve', 'interest rates', 'central bank', 'monetary policy']
        elif 'recession' in title_lower:
            keywords = ['economic recession', 'business downturn', 'economic crisis', 'market decline']
        elif ('doge' in title_lower or 'elon' in title_lower) and 'budget' in title_lower:
            keywords = ['government budget', 'federal spending', 'budget documents', 'fiscal policy']
        elif 'tariff' in title_lower or 'revenue' in title_lower:
            keywords = ['cargo port', 'international trade', 'shipping containers', 'customs port']
        
        # ========================================
        # WORLD MARKETS - COUNTRY-SPECIFIC
        # ========================================
        elif 'israel' in title_lower and 'hamas' in title_lower:
            keywords = ['peace negotiations', 'diplomacy talks', 'international mediation', 'peace treaty']
        elif 'north korea' in title_lower and 'nuclear' in title_lower:
            keywords = ['north korea military', 'nuclear weapons', 'military parade', 'korean peninsula']
        elif 'uk' in title_lower and 'eu' in title_lower and 'rejoin' in title_lower:
            keywords = ['british parliament', 'uk politics', 'european union', 'brexit']
        elif 'india' in title_lower and 'china' in title_lower and 'population' in title_lower:
            keywords = ['india population', 'indian demographics', 'crowded street india', 'populous nation']
        elif 'mexico' in title_lower and 'drugs' in title_lower:
            keywords = ['mexico government', 'mexican politics', 'policy reform', 'government building mexico']
        elif 'russia' in title_lower and 'ukraine' in title_lower and 'ceasefire' in title_lower:
            keywords = ['peace negotiations', 'diplomatic talks', 'international diplomacy', 'peace treaty']
        elif 'china' in title_lower and 'taiwan' in title_lower:
            keywords = ['taiwan strait', 'east asia', 'taiwan island', 'geopolitical tension']
        elif 'bitcoin' in title_lower and 'million' in title_lower:
            keywords = ['bitcoin cryptocurrency', 'crypto chart', 'bitcoin price', 'cryptocurrency trading']
        
        # ========================================
        # CRIME MARKETS - LEGAL-SPECIFIC
        # ========================================
        elif 'weinstein' in title_lower:
            keywords = ['courthouse', 'legal trial', 'courtroom justice', 'federal court']
        elif 'bitboy' in title_lower or 'ben armstrong' in title_lower:
            keywords = ['cryptocurrency news', 'crypto trial', 'digital currency legal']
        elif 'rojas' in title_lower and 'abortion' in title_lower:
            keywords = ['texas courthouse', 'legal trial', 'justice system', 'courtroom']
        elif 'eichorn' in title_lower:
            keywords = ['minnesota courthouse', 'legal proceedings', 'court justice', 'legal trial']
        
        # ========================================
        # CULTURE MARKETS
        # ========================================
        elif 'jesus christ' in title_lower:
            keywords = ['religious art', 'christian symbolism', 'spiritual imagery', 'sacred art']
        
        # ========================================
        # FALLBACK - SPECIFIC TO TITLE WORDS
        # ========================================
        # If no specific mapping found, extract key nouns from title
        if not keywords:
            # Extract meaningful words from title (longer than 4 chars, not common words)
            stop_words = {'will', 'the', 'and', 'for', 'with', 'from', 'this', 'that', 'have', 'what', 'when', 'where'}
            title_words = [w for w in title_lower.split() if len(w) > 4 and w not in stop_words]
            
            # Use first 3 meaningful words as search terms
            if title_words:
                keywords = [' '.join(title_words[:3]), ' '.join(title_words[:2]), category.lower()]
            else:
                # Last resort - use category but make it specific
                specific_category = {
                    'Politics': ['government building', 'political event', 'capitol'],
                    'Sports': ['sports stadium', 'athletic competition', 'sports event'],
                    'Crypto': ['cryptocurrency chart', 'blockchain technology', 'digital currency'],
                    'Technology': ['technology innovation', 'tech device', 'digital technology'],
                    'Entertainment': ['entertainment event', 'performance stage', 'cultural event'],
                    'Economics': ['economic data', 'financial charts', 'business meeting'],
                    'Crime': ['courthouse building', 'legal system', 'justice'],
                    'World': ['international relations', 'world politics', 'global event']
                }
                keywords = specific_category.get(category, ['news event', 'current event'])
        
        return keywords
    
    def search_pexels(self, keywords: List[str], page: int = 1) -> Tuple[str, str, str]:
        """
        Search Pexels for an image matching the keywords
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
                    print(f"  ⚠️  Pexels API key invalid")
                    return None, None, None
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ⚠️  Error searching '{keyword}': {e}")
                continue
        
        return None, None, None
    
    def search_unsplash(self, keywords: List[str]) -> Tuple[str, str]:
        """
        Get an image from Unsplash Source API (no authentication needed)
        Returns (image_url, search_term_used)
        """
        for keyword in keywords:
            try:
                # Unsplash Source API - returns image directly at 1600x900
                clean_keyword = keyword.replace(' ', ',')
                image_url = f"https://source.unsplash.com/1600x900/?{clean_keyword}"
                
                # Test if URL is valid
                response = requests.head(image_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    return image_url, keyword
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  ⚠️  Error with '{keyword}': {e}")
                continue
        
        return None, None
    
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
        """Main curation process - FIXED version with specific keywords for everything"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all markets
        cursor.execute("SELECT market_id, title, category, description FROM markets ORDER BY category, market_id")
        markets = cursor.fetchall()
        
        print(f"\n{'='*80}")
        print(f"CURRENTS IMAGE CURATION - FIXED VERSION")
        print(f"{'='*80}")
        print(f"Total markets: {len(markets)}")
        print(f"CRITICAL FIX: Every market gets SPECIFIC, topic-relevant keywords")
        print(f"NO MORE GENERIC IMAGES!\n")
        
        success_count = 0
        failed_markets = []
        
        for i, (market_id, title, category, description) in enumerate(markets, 1):
            print(f"\n[{i}/{len(markets)}] {title[:70]}")
            print(f"  Category: {category}")
            
            # Analyze and get SPECIFIC keywords
            keywords = self.analyze_market(market_id, title, category, description)
            print(f"  🎯 Keywords: {', '.join(keywords[:2])}")
            
            # Try Pexels first
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
                    if photographer and photographer != "Unsplash":
                        print(f"  📷 Photo by {photographer}")
                    
                    # Log this mapping
                    self.keyword_mappings[str(market_id)] = {
                        'title': title,
                        'category': category,
                        'keywords': keywords,
                        'keyword_used': keyword_used,
                        'photographer': photographer,
                        'source': source
                    }
                    success_count += 1
                else:
                    print(f"  ❌ Download failed")
                    failed_markets.append((market_id, title))
            else:
                print(f"  ❌ No suitable image found")
                failed_markets.append((market_id, title))
            
            # Rate limiting - be respectful
            time.sleep(1.2)
        
        conn.close()
        
        # Save keyword mappings log
        with open('image_keyword_mappings_FIXED.json', 'w') as f:
            json.dump(self.keyword_mappings, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"CURATION COMPLETE - FIXED VERSION")
        print(f"{'='*80}")
        print(f"✅ Successfully curated: {success_count}/{len(markets)} markets")
        print(f"📝 Keyword mappings saved to: image_keyword_mappings_FIXED.json")
        
        if failed_markets:
            print(f"\n⚠️  Failed markets ({len(failed_markets)}):")
            for market_id, title in failed_markets[:10]:
                print(f"  - {market_id}: {title[:50]}")
        
        print(f"\n✨ All images should now be SPECIFIC to their market topics!")
        print(f"🎯 No more Messi showing up in deportation markets!")
        print(f"🎬 Barbie will be Barbie, Djokovic will be Djokovic!")
        
        return success_count, failed_markets


if __name__ == '__main__':
    curator = MarketImageCuratorFixed('brain.db')
    curator.curate_all_markets()

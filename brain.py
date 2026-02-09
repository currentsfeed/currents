"""
BRain - Intelligence Layer for Currents
Handles ranking, trending, personalization
"""
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class BRain:
    def __init__(self, db_path='brain.db'):
        self.db_path = db_path
    
    def _get_conn(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def calculate_belief_intensity(self, market: Dict) -> float:
        """
        Calculate belief intensity score for a market
        
        Formula: volume_score * 0.4 + momentum * 0.3 + contestedness * 0.3
        """
        # Volume score (normalized)
        volume_score = market['volume_24h'] / 10000
        
        # Contestedness (how close to 50/50)
        prob = market['probability']
        contestedness = 1 - abs(0.5 - prob) * 2
        
        # Momentum (simplified - could be enhanced with history)
        momentum = 0.5  # Placeholder
        
        # Composite score
        intensity = (
            volume_score * 0.4 +
            momentum * 0.3 +
            contestedness * 0.3
        )
        
        return intensity
    
    def get_homepage_feed(self, user_id: Optional[str] = None, limit: int = 20) -> Dict:
        """
        Get ranked markets for homepage
        
        Returns: {
            'hero': [market],
            'grid': [markets],
            'stream': [markets]
        }
        """
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Fetch all open markets
        cursor.execute("""
            SELECT m.*, 
                   GROUP_CONCAT(DISTINCT mt.tag) as tags
            FROM markets m
            LEFT JOIN market_tags mt ON m.market_id = mt.market_id
            WHERE m.status = 'open'
            GROUP BY m.market_id
        """)
        
        markets = []
        for row in cursor.fetchall():
            market = dict(row)
            market['tags'] = market['tags'].split(',') if market['tags'] else []
            market['belief_intensity'] = self.calculate_belief_intensity(market)
            markets.append(market)
        
        # Sort by belief intensity
        markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
        
        # Split into sections
        hero = markets[0:1] if markets else []
        grid = markets[1:9] if len(markets) > 1 else []
        stream = markets[9:limit] if len(markets) > 9 else []
        
        conn.close()
        
        return {
            'hero': hero,
            'grid': grid,
            'stream': stream,
            'generated_at': datetime.now().isoformat()
        }
    
    def get_market_detail(self, market_id: str) -> Optional[Dict]:
        """Get full market details including history"""
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get market
        cursor.execute("""
            SELECT m.*,
                   GROUP_CONCAT(DISTINCT mt.tag) as tags,
                   GROUP_CONCAT(DISTINCT mtx.taxonomy_path) as taxonomy
            FROM markets m
            LEFT JOIN market_tags mt ON m.market_id = mt.market_id
            LEFT JOIN market_taxonomy mtx ON m.market_id = mtx.market_id
            WHERE m.market_id = ?
            GROUP BY m.market_id
        """, (market_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        market = dict(row)
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        market['taxonomy'] = market['taxonomy'].split(',') if market['taxonomy'] else []
        
        # Get probability history
        cursor.execute("""
            SELECT probability, volume, timestamp
            FROM probability_history
            WHERE market_id = ?
            ORDER BY timestamp ASC
        """, (market_id,))
        
        market['probability_history'] = [dict(row) for row in cursor.fetchall()]
        
        # Calculate outcomes
        market['outcomes'] = [
            {'name': 'Yes', 'probability': market['probability']},
            {'name': 'No', 'probability': 1 - market['probability']}
        ]
        
        conn.close()
        return market
    
    def get_related_markets(self, market_id: str, limit: int = 3) -> List[Dict]:
        """Find related markets based on tag similarity"""
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get target market tags
        cursor.execute("""
            SELECT tag FROM market_tags WHERE market_id = ?
        """, (market_id,))
        
        target_tags = set(row['tag'] for row in cursor.fetchall())
        
        if not target_tags:
            conn.close()
            return []
        
        # Find markets with overlapping tags
        cursor.execute("""
            SELECT m.*, 
                   COUNT(DISTINCT mt.tag) as tag_overlap,
                   GROUP_CONCAT(DISTINCT mt.tag) as tags
            FROM markets m
            JOIN market_tags mt ON m.market_id = mt.market_id
            WHERE mt.tag IN ({})
              AND m.market_id != ?
              AND m.status = 'open'
            GROUP BY m.market_id
            ORDER BY tag_overlap DESC
            LIMIT ?
        """.format(','.join('?' * len(target_tags))), (*target_tags, market_id, limit))
        
        related = []
        for row in cursor.fetchall():
            market = dict(row)
            market['tags'] = market['tags'].split(',') if market['tags'] else []
            related.append(market)
        
        conn.close()
        return related
    
    def track_interaction(self, user_id: str, market_id: str, event_type: str, metadata: Optional[Dict] = None):
        """Track user interaction for personalization"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO interactions (user_id, market_id, event_type, metadata, timestamp)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (user_id, market_id, event_type, str(metadata) if metadata else None))
        
        conn.commit()
        conn.close()
    
    def compute_trending(self, scope: str = 'global', window: str = '24h'):
        """Compute and cache trending scores"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Clear old cache
        cursor.execute("DELETE FROM trending_cache WHERE scope = ? AND window = ?", (scope, window))
        
        # Compute new scores (simplified - just using volume for now)
        cursor.execute("""
            SELECT market_id, volume_24h
            FROM markets
            WHERE status = 'open'
            ORDER BY volume_24h DESC
        """)
        
        rank = 1
        for row in cursor.fetchall():
            market_id, volume = row
            score = volume / 1000  # Normalize
            
            cursor.execute("""
                INSERT INTO trending_cache (market_id, scope, score, rank, window)
                VALUES (?, ?, ?, ?, ?)
            """, (market_id, scope, score, rank, window))
            
            rank += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Computed trending scores for {scope} / {window}")

if __name__ == '__main__':
    # Test the BRain
    brain = BRain()
    
    print("\n🧠 Testing BRain...\n")
    
    # Get homepage feed
    feed = brain.get_homepage_feed()
    print(f"📰 Homepage Feed:")
    print(f"  Hero: {feed['hero'][0]['title'] if feed['hero'] else 'None'}")
    print(f"  Grid: {len(feed['grid'])} markets")
    print(f"  Stream: {len(feed['stream'])} markets")
    
    # Get market detail
    if feed['hero']:
        market_id = feed['hero'][0]['market_id']
        detail = brain.get_market_detail(market_id)
        print(f"\n📊 Market Detail ({market_id}):")
        print(f"  Title: {detail['title']}")
        print(f"  Probability: {detail['probability'] * 100:.0f}%")
        print(f"  History points: {len(detail['probability_history'])}")
        
        # Get related
        related = brain.get_related_markets(market_id)
        print(f"  Related markets: {len(related)}")
    
    # Compute trending
    brain.compute_trending()
    
    print("\n✅ BRain is working!\n")

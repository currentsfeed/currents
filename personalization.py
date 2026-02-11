"""
BRain Personalization Engine
Implements full ranking algorithm from spec:
- PersonalScore (interest, similarity, depth, freshness, followup, negative, diversity)
- TrendingScore (24h rolling, localized + global blend)
- FinalScore = PersonalScore + trending + rising + editorial

Modified: Uses local SQLite database for market data
"""
import sqlite3
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import json

DB_PATH = 'brain.db'  # Local database for all data

# Ranking weights (from BRain spec)
PERSONAL_WEIGHTS = {
    'interest': 0.35,
    'similarity': 0.25,
    'depth': 0.15,
    'freshness': 0.10,
    'followup': 0.10,
    'negative': -0.10,
    'diversity': -0.05
}

FINAL_WEIGHTS = {
    'trending': 0.25,
    'rising': 0.20,
    'editorial': 0.05
}

class PersonalizationEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def _select_hero(self, ranked_markets: List[Dict]) -> List[Dict]:
        """
        Select hero market from visual priority categories with rotation
        Categories: Sports, Entertainment, Technology, Crypto
        Returns: List with 1 market (or empty if none found)
        """
        if not ranked_markets:
            return []
        
        # Visual priority categories (for hero)
        VISUAL_CATEGORIES = ['Sports', 'Entertainment', 'Technology', 'Crypto', 
                            'Soccer', 'Basketball', 'American Football', 'Baseball',
                            'Tennis', 'Formula 1', 'MMA']
        
        # Filter top 20 markets for visual categories
        visual_candidates = [
            m for m in ranked_markets[:20]
            if m.get('category', '') in VISUAL_CATEGORIES
        ]
        
        if not visual_candidates:
            # Fallback to top 5 if no visual markets found
            visual_candidates = ranked_markets[:5]
        
        # Randomly select from top visual candidates (adds rotation)
        hero_market = random.choice(visual_candidates[:min(10, len(visual_candidates))])
        return [hero_market]
    
    def _fetch_markets_from_db(self, limit: int = 200) -> List[Dict]:
        """Fetch markets from local database"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                m.market_id,
                m.title,
                m.description,
                m.category,
                m.probability,
                m.volume_24h,
                m.volume_total,
                m.image_url,
                m.created_at,
                m.resolution_date,
                m.editorial_description
            FROM markets m
            WHERE m.status = 'open'
            ORDER BY m.volume_total DESC
            LIMIT ?
        """, (limit,))
        
        markets = []
        for row in cursor.fetchall():
            market_id = row[0]
            market = {
                'market_id': market_id,
                'title': row[1],
                'description': row[2],
                'category': row[3],
                'probability': row[4],
                'volume_24h': row[5] or 0,
                'volume_total': row[6] or 0,
                'image_url': row[7],
                'created_at': row[8],
                'resolution_date': row[9],
                'editorial_description': row[10],
                'tags': []
            }
            
            # Fetch tags for this market
            cursor.execute("""
                SELECT tag FROM market_tags
                WHERE market_id = ?
                ORDER BY tag
            """, (market_id,))
            
            market['tags'] = [tag_row[0] for tag_row in cursor.fetchall()]
            
            markets.append(market)
        
        conn.close()
        return markets
    
    def get_personalized_feed(self, user_key: Optional[str] = None, limit: int = 20) -> Dict:
        """
        Get personalized feed for user
        If user_key is None or user has no profile, return global ranking
        """
        # Fetch markets from local database
        markets = self._fetch_markets_from_db(limit=200)
        
        if not markets:
            return {
                'hero': [],
                'grid': [],
                'stream': [],
                'personalized': False,
                'user_key': user_key,
                'error': 'No markets found in database'
            }
        
        # Check if user has profile (still in brain.db)
        conn = self._get_conn()
        cursor = conn.cursor()
        
        if user_key:
            cursor.execute("""
                SELECT total_interactions FROM user_profiles
                WHERE user_key = ?
            """, (user_key,))
            profile_row = cursor.fetchone()
            has_profile = profile_row and profile_row[0] > 0
        else:
            has_profile = False
        
        # Rank markets
        if has_profile:
            ranked_markets = self._rank_personalized(cursor, user_key, markets)
        else:
            ranked_markets = self._rank_global(markets)
        
        conn.close()
        
        # Split into sections
        # Hero: Select from visual priority categories (rotates randomly)
        hero = self._select_hero(ranked_markets)
        
        # Grid: 9 markets (after hero)
        # Remove hero market from ranked list
        remaining_markets = [m for m in ranked_markets if m['market_id'] != (hero[0]['market_id'] if hero else None)]
        grid = remaining_markets[0:9] if remaining_markets else []
        stream = remaining_markets[9:limit-1] if len(remaining_markets) > 9 else []
        
        return {
            'hero': hero,
            'grid': grid,
            'stream': stream,
            'personalized': has_profile,
            'user_key': user_key
        }
    
    def _rank_personalized(self, cursor, user_key: str, markets: List[Dict]) -> List[Dict]:
        """
        Rank markets using full personalization algorithm
        """
        # Get user profile
        user_scores = self._get_user_scores(cursor, user_key)
        recent_viewed = self._get_recent_viewed(cursor, user_key)
        
        scored_markets = []
        for market in markets:
            # Calculate PersonalScore components
            interest = self._calculate_interest(market, user_scores)
            similarity = self._calculate_similarity(market, recent_viewed, user_scores)
            depth = self._calculate_depth(cursor, user_key, market)
            freshness = self._calculate_freshness(market)
            followup = self._calculate_followup(cursor, user_key, market)
            negative = self._calculate_negative(market, user_scores)
            diversity = 0.0  # Will apply after sorting
            
            # PersonalScore
            personal_score = (
                PERSONAL_WEIGHTS['interest'] * interest +
                PERSONAL_WEIGHTS['similarity'] * similarity +
                PERSONAL_WEIGHTS['depth'] * depth +
                PERSONAL_WEIGHTS['freshness'] * freshness +
                PERSONAL_WEIGHTS['followup'] * followup +
                PERSONAL_WEIGHTS['negative'] * negative +
                PERSONAL_WEIGHTS['diversity'] * diversity
            )
            
            # Get trending score
            trending = self._get_trending_score(cursor, market['market_id'])
            
            # Get rising score (belief change)
            rising = self._calculate_rising(market)
            
            # Editorial boost (placeholder)
            editorial = 0.0
            
            # NEWS BOOST: Prioritize fresh news and sports (same as global ranking)
            news_boost = 0.0
            NEWS_CATEGORIES = ['Politics', 'Entertainment', 'World', 'Crime', 'Economics', 'Culture',
                              'Basketball', 'Soccer', 'Hockey', 'Baseball', 'Rugby', 'Australian Football']
            if market.get('category') in NEWS_CATEGORIES:
                created_at = market.get('created_at', '')
                if created_at:
                    try:
                        created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        hours_old = (datetime.now() - created_date).total_seconds() / 3600
                        
                        if hours_old < 24:
                            news_boost = 0.8
                        elif hours_old < 168:
                            news_boost = 0.5
                        elif hours_old < 720:
                            news_boost = 0.2
                    except:
                        pass
            
            # SPORTS BOOST: Extra boost for upcoming sports games (resolving in next 2-3 days)
            sports_boost = 0.0
            if market.get('category') in ['Basketball', 'Soccer', 'Hockey', 'Baseball', 'Rugby', 'Australian Football']:
                try:
                    resolution_date = market.get('resolution_date', '')
                    if resolution_date:
                        res_date = datetime.fromisoformat(resolution_date)
                        days_until = (res_date - datetime.now()).total_seconds() / 86400
                        
                        # Big boost for games in next 1-3 days
                        if 0 <= days_until <= 3:
                            sports_boost = 1.5  # HUGE boost for upcoming games
                except:
                    pass
            
            # FinalScore (with news boost + sports boost)
            final_score = (
                personal_score +
                FINAL_WEIGHTS['trending'] * trending +
                FINAL_WEIGHTS['rising'] * rising +
                FINAL_WEIGHTS['editorial'] * editorial +
                news_boost +
                sports_boost
            )
            
            market['scores'] = {
                'final': final_score,
                'personal': personal_score,
                'interest': interest,
                'similarity': similarity,
                'depth': depth,
                'freshness': freshness,
                'followup': followup,
                'negative': negative,
                'trending': trending,
                'rising': rising,
                'news_boost': news_boost,
                'sports_boost': sports_boost
            }
            
            scored_markets.append(market)
        
        # Sort by final score
        scored_markets.sort(key=lambda x: x['scores']['final'], reverse=True)
        
        # Apply diversity penalty
        scored_markets = self._apply_diversity_penalty(scored_markets)
        
        return scored_markets
    
    def _rank_global(self, markets: List[Dict]) -> List[Dict]:
        """
        Global ranking (no personalization) - belief intensity + trending + NEWS BOOST
        Prioritizes fresh news items (politics, entertainment, world events)
        """
        # Get brain.db connection for trending data
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # News categories that get freshness boost (including sports)
        NEWS_CATEGORIES = ['Politics', 'Entertainment', 'World', 'Crime', 'Economics', 'Culture',
                          'Basketball', 'Soccer', 'Hockey', 'Baseball', 'Rugby', 'Australian Football']
        
        for market in markets:
            # Belief intensity (volume + contestedness)
            volume_score = math.log(1 + market.get('volume_24h', 0)) / 10
            prob = market.get('probability', 0.5)
            contestedness = 1 - abs(0.5 - prob) * 2
            belief_intensity = volume_score * 0.6 + contestedness * 0.4
            
            # Trending
            trending = self._get_trending_score(cursor, market['market_id'])
            
            # Rising
            rising = self._calculate_rising(market)
            
            # NEWS BOOST: Prioritize fresh news items
            news_boost = 0.0
            if market.get('category') in NEWS_CATEGORIES:
                # Check how recent the market is
                created_at = market.get('created_at', '')
                if created_at:
                    try:
                        created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        hours_old = (datetime.now() - created_date).total_seconds() / 3600
                        
                        # Strong boost for very recent news (< 24h)
                        if hours_old < 24:
                            news_boost = 0.8
                        # Medium boost for recent news (< 7 days)
                        elif hours_old < 168:
                            news_boost = 0.5
                        # Small boost for somewhat recent (< 30 days)
                        elif hours_old < 720:
                            news_boost = 0.2
                    except:
                        pass
            
            # SPORTS BOOST: Extra boost for upcoming sports games (resolving in next 2-3 days)
            sports_boost = 0.0
            if market.get('category') in ['Basketball', 'Soccer', 'Hockey', 'Baseball', 'Rugby', 'Australian Football']:
                try:
                    resolution_date = market.get('resolution_date', '')
                    if resolution_date:
                        res_date = datetime.fromisoformat(resolution_date)
                        days_until = (res_date - datetime.now()).total_seconds() / 86400
                        
                        # Big boost for games in next 1-3 days
                        if 0 <= days_until <= 3:
                            sports_boost = 1.5  # HUGE boost for upcoming games
                except:
                    pass
            
            final_score = belief_intensity + FINAL_WEIGHTS['trending'] * trending + FINAL_WEIGHTS['rising'] * rising + news_boost + sports_boost
            
            market['scores'] = {
                'final': final_score,
                'belief_intensity': belief_intensity,
                'trending': trending,
                'rising': rising,
                'news_boost': news_boost,
                'sports_boost': sports_boost
            }
        
        conn.close()
        markets.sort(key=lambda x: x['scores']['final'], reverse=True)
        return markets
    
    def _get_user_scores(self, cursor, user_key: str) -> Dict:
        """Get user's category and tag scores"""
        cursor.execute("""
            SELECT topic_type, topic_value, score
            FROM user_topic_scores
            WHERE user_key = ?
        """, (user_key,))
        
        scores = defaultdict(dict)
        for row in cursor.fetchall():
            topic_type, topic_value, score = row
            scores[topic_type][topic_value] = score / 100.0  # Normalize to 0-1
        
        return scores
    
    def _get_recent_viewed(self, cursor, user_key: str, hours: int = 24) -> List[str]:
        """Get market IDs user viewed recently"""
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        cursor.execute("""
            SELECT DISTINCT market_id
            FROM user_interactions
            WHERE user_key = ? AND ts > ?
            ORDER BY ts DESC
            LIMIT 20
        """, (user_key, cutoff))
        
        return [row[0] for row in cursor.fetchall()]
    
    def _calculate_interest(self, market: Dict, user_scores: Dict) -> float:
        """
        Affinity from user profile to market tags/category
        TAG-LEVEL LEARNING (not category-level)
        Tags weighted much higher than categories
        """
        score = 0.0
        count = 0
        
        # Tag matches (PRIMARY - 90% weight)
        tags = market.get('tags', [])
        tag_scores = user_scores.get('tag', {})
        for tag in tags:
            if tag in tag_scores:
                score += tag_scores[tag] * 0.9
                count += 1
        
        # Category match (SECONDARY - only 10% weight)
        category = market.get('category')
        if category and category in user_scores.get('category', {}):
            score += user_scores['category'][category] * 0.1
            count += 1
        
        return score / max(count, 1)
    
    def _calculate_similarity(self, market: Dict, recent_viewed: List[str], user_scores: Dict) -> float:
        """
        Similarity to recently engaged markets
        """
        # Simplified: boost if same category as recently viewed
        if not recent_viewed:
            return 0.0
        
        # Check if market shares category with recent views
        # (Full implementation would compare tags/taxonomy)
        return 0.5  # Placeholder
    
    def _calculate_depth(self, cursor, user_key: str, market: Dict) -> float:
        """
        User engagement depth with similar markets
        """
        category = market.get('category')
        if not category:
            return 0.0
        
        # Get average dwell time on similar category markets
        cursor.execute("""
            SELECT AVG(CAST(dwell_ms AS REAL)) as avg_dwell
            FROM user_interactions ui
            JOIN markets m ON ui.market_id = m.market_id
            WHERE ui.user_key = ? AND m.category = ? AND ui.dwell_ms IS NOT NULL
        """, (user_key, category))
        
        row = cursor.fetchone()
        avg_dwell = row[0] if row and row[0] else 0
        
        # Normalize (30s = 0.5, 60s = 1.0)
        return min(1.0, avg_dwell / 60000)
    
    def _calculate_freshness(self, market: Dict) -> float:
        """
        Preference for newer markets (exp decay)
        """
        created_at = market.get('created_at')
        if not created_at:
            return 0.5
        
        try:
            created = datetime.fromisoformat(created_at)
            days_old = (datetime.now() - created).days
            # Decay: half-life of 7 days
            return math.exp(-days_old / 7)
        except:
            return 0.5
    
    def _calculate_followup(self, cursor, user_key: str, market: Dict) -> float:
        """
        Boost if meaningful change since last seen
        """
        market_id = market['market_id']
        
        cursor.execute("""
            SELECT belief_at_view FROM seen_snapshots
            WHERE user_key = ? AND market_id = ?
        """, (user_key, market_id))
        
        row = cursor.fetchone()
        if not row:
            return 0.0  # Never seen before
        
        belief_at_view = row[0]
        current_belief = market.get('probability', 0.5)
        
        # Check if changed by > 5%
        change = abs(current_belief - belief_at_view)
        if change >= 0.05:
            return change * 2  # Scale up the change
        
        return 0.0
    
    def _calculate_negative(self, market: Dict, user_scores: Dict) -> float:
        """
        Penalty from negative signals (hide/not_interested)
        """
        # Check if user has negative scores for this category/tags
        negatives = user_scores.get('negative', {})
        
        penalty = 0.0
        category = market.get('category')
        if category and category in negatives:
            penalty += abs(negatives[category])
        
        for tag in market.get('tags', []):
            if tag in negatives:
                penalty += abs(negatives[tag])
        
        return penalty
    
    def _get_trending_score(self, cursor, market_id: str) -> float:
        """
        Get trending score from cache
        """
        cursor.execute("""
            SELECT score FROM trending_cache
            WHERE market_id = ? AND scope = 'global' AND window = '24h'
        """, (market_id,))
        
        row = cursor.fetchone()
        return row[0] if row else 0.0
    
    def _calculate_rising(self, market: Dict) -> float:
        """
        Belief shift magnitude (simplified)
        """
        # TODO: Compare current probability to 24h ago
        # For now, use contestedness as proxy
        prob = market.get('probability', 0.5)
        return abs(0.5 - prob)
    
    def _apply_diversity_penalty(self, markets: List[Dict]) -> List[Dict]:
        """
        Penalize consecutive markets from same category
        """
        category_streak = defaultdict(int)
        
        for i, market in enumerate(markets):
            category = market.get('category', 'unknown')
            
            # Count streak length
            streak = 0
            for j in range(max(0, i-3), i):
                if markets[j].get('category') == category:
                    streak += 1
            
            # Apply penalty
            if streak >= 2:
                penalty = 0.1 * streak
                market['scores']['final'] -= penalty
                market['scores']['diversity'] = -penalty
        
        # Re-sort after penalty
        markets.sort(key=lambda x: x['scores']['final'], reverse=True)
        return markets

# Global instance
personalizer = PersonalizationEngine()

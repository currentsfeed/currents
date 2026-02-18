"""
BRain v1 - Scoring System
Implements NEW vs KNOWN user detection, component scoring, penalties, and bonuses
Per Roy's spec: balances relevance, freshness, trends, non-repetition
"""
import sqlite3
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

DB_PATH = 'brain.db'

class BRainV1Scorer:
    def __init__(self, db_path=DB_PATH, config=None):
        self.db_path = db_path
        
        # Load config
        if config is None:
            import json
            with open('brain_v1_config.json', 'r') as f:
                config = json.load(f)
        
        self.config = config
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def sigmoid(self, x: float) -> float:
        """Sigmoid normalization: 1 / (1 + exp(-x))"""
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0
    
    def log1p(self, x: float) -> float:
        """log(1 + x)"""
        return math.log(1.0 + max(0, x))
    
    def is_new_user(self, user_key: str) -> bool:
        """
        Determine if user is NEW (< 10 interactions in 30d) or KNOWN
        
        Per spec: NEW if interactions_count_30d < 10 (excluding impressions)
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        
        cursor.execute("""
            SELECT COUNT(*)
            FROM user_interactions
            WHERE user_key = ?
              AND event_type != 'impression'
              AND ts > ?
        """, (user_key, cutoff))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        threshold = self.config['user_types']['new_user_threshold']
        return count < threshold
    
    def calculate_lt_score(self, market: Dict, user_key: str) -> float:
        """
        Calculate Long-Term relevance score
        Based on user_topic_scores (long-term learned preferences)
        
        Returns: 0.0-1.0 normalized similarity
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Get user's long-term scores
        cursor.execute("""
            SELECT topic_type, topic_value, score
            FROM user_topic_scores
            WHERE user_key = ?
        """, (user_key,))
        
        user_scores = defaultdict(dict)
        for row in cursor.fetchall():
            topic_type, topic_value, score = row
            user_scores[topic_type][topic_value] = score / 100.0  # Normalize
        
        conn.close()
        
        # Calculate similarity
        score = 0.0
        
        # Category match
        category = market.get('category')
        if category and category in user_scores.get('category', {}):
            score += user_scores['category'][category] * 0.5
        
        # Tag matches
        tags = market.get('tags', [])
        tag_scores = user_scores.get('tag', {})
        for tag in tags:
            if tag in tag_scores:
                score += tag_scores[tag] * 0.3
        
        # Normalize to 0-1 (cap at 1.0)
        return min(score, 1.0)
    
    def calculate_st_score(self, market: Dict, user_key: str) -> float:
        """
        Calculate Short-Term (session) relevance score
        Based on user_session_state (recent intent)
        
        Returns: 0.0-1.0 normalized similarity
        """
        try:
            from session_manager import session_manager
        except ImportError:
            return 0.0
        
        # Get session weights
        session = session_manager.get_session_weights(user_key)
        category_weights = session['category_weights']
        tag_weights = session['tag_weights']
        
        score = 0.0
        
        # Category match
        category = market.get('category')
        if category and category in category_weights:
            # Normalize session weights (they can be > 1.0)
            max_cat_weight = max(category_weights.values()) if category_weights else 1.0
            normalized = category_weights[category] / max(max_cat_weight, 1.0)
            score += normalized * 0.5
        
        # Tag matches
        tags = market.get('tags', [])
        if tag_weights:
            max_tag_weight = max(tag_weights.values())
            for tag in tags:
                if tag in tag_weights:
                    normalized = tag_weights[tag] / max(max_tag_weight, 1.0)
                    score += normalized * 0.3
        
        return min(score, 1.0)
    
    def calculate_trend_score(self, market: Dict, geo_bucket: str) -> float:
        """
        Calculate Trend score (blend of global + local)
        
        Per spec:
        - TG = sigmoid(0.7*log1p(trades_1h_GLOBAL) + 0.3*log1p(views_1h_GLOBAL))
        - TL = sigmoid(0.7*log1p(trades_1h_LOCAL) + 0.3*log1p(views_1h_LOCAL))
        - Trend = 0.7*TG + 0.3*TL
        
        Returns: 0.0-1.0 trending score
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        market_id = market['market_id']
        
        # Get global velocity
        cursor.execute("""
            SELECT trades_1h, views_1h
            FROM market_velocity_rollups
            WHERE market_id = ? AND geo_bucket = 'GLOBAL'
        """, (market_id,))
        
        row_global = cursor.fetchone()
        if row_global:
            trades_global = row_global[0] or 0
            views_global = row_global[1] or 0
        else:
            trades_global = 0
            views_global = 0
        
        # Get local velocity
        cursor.execute("""
            SELECT trades_1h, views_1h
            FROM market_velocity_rollups
            WHERE market_id = ? AND geo_bucket = ?
        """, (market_id, geo_bucket))
        
        row_local = cursor.fetchone()
        if row_local:
            trades_local = row_local[0] or 0
            views_local = row_local[1] or 0
        else:
            trades_local = 0
            views_local = 0
        
        conn.close()
        
        # Calculate TG and TL
        TG = self.sigmoid(0.7 * self.log1p(trades_global) + 0.3 * self.log1p(views_global))
        TL = self.sigmoid(0.7 * self.log1p(trades_local) + 0.3 * self.log1p(views_local))
        
        # Blend per spec
        blend = self.config['scoring']['trend_blend']
        trend_score = blend['global_weight'] * TG + blend['local_weight'] * TL
        
        return trend_score
    
    def calculate_fresh_score(self, market: Dict) -> float:
        """
        Calculate Freshness score
        
        Per spec: Fresh = exp(- age_hours / 72.0)
        Decays over ~3 days
        
        Returns: 0.0-1.0 freshness score
        """
        created_at = market.get('created_at')
        if not created_at:
            return 0.5  # Default
        
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except:
            return 0.5
        
        age_hours = (datetime.now() - created).total_seconds() / 3600
        
        decay_hours = self.config['freshness']['decay_hours']
        fresh_score = math.exp(-age_hours / decay_hours)
        
        return fresh_score
    
    def calculate_base_score(self, market: Dict, user_key: str, 
                            geo_bucket: str, is_new: bool) -> Dict:
        """
        Calculate base score based on user type
        
        NEW: Base = 0.55*Trend + 0.30*ST + 0.15*Fresh
        KNOWN: Base = 0.45*LT + 0.25*ST + 0.20*Trend + 0.10*Fresh
        
        Returns: {base_score, components: {LT, ST, Trend, Fresh}}
        """
        # Calculate components
        LT = self.calculate_lt_score(market, user_key) if not is_new else 0.0
        ST = self.calculate_st_score(market, user_key)
        Trend = self.calculate_trend_score(market, geo_bucket)
        Fresh = self.calculate_fresh_score(market)
        
        # Apply weights based on user type
        if is_new:
            weights = self.config['scoring']['new_user']
            base_score = (
                weights['trend_weight'] * Trend +
                weights['session_weight'] * ST +
                weights['fresh_weight'] * Fresh
            )
        else:
            weights = self.config['scoring']['known_user']
            base_score = (
                weights['long_term_weight'] * LT +
                weights['session_weight'] * ST +
                weights['trend_weight'] * Trend +
                weights['fresh_weight'] * Fresh
            )
        
        return {
            'base_score': base_score,
            'components': {
                'LT': LT,
                'ST': ST,
                'Trend': Trend,
                'Fresh': Fresh
            }
        }
    
    def calculate_cooldown_mult(self, last_shown_at: Optional[str]) -> float:
        """
        Calculate cooldown multiplier based on time since last shown
        
        Per spec:
        - < 2h: 0.10
        - 2-6h: 0.35
        - 6-24h: 0.70
        - else: 1.00
        
        Returns: multiplier 0.0-1.0
        """
        if not last_shown_at:
            return 1.00
        
        try:
            last_shown = datetime.fromisoformat(last_shown_at.replace('Z', '+00:00'))
        except:
            return 1.00
        
        hours_since = (datetime.now() - last_shown).total_seconds() / 3600
        
        cooldown_config = self.config['penalties']['cooldown']
        
        if hours_since < 2:
            return cooldown_config['2h']
        elif hours_since < 6:
            return cooldown_config['6h']
        elif hours_since < 24:
            return cooldown_config['24h']
        else:
            return cooldown_config['default']
    
    def calculate_freq_mult(self, impressions_24h: int) -> float:
        """
        Calculate frequency multiplier based on 24h impression count
        
        Per spec:
        - 0: 1.00
        - 1: 0.80
        - 2: 0.60
        - 3: 0.40
        - 4+: 0.25
        
        Returns: multiplier 0.0-1.0
        """
        freq_config = self.config['penalties']['frequency']
        
        if impressions_24h == 0:
            return freq_config['0']
        elif impressions_24h == 1:
            return freq_config['1']
        elif impressions_24h == 2:
            return freq_config['2']
        elif impressions_24h == 3:
            return freq_config['3']
        else:
            return freq_config['4+']
    
    def is_changed(self, market: Dict, geo_bucket: str) -> Tuple[bool, Dict]:
        """
        Determine if market has "changed" enough to justify re-show
        
        Changed is TRUE if ANY:
        - odds_change_1h >= 0.03 (3 percentage points)
        - OR ends_in_hours <= 6
        
        Returns: (is_changed, details)
        """
        market_id = market['market_id']
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Get odds change
        cursor.execute("""
            SELECT odds_change_1h
            FROM market_velocity_rollups
            WHERE market_id = ? AND geo_bucket = ?
        """, (market_id, geo_bucket))
        
        row = cursor.fetchone()
        odds_change_1h = row[0] if row else 0.0
        
        conn.close()
        
        # Check odds change threshold
        changed_config = self.config['changed_logic']
        odds_changed = odds_change_1h >= changed_config['odds_change_threshold']
        
        # Check if ending soon
        resolution_date = market.get('resolution_date')
        ending_soon = False
        ends_in_hours = None
        
        if resolution_date:
            try:
                res_date = datetime.fromisoformat(resolution_date.replace('Z', '+00:00'))
                ends_in_hours = (res_date - datetime.now()).total_seconds() / 3600
                ending_soon = ends_in_hours <= changed_config['ending_soon_hours']
            except:
                pass
        
        is_changed = odds_changed or ending_soon
        
        return is_changed, {
            'odds_change_1h': odds_change_1h,
            'ends_in_hours': ends_in_hours,
            'odds_changed': odds_changed,
            'ending_soon': ending_soon
        }
    
    def calculate_final_score(self, market: Dict, user_key: str, 
                             geo_bucket: str, impression_data: Optional[Dict] = None) -> Dict:
        """
        Calculate final score with all components, penalties, and bonuses
        
        Per spec:
        Score = (Base * cooldown_mult * freq_mult) + changed_boost + owned_boost
        
        Returns: {score, reason_tags, components, penalties, bonuses}
        """
        # Determine user type
        is_new = self.is_new_user(user_key)
        
        # Calculate base score
        base_result = self.calculate_base_score(market, user_key, geo_bucket, is_new)
        base_score = base_result['base_score']
        components = base_result['components']
        
        # Get impression data
        if impression_data is None:
            impression_data = {
                'impressions_24h': 0,
                'impressions_7d': 0,
                'last_shown_at': None,
                'last_clicked_at': None,
                'last_traded_at': None,
                'last_hidden_at': None
            }
        
        # Check if hidden recently (suppress entirely)
        hide_days = self.config['penalties']['hide_suppression_days']
        if impression_data.get('last_hidden_at'):
            try:
                hidden_at = datetime.fromisoformat(impression_data['last_hidden_at'].replace('Z', '+00:00'))
                days_since_hide = (datetime.now() - hidden_at).total_seconds() / 86400
                if days_since_hide < hide_days:
                    # Drop from candidates (return very low score)
                    return {
                        'score': 0.0,
                        'reason_tags': ['Hidden'],
                        'components': components,
                        'penalties': {'hidden': True},
                        'bonuses': {}
                    }
            except:
                pass
        
        # Calculate penalties
        cooldown_mult = self.calculate_cooldown_mult(impression_data.get('last_shown_at'))
        freq_mult = self.calculate_freq_mult(impression_data.get('impressions_24h', 0))
        
        # Check if changed
        is_changed, changed_details = self.is_changed(market, geo_bucket)
        
        # Apply "changed" softening
        changed_config = self.config['changed_logic']
        if is_changed:
            cooldown_mult = max(cooldown_mult, changed_config['changed_cooldown_floor'])
            freq_mult = max(freq_mult, changed_config['changed_freq_floor'])
            changed_boost = changed_config['changed_boost']
        else:
            changed_boost = 0.0
        
        # Calculate owned boost
        owned_boost = 0.0
        if impression_data.get('last_traded_at'):
            try:
                traded_at = datetime.fromisoformat(impression_data['last_traded_at'].replace('Z', '+00:00'))
                days_since_trade = (datetime.now() - traded_at).total_seconds() / 86400
                owned_days = self.config['bonuses']['owned_days']
                if days_since_trade < owned_days:
                    owned_boost = self.config['bonuses']['owned_boost']
            except:
                pass
        
        # Final score
        score = (base_score * cooldown_mult * freq_mult) + changed_boost + owned_boost
        
        # Build reason tags
        reason_tags = []
        if is_new:
            reason_tags.append('NewUser')
        if components['LT'] > 0.5:
            reason_tags.append('LT:Match')
        if components['ST'] > 0.5:
            reason_tags.append('ST:Match')
        if components['Trend'] > 0.5:
            reason_tags.append('Trend:High')
        if components['Fresh'] > 0.7:
            reason_tags.append('Fresh')
        if is_changed:
            reason_tags.append('Changed')
        if owned_boost > 0:
            reason_tags.append('Owned')
        if cooldown_mult < 1.0:
            reason_tags.append(f'Cooldown:{cooldown_mult:.2f}')
        if freq_mult < 1.0:
            reason_tags.append(f'Freq:{freq_mult:.2f}')
        
        return {
            'score': score,
            'reason_tags': reason_tags,
            'components': components,
            'penalties': {
                'cooldown_mult': cooldown_mult,
                'freq_mult': freq_mult
            },
            'bonuses': {
                'changed_boost': changed_boost,
                'owned_boost': owned_boost,
                'changed_details': changed_details
            }
        }

# Global instance
brain_v1_scorer = BRainV1Scorer()

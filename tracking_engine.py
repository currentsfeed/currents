"""
BRain Tracking Engine
Captures user interactions and updates profile scores in real-time
"""
import sqlite3
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional

DB_PATH = 'brain.db'

# Action weights (from BRain spec)
ACTION_WEIGHTS = {
    'participate': 6.0,
    'participate_intent': 3.0,
    'share': 4.0,
    'comment': 4.5,
    'bookmark': 3.5,
    'click': 2.0,
    'view_market': 2.0,
    'return_visit': 3.0,
    'dwell_30+': 2.0,
    'dwell_5+': 1.0,
    'scroll_past': -0.5,
    'skip_fast': -1.0,
    'hide': -6.0
}

# Score multipliers for different topic types
SCORE_MULTIPLIERS = {
    'category': 0.35,
    'tag': 0.30,
    'topic': 0.25,
    'related': 0.20
}

# Profile limits
TOP_N_TAGS = 200
TOP_N_TAXONOMY = 200
DECAY_HALF_LIFE_DAYS = 30

class TrackingEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def _get_conn(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def record_interaction(self, user_key: str, market_id: str, event_type: str,
                          dwell_ms: Optional[int] = None, section: Optional[str] = None,
                          position: Optional[int] = None, geo_country: Optional[str] = None) -> int:
        """
        Record a user interaction event
        Returns: interaction_id
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Insert interaction
        cursor.execute("""
            INSERT INTO user_interactions 
            (user_key, market_id, event_type, ts, dwell_ms, section, position, geo_country)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_key, market_id, event_type, datetime.now().isoformat(),
              dwell_ms, section, position, geo_country))
        
        interaction_id = cursor.lastrowid
        
        # Update profile immediately
        self._update_profile_from_interaction(
            cursor, user_key, market_id, event_type, dwell_ms
        )
        
        conn.commit()
        conn.close()
        
        return interaction_id
    
    def _update_profile_from_interaction(self, cursor, user_key: str, market_id: str,
                                        event_type: str, dwell_ms: Optional[int]):
        """
        Update user profile based on interaction
        """
        # Get market metadata
        cursor.execute("""
            SELECT category FROM markets WHERE market_id = ?
        """, (market_id,))
        row = cursor.fetchone()
        if not row:
            return
        
        category = row[0]
        
        # Get market tags
        cursor.execute("""
            SELECT tag FROM market_tags WHERE market_id = ?
        """, (market_id,))
        tags = [r[0] for r in cursor.fetchall()]
        
        # Calculate score delta
        base_weight = ACTION_WEIGHTS.get(event_type, 1.0)
        
        # Adjust for dwell time if applicable
        if event_type.startswith('dwell') or dwell_ms:
            if dwell_ms:
                # Scale by dwell time (max at 60s)
                dwell_factor = min(1.0, dwell_ms / 60000)
                delta = base_weight * dwell_factor
            else:
                delta = base_weight
        else:
            delta = base_weight
        
        # Update category score
        if category:
            self._update_topic_score(
                cursor, user_key, 'category', category,
                delta * SCORE_MULTIPLIERS['category']
            )
        
        # Update tag scores
        for tag in tags:
            self._update_topic_score(
                cursor, user_key, 'tag', tag,
                delta * SCORE_MULTIPLIERS['tag']
            )
        
        # Record co-occurrences
        if len(tags) > 1:
            for i, tag_a in enumerate(tags):
                for tag_b in tags[i+1:]:
                    self._record_cooccurrence(cursor, tag_a, tag_b)
        
        # Update user profile last_active
        cursor.execute("""
            INSERT INTO user_profiles (user_key, last_active, total_interactions)
            VALUES (?, ?, 1)
            ON CONFLICT(user_key) DO UPDATE SET
                last_active = ?,
                total_interactions = total_interactions + 1
        """, (user_key, datetime.now().isoformat(), datetime.now().isoformat()))
    
    def _update_topic_score(self, cursor, user_key: str, topic_type: str,
                           topic_value: str, delta: float):
        """
        Update score for a specific topic
        """
        # Get current score
        cursor.execute("""
            SELECT raw_score, interactions, last_updated FROM user_topic_scores
            WHERE user_key = ? AND topic_type = ? AND topic_value = ?
        """, (user_key, topic_type, topic_value))
        
        row = cursor.fetchone()
        
        if row:
            raw_score, interactions, last_updated = row
            
            # Apply decay
            if last_updated:
                days_since = (datetime.now() - datetime.fromisoformat(last_updated)).days
                decay_factor = math.exp(-days_since / DECAY_HALF_LIFE_DAYS)
                raw_score = raw_score * decay_factor
            
            # Add delta
            new_raw_score = raw_score + delta
            new_interactions = interactions + 1
            
            # Normalize to 0-100 scale with sigmoid
            normalized_score = 100 / (1 + math.exp(-new_raw_score + 5))
            
            # Update
            cursor.execute("""
                UPDATE user_topic_scores
                SET raw_score = ?, score = ?, interactions = ?, last_updated = ?
                WHERE user_key = ? AND topic_type = ? AND topic_value = ?
            """, (new_raw_score, normalized_score, new_interactions,
                  datetime.now().isoformat(), user_key, topic_type, topic_value))
        else:
            # Create new entry
            raw_score = delta
            normalized_score = 100 / (1 + math.exp(-raw_score + 5))
            
            cursor.execute("""
                INSERT INTO user_topic_scores
                (user_key, topic_type, topic_value, raw_score, score, interactions, last_updated)
                VALUES (?, ?, ?, ?, ?, 1, ?)
            """, (user_key, topic_type, topic_value, raw_score, normalized_score,
                  datetime.now().isoformat()))
        
        # Record score history snapshot (for evolution timeline)
        cursor.execute("""
            INSERT INTO score_history (user_key, topic_type, topic_value, score)
            VALUES (?, ?, ?, ?)
        """, (user_key, topic_type, topic_value, normalized_score))
    
    def _record_cooccurrence(self, cursor, tag_a: str, tag_b: str):
        """
        Record that two tags appeared together
        """
        # Ensure alphabetical order for consistent storage
        if tag_a > tag_b:
            tag_a, tag_b = tag_b, tag_a
        
        cursor.execute("""
            INSERT INTO tag_cooccurrence (tag_a, tag_b, count)
            VALUES (?, ?, 1)
            ON CONFLICT(tag_a, tag_b) DO UPDATE SET
                count = count + 1,
                last_updated = CURRENT_TIMESTAMP
        """, (tag_a, tag_b))
    
    def record_seen(self, user_key: str, market_id: str, belief: float,
                   volume: float, status: str) -> None:
        """
        Record that user saw a market (for resurfacing logic)
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO seen_snapshots
            (user_key, market_id, last_seen_ts, belief_at_view, volume_at_view,
             status_at_view, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_key, market_id) DO UPDATE SET
                last_seen_ts = ?,
                belief_at_view = ?,
                volume_at_view = ?,
                status_at_view = ?,
                updated_at = ?
        """, (user_key, market_id, datetime.now().isoformat(), belief, volume, status,
              datetime.now().isoformat(),
              datetime.now().isoformat(), belief, volume, status,
              datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self, user_key: str) -> Dict:
        """
        Get complete user profile with top scores
        """
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get basic profile
        cursor.execute("""
            SELECT * FROM user_profiles WHERE user_key = ?
        """, (user_key,))
        profile_row = cursor.fetchone()
        
        if not profile_row:
            conn.close()
            return None
        
        profile = dict(profile_row)
        
        # Get top category scores
        cursor.execute("""
            SELECT topic_value, score, interactions, last_updated
            FROM user_topic_scores
            WHERE user_key = ? AND topic_type = 'category'
            ORDER BY score DESC
            LIMIT 20
        """, (user_key,))
        profile['categories'] = [dict(row) for row in cursor.fetchall()]
        
        # Get top tag scores
        cursor.execute("""
            SELECT topic_value, score, interactions, last_updated
            FROM user_topic_scores
            WHERE user_key = ? AND topic_type = 'tag'
            ORDER BY score DESC
            LIMIT 20
        """, (user_key,))
        profile['tags'] = [dict(row) for row in cursor.fetchall()]
        
        # Get recent interactions
        cursor.execute("""
            SELECT i.*, m.title as market_title, m.category
            FROM user_interactions i
            LEFT JOIN markets m ON i.market_id = m.market_id
            WHERE i.user_key = ?
            ORDER BY i.ts DESC
            LIMIT 20
        """, (user_key,))
        profile['recent_interactions'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return profile
    
    def get_all_users(self) -> List[Dict]:
        """
        Get list of all users who have interacted
        """
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_key, display_name, total_interactions, last_active
            FROM user_profiles
            ORDER BY last_active DESC
        """)
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def get_score_evolution(self, user_key: str, topic_type: str, topic_value: str) -> List[Dict]:
        """
        Get score history for timeline charts
        """
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT snapshot_ts, score
            FROM score_history
            WHERE user_key = ? AND topic_type = ? AND topic_value = ?
            ORDER BY snapshot_ts ASC
        """, (user_key, topic_type, topic_value))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return history
    
    def get_cooccurrence_matrix(self, top_n: int = 20) -> Dict:
        """
        Get tag co-occurrence matrix for heatmap
        """
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get top N most co-occurring tags
        cursor.execute("""
            SELECT tag_a, tag_b, count
            FROM tag_cooccurrence
            ORDER BY count DESC
            LIMIT ?
        """, (top_n * top_n,))
        
        cooccurrences = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return cooccurrences

# Global instance
tracker = TrackingEngine()

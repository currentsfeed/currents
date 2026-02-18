"""
BRain v1 - Session State Manager
Manages short-term user intent with fast decay (session vs long-term)
"""
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from collections import defaultdict

DB_PATH = 'brain.db'

class SessionManager:
    def __init__(self, db_path=DB_PATH, config=None):
        self.db_path = db_path
        self.config = config or {
            'timeout_minutes': 60,
            'decay_multiplier': 0.90
        }
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def get_or_create_session(self, user_key: str) -> Dict:
        """
        Get active session or create new one if expired
        
        Returns: {session_id, tag_weights, category_weights, last_event_at}
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        now = datetime.now()
        timeout_minutes = self.config['timeout_minutes']
        
        # Check for existing session
        cursor.execute("""
            SELECT session_id, tag_weights, category_weights, last_event_at, expires_at
            FROM user_session_state
            WHERE user_key = ?
        """, (user_key,))
        
        row = cursor.fetchone()
        
        if row:
            session_id, tag_weights_json, category_weights_json, last_event_str, expires_at_str = row
            last_event_at = datetime.fromisoformat(last_event_str)
            expires_at = datetime.fromisoformat(expires_at_str)
            
            # Check if session expired (60min timeout)
            time_since_last = (now - last_event_at).total_seconds() / 60
            
            if time_since_last <= timeout_minutes and now < expires_at:
                # Session still active
                conn.close()
                return {
                    'session_id': session_id,
                    'tag_weights': json.loads(tag_weights_json),
                    'category_weights': json.loads(category_weights_json),
                    'last_event_at': last_event_at
                }
        
        # Create new session (expired or doesn't exist)
        session_id = str(uuid.uuid4())
        expires_at = now + timedelta(hours=2)  # Max session lifetime
        
        cursor.execute("""
            INSERT INTO user_session_state
                (user_key, session_id, tag_weights, category_weights, 
                 last_event_at, expires_at)
            VALUES (?, ?, '{}', '{}', ?, ?)
            ON CONFLICT(user_key) DO UPDATE SET
                session_id = ?,
                tag_weights = '{}',
                category_weights = '{}',
                last_event_at = ?,
                expires_at = ?
        """, (user_key, session_id, now, expires_at,
              session_id, now, expires_at))
        
        conn.commit()
        conn.close()
        
        return {
            'session_id': session_id,
            'tag_weights': {},
            'category_weights': {},
            'last_event_at': now
        }
    
    def update_session_weights(self, user_key: str, market_data: Dict, 
                               event_weight: float):
        """
        Update session weights with decay
        
        Applies:
        1. Decay existing weights by 0.90
        2. Add new event contribution
        
        market_data: {category, tags: []}
        event_weight: Action weight (e.g., 6.0 for participate, 2.0 for click)
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Get current session
        session = self.get_or_create_session(user_key)
        
        tag_weights = session['tag_weights']
        category_weights = session['category_weights']
        
        decay_mult = self.config['decay_multiplier']
        
        # Apply decay to all existing weights
        for tag in tag_weights:
            tag_weights[tag] *= decay_mult
        
        for cat in category_weights:
            category_weights[cat] *= decay_mult
        
        # Add new contributions
        category = market_data.get('category')
        if category:
            category_weights[category] = category_weights.get(category, 0.0) + event_weight
        
        tags = market_data.get('tags', [])
        for tag in tags:
            tag_weights[tag] = tag_weights.get(tag, 0.0) + (event_weight * 0.8)  # Tag multiplier
        
        # Trim to top N to prevent unbounded growth
        # Keep top 50 tags and top 20 categories
        tag_weights = dict(sorted(tag_weights.items(), key=lambda x: x[1], reverse=True)[:50])
        category_weights = dict(sorted(category_weights.items(), key=lambda x: x[1], reverse=True)[:20])
        
        # Update database
        now = datetime.now()
        expires_at = now + timedelta(hours=2)
        
        cursor.execute("""
            UPDATE user_session_state
            SET tag_weights = ?,
                category_weights = ?,
                last_event_at = ?,
                expires_at = ?
            WHERE user_key = ?
        """, (json.dumps(tag_weights), json.dumps(category_weights),
              now, expires_at, user_key))
        
        conn.commit()
        conn.close()
    
    def get_session_weights(self, user_key: str) -> Dict:
        """
        Get current session weights
        
        Returns: {tag_weights: {}, category_weights: {}}
        """
        session = self.get_or_create_session(user_key)
        return {
            'tag_weights': session['tag_weights'],
            'category_weights': session['category_weights']
        }
    
    def cleanup_expired_sessions(self):
        """
        Remove expired sessions (maintenance job)
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        now = datetime.now()
        
        cursor.execute("""
            DELETE FROM user_session_state
            WHERE expires_at < ?
        """, (now,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted

# Global instance
session_manager = SessionManager()

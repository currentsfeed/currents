"""
BRain v1 - Impression Tracker
Handles impression logging with frequency caps and cooldown tracking
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DB_PATH = 'brain.db'

class ImpressionTracker:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def log_impressions(self, user_key: str, market_ids: List[str], 
                       timestamp: Optional[datetime] = None) -> int:
        """
        Log impressions for a batch of markets shown to user
        Updates impressions_24h, impressions_7d, last_shown_at
        
        Returns: number of impressions logged
        """
        if not market_ids:
            return 0
        
        if timestamp is None:
            timestamp = datetime.now()
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Batch upsert impressions
        logged_count = 0
        for market_id in market_ids:
            cursor.execute("""
                INSERT INTO user_market_impressions 
                    (user_key, market_id, impressions_24h, impressions_7d, 
                     last_shown_at, updated_at)
                VALUES (?, ?, 1, 1, ?, ?)
                ON CONFLICT(user_key, market_id) DO UPDATE SET
                    impressions_24h = impressions_24h + 1,
                    impressions_7d = impressions_7d + 1,
                    last_shown_at = ?,
                    updated_at = ?
            """, (user_key, market_id, timestamp, timestamp, timestamp, timestamp))
            logged_count += 1
        
        # Also log as 'impression' events in user_interactions for velocity tracking
        for market_id in market_ids:
            cursor.execute("""
                INSERT INTO user_interactions
                    (user_key, market_id, event_type, ts)
                VALUES (?, ?, 'impression', ?)
            """, (user_key, market_id, timestamp))
        
        conn.commit()
        conn.close()
        
        return logged_count
    
    def update_interaction_timestamp(self, user_key: str, market_id: str,
                                     interaction_type: str,
                                     timestamp: Optional[datetime] = None):
        """
        Update last_clicked_at, last_traded_at, or last_hidden_at
        
        interaction_type: 'click', 'trade', 'hide'
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        column_map = {
            'click': 'last_clicked_at',
            'trade': 'last_traded_at',
            'hide': 'last_hidden_at'
        }
        
        column = column_map.get(interaction_type)
        if not column:
            conn.close()
            return
        
        # Update or insert
        cursor.execute(f"""
            INSERT INTO user_market_impressions
                (user_key, market_id, {column}, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_key, market_id) DO UPDATE SET
                {column} = ?,
                updated_at = ?
        """, (user_key, market_id, timestamp, timestamp, timestamp, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_impression_data(self, user_key: str, market_ids: List[str]) -> Dict[str, Dict]:
        """
        Get impression data for multiple markets
        
        Returns: {market_id: {impressions_24h, impressions_7d, last_shown_at, ...}}
        """
        if not market_ids:
            return {}
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in market_ids])
        cursor.execute(f"""
            SELECT market_id, impressions_24h, impressions_7d,
                   last_shown_at, last_clicked_at, last_traded_at, last_hidden_at
            FROM user_market_impressions
            WHERE user_key = ? AND market_id IN ({placeholders})
        """, [user_key] + market_ids)
        
        results = {}
        for row in cursor.fetchall():
            results[row[0]] = {
                'impressions_24h': row[1],
                'impressions_7d': row[2],
                'last_shown_at': row[3],
                'last_clicked_at': row[4],
                'last_traded_at': row[5],
                'last_hidden_at': row[6]
            }
        
        conn.close()
        return results
    
    def cleanup_old_impressions(self, days: int = 7):
        """
        Reset impression counters for data older than N days
        Run this as a daily maintenance job
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cutoff_24h = (datetime.now() - timedelta(hours=24)).isoformat()
        cutoff_7d = (datetime.now() - timedelta(days=7)).isoformat()
        
        # Reset 24h counters
        cursor.execute("""
            UPDATE user_market_impressions
            SET impressions_24h = 0
            WHERE last_shown_at < ?
        """, (cutoff_24h,))
        
        # Reset 7d counters
        cursor.execute("""
            UPDATE user_market_impressions
            SET impressions_7d = 0
            WHERE last_shown_at < ?
        """, (cutoff_7d,))
        
        conn.commit()
        
        # Get counts
        cursor.execute("SELECT changes()")
        changes = cursor.fetchone()[0]
        
        conn.close()
        return changes

# Global instance
impression_tracker = ImpressionTracker()

"""
BRain v1 - Velocity Computer
Computes rolling activity stats (5m/1h/24h) for trending and "changed" logic
Run this every 1-5 minutes via cron
"""
import sqlite3
import math
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

DB_PATH = 'brain.db'

class VelocityComputer:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def compute_all_rollups(self):
        """
        Compute velocity rollups for all markets and geo buckets
        Call this every 1-5 minutes
        
        Returns: {updated_count, duration_ms}
        """
        start = datetime.now()
        
        # Compute global rollups
        global_count = self._compute_rollups_for_geo('GLOBAL')
        
        # Compute per-country rollups (get active countries from recent interactions)
        countries = self._get_active_countries()
        country_count = 0
        for country in countries:
            country_count += self._compute_rollups_for_geo(country)
        
        # Compute odds changes
        odds_count = self._compute_odds_changes()
        
        duration_ms = (datetime.now() - start).total_seconds() * 1000
        
        return {
            'updated_count': global_count + country_count + odds_count,
            'duration_ms': duration_ms,
            'geo_buckets': 1 + len(countries)
        }
    
    def _get_active_countries(self) -> List[str]:
        """Get list of countries with recent activity (last 7 days)"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(days=7)).isoformat()
        
        cursor.execute("""
            SELECT DISTINCT geo_country
            FROM user_interactions
            WHERE geo_country IS NOT NULL
              AND geo_country NOT IN ('', 'UNKNOWN', 'LOCAL')
              AND ts > ?
        """, (cutoff,))
        
        countries = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return countries
    
    def _compute_rollups_for_geo(self, geo_bucket: str) -> int:
        """
        Compute rollups for a specific geo bucket (GLOBAL or country code)
        
        Returns: number of markets updated
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        now = datetime.now()
        
        # Time windows
        cutoff_5m = (now - timedelta(minutes=5)).isoformat()
        cutoff_1h = (now - timedelta(hours=1)).isoformat()
        cutoff_24h = (now - timedelta(hours=24)).isoformat()
        
        # Build geo filter
        if geo_bucket == 'GLOBAL':
            geo_filter = "1=1"  # All interactions
            geo_params = []
        else:
            geo_filter = "geo_country = ?"
            geo_params = [geo_bucket]
        
        # Get all active markets
        cursor.execute("""
            SELECT DISTINCT market_id
            FROM user_interactions
            WHERE ts > ?
        """, (cutoff_24h,))
        
        active_markets = [row[0] for row in cursor.fetchall()]
        
        updated_count = 0
        
        for market_id in active_markets:
            # Count views (impressions + clicks + view_market)
            view_events = ['impression', 'click', 'view_market']
            trade_events = ['participate', 'participate_intent']
            
            # 5-minute window
            cursor.execute(f"""
                SELECT 
                    SUM(CASE WHEN event_type IN ('impression','click','view_market') THEN 1 ELSE 0 END) as views,
                    SUM(CASE WHEN event_type IN ('participate','participate_intent') THEN 1 ELSE 0 END) as trades
                FROM user_interactions
                WHERE market_id = ?
                  AND ts > ?
                  AND {geo_filter}
            """, [market_id, cutoff_5m] + geo_params)
            
            row_5m = cursor.fetchone()
            views_5m = row_5m[0] or 0
            trades_5m = row_5m[1] or 0
            
            # 1-hour window
            cursor.execute(f"""
                SELECT 
                    SUM(CASE WHEN event_type IN ('impression','click','view_market') THEN 1 ELSE 0 END) as views,
                    SUM(CASE WHEN event_type IN ('participate','participate_intent') THEN 1 ELSE 0 END) as trades
                FROM user_interactions
                WHERE market_id = ?
                  AND ts > ?
                  AND {geo_filter}
            """, [market_id, cutoff_1h] + geo_params)
            
            row_1h = cursor.fetchone()
            views_1h = row_1h[0] or 0
            trades_1h = row_1h[1] or 0
            
            # 24-hour window
            cursor.execute(f"""
                SELECT 
                    SUM(CASE WHEN event_type IN ('impression','click','view_market') THEN 1 ELSE 0 END) as views,
                    SUM(CASE WHEN event_type IN ('participate','participate_intent') THEN 1 ELSE 0 END) as trades
                FROM user_interactions
                WHERE market_id = ?
                  AND ts > ?
                  AND {geo_filter}
            """, [market_id, cutoff_24h] + geo_params)
            
            row_24h = cursor.fetchone()
            views_24h = row_24h[0] or 0
            trades_24h = row_24h[1] or 0
            
            # Volume (if we have it - placeholder for now)
            volume_5m = None
            volume_1h = None
            volume_24h = None
            
            # Upsert rollup
            cursor.execute("""
                INSERT INTO market_velocity_rollups
                    (market_id, geo_bucket, 
                     views_5m, views_1h, views_24h,
                     trades_5m, trades_1h, trades_24h,
                     volume_5m, volume_1h, volume_24h,
                     updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(market_id, geo_bucket) DO UPDATE SET
                    views_5m = ?,
                    views_1h = ?,
                    views_24h = ?,
                    trades_5m = ?,
                    trades_1h = ?,
                    trades_24h = ?,
                    volume_5m = ?,
                    volume_1h = ?,
                    volume_24h = ?,
                    updated_at = ?
            """, (market_id, geo_bucket,
                  views_5m, views_1h, views_24h,
                  trades_5m, trades_1h, trades_24h,
                  volume_5m, volume_1h, volume_24h,
                  now,
                  views_5m, views_1h, views_24h,
                  trades_5m, trades_1h, trades_24h,
                  volume_5m, volume_1h, volume_24h,
                  now))
            
            updated_count += 1
        
        conn.commit()
        conn.close()
        
        return updated_count
    
    def _compute_odds_changes(self) -> int:
        """
        Compute odds_change_1h and odds_change_24h for all markets
        Requires market_probability_history table
        
        Returns: number of markets updated
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        now = datetime.now()
        cutoff_1h = (now - timedelta(hours=1)).isoformat()
        cutoff_24h = (now - timedelta(hours=24)).isoformat()
        
        # Get all active markets
        cursor.execute("""
            SELECT market_id, probability
            FROM markets
            WHERE status = 'open'
        """)
        
        markets = cursor.fetchall()
        updated_count = 0
        
        for market_id, current_prob in markets:
            # Get probability 1h ago
            cursor.execute("""
                SELECT probability
                FROM market_probability_history
                WHERE market_id = ?
                  AND recorded_at <= ?
                ORDER BY recorded_at DESC
                LIMIT 1
            """, (market_id, cutoff_1h))
            
            row_1h = cursor.fetchone()
            prob_1h_ago = row_1h[0] if row_1h else current_prob
            odds_change_1h = abs(current_prob - prob_1h_ago)
            
            # Get probability 24h ago
            cursor.execute("""
                SELECT probability
                FROM market_probability_history
                WHERE market_id = ?
                  AND recorded_at <= ?
                ORDER BY recorded_at DESC
                LIMIT 1
            """, (market_id, cutoff_24h))
            
            row_24h = cursor.fetchone()
            prob_24h_ago = row_24h[0] if row_24h else current_prob
            odds_change_24h = abs(current_prob - prob_24h_ago)
            
            # Update all geo buckets for this market
            cursor.execute("""
                UPDATE market_velocity_rollups
                SET odds_change_1h = ?,
                    odds_change_24h = ?,
                    updated_at = ?
                WHERE market_id = ?
            """, (odds_change_1h, odds_change_24h, now, market_id))
            
            updated_count += cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return updated_count
    
    def record_current_probabilities(self):
        """
        Snapshot current market probabilities for odds_change computation
        Run this every 5-15 minutes
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        
        now = datetime.now()
        
        cursor.execute("""
            SELECT market_id, probability
            FROM markets
            WHERE status = 'open'
        """)
        
        markets = cursor.fetchall()
        
        for market_id, probability in markets:
            cursor.execute("""
                INSERT INTO market_probability_history
                    (market_id, probability, recorded_at)
                VALUES (?, ?, ?)
            """, (market_id, probability, now))
        
        conn.commit()
        
        # Cleanup old history (keep last 7 days)
        cutoff = (now - timedelta(days=7)).isoformat()
        cursor.execute("""
            DELETE FROM market_probability_history
            WHERE recorded_at < ?
        """, (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return {
            'recorded': len(markets),
            'deleted_old': deleted
        }

# Global instance
velocity_computer = VelocityComputer()

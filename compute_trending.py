#!/usr/bin/env python3
"""
Compute trending scores (24h rolling window)
Run this every 30 minutes via cron or manually
"""
import sqlite3
import math
from datetime import datetime, timedelta
from collections import defaultdict

DB_PATH = 'brain.db'

def compute_trending_scores(scope='global', window_hours=24):
    """
    Compute trending scores: 85% interaction interest + 15% volume
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"🔥 Computing trending scores for {scope} (last {window_hours}h)...")
    
    cutoff = (datetime.now() - timedelta(hours=window_hours)).isoformat()
    
    # 1. Get interaction-based interest scores
    cursor.execute("""
        SELECT 
            ui.market_id,
            COUNT(DISTINCT ui.user_key) as unique_users,
            SUM(CASE ui.event_type
                WHEN 'participate' THEN 6.0
                WHEN 'share' THEN 4.0
                WHEN 'comment' THEN 4.5
                WHEN 'click' THEN 2.0
                WHEN 'view_market' THEN 2.0
                WHEN 'dwell_30+' THEN 2.0
                WHEN 'dwell_5+' THEN 1.0
                ELSE 1.0
            END) as total_weight
        FROM user_interactions ui
        WHERE ui.ts > ?
        GROUP BY ui.market_id
    """, (cutoff,))
    
    interest_scores = {}
    for row in cursor.fetchall():
        market_id, unique_users, total_weight = row
        # Average weight per user who interacted
        avg_interest = total_weight / max(unique_users, 1)
        interest_scores[market_id] = avg_interest
    
    # 2. Get volume-based scores
    cursor.execute("""
        SELECT market_id, volume_24h
        FROM markets
        WHERE status = 'open'
    """)
    
    volume_scores = {}
    for row in cursor.fetchall():
        market_id, volume = row
        # Log scale
        volume_scores[market_id] = math.log(1 + (volume or 0))
    
    # 3. Normalize both to 0-1 scale
    if interest_scores:
        max_interest = max(interest_scores.values())
        interest_scores = {k: v/max_interest for k, v in interest_scores.items()}
    
    if volume_scores:
        max_volume = max(volume_scores.values())
        volume_scores = {k: v/max_volume if max_volume > 0 else 0 for k, v in volume_scores.items()}
    
    # 4. Combine: 85% interest + 15% volume
    all_market_ids = set(interest_scores.keys()) | set(volume_scores.keys())
    
    trending_scores = {}
    for market_id in all_market_ids:
        interest = interest_scores.get(market_id, 0.0)
        volume = volume_scores.get(market_id, 0.0)
        trending_score = 0.85 * interest + 0.15 * volume
        trending_scores[market_id] = trending_score
    
    # 5. Clear old cache and insert new scores
    cursor.execute("""
        DELETE FROM trending_cache
        WHERE scope = ? AND window = ?
    """, (scope, f'{window_hours}h'))
    
    for market_id, score in trending_scores.items():
        cursor.execute("""
            INSERT INTO trending_cache (market_id, scope, score, window, computed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (market_id, scope, score, f'{window_hours}h', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Computed {len(trending_scores)} trending scores")
    print(f"📈 Top 5 trending markets:")
    
    sorted_markets = sorted(trending_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    for market_id, score in sorted_markets:
        print(f"  {market_id}: {score:.3f}")

if __name__ == '__main__':
    compute_trending_scores()

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
    
    # 5. Filter to only truly trending markets
    # Only include markets with meaningful activity (score > 0.1) or top 50
    sorted_trending = sorted(trending_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 50 markets OR all markets with score > 0.1, whichever is smaller
    min_threshold = 0.1
    filtered_trending = []
    for market_id, score in sorted_trending[:50]:  # Top 50 max
        if score >= min_threshold or len(filtered_trending) < 20:  # Always include top 20
            filtered_trending.append((market_id, score))
    
    # 6. Clear old cache and insert new scores
    cursor.execute("""
        DELETE FROM trending_cache
        WHERE scope = ? AND window = ?
    """, (scope, f'{window_hours}h'))
    
    for market_id, score in filtered_trending:
        cursor.execute("""
            INSERT INTO trending_cache (market_id, scope, score, window, computed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (market_id, scope, score, f'{window_hours}h', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Computed {len(trending_scores)} raw scores, stored {len(filtered_trending)} trending markets")
    print(f"📈 Top 5 trending markets:")
    
    for market_id, score in filtered_trending[:5]:
        print(f"  {market_id}: {score:.3f}")

def compute_localized_trending(window_hours=24):
    """
    Compute localized trending scores per country
    When people from the same area like something, make it trending in that area
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"🌍 Computing localized trending scores (last {window_hours}h)...")
    
    cutoff = (datetime.now() - timedelta(hours=window_hours)).isoformat()
    
    # Get interactions grouped by geo_country
    cursor.execute("""
        SELECT 
            ui.geo_country,
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
          AND ui.geo_country IS NOT NULL 
          AND ui.geo_country NOT IN ('UNKNOWN', 'LOCAL', '')
        GROUP BY ui.geo_country, ui.market_id
        HAVING COUNT(DISTINCT ui.user_key) >= 2
    """, (cutoff,))
    
    # Group by country
    country_scores = defaultdict(dict)
    for row in cursor.fetchall():
        geo_country, market_id, unique_users, total_weight = row
        avg_interest = total_weight / max(unique_users, 1)
        country_scores[geo_country][market_id] = avg_interest
    
    # Normalize per country and store (only top trending)
    total_localized = 0
    min_threshold = 0.15  # Higher threshold for localized (requires more signal)
    
    for geo_country, market_scores in country_scores.items():
        if not market_scores:
            continue
        
        # Normalize to 0-1 within this country
        max_score = max(market_scores.values())
        normalized_scores = {k: v/max_score for k, v in market_scores.items()}
        
        # Filter to top 20 per country or score > threshold
        sorted_local = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        filtered_local = []
        for market_id, score in sorted_local[:20]:  # Top 20 per country max
            if score >= min_threshold or len(filtered_local) < 10:  # Always include top 10
                filtered_local.append((market_id, score))
        
        # Delete old localized scores for this country
        cursor.execute("""
            DELETE FROM trending_cache
            WHERE scope = ? AND window = ?
        """, (f'local:{geo_country}', f'{window_hours}h'))
        
        # Insert new localized scores
        for market_id, score in filtered_local:
            cursor.execute("""
                INSERT INTO trending_cache (market_id, scope, score, window, computed_at)
                VALUES (?, ?, ?, ?, ?)
            """, (market_id, f'local:{geo_country}', score, f'{window_hours}h', datetime.now().isoformat()))
            total_localized += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Computed localized trending for {len(country_scores)} countries ({total_localized} scores)")
    
    # Show top countries
    sorted_countries = sorted(country_scores.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    for geo_country, market_scores in sorted_countries:
        top_market = sorted(market_scores.items(), key=lambda x: x[1], reverse=True)[0]
        print(f"  {geo_country}: {len(market_scores)} trending markets (top: {top_market[0]})")

if __name__ == '__main__':
    # Compute global trending
    compute_trending_scores()
    
    # Compute localized trending
    compute_localized_trending()

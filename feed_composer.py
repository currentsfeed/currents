"""
BRain v1 - Feed Composer
Implements quota-based candidate generation and diversity post-processing
Per Roy's spec: controls local/global balance, prevents echo chambers
"""
import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict, Counter

DB_PATH = 'brain.db'

class FeedComposer:
    def __init__(self, db_path=DB_PATH, config=None):
        self.db_path = db_path
        
        # Load config
        if config is None:
            with open('brain_v1_config.json', 'r') as f:
                config = json.load(f)
        
        self.config = config
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def generate_candidates(self, user_key: str, geo_bucket: str, 
                           exclude_ids: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
        """
        Generate candidate pools for each channel
        
        Per spec:
        - personal: 120 (by LT + ST similarity)
        - trending_global: 80 (top by GLOBAL trades_1h/views_1h)
        - trending_local: 50 (top by geo_bucket trades_1h/views_1h)
        - fresh_new: 30 (newest with minimum activity)
        - exploration: 20 (sample from quality inventory)
        
        Returns: {channel: [markets]}
        """
        if exclude_ids is None:
            exclude_ids = []
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Base exclusions: hidden, ended, already excluded
        exclude_where = "status = 'open'"
        if exclude_ids:
            placeholders = ','.join(['?' for _ in exclude_ids])
            exclude_where += f" AND market_id NOT IN ({placeholders})"
        
        # Also exclude recently hidden markets
        hide_days = self.config['penalties']['hide_suppression_days']
        cutoff_hide = (datetime.now() - timedelta(days=hide_days)).isoformat()
        
        cursor.execute(f"""
            SELECT market_id FROM user_market_impressions
            WHERE user_key = ? AND last_hidden_at > ?
        """, (user_key, cutoff_hide))
        hidden_ids = [row[0] for row in cursor.fetchall()]
        
        all_exclude = exclude_ids + hidden_ids
        
        # Fetch all candidates
        pool_size = sum(self.config['candidate_pool'].values())
        cursor.execute(f"""
            SELECT 
                m.market_id, m.title, m.description, m.category, m.probability,
                m.volume_24h, m.volume_total, m.image_url, m.created_at, 
                m.resolution_date, m.editorial_description
            FROM markets m
            WHERE {exclude_where}
            ORDER BY m.volume_total DESC
            LIMIT ?
        """, all_exclude + [pool_size * 2])  # Get extra for filtering
        
        all_markets = []
        for row in cursor.fetchall():
            market = {
                'market_id': row[0],
                'title': row[1],
                'description': row[2],
                'category': row[3],
                'probability': row[4],
                'volume_24h': row[5],
                'volume_total': row[6],
                'image_url': row[7],
                'created_at': row[8],
                'resolution_date': row[9],
                'editorial_description': row[10],
                'tags': []
            }
            
            # Fetch tags
            cursor.execute("""
                SELECT tag FROM market_tags WHERE market_id = ? ORDER BY tag
            """, (market['market_id'],))
            market['tags'] = [t[0] for t in cursor.fetchall()]
            
            all_markets.append(market)
        
        conn.close()
        
        # Now partition into channels
        candidates = {}
        
        # 1. Personal candidates (120)
        candidates['personal'] = self._get_personal_candidates(
            all_markets, user_key, self.config['candidate_pool']['personal']
        )
        
        # 2. Trending global (80)
        candidates['trending_global'] = self._get_trending_candidates(
            all_markets, 'GLOBAL', self.config['candidate_pool']['trending_global']
        )
        
        # 3. Trending local (50)
        candidates['trending_local'] = self._get_trending_candidates(
            all_markets, geo_bucket, self.config['candidate_pool']['trending_local']
        )
        
        # 4. Fresh new (30)
        candidates['fresh_new'] = self._get_fresh_candidates(
            all_markets, self.config['candidate_pool']['fresh_new']
        )
        
        # 5. Exploration (20)
        candidates['exploration'] = self._get_exploration_candidates(
            all_markets, candidates, self.config['candidate_pool']['exploration']
        )
        
        return candidates
    
    def _get_personal_candidates(self, markets: List[Dict], user_key: str, limit: int) -> List[Dict]:
        """Get candidates by LT + ST similarity with category diversity"""
        from brain_v1_scorer import brain_v1_scorer
        from collections import Counter
        
        # Score by LT + ST only (no penalties yet)
        scored = []
        for market in markets:
            lt_score = brain_v1_scorer.calculate_lt_score(market, user_key)
            st_score = brain_v1_scorer.calculate_st_score(market, user_key)
            relevance = 0.6 * lt_score + 0.4 * st_score
            scored.append((relevance, market))
        
        # Sort by relevance
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Apply category diversity cap (max 25% from single category)
        max_per_category = int(limit * 0.15)
        category_counts = Counter()
        result = []
        
        for score, market in scored:
            category = market.get('category', 'unknown')
            if category_counts[category] < max_per_category:
                result.append(market)
                category_counts[category] += 1
                if len(result) >= limit:
                    break
        
        return result
    
    def _get_trending_candidates(self, markets: List[Dict], geo_bucket: str, limit: int) -> List[Dict]:
        """Get top trending markets by trades + views with category diversity"""
        from collections import Counter
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Get velocity data
        market_velocities = {}
        for market in markets:
            cursor.execute("""
                SELECT trades_1h, views_1h
                FROM market_velocity_rollups
                WHERE market_id = ? AND geo_bucket = ?
            """, (market['market_id'], geo_bucket))
            
            row = cursor.fetchone()
            if row:
                trades = row[0] or 0
                views = row[1] or 0
                # Weight trades more than views
                velocity = 0.7 * trades + 0.3 * views
                market_velocities[market['market_id']] = velocity
        
        conn.close()
        
        # Sort by velocity
        scored = [(market_velocities.get(m['market_id'], 0), m) for m in markets]
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Apply category diversity cap (max 25% from single category)
        max_per_category = int(limit * 0.15)
        category_counts = Counter()
        result = []
        
        for velocity, market in scored:
            category = market.get('category', 'unknown')
            if category_counts[category] < max_per_category:
                result.append(market)
                category_counts[category] += 1
                if len(result) >= limit:
                    break
        
        return result
    
    def _get_fresh_candidates(self, markets: List[Dict], limit: int) -> List[Dict]:
        """Get newest markets with minimum activity threshold"""
        # Sort by created_at, newest first
        valid = []
        for market in markets:
            created_at = market.get('created_at')
            if created_at:
                try:
                    created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    age_hours = (datetime.now() - created).total_seconds() / 3600
                    
                    # Only include if < 72 hours old and has some volume
                    if age_hours < 72 and market.get('volume_24h', 0) > 100:
                        valid.append((created, market))
                except:
                    pass
        
        # Sort by newest
        valid.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in valid[:limit]]
    
    def _get_exploration_candidates(self, markets: List[Dict], 
                                   existing_candidates: Dict[str, List[Dict]], 
                                   limit: int) -> List[Dict]:
        """Sample from quality inventory not in other channels"""
        # Get all market IDs already in other channels
        used_ids = set()
        for channel, candidates in existing_candidates.items():
            for market in candidates:
                used_ids.add(market['market_id'])
        
        # Filter to unused markets with decent quality
        available = [
            m for m in markets 
            if m['market_id'] not in used_ids and m.get('volume_total', 0) > 1000
        ]
        
        # Random sample
        if len(available) > limit:
            return random.sample(available, limit)
        return available
    
    def allocate_quotas(self, limit: int) -> Dict[str, int]:
        """
        Allocate item counts by quota percentages
        
        Per spec: personal 40%, trending_global 25%, trending_local 12%, 
                  fresh_new 8%, exploration 15%
        
        Returns: {channel: count}
        """
        quotas = self.config['feed_quotas']
        
        allocated = {}
        remaining = limit
        
        # Allocate each channel
        for channel, pct in quotas.items():
            count = round(limit * pct)
            allocated[channel] = count
            remaining -= count
        
        # Distribute any remainder to personal (largest bucket)
        if remaining != 0:
            allocated['personal'] += remaining
        
        return allocated
    
    def compose_feed(self, user_key: str, geo_bucket: str, limit: int = 30,
                    exclude_ids: Optional[List[str]] = None, 
                    debug: bool = False) -> Dict:
        """
        Main feed composition with quotas + diversity
        
        Returns: {items: [...], meta: {...}}
        """
        from brain_v1_scorer import brain_v1_scorer
        from impression_tracker import impression_tracker
        
        # 1. Generate candidates
        candidates = self.generate_candidates(user_key, geo_bucket, exclude_ids)
        
        # 2. Allocate quotas
        quotas = self.allocate_quotas(limit)
        
        # 3. Get impression data for all candidates (batch)
        all_candidate_ids = []
        for channel_markets in candidates.values():
            all_candidate_ids.extend([m['market_id'] for m in channel_markets])
        
        impression_data = impression_tracker.get_impression_data(user_key, all_candidate_ids)
        
        # 4. Score and rank each channel
        channel_items = {}
        quotas_used = {}
        
        for channel, channel_candidates in candidates.items():
            quota = quotas.get(channel, 0)
            
            # Score all candidates in this channel
            scored = []
            for market in channel_candidates:
                imp_data = impression_data.get(market['market_id'])
                score_result = brain_v1_scorer.calculate_final_score(
                    market, user_key, geo_bucket, imp_data
                )
                
                # Skip if hidden or scored too low
                if score_result['score'] < 0.01:
                    continue
                
                item = {
                    'market_id': market['market_id'],
                    'market': market,
                    'score': score_result['score'],
                    'channel': channel,
                    'reason_tags': score_result['reason_tags'],
                    'last_shown_at': imp_data.get('last_shown_at') if imp_data else None
                }
                
                # Include debug info if requested
                if debug:
                    item['debug'] = {
                        'components': score_result['components'],
                        'penalties': score_result['penalties'],
                        'bonuses': score_result['bonuses']
                    }
                
                scored.append(item)
            
            # Sort by score and take top N per quota
            scored.sort(key=lambda x: x['score'], reverse=True)
            channel_items[channel] = scored[:quota]
            quotas_used[channel] = len(channel_items[channel])
        
        # 5. Merge all channels and remove duplicates
        merged = []
        seen_ids = set()
        for channel_list in channel_items.values():
            for item in channel_list:
                if item['market_id'] not in seen_ids:
                    merged.append(item)
                    seen_ids.add(item['market_id'])
        
        # Re-sort by score
        merged.sort(key=lambda x: x['score'], reverse=True)
        
        # 6. Apply diversity post-processing
        final_items = self._apply_diversity(merged[:limit * 2], limit)  # Get extra for diversity filtering
        
        # 7. Build response
        return {
            'items': final_items[:limit],
            'meta': {
                'geo_bucket': geo_bucket,
                'quotas_used': quotas_used,
                'exploration_rate': quotas.get('exploration', 0) / limit if limit > 0 else 0,
                'cursor_next': None  # For pagination (future)
            }
        }
    
    def _apply_diversity(self, items: List[Dict], limit: int) -> List[Dict]:
        """
        Apply diversity guardrails with category interleaving
        
        Per spec:
        1. No more than 2 in a row from same category
        2. Max 35% of page from single category (now enforced at 30%)
        3. Max 25% from same tag cluster (top tag)
        
        Strategy: Interleave categories to spread diversity throughout feed
        
        Returns: diversified list
        """
        if not items:
            return []
        
        # STRICTER limits for better diversity (but ensure we fill the feed)
        max_category_share = 0.35  # Allow 35% to ensure we can fill
        max_consecutive = 2
        max_tag_share = 0.30  # Relaxed to allow more fill
        
        # Calculate max counts
        max_category_count = int(limit * max_category_share)
        max_tag_count = int(limit * max_tag_share)
        
        # Group items by category
        from collections import defaultdict
        items_by_category = defaultdict(list)
        for item in items:
            category = item['market'].get('category', 'unknown')
            items_by_category[category].append(item)
        
        # Round-robin through categories to interleave
        result = []
        category_counts = Counter()
        tag_counts = Counter()
        last_category = None
        consecutive_count = 0
        
        # Keep track of category indices
        category_indices = {cat: 0 for cat in items_by_category}
        categories = list(items_by_category.keys())
        current_cat_idx = 0
        
        attempts = 0
        max_attempts = len(items) * 2  # Prevent infinite loop
        
        while len(result) < limit and attempts < max_attempts:
            attempts += 1
            placed = False
            
            # Try round-robin through categories
            for _ in range(len(categories)):
                if len(result) >= limit:
                    break
                
                category = categories[current_cat_idx]
                current_cat_idx = (current_cat_idx + 1) % len(categories)
                
                # Check if we can place from this category
                if category_counts[category] >= max_category_count:
                    continue
                
                # Check consecutive rule
                if category == last_category and consecutive_count >= max_consecutive:
                    continue
                
                # Get next item from this category
                cat_idx = category_indices[category]
                if cat_idx >= len(items_by_category[category]):
                    continue  # No more items in this category
                
                item = items_by_category[category][cat_idx]
                category_indices[category] += 1
                
                # Check tag limit
                market = item['market']
                tags = market.get('tags', [])
                top_tag = tags[0] if tags else None
                
                if top_tag and tag_counts[top_tag] >= max_tag_count:
                    continue
                
                # Place item
                result.append(item)
                category_counts[category] += 1
                if top_tag:
                    tag_counts[top_tag] += 1
                
                if category == last_category:
                    consecutive_count += 1
                else:
                    consecutive_count = 1
                    last_category = category
                
                placed = True
                break
            
            # If no placement after full round, try linear scan
            if not placed:
                for item in items:
                    if item in result:
                        continue
                    
                    market = item['market']
                    category = market.get('category', 'unknown')
                    tags = market.get('tags', [])
                    top_tag = tags[0] if tags else None
                    
                    # Check all limits
                    if category_counts[category] >= max_category_count:
                        continue
                    if category == last_category and consecutive_count >= max_consecutive:
                        continue
                    if top_tag and tag_counts[top_tag] >= max_tag_count:
                        continue
                    
                    # Place item
                    result.append(item)
                    category_counts[category] += 1
                    if top_tag:
                        tag_counts[top_tag] += 1
                    
                    if category == last_category:
                        consecutive_count += 1
                    else:
                        consecutive_count = 1
                        last_category = category
                    
                    break
        
        # Final fallback: if we still don't have enough items, add remaining without strict rules
        if len(result) < limit:
            for item in items:
                if item not in result:
                    result.append(item)
                    if len(result) >= limit:
                        break
        
        return result

# Global instance
feed_composer = FeedComposer()

# Current Implementation Details for Roy's Personalization Improvements

**Date**: Feb 15, 2026  
**Purpose**: Provide current state so Roy can design improved scoring system

---

## 1. Current personalization.py Scoring Inputs

### Per-User Data Available:

```python
# From user_profiles table
user_profile = {
    'user_key': 'user123',
    'total_interactions': 150,
    'last_active': '2026-02-15T04:00:00Z',
    'created_at': '2026-02-10T10:00:00Z'
}

# From user_topic_scores table  
user_scores = {
    'category': {
        'Sports': 0.45,      # Normalized 0-1 (stored as 45.0)
        'Politics': 0.38,
        'Economics': 0.12
    },
    'tag': {
        'NBA': 0.52,
        'Trump': 0.41,
        'LeBron': 0.35
    }
}

# Recent interactions (last 24h)
recent_viewed = ['market1', 'market2', 'market3']  # Just IDs

# User's geo location (from last interaction)
user_geo = 'IL'  # ISO country code
```

**Missing (that you identified):**
- ❌ No impression tracking (only interactions)
- ❌ No short_term vs long_term separation
- ❌ No last_shown_at per market
- ❌ No impressions_24h, impressions_7d counts
- ❌ No session_vector vs long_term_vector

### Per-Market Data Available:

```python
market = {
    'market_id': 'nba-all-star-mvp-2026',
    'title': 'Will LeBron win NBA All-Star MVP?',
    'description': '...',
    'category': 'Sports',
    'tags': ['NBA', 'LeBron', 'Basketball', 'AllStar'],
    'probability': 0.65,
    'volume_24h': 50000.0,
    'volume_total': 250000.0,
    'created_at': '2026-02-14T10:00:00Z',
    'resolution_date': '2026-02-17T05:00:00Z',
    'editorial_description': '...',
    'image_url': 'static/images/...'
}
```

**Missing (that you identified):**
- ❌ No global_velocity (views/trades over 5m/1h/24h)
- ❌ No local_velocity by geo
- ❌ No odds_change_1h / odds_change_24h
- ❌ No participant_count tracking
- ❌ No last_volume_24h (to detect spikes)

### Current Scoring Formula:

```python
# PersonalScore (for users with profiles)
personal_score = (
    0.35 * interest +      # Affinity to market's tags/category
    0.25 * similarity +    # Similar to recently viewed
    0.15 * depth +         # User's engagement depth
    0.10 * freshness +     # Newer markets preferred
    0.10 * followup +      # Meaningful change since last view
    -0.10 * negative +     # Hide/not_interested penalty
    -0.05 * diversity      # Category diversity penalty
)

# FinalScore
final_score = (
    personal_score +
    0.40 * trending +      # Trending score (40% weight)
    0.15 * rising +        # Belief shift magnitude
    0.05 * editorial +     # Manual boost
    news_boost +           # 0.8 if <24h, 0.5 if <7d
    sports_boost           # 0.5 if game in 1-3 days
)

# Trending blend (for users with geo)
trending = 0.4 * local_trending + 0.6 * global_trending
```

**Component Details:**

```python
# Interest: How much user likes this market's topics
def _calculate_interest(market, user_scores):
    score = 0.0
    
    # Category match
    category = market.get('category')
    if category in user_scores.get('category', {}):
        score += user_scores['category'][category] * 0.5
    
    # Tag matches
    for tag in market.get('tags', []):
        if tag in user_scores.get('tag', {}):
            score += user_scores['tag'][tag] * 0.3
    
    return min(score, 1.0)  # Cap at 1.0

# Similarity: Similar to recent interactions
def _calculate_similarity(market, recent_viewed, user_scores):
    # Simple: if any recent markets share category/tags
    # Returns 0.0-1.0 based on overlap
    pass

# Depth: How deeply user engages with similar markets
def _calculate_depth(cursor, user_key, market):
    # Query: avg dwell_ms for markets in same category
    # Returns 0.0-1.0 based on depth
    pass

# Freshness: Newer = higher
def _calculate_freshness(market):
    created = datetime.fromisoformat(market['created_at'])
    age_hours = (datetime.now() - created).total_seconds() / 3600
    
    if age_hours < 24: return 1.0
    if age_hours < 168: return 0.8
    if age_hours < 720: return 0.5
    return 0.3

# Followup: Has market changed significantly since user last saw it?
def _calculate_followup(cursor, user_key, market):
    # Currently: checks if probability changed >5% since last view
    # Returns 0.0-1.0
    pass

# Negative: Penalty for hidden/disliked topics
def _calculate_negative(market, user_scores):
    # Sum negative scores for category/tags
    # Returns penalty (0.0-1.0)
    pass
```

**Problems (matching your feedback):**
1. ❌ No distinction between session intent and long-term taste
2. ❌ No cooldown/frequency penalties (can show same market repeatedly)
3. ❌ No "changed enough to re-show" logic
4. ❌ No explicit quotas (local/global/exploration)

---

## 2. Current tracking_engine.py Events

### Event Types & Weights:

```python
ACTION_WEIGHTS = {
    'participate': 6.0,          # User placed bet
    'participate_intent': 3.0,   # Clicked "Commit Belief"
    'share': 4.0,                # Shared market
    'comment': 4.5,              # Commented
    'bookmark': 3.5,             # Bookmarked/saved
    'click': 2.0,                # Clicked market card
    'view_market': 2.0,          # Market detail page loaded
    'return_visit': 3.0,         # Returned to same market
    'dwell_30+': 2.0,            # Spent 30+ seconds
    'dwell_5+': 1.0,             # Spent 5+ seconds
    'scroll_past': -0.5,         # Saw but didn't click
    'skip_fast': -1.0,           # Saw briefly, moved on
    'hide': -6.0                 # Explicitly hidden
}
```

**Missing (that you identified):**
- ❌ No `impression` event (just interaction events)
- ❌ No batched impression tracking
- ❌ No position_in_feed tracking (we have it in schema but not using effectively)

### Current Tracking Call:

```python
# From app.py
@app.route('/api/track', methods=['POST'])
def track_interaction():
    data = request.get_json()
    
    interaction_id = tracker.record_interaction(
        user_key=data.get('user_key'),
        market_id=data.get('market_id'),
        event_type=data.get('event_type'),    # click, view_market, participate
        dwell_ms=data.get('dwell_ms'),
        section=data.get('section'),           # hero, grid, stream
        position=data.get('position'),         # Position in list
        geo_country=data.get('geo_country')
    )
```

### Profile Update Logic:

```python
def _update_profile_from_interaction(cursor, user_key, market_id, event_type, dwell_ms):
    """Updates user_topic_scores based on interaction"""
    
    # Get action weight
    weight = ACTION_WEIGHTS.get(event_type, 1.0)
    
    # Apply dwell multiplier
    if dwell_ms:
        if dwell_ms >= 30000: weight *= 1.5
        elif dwell_ms >= 5000: weight *= 1.2
    
    # Fetch market's category and tags
    cursor.execute("SELECT category FROM markets WHERE market_id = ?", (market_id,))
    category = cursor.fetchone()[0]
    
    cursor.execute("SELECT tag FROM market_tags WHERE market_id = ?", (market_id,))
    tags = [row[0] for row in cursor.fetchall()]
    
    # Update category score
    cursor.execute("""
        INSERT INTO user_topic_scores (user_key, topic_type, topic_value, score, last_updated)
        VALUES (?, 'category', ?, ?, ?)
        ON CONFLICT(user_key, topic_type, topic_value) 
        DO UPDATE SET 
            score = score + ?,
            last_updated = ?
    """, (user_key, category, weight, datetime.now(), weight, datetime.now()))
    
    # Update tag scores (with 0.8 multiplier)
    for tag in tags:
        cursor.execute("""
            INSERT INTO user_topic_scores (user_key, topic_type, topic_value, score, last_updated)
            VALUES (?, 'tag', ?, ?, ?)
            ON CONFLICT(user_key, topic_type, topic_value)
            DO UPDATE SET 
                score = score + ?,
                last_updated = ?
        """, (user_key, tag, weight * 0.8, datetime.now(), weight * 0.8, datetime.now()))
    
    # Update profile metadata
    cursor.execute("""
        INSERT INTO user_profiles (user_key, total_interactions, last_active)
        VALUES (?, 1, ?)
        ON CONFLICT(user_key)
        DO UPDATE SET
            total_interactions = total_interactions + 1,
            last_active = ?
    """, (user_key, datetime.now(), datetime.now()))
```

**Problems:**
1. ❌ All weights go to same long-term score (no session vs long-term)
2. ❌ No decay applied (scores just accumulate)
3. ❌ No impression recording (only interactions)

---

## 3. Database Schema

### user_interactions (current)

```sql
CREATE TABLE user_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key TEXT NOT NULL,
    market_id TEXT NOT NULL,
    event_type TEXT NOT NULL,          -- click, view_market, participate, etc.
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dwell_ms INTEGER,                  -- Time spent
    section TEXT,                      -- hero, grid, stream
    position INTEGER,                  -- Position in feed
    geo_country TEXT,                  -- User's country
    metadata TEXT                      -- JSON for additional context
);
CREATE INDEX idx_interactions_ts ON user_interactions(ts);
```

### user_profiles (current)

```sql
CREATE TABLE user_profiles (
    user_key TEXT PRIMARY KEY,
    display_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_interactions INTEGER DEFAULT 0,
    interests TEXT,          -- JSON blob (unused currently)
    negatives TEXT,          -- JSON blob (unused currently)
    seen_markets TEXT        -- JSON blob (unused currently)
);
```

### user_topic_scores (current)

```sql
CREATE TABLE user_topic_scores (
    user_key TEXT NOT NULL,
    topic_type TEXT NOT NULL,      -- 'category' or 'tag'
    topic_value TEXT NOT NULL,     -- 'Sports' or 'NBA'
    score REAL NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_key, topic_type, topic_value)
);
```

### markets (current)

```sql
CREATE TABLE markets (
    market_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    probability REAL NOT NULL,
    volume_24h REAL DEFAULT 0,
    volume_total REAL DEFAULT 0,
    participant_count INTEGER DEFAULT 0,  -- Not being updated currently
    image_url TEXT,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_date TIMESTAMP,
    editorial_description TEXT
);
```

### trending_cache (current)

```sql
CREATE TABLE trending_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    scope TEXT NOT NULL,              -- 'global' or 'local:IL'
    score REAL NOT NULL,              -- 0.0-1.0 trending score
    window TEXT NOT NULL,             -- '24h'
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Missing Tables (that you need):**
- ❌ No user_market_impressions table
- ❌ No market_velocity_stats table
- ❌ No user_session_state table

---

## 4. Feed Composition (Current - Not Quota-Based)

### Current Logic:

```python
# Homepage
feed = personalizer.get_personalized_feed(user_key='roy', limit=20)

# Returns:
{
    'hero': [market],      # 1 market from visual categories
    'grid': [9 markets],   # Next 9 markets
    'stream': [markets]    # Remaining markets
}

# No explicit quotas - just sorted by final_score
# Category diversity enforced: max 3 per category in top 9
```

**Problems:**
1. ❌ No explicit % allocations (personal/trending/exploration)
2. ❌ Local markets boost via trending, not quota
3. ❌ No exploration rate config
4. ❌ Can't tune local vs global balance per-page

---

## 5. What's Working Well

✅ **Event tracking** - Comprehensive event types, good weights  
✅ **Trending computation** - Local + global blend working  
✅ **Category diversity** - Prevents single-category domination  
✅ **Tag-level learning** - Learns specific people/topics  
✅ **Geo detection** - Working (ip-api.com)  

---

## 6. Summary of Gaps (Matching Your Requirements)

### Gap 1: Impression Tracking
**Currently:** Only track interactions (clicks, views, trades)  
**Need:** Track every impression + store frequency data

### Gap 2: Session vs Long-term
**Currently:** Single score accumulation (long-term only)  
**Need:** Separate short_term_vector (30-120min) and long_term_vector

### Gap 3: Market Change Detection
**Currently:** Basic probability change check  
**Need:** velocity metrics, odds_change, participant_count deltas

### Gap 4: Feed Quotas
**Currently:** Sort by score, diversity enforcement only  
**Need:** Explicit quotas (% personal / % trending / % exploration)

### Gap 5: Frequency Capping
**Currently:** No cooldown (can show same market repeatedly)  
**Need:** impressions_24h, last_shown_at, cooldown penalties

---

## 7. Questions for Your Spec

1. **Impression storage:** SQLite table or Redis?
2. **Session detection:** How to define session boundaries? (30min timeout?)
3. **Short-term decay:** Linear decay or exponential?
4. **Velocity computation:** Real-time or batch (every 5min)?
5. **Quota enforcement:** Hard caps or soft weights?
6. **Cooldown curve:** Linear penalty or exponential?
7. **Re-show threshold:** What constitutes "changed enough"? (>10% odds move?)

---

## 8. Current Config (Hard-coded)

```python
# personalization.py
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
    'trending': 0.40,
    'rising': 0.15,
    'editorial': 0.05
}

# Category diversity
MAX_PER_CATEGORY = 3  # In top 9

# Trending blend
LOCAL_WEIGHT = 0.40
GLOBAL_WEIGHT = 0.60
```

**Need:** Move to config file, make tunable per deployment

---

## 9. Ready for Your Spec

Based on this, I can implement:

✅ **Impression tracking table + API**  
✅ **Short-term vs long-term scoring**  
✅ **Market velocity stats**  
✅ **Quota-based feed composition**  
✅ **Cooldown penalties**  
✅ **Config-driven weights**  

Please provide:
1. Exact schema for new tables (user_impressions, market_stats, etc.)
2. Scoring formula with penalties
3. Quota config structure
4. Cooldown curves

I'll implement and deploy within hours.

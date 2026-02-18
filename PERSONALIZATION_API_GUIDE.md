# Personalization API Integration Guide

**Date**: Feb 15, 2026  
**Purpose**: Guide for replacing or externalizing the personalization logic

## Current Architecture

### Overview

Currently, personalization is **integrated directly** in the Flask application:

```
┌─────────────┐
│   app.py    │ ← Flask routes
└──────┬──────┘
       │
       ├──→ personalization.py (PersonalizationEngine)
       ├──→ tracking_engine.py (InteractionTracker)
       └──→ brain.db (SQLite database)
```

**Key components:**
1. **personalization.py** - Ranking algorithm (PersonalScore + trending + rising)
2. **tracking_engine.py** - Records user interactions
3. **brain.db** - Stores markets, user profiles, interactions, trending cache

### Current Integration Points

#### 1. Personalization Calls (app.py)

```python
from personalization import personalizer

# Homepage
feed = personalizer.get_personalized_feed(
    user_key='user123',      # User identifier
    limit=20,                # Number of markets to return
    user_country='IL'        # ISO country code for geo-based trending
)

# Returns:
{
    'hero': [market],        # 1 market for hero section
    'grid': [markets],       # 9 markets for main grid
    'stream': [markets],     # Remaining markets
    'personalized': True,    # Whether personalization was used
    'user_key': 'user123'
}
```

#### 2. Interaction Tracking (app.py)

```python
from tracking_engine import tracker

# Track single interaction
interaction_id = tracker.record_interaction(
    user_key='user123',
    market_id='market_xyz',
    event_type='click',      # click, view_market, participate, share, etc.
    dwell_ms=5000,          # Time spent (optional)
    geo_country='IL',       # User's country (optional)
    context={'position': 3}  # Additional context (optional)
)
```

#### 3. Trending Computation (compute_trending.py)

```python
# Run every 30 minutes via cron
python3 compute_trending.py

# Reads: user_interactions table (last 24h)
# Writes: trending_cache table (scores per market)
```

## Option 1: Create Internal REST API

**Convert personalization to REST endpoints** without changing the logic.

### Step 1: Create BRain API Routes

Add to `app.py`:

```python
# ============================================
# BRain Personalization API
# ============================================

@app.route('/api/brain/feed', methods=['POST'])
def brain_get_feed():
    """
    Get personalized feed for user
    
    POST /api/brain/feed
    {
        "user_key": "user123",
        "limit": 20,
        "user_country": "IL"
    }
    
    Returns:
    {
        "hero": [...],
        "grid": [...],
        "stream": [...],
        "personalized": true,
        "user_key": "user123"
    }
    """
    try:
        data = request.get_json()
        user_key = data.get('user_key')
        limit = data.get('limit', 20)
        user_country = data.get('user_country')
        
        feed = personalizer.get_personalized_feed(
            user_key=user_key,
            limit=limit,
            user_country=user_country
        )
        
        return jsonify(feed)
    except Exception as e:
        logger.error(f"BRain feed error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/brain/rank', methods=['POST'])
def brain_rank_markets():
    """
    Rank a list of markets for a user
    
    POST /api/brain/rank
    {
        "user_key": "user123",
        "market_ids": ["market1", "market2", "market3"],
        "user_country": "IL"
    }
    
    Returns:
    {
        "ranked_markets": [
            {
                "market_id": "market1",
                "rank": 1,
                "score": 2.45,
                "scores": {
                    "personal": 1.2,
                    "trending": 0.8,
                    "rising": 0.3,
                    "editorial": 0.15
                }
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        user_key = data.get('user_key')
        market_ids = data.get('market_ids', [])
        user_country = data.get('user_country')
        
        # Fetch markets from DB
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in market_ids])
        cursor.execute(f"""
            SELECT market_id, title, description, category, probability,
                   volume_24h, volume_total, image_url, created_at, resolution_date,
                   editorial_description
            FROM markets
            WHERE market_id IN ({placeholders})
        """, market_ids)
        
        markets = []
        for row in cursor.fetchall():
            markets.append({
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
                'editorial_description': row[10]
            })
        
        conn.close()
        
        # Rank markets
        if user_key:
            ranked = personalizer._rank_personalized(cursor, user_key, markets)
        else:
            ranked = personalizer._rank_global(markets, user_country=user_country)
        
        # Format response
        result = {
            'ranked_markets': [
                {
                    'market_id': m['market_id'],
                    'rank': idx + 1,
                    'score': m['scores']['final'],
                    'scores': m['scores']
                }
                for idx, m in enumerate(ranked)
            ]
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"BRain rank error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/brain/user/<user_key>', methods=['GET'])
def brain_get_user_profile(user_key):
    """
    Get user profile (learned preferences)
    
    GET /api/brain/user/user123
    
    Returns:
    {
        "user_key": "user123",
        "total_interactions": 150,
        "top_categories": [
            {"category": "Sports", "score": 45.2},
            {"category": "Politics", "score": 38.7}
        ],
        "top_tags": [
            {"tag": "NBA", "score": 52.1},
            {"tag": "Trump", "score": 41.3}
        ],
        "last_active": "2026-02-15T04:30:00Z"
    }
    """
    try:
        profile = tracker.get_user_profile(user_key)
        return jsonify(profile)
    except Exception as e:
        logger.error(f"BRain profile error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/brain/trending', methods=['GET'])
def brain_get_trending():
    """
    Get trending markets
    
    GET /api/brain/trending?scope=global&limit=50
    GET /api/brain/trending?scope=local:IL&limit=20
    
    Returns:
    {
        "trending": [
            {
                "market_id": "nba-all-star-mvp-2026",
                "score": 0.85,
                "scope": "global"
            },
            ...
        ]
    }
    """
    try:
        scope = request.args.get('scope', 'global')
        limit = int(request.args.get('limit', 50))
        
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT market_id, score, scope
            FROM trending_cache
            WHERE scope = ?
            ORDER BY score DESC
            LIMIT ?
        """, (scope, limit))
        
        trending = [
            {'market_id': row[0], 'score': row[1], 'scope': row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return jsonify({'trending': trending})
    except Exception as e:
        logger.error(f"BRain trending error: {e}")
        return jsonify({'error': str(e)}), 500
```

### Step 2: Authentication (Optional)

Add API key authentication:

```python
import os
from functools import wraps

BRAIN_API_KEY = os.environ.get('BRAIN_API_KEY', 'dev-key-12345')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != BRAIN_API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Apply to routes
@app.route('/api/brain/feed', methods=['POST'])
@require_api_key
def brain_get_feed():
    # ... existing code
```

### Step 3: Update Frontend to Use API

Replace direct calls:

```python
# OLD (direct call)
feed = personalizer.get_personalized_feed(user_key, limit, user_country)

# NEW (API call)
import requests

response = requests.post('http://localhost:5555/api/brain/feed', json={
    'user_key': user_key,
    'limit': limit,
    'user_country': user_country
}, headers={'X-API-Key': BRAIN_API_KEY})

feed = response.json()
```

## Option 2: External Personalization Service

**Replace personalization entirely** with external service.

### Architecture

```
┌─────────────┐
│   app.py    │
└──────┬──────┘
       │
       │ HTTP POST
       ↓
┌──────────────────────┐
│ External BRain API   │ ← Your custom implementation
│ (separate service)   │
└──────┬───────────────┘
       │
       └──→ PostgreSQL / Redis / Your choice
```

### Data Contract

#### Input: Get Personalized Feed

```json
POST https://your-brain-api.com/v1/feed
{
  "user_key": "user123",
  "limit": 20,
  "user_country": "IL",
  "available_markets": [
    {
      "market_id": "market1",
      "title": "Will LeBron win MVP?",
      "category": "Sports",
      "tags": ["NBA", "LeBron", "Basketball"],
      "probability": 0.65,
      "volume_24h": 50000,
      "created_at": "2026-02-14T10:00:00Z"
    },
    // ... more markets
  ]
}
```

#### Output: Ranked Feed

```json
{
  "hero": [
    {
      "market_id": "market1",
      "rank": 1,
      "score": 2.45,
      "reason": "High trending + personal interest in NBA"
    }
  ],
  "grid": [
    // 9 markets
  ],
  "stream": [
    // Remaining markets
  ],
  "personalized": true,
  "algorithm_version": "v2.0"
}
```

#### Input: Record Interaction

```json
POST https://your-brain-api.com/v1/interactions
{
  "user_key": "user123",
  "market_id": "market1",
  "event_type": "click",
  "dwell_ms": 5000,
  "geo_country": "IL",
  "timestamp": "2026-02-15T04:30:00Z",
  "context": {
    "position": 3,
    "section": "grid"
  }
}
```

#### Output: Confirmation

```json
{
  "interaction_id": "int_xyz123",
  "status": "recorded",
  "profile_updated": true
}
```

### Implementation in app.py

```python
import requests
import os

EXTERNAL_BRAIN_URL = os.environ.get('BRAIN_API_URL', 'https://your-brain-api.com/v1')
BRAIN_API_KEY = os.environ.get('BRAIN_API_KEY')

class ExternalPersonalizationClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
    
    def get_personalized_feed(self, user_key, limit=20, user_country=None):
        """Call external API for personalized feed"""
        # Fetch all available markets from local DB
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT market_id, title, category, probability, volume_24h, created_at
            FROM markets
            WHERE status = 'open'
            ORDER BY volume_total DESC
            LIMIT 200
        """)
        
        markets = [
            {
                'market_id': row[0],
                'title': row[1],
                'category': row[2],
                'probability': row[3],
                'volume_24h': row[4],
                'created_at': row[5]
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        
        # Call external API
        response = self.session.post(
            f'{self.base_url}/feed',
            json={
                'user_key': user_key,
                'limit': limit,
                'user_country': user_country,
                'available_markets': markets
            },
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback to simple ranking if external API fails
            logger.warning(f"External API failed: {response.status_code}")
            return self._fallback_ranking(markets, limit)
    
    def record_interaction(self, user_key, market_id, event_type, **kwargs):
        """Send interaction to external API"""
        try:
            response = self.session.post(
                f'{self.base_url}/interactions',
                json={
                    'user_key': user_key,
                    'market_id': market_id,
                    'event_type': event_type,
                    'timestamp': datetime.now().isoformat(),
                    **kwargs
                },
                timeout=2
            )
            return response.json()
        except Exception as e:
            logger.error(f"Failed to record interaction: {e}")
            return {'status': 'failed'}
    
    def _fallback_ranking(self, markets, limit):
        """Simple fallback if external API unavailable"""
        # Sort by volume + contestedness
        ranked = sorted(markets, key=lambda m: m['volume_24h'], reverse=True)
        return {
            'hero': [ranked[0]] if ranked else [],
            'grid': ranked[1:10] if len(ranked) > 1 else [],
            'stream': ranked[10:limit] if len(ranked) > 10 else [],
            'personalized': False,
            'algorithm_version': 'fallback'
        }

# Replace global personalizer
if os.environ.get('USE_EXTERNAL_BRAIN') == 'true':
    personalizer = ExternalPersonalizationClient(EXTERNAL_BRAIN_URL, BRAIN_API_KEY)
else:
    from personalization import personalizer
```

## Option 3: Hybrid Approach

Keep trending/tracking local, externalize PersonalScore computation only.

### Architecture

```
┌─────────────┐
│   app.py    │
└──────┬──────┘
       │
       ├──→ tracking_engine.py (local)
       ├──→ compute_trending.py (local)
       ├──→ brain.db (local)
       │
       └──→ HTTP → External PersonalScore API
```

### Benefits

- Trending stays fast (local DB queries)
- Tracking has low latency (local writes)
- Only PersonalScore computation externalized
- Can A/B test different personalization algorithms

## Migration Path

### Phase 1: Add API Layer (Keep Logic)

1. Create `/api/brain/*` endpoints (Option 1)
2. Keep using internal `personalizer`
3. Test API endpoints work correctly
4. Update monitoring to track API latency

### Phase 2: Extract to Microservice

1. Copy `personalization.py` to new service
2. Set up separate database (or read-replica)
3. Update `app.py` to call external API
4. Add fallback logic for API failures
5. Deploy external service
6. Switch traffic gradually (10% → 50% → 100%)

### Phase 3: Enhance External Service

1. Implement new algorithms
2. Add ML models
3. Use better data stores (Redis for cache, PostgreSQL for profiles)
4. Scale independently

## Current Database Schema

If external service needs direct DB access:

### Markets Table

```sql
CREATE TABLE markets (
    market_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    probability REAL NOT NULL,
    volume_24h REAL DEFAULT 0,
    volume_total REAL DEFAULT 0,
    image_url TEXT,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_date TIMESTAMP,
    editorial_description TEXT
);
```

### User Interactions Table

```sql
CREATE TABLE user_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key TEXT NOT NULL,
    market_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dwell_ms INTEGER,
    geo_country TEXT,
    context TEXT
);
```

### User Profiles Table

```sql
CREATE TABLE user_profiles (
    user_key TEXT PRIMARY KEY,
    profile_data TEXT,  -- JSON blob of scores
    total_interactions INTEGER DEFAULT 0,
    last_active TIMESTAMP
);
```

### Trending Cache Table

```sql
CREATE TABLE trending_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    scope TEXT NOT NULL,
    score REAL NOT NULL,
    window TEXT NOT NULL,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Current Algorithm Weights

For reference if rebuilding externally:

```python
# PersonalScore weights
PERSONAL_WEIGHTS = {
    'interest': 0.35,      # Tag/taxonomy affinity
    'similarity': 0.25,    # Similar to recent engagement
    'depth': 0.15,         # Engagement depth
    'freshness': 0.10,     # Newer markets
    'followup': 0.10,      # Meaningful updates
    'negative': -0.10,     # Hide/not interested
    'diversity': -0.05     # Prevent echo chamber
}

# FinalScore weights
FINAL_WEIGHTS = {
    'trending': 0.40,      # 40% of feed (Roy's spec)
    'rising': 0.15,        # Belief shifts
    'editorial': 0.05      # Manual boosts
}

# Trending blend (for users with geo)
local_trending = 0.40
global_trending = 0.60
```

## Testing the API

### Example: Test Feed Endpoint

```bash
curl -X POST http://localhost:5555/api/brain/feed \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-12345" \
  -d '{
    "user_key": "roy",
    "limit": 20,
    "user_country": "IL"
  }'
```

### Example: Test Interaction Tracking

```bash
curl -X POST http://localhost:5555/api/track \
  -H "Content-Type: application/json" \
  -d '{
    "user_key": "roy",
    "market_id": "nba-all-star-mvp-2026",
    "event_type": "click",
    "dwell_ms": 5000,
    "context": {"position": 1}
  }'
```

## Recommendations

### For MVP / Near-term

**→ Use Option 1 (Internal REST API)**

**Why:**
- Fast to implement (add routes, keep logic)
- No infrastructure changes
- Easy to test
- Can hand off API spec to other developers
- Allows gradual migration to Option 2

### For Scale / Long-term

**→ Migrate to Option 2 (External Service)**

**Why:**
- Independent scaling (personalization ≠ frontend)
- Better data stores (Redis, PostgreSQL)
- Can deploy ML models
- A/B test algorithms
- Team can own it separately

### Quick Win

**→ Start with Option 3 (Hybrid)**

**Why:**
- Keep fast parts local (trending, tracking)
- Externalize slow/complex part (PersonalScore)
- Best of both worlds
- Easy rollback if external fails

## Next Steps

1. **Document current API contract** (I can help with this)
2. **Add `/api/brain/*` endpoints** to current app
3. **Test endpoints work** with existing logic
4. **Share API spec** with new developer
5. **They build external service** matching contract
6. **Switch over** when ready

Let me know which option you prefer and I can help implement it!

---

**Contact for Questions:**
- Current implementation: `personalization.py`, `tracking_engine.py`
- Algorithm spec: `BRAIN_SPEC_FINAL.md`
- Database: `brain.db` (SQLite)
- Deployment: v159 (Feb 15, 2026)

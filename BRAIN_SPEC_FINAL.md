# BRain Behavioral Scoring System - FINAL SPECIFICATION
**Version:** 2.0 (Merged from Original + Extended Design)
**Date:** Feb 11, 2026
**Status:** Implementation Ready

---

## Document Purpose

This document merges:
1. **Original BRain spec** (Roy's V1 developer guide)
2. **Extended behavioral learning design** (action impact, co-occurrence, interface)

---

## Core Principles (from Original)

### 1. Fast & Deterministic (V1)
- Rule-based scoring, fully explainable
- Low-latency, cacheable responses
- No duplicates across homepage sections

### 2. Graceful Degradation
- Always returns content (fallbacks ensure never-empty sections)
- Guest + authenticated identity model
- Privacy-aware (IP-based geo behind toggle)

### 3. Implicit Learning
- **NO user ratings or explicit feedback**
- Everything learned from interaction events
- Profile built automatically from behavior

---

## Action Weights & Event Schema

### 6.3 Interaction Weights (from Original Spec)

| Event Type | Weight | Notes |
|------------|--------|-------|
| **participate** | +6 | Strong positive (user placed bet) |
| **participate_intent** | +3 | High intent (clicked "Commit Belief") |
| **share** | +4 | Positive + viral signal |
| **click** | +2 | Opened market detail |
| **view_market** | +2 | Market page loaded |
| **dwell>=30s** | +2 | Depth signal (analyzed market) |
| **dwell>=5s** | +1 | Weak positive (skimmed) |
| **skip_fast** | -1 | Optional (saw but ignored quickly) |
| **hide/not_interested** | -6 | Strong negative |

### Extended Action Types (Additional)

| Event Type | Weight | Notes |
|------------|--------|-------|
| **bookmark/save** | +3.5 | Saved for later |
| **comment** | +4.5 | Engaged in discussion |
| **return_visit** | +3 | Came back to same market |
| **scroll_past** | -0.5 | Saw in feed but didn't click |

### Event Schema (V1)

```json
{
  "user_key": "string",           // user_id (auth) or anon_id (guest)
  "market_id": "string",
  "event_type": "string",         // participate, share, click, etc.
  "ts": "ISO8601",
  "dwell_ms": "number?",          // optional: time spent on page
  "context": {
    "section": "string",          // hero/categories/more
    "position": "number"          // rank in list
  },
  "geo_country": "string?"        // optional: server can attach
}
```

---

## Score Calculation (Original + Extended)

### 10.2 Ranking Formula (from Original Spec)

```python
PersonalScore = (
    0.35 * interest +       # Affinity from profile to market tags/taxonomy
    0.25 * similarity +     # Similarity to recently engaged markets
    0.15 * depth +          # User engagement depth with similar markets
    0.10 * freshness +      # Preference for newer/updated markets
    0.10 * followup +       # Boost if meaningful change since last seen
    -0.10 * negative +      # Penalty from hide/not_interested
    -0.05 * diversity       # Penalty for too-similar streaks
)

FinalScore = (
    PersonalScore +
    0.25 * trending +       # Localized/global trending score
    0.20 * rising +         # Belief shift magnitude
    0.05 * editorial        # Manual/curation boost
)
```

### How Profile Updates Work

When user takes action on a market:

1. **Map market → metadata**
   ```python
   market = {
       'taxonomy_node_ids': ['sports', 'soccer', 'world_cup'],
       'tag_ids': ['messi', 'argentina', 'tournament'],
       'lang': 'en'
   }
   ```

2. **Compute delta**
   ```python
   delta = weight(event_type) * f(dwell_ms)
   
   # Example: participate (weight=6) with 45 seconds dwell
   delta = 6 * 1.0 = 6.0
   ```

3. **Apply to profile**
   ```python
   # Direct tags
   profile['interests']['tags']['messi'] += delta * 1.0
   profile['interests']['tags']['argentina'] += delta * 1.0
   
   # Taxonomy nodes
   profile['interests']['taxonomy']['world_cup'] += delta * 1.0
   profile['interests']['taxonomy']['soccer'] += delta * 0.8
   profile['interests']['taxonomy']['sports'] += delta * 0.5  # ancestor propagation
   
   # Language affinity
   profile['interests']['language']['en'] += delta * 0.3
   ```

4. **Apply recency decay**
   ```python
   time_since_last = now - last_ts
   decay_factor = exp(-time_since_last / 30_days)
   
   score_after_decay = score * decay_factor
   ```

5. **Keep top N items**
   ```python
   # Keep top 200 tags, top 200 taxonomy nodes
   profile['interests']['tags'] = sorted(tags, by='score')[:200]
   ```

---

## User Profile Structure

### 7.1 Profile Schema (from Original)

```python
UserProfile = {
    'user_key': 'user_abc123',
    'updated_at': '2026-02-11T07:00:00Z',
    'interests': {
        'taxonomy': [
            {'node_id': 'sports', 'score': 45.2, 'last_ts': '2026-02-11T06:45:00Z'},
            {'node_id': 'politics', 'score': 38.7, 'last_ts': '2026-02-10T15:30:00Z'},
            # ... keep top 200
        ],
        'tags': [
            {'tag_id': 'messi', 'score': 52.1, 'last_ts': '2026-02-11T06:45:00Z'},
            {'tag_id': 'trump', 'score': 41.3, 'last_ts': '2026-02-10T18:00:00Z'},
            # ... keep top 200
        ],
        'language': [
            {'lang': 'en', 'score': 75.5, 'last_ts': '2026-02-11T06:30:00Z'},
            {'lang': 'he', 'score': 24.5, 'last_ts': '2026-02-09T12:00:00Z'}
        ]
    },
    'negatives': {
        'tags': [
            {'tag_id': 'crypto', 'score': -15.2, 'last_ts': '2026-02-08T10:00:00Z'}
        ],
        'taxonomy': []
    },
    'seen': {
        'recent_market_ids': ['market_xyz', 'market_abc', ...]  # hot-set for filtering
    }
}
```

---

## Seen Content & Resurfacing

### 8.2 Seen Snapshot Storage (from Original)

```python
SeenRecord = {
    'user_key': 'user_abc123',
    'market_id': 'market_xyz',
    'last_seen_ts': '2026-02-11T05:30:00Z',
    'snapshot_at_view': {
        'belief': 0.48,        # probability at time of view
        'volume_usd': 125000,
        'status': 'open',
        'updated_at': '2026-02-11T05:29:00Z'
    }
}
```

### 8.3 Resurfacing Rules (HARD)

**Do NOT show a seen market unless at least one is true:**
- Belief/probability changed by **> 5% absolute** since snapshot_at_view, OR
- New development flag for same story/topic, OR
- User explicitly follows/subscribes (future feature)

**When resurfacing:**
- Include `change_since_last_seen` metadata explaining why it returned
- Example: "Probability moved from 48% to 62% (+14%)"

---

## Trending Engine (Global + Localized)

### 13.1 Trending Score Definition (from Original)

```python
TrendingScore = 0.85 * interest_norm + 0.15 * volume_norm
```

**Components:**
1. **Interest component (85%):**
   - Compute per (user_key, market_id) interaction score from events in 24h window
   - Aggregate per market by **averaging across users who interacted** (not all active users)
   - Normalize within each scope using percentile normalization

2. **Volume component (15%):**
   - Volume = sum(trade_usd) for all trades in market within window
   - Use log scaling: `log(1 + volume_usd)` before normalization

### 13.4 Localization Blend (from Original)

```python
trending_boost = 0.80 * TrendingScore(local_scope) + 0.20 * TrendingScore(global)
```

**Fallback chain (no duplicates):**
- Country → Subregion → Region → Supergroup → Global
- When widening, **never repeat markets already selected** from narrower scopes

**Israel special case:** Treated closer to Europe/US for fallback ordering (configurable)

### 13.5 Insufficient Local Relevance (V1 Defaults)

Fallback if either:
- < 200 markets have a computed trending score in scope, OR
- < 500 active users in scope (5-day active definition)

---

## Extended Features (Beyond Original Spec)

### Co-Occurrence Tracking

Track which tags/categories users engage with together:

```python
def record_cooccurrence(user_id, category, tags):
    """
    When user engages with a market, record tag co-occurrences
    """
    for tag_a in tags:
        for tag_b in tags:
            if tag_a != tag_b:
                increment_cooccurrence(tag_a, tag_b)
    
    # Also track category + tag co-occurrence
    for tag in tags:
        increment_cooccurrence(category, tag)
```

**Use case:** "Users who engage with 'Trump' markets also engage with 'Election' (92% overlap)"

### Score Evolution Timeline

Track how scores change over time:

```python
score_history = {
    'user_id': 'user_abc123',
    'topic_type': 'category',
    'topic_value': 'Politics',
    'snapshots': [
        {'ts': '2026-02-01', 'score': 35.2},
        {'ts': '2026-02-05', 'score': 42.1},
        {'ts': '2026-02-10', 'score': 48.7},
        {'ts': '2026-02-11', 'score': 52.3}
    ]
}
```

---

## API Contracts (from Original)

### GET /brain/homepage

Returns all section outputs in one call:

```json
{
  "algorithm_version": "v1.x",
  "geo_country": "IL",
  "sections": {
    "hero": {
      "market_ids": ["market_xyz"],
      "assets": [{"market_id": "market_xyz", "image_url": "..."}]
    },
    "categories": {
      "market_ids": ["market_abc", "market_def"],
      "assets": [...]
    },
    "more": {
      "market_ids": ["market_123", "market_456", ...],
      "assets": [...],
      "cursor": "next_page_token"
    }
  },
  "meta": {
    "composition": {"personalized": 0.60, "trending": 0.20, "exploration": 0.20},
    "cache": {"hit": true, "ttl": 300}
  }
}
```

### POST /brain/user/track-activity

Ingest batched events (async write):

```json
{
  "user_key": "user_abc123",
  "geo_country": "IL",
  "events": [
    {
      "market_id": "market_xyz",
      "event_type": "participate",
      "ts": "2026-02-11T07:00:00Z",
      "dwell_ms": 45000,
      "context": {
        "section": "hero",
        "position": 0
      }
    },
    {
      "market_id": "market_abc",
      "event_type": "view_market",
      "ts": "2026-02-11T07:01:00Z",
      "context": {
        "section": "more",
        "position": 5
      }
    }
  ]
}
```

---

## Database Schema

### user_interactions (Event Log)

```sql
CREATE TABLE user_interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_key TEXT NOT NULL,
    market_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    ts TIMESTAMP NOT NULL,
    dwell_ms INTEGER,
    section TEXT,
    position INTEGER,
    geo_country TEXT,
    metadata JSONB
);

CREATE INDEX idx_interactions_user ON user_interactions(user_key, ts DESC);
CREATE INDEX idx_interactions_market ON user_interactions(market_id, ts DESC);
CREATE INDEX idx_interactions_ts ON user_interactions(ts DESC);
```

### user_profiles (Aggregated State)

```sql
CREATE TABLE user_profiles (
    user_key TEXT PRIMARY KEY,
    display_name TEXT,
    created_at TIMESTAMP,
    last_active TIMESTAMP,
    total_interactions INTEGER DEFAULT 0,
    interests JSONB,          -- {taxonomy: [...], tags: [...], language: [...]}
    negatives JSONB,          -- {tags: [...], taxonomy: [...]}
    seen_markets JSONB        -- {recent_market_ids: [...]}
);
```

### seen_snapshots (Resurfacing Logic)

```sql
CREATE TABLE seen_snapshots (
    user_key TEXT NOT NULL,
    market_id TEXT NOT NULL,
    last_seen_ts TIMESTAMP NOT NULL,
    belief_at_view REAL,
    volume_at_view REAL,
    status_at_view TEXT,
    updated_at TIMESTAMP,
    PRIMARY KEY (user_key, market_id)
);

CREATE INDEX idx_seen_user ON seen_snapshots(user_key);
```

### market_trending_rolling (Trending Scores)

```sql
CREATE TABLE market_trending_rolling (
    market_id TEXT NOT NULL,
    scope TEXT NOT NULL,      -- 'global', 'country:IL', 'region:europe', etc.
    trending_score REAL NOT NULL,
    interest_norm REAL,
    volume_norm REAL,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    computed_at TIMESTAMP,
    PRIMARY KEY (market_id, scope, window_start)
);

CREATE INDEX idx_trending_scope ON market_trending_rolling(scope, trending_score DESC);
```

---

## Learning Interface (Observation Dashboard)

### Dashboard Sections

#### 1. User Profile Viewer
- Top categories (0-100 scores)
- Top tags (with interaction counts)
- Language affinity
- Recent actions timeline

#### 2. Score Evolution Charts
- Line charts showing category/tag scores over time
- Event markers (when bets/shares happened)
- Decay visualization

#### 3. Action Impact Analyzer
```
Action: PARTICIPATE on "Will Messi win World Cup?"
User: user_abc123
Time: 2026-02-11 07:00:00

SCORE UPDATES:
Category: Sports
  Before: 38.5 → After: 48.5 (+10.0) ✅

Tags:
  Messi:       25.2 → 31.2 (+6.0) ✅
  World Cup:   18.5 → 24.5 (+6.0) ✅
  Soccer:      32.1 → 38.1 (+6.0) ✅
  Argentina:   10.0 → 16.0 (+6.0) ✅

Taxonomy Ancestors (propagated):
  soccer → sports: +3.0 (50% propagation)
  
Language:
  en: 65.2 → 66.8 (+1.6)

Co-occurrence Created:
  Sports + Argentina: +1
  Messi + World Cup: +1
```

#### 4. Trending Dashboard
- Top 20 markets by scope (global, country, region)
- Interest vs volume breakdown
- Active user count per scope

#### 5. Co-Occurrence Heatmap
```
           Trump  Bitcoin  Sports  AI  Ukraine
Trump       100     35      12    18     42
Bitcoin      35    100       8    61     14
Sports       12      8     100     9     11
AI           18     61       9   100     19
Ukraine      42     14      11    19    100
```

#### 6. Algorithm Performance Metrics
- Engagement rate: Personalized vs Global
- Average dwell time per segment
- Return visit rate
- Bet conversion rate
- Diversity metrics (category distribution)

---

## Implementation Checklist (from Original)

### Build Order:
1. ✅ Metadata ingestion (market → tags/taxonomy/lang/assets)
2. ✅ Snapshot ingestion (belief/volume updates)
3. [ ] **Tracking API** with batching + durable event log
4. [ ] **Seen snapshot storage** + resurfacing diff logic
5. [ ] **User profile store** (Redis + Postgres) + incremental updates
6. [ ] **Homepage API** with candidate generation + ranking + constraints + no-duplicates
7. [ ] **Trending aggregation job** + Redis zsets per scope + blending/fallback
8. [ ] **Caching** + client localStorage contract + graceful degradation
9. [ ] **Learning interface** (observation dashboard)
10. [ ] Load tests + monitoring + flag-based rollout

---

## Configuration Values

### Action Weights (Tunable)
```python
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
```

### Ranking Weights (Tunable)
```python
PERSONAL_SCORE_WEIGHTS = {
    'interest': 0.35,
    'similarity': 0.25,
    'depth': 0.15,
    'freshness': 0.10,
    'followup': 0.10,
    'negative': -0.10,
    'diversity': -0.05
}

FINAL_SCORE_WEIGHTS = {
    'personal': 1.0,        # PersonalScore is the base
    'trending': 0.25,
    'rising': 0.20,
    'editorial': 0.05
}

TRENDING_WEIGHTS = {
    'interest': 0.85,
    'volume': 0.15
}

TRENDING_BLEND = {
    'local': 0.80,
    'global': 0.20
}
```

### Profile Limits
```python
TOP_N_TAGS = 200
TOP_N_TAXONOMY = 200
RECENT_SEEN_LIMIT = 500
DECAY_HALF_LIFE_DAYS = 30
```

### Thresholds
```python
RESURFACING_BELIEF_DELTA = 0.05  # 5% absolute change
INSUFFICIENT_LOCAL_MARKETS = 200
INSUFFICIENT_ACTIVE_USERS = 500
ACTIVE_USER_WINDOW_DAYS = 5
```

---

## Open Questions for Roy

1. **Action Weight Tuning:**
   - Original has `participate=+6`, I had `position=1.0` (normalized). Should we keep +6 scale or normalize to 0-1?
   - Is `comment=+4.5` right? (I added this, not in original)

2. **Trending Refresh Rate:**
   - Original says ~10 minutes. Too frequent? Too slow?

3. **Profile Size:**
   - Top 200 tags/taxonomy enough? Or should we keep more?

4. **Diversity Penalty:**
   - Original has -0.05 weight in PersonalScore. Enough to prevent filter bubbles?

5. **Localization:**
   - Original has 4-level geo hierarchy. Do we need all levels for V1, or start with country-only?

6. **Learning Interface Access:**
   - Admin-only? Or visible to users (view their own profile)?

---

**Next: Let's discuss any section and tune parameters!**

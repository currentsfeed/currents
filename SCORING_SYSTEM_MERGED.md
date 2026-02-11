# BRain Behavioral Scoring System - Complete Specification
**Version:** 2.0 (Merged)
**Date:** Feb 11, 2026
**Status:** Design for Implementation

---

## Core Philosophy

### 1. Implicit Learning Only
- **NO user ratings or explicit feedback**
- Everything learned from behavior: views, dwell time, bets, shares, comments
- Users never see scores or adjust settings manually
- System builds profiles automatically from actions

### 2. Action-Based Signal Hierarchy
Every interaction generates signals that update topic/tag/category scores.

### 3. Temporal Decay
Recent behavior matters more; old interests fade naturally over time.

---

## Action Weights & Scoring Table

### Primary Action Types

| Action | Weight | Score Delta | Frequency Cap | Description |
|--------|--------|-------------|---------------|-------------|
| **Position Taken** | 1.00 | +0.30 per tag | None | User places bet/prediction - strongest signal |
| **Share** | 0.85 | +0.25 per tag | 5/day per market | User shares market externally |
| **Comment** | 0.75 | +0.20 per tag | None | User posts discussion comment |
| **Dwell 60+s** | 0.60 | +0.20 per tag | None | Deep engagement (reading/analyzing) |
| **Dwell 30-60s** | 0.45 | +0.15 per tag | None | Medium engagement |
| **Dwell 15-30s** | 0.30 | +0.10 per tag | None | Light engagement (skimmed) |
| **Return Visit** | 0.50 | +0.15 per tag | 3 returns/market | Came back to same market |
| **Click/View** | 0.20 | +0.05 per tag | None | Opened market detail |
| **Scroll Past** | -0.05 | -0.02 per tag | None | Saw in feed but didn't click |
| **Bookmark/Save** | 0.70 | +0.22 per tag | None | Saved for later |

### Score Updates Per Action

When a user takes an action on a market, **all associated tags/topics/categories** get updated:

**Example: User bets on "Will Messi win 2026 World Cup?"**
```
Action: Position Taken (weight: 1.00)

Updates:
- Category: Sports         +0.35 (weight * 0.35)
- Tag: Messi              +0.30 (weight * 0.30)
- Tag: World Cup          +0.30
- Tag: Soccer             +0.30
- Tag: Argentina          +0.30
- Topic: Int'l Sports     +0.25 (weight * 0.25)
- Topic: Major Events     +0.25
```

**Multipliers:**
- Category gets: `action_weight × 0.35`
- People/Event tags get: `action_weight × 0.30`
- Topic tags get: `action_weight × 0.25`
- Related topics get: `action_weight × 0.20`

---

## Interaction Tracking Schema

### Database Tables

#### 1. user_interactions
```sql
CREATE TABLE user_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    market_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL,  -- 'view', 'click', 'position', 'share', etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    device TEXT,                     -- 'mobile', 'desktop', 'tablet'
    duration_seconds INTEGER,        -- Time spent (for dwell actions)
    metadata TEXT,                   -- JSON for extra context
    FOREIGN KEY (market_id) REFERENCES markets (market_id)
);

CREATE INDEX idx_user_interactions_user ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_market ON user_interactions(market_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp);
```

#### 2. user_topic_scores
```sql
CREATE TABLE user_topic_scores (
    user_id TEXT,
    topic_type TEXT,                 -- 'category', 'tag', 'person', 'event', 'topic'
    topic_value TEXT,
    score REAL DEFAULT 0.0,          -- 0-100 scale
    raw_score REAL DEFAULT 0.0,      -- Unnormalized accumulator
    interactions INTEGER DEFAULT 0,  -- Count of interactions
    last_updated TIMESTAMP,
    last_decay TIMESTAMP,            -- Last time decay was applied
    PRIMARY KEY (user_id, topic_type, topic_value)
);

CREATE INDEX idx_user_scores_user ON user_topic_scores(user_id);
CREATE INDEX idx_user_scores_score ON user_topic_scores(score DESC);
```

#### 3. user_profiles
```sql
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    display_name TEXT,
    created_at TIMESTAMP,
    last_active TIMESTAMP,
    total_interactions INTEGER DEFAULT 0,
    profile_data TEXT               -- JSON for preferences, settings
);
```

---

## Score Calculation Logic

### Formula for Topic Score
```python
def calculate_topic_score(user_id, topic_type, topic_value):
    """
    Calculate affinity score for a topic (0-100 scale)
    Based on all historical interactions
    """
    interactions = get_user_interactions(user_id, topic_type, topic_value)
    
    raw_score = 0.0
    now = datetime.now()
    
    for interaction in interactions:
        # 1. Base action weight
        action_weight = ACTION_WEIGHTS[interaction.type]
        
        # 2. Recency weight (exponential decay: 30-day half-life)
        days_ago = (now - interaction.timestamp).days
        recency_weight = math.exp(-days_ago / 30)
        
        # 3. Engagement depth (for dwell actions)
        if interaction.type.startswith('dwell'):
            depth_weight = min(1.0, interaction.duration_seconds / 60)
        else:
            depth_weight = 1.0
        
        # 4. Composite delta
        delta = action_weight * recency_weight * depth_weight
        raw_score += delta
    
    # 5. Normalize to 0-100 with sigmoid
    # Sigmoid: 100 / (1 + exp(-x + offset))
    normalized_score = 100 / (1 + math.exp(-raw_score + 5))
    
    # 6. Confidence boost (more interactions = higher confidence)
    interaction_count = len(interactions)
    confidence = min(1.0, interaction_count / 10)  # Max at 10 interactions
    
    # 7. Final score with confidence adjustment
    final_score = normalized_score * (0.7 + 0.3 * confidence)
    
    return round(final_score, 2)
```

### Update Score on Action
```python
def record_action(user_id, market_id, action_type, duration_seconds=None):
    """
    Record user action and update all relevant topic scores
    """
    # 1. Insert interaction record
    interaction = {
        'user_id': user_id,
        'market_id': market_id,
        'interaction_type': action_type,
        'timestamp': datetime.now(),
        'duration_seconds': duration_seconds
    }
    insert_interaction(interaction)
    
    # 2. Get market metadata (tags, category, topics)
    market = get_market(market_id)
    
    # 3. Get action weight
    action_weight = ACTION_WEIGHTS.get(action_type, 0.2)
    
    # 4. Update category score
    update_topic_score(
        user_id, 
        'category', 
        market.category, 
        delta=action_weight * 0.35
    )
    
    # 5. Update tag scores
    for tag in market.tags:
        tag_type = get_tag_type(tag)  # 'person', 'event', 'topic', etc.
        update_topic_score(
            user_id,
            tag_type,
            tag,
            delta=action_weight * 0.30
        )
    
    # 6. Update related topic scores
    for topic in market.related_topics:
        update_topic_score(
            user_id,
            'topic',
            topic,
            delta=action_weight * 0.25
        )
    
    # 7. Record co-occurrence patterns
    record_cooccurrence(user_id, market.category, market.tags)
```

---

## Temporal Decay System

### Weekly Decay
```python
def apply_weekly_decay():
    """
    Apply 5% decay to all scores every 7 days
    Run as daily cron job, check last_decay timestamp
    """
    DECAY_RATE = 0.95  # 5% decay
    DECAY_INTERVAL_DAYS = 7
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all scores that need decay
    cursor.execute("""
        SELECT user_id, topic_type, topic_value, score, last_decay
        FROM user_topic_scores
        WHERE last_decay IS NULL 
           OR (julianday('now') - julianday(last_decay)) >= ?
    """, (DECAY_INTERVAL_DAYS,))
    
    for row in cursor.fetchall():
        user_id, topic_type, topic_value, score, last_decay = row
        
        # Calculate new score
        new_score = score * DECAY_RATE
        
        # Update
        cursor.execute("""
            UPDATE user_topic_scores
            SET score = ?, last_decay = CURRENT_TIMESTAMP
            WHERE user_id = ? AND topic_type = ? AND topic_value = ?
        """, (new_score, user_id, topic_type, topic_value))
    
    conn.commit()
```

**Decay Schedule:**
- Runs daily via cron
- Applies 5% decay every 7 days
- Scores below 1.0 are removed (garbage collection)

**Effect:**
- Recent behavior matters more
- Old interests fade naturally
- System adapts to changing preferences

---

## Personalized Feed Ranking

### Algorithm
```python
def get_personalized_feed(user_id, markets):
    """
    Rank markets based on:
    - Global belief intensity (50%)
    - User affinity (45%)
    - Diversity penalty (5%)
    """
    ranked = []
    
    for market in markets:
        # 1. Base score: Belief Intensity
        belief_intensity = calculate_belief_intensity(market)
        
        # 2. User affinity
        category_score = get_user_score(user_id, 'category', market.category)
        
        tag_scores = [get_user_score(user_id, 'tag', tag) for tag in market.tags]
        avg_tag_score = sum(tag_scores) / len(tag_scores) if tag_scores else 0
        
        affinity = (
            category_score * 0.4 +
            avg_tag_score * 0.6
        )
        
        # 3. Diversity penalty (prevent filter bubbles)
        diversity_penalty = calculate_diversity_penalty(user_id, market.category)
        
        # 4. Composite score
        final_score = (
            belief_intensity * 0.50 +
            affinity * 0.45 +
            diversity_penalty * 0.05
        )
        
        ranked.append({
            'market': market,
            'score': final_score,
            'breakdown': {
                'belief_intensity': belief_intensity,
                'affinity': affinity,
                'category_score': category_score,
                'tag_score': avg_tag_score,
                'diversity': diversity_penalty
            }
        })
    
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked
```

### Diversity Penalty
```python
def calculate_diversity_penalty(user_id, category):
    """
    Prevent showing too much of the same category in 24h window
    """
    recent_views = get_recent_views(user_id, hours=24)
    category_count = sum(1 for v in recent_views if v.category == category)
    
    # Penalty curve
    if category_count < 3:
        return 1.0    # No penalty
    elif category_count < 5:
        return 0.85   # Small penalty
    elif category_count < 8:
        return 0.70   # Medium penalty
    elif category_count < 12:
        return 0.50   # Large penalty
    else:
        return 0.30   # Very large penalty (still shown, but way down)
```

---

## Cold Start Problem

### New User Strategy
```python
def get_feed_for_new_user(user_id):
    """
    Special strategy for users with < 20 interactions
    """
    interaction_count = get_interaction_count(user_id)
    
    if interaction_count < 10:
        # Pure global ranking + category sampling
        markets = get_all_markets()
        global_top = rank_by_belief_intensity(markets)[:10]
        
        # Sample one from each category
        category_samples = []
        for category in ALL_CATEGORIES:
            top = get_top_market_by_category(category)
            if top:
                category_samples.append(top)
        
        return {
            'hero': global_top[0],
            'featured': global_top[1:5],
            'grid': global_top[5:9] + category_samples[:4],
            'stream': category_samples[4:]
        }
    
    elif interaction_count < 20:
        # 70% personalized, 30% exploration
        personalized = get_personalized_feed(user_id, markets)
        global_ranking = rank_by_belief_intensity(markets)
        
        # Mix: take top personalized, inject some global
        mixed = personalized[:14] + global_ranking[:6]
        shuffle_within_sections(mixed)
        
        return format_feed(mixed)
    
    else:
        # Fully personalized
        return get_personalized_feed(user_id, markets)
```

**Rapid Learning for New Users:**
- First 20 actions get 2× weight
- Ensures quick profile building
- Prevents extended cold start period

---

## Tag & Topic Extraction

### Market Metadata Structure
```json
{
  "market_id": "abc123",
  "title": "Will Messi win 2026 World Cup with Argentina?",
  "category": "Sports",
  "tags": ["Messi", "World Cup", "Soccer", "Argentina", "Tournament"],
  "people_tags": ["Messi"],
  "topic_tags": ["World Cup", "Soccer", "International Sports"],
  "location_tags": ["Argentina"],
  "event_tags": ["2026 World Cup"],
  "related_topics": ["Major Sporting Events", "National Teams"]
}
```

### Tag Types
1. **Category**: Top-level (9 categories: Sports, Politics, Crypto, etc.)
2. **People Tags**: Individual names (Trump, Messi, Biden, Musk)
3. **Event Tags**: Specific events (2026 World Cup, Election 2024, Super Bowl)
4. **Topic Tags**: Themes (AI, cryptocurrency, climate, economy)
5. **Location Tags**: Geographic (USA, Europe, Argentina, Ukraine)

---

## Learning Interface (Observation Dashboard)

### Purpose
**NOT for manual tuning**, but for:
- Observing how the system learns
- Understanding user behavior patterns
- Testing algorithm changes
- Debugging scoring anomalies

### Interface Sections

#### 1. User Profile Viewer
Shows:
- Top categories (with scores 0-100)
- Top tags (with interaction counts)
- Recent actions (last 24h timeline)
- Score evolution over time (charts)

#### 2. Action Impact Analyzer
Shows what happens when user takes an action:
- Before/after scores for all affected tags
- Which topics got boosted
- Co-occurrence patterns created

#### 3. Algorithm Performance Dashboard
Metrics:
- Engagement rate (personalized vs global)
- Average time per market
- Return visit rate
- Bet conversion rate
- Diversity metrics

#### 4. Tag Co-Occurrence Heatmap
Shows which tags users engage with together.
Example: Users who like "Trump" markets also engage with "Election" (92% overlap)

#### 5. Score Evolution Timeline
Line charts showing how category/tag scores change over time.

---

## Implementation Timeline

### Phase 1: Core Tracking (Week 1)
- [ ] Create `user_interactions` table
- [ ] Add middleware to track all actions
- [ ] Store views, clicks, dwell time, positions, shares
- [ ] Basic score update logic

### Phase 2: Scoring Engine (Week 1-2)
- [ ] Implement action weight system
- [ ] Build score calculation formulas
- [ ] Add recency decay scheduler
- [ ] Create personalized ranking algorithm

### Phase 3: Learning Interface (Week 2)
- [ ] User profile viewer
- [ ] Score evolution charts
- [ ] Action impact analyzer
- [ ] Performance dashboard

### Phase 4: Testing & Tuning (Week 2-3)
- [ ] Simulate users with bot interactions
- [ ] Test with real test users
- [ ] Tune weights based on engagement data
- [ ] A/B test personalized vs global

---

## Configuration (Tuning Knobs)

### Action Weights
```python
ACTION_WEIGHTS = {
    'position': 1.00,
    'share': 0.85,
    'comment': 0.75,
    'bookmark': 0.70,
    'dwell_60+': 0.60,
    'return_visit': 0.50,
    'dwell_30-60': 0.45,
    'dwell_15-30': 0.30,
    'view': 0.20,
    'scroll_past': -0.05
}
```

### Score Multipliers
```python
SCORE_MULTIPLIERS = {
    'category': 0.35,
    'people_tag': 0.30,
    'event_tag': 0.30,
    'topic_tag': 0.25,
    'related_topic': 0.20
}
```

### Decay Settings
```python
DECAY_RATE = 0.95          # 5% decay per interval
DECAY_INTERVAL_DAYS = 7    # Apply every 7 days
```

### Personalization Weights
```python
RANKING_WEIGHTS = {
    'belief_intensity': 0.50,
    'user_affinity': 0.45,
    'diversity': 0.05
}

AFFINITY_WEIGHTS = {
    'category_match': 0.4,
    'tag_match': 0.6
}
```

---

## Open Questions for Discussion

1. **Action Weights**: Are these balanced?
   - Should positions be even higher (1.5)?
   - Should comments be weighted less (people spam)?

2. **Decay Rate**: 5% per week appropriate?
   - Faster decay (more reactive to new interests)?
   - Slower decay (more stable preferences)?

3. **Cold Start**: Good balance?
   - More aggressive category sampling?
   - Longer pure-global period?

4. **Diversity Penalty**: Right thresholds?
   - Currently penalizes after 3+ views in 24h
   - Too strict? Too lenient?

5. **Score Scale**: Keep 0-100 or switch to 0-1.0?
   - 0-100 easier to visualize
   - 0-1.0 more flexible for math

6. **Interface Access**: Who sees it?
   - Admin-only for now?
   - Eventually user-facing (view your profile)?

---

## Next Steps

**After Roy's feedback:**
1. Refine weights/parameters based on discussion
2. Implement core tracking system
3. Build scoring engine with decay
4. Create observation interface
5. Test with simulated users
6. Deploy with gradual rollout

**Questions?** Let's iterate on any section!

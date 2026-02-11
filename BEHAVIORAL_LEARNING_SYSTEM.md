# Behavioral Learning System - Detailed Design
**Date:** Feb 11, 2026
**Status:** Design Proposal for Discussion

## Core Principles

### 1. Implicit Learning Only
- **NO user ratings or explicit feedback**
- Everything learned from behavior: views, time, interactions, bets
- System builds user profiles automatically
- Users never see scores or adjust settings

### 2. Action-Based Scoring
Every action updates tag/topic/category scores:
```
View → Small signal (+0.05 per topic/tag)
Time Spent → Medium signal (+0.1 per 30 seconds)
Return Visit → Strong signal (+0.15 per topic/tag)
Bet/Position → Very strong signal (+0.3 per topic/tag)
Share → Very strong signal (+0.25 per topic/tag)
Comment → Strong signal (+0.2 per topic/tag)
```

### 3. Score Decay Over Time
Scores gradually decay to adapt to changing interests:
```python
# Every 7 days, scores decay by 5%
decayed_score = current_score * 0.95

# This means:
# - Recent behavior matters more
# - Old interests fade naturally
# - System adapts to changing preferences
```

---

## Behavioral Signals

### Signal Hierarchy (Strongest to Weakest)

#### 1. **Position Placement (Weight: 1.0)** 🔥
User puts money on a belief = strongest possible signal
- Updates ALL associated tags (+0.30 each)
- Updates market category (+0.35)
- Updates related topics (+0.25 each)
- Creates "co-occurrence" patterns (users who bet on X also bet on Y)

**Example:**
```
User bets on "Will Messi win 2026 World Cup?"
→ Sport category: +0.35
→ Tags: "Messi" +0.30, "World Cup" +0.30, "Soccer" +0.30, "Argentina" +0.30
→ Related topics: "International Sports" +0.25, "Major Tournaments" +0.25
```

#### 2. **Share Action (Weight: 0.85)** 📤
User shares market = strong interest + amplification intent
- Updates tags (+0.25 each)
- Updates category (+0.30)
- Updates topics (+0.20 each)
- Creates "viral affinity" (what users share reveals deep interest)

#### 3. **Comment/Discussion (Weight: 0.75)** 💬
User engages in discussion = intellectual investment
- Updates tags (+0.20 each)
- Updates category (+0.25)
- Updates topics (+0.18 each)

#### 4. **Dwell Time (Weight: 0.60)** ⏱️
Time spent reading/analyzing market
```python
# Engagement thresholds
< 5 seconds:  No signal (bounce)
5-15 seconds: +0.05 (skimmed)
15-30 seconds: +0.10 (read)
30-60 seconds: +0.15 (analyzed)
60+ seconds: +0.20 (deep study)
```

#### 5. **Return Visits (Weight: 0.50)** 🔄
User comes back to same market
- First return: +0.15 per topic/tag
- Second return: +0.10 per topic/tag
- Third+ return: +0.08 per topic/tag (diminishing returns)

#### 6. **Initial View (Weight: 0.20)** 👀
User views market (baseline signal)
- Updates tags (+0.05 each)
- Updates category (+0.08)
- Updates topics (+0.04 each)

#### 7. **Scroll Past (Weight: -0.05)** ⏩
User sees market in feed but doesn't click
- NEGATIVE signal (very small)
- Helps filter out uninteresting topics

---

## Tag & Topic Extraction

### Market Metadata Structure
```json
{
  "market_id": "abc123",
  "title": "Will Messi win 2026 World Cup with Argentina?",
  "category": "Sports",
  "tags": [
    "Messi",
    "World Cup",
    "Soccer",
    "Argentina",
    "International Sports",
    "Major Tournament"
  ],
  "people_tags": ["Messi"],
  "topic_tags": ["World Cup", "Soccer", "International Sports"],
  "location_tags": ["Argentina"],
  "event_tags": ["2026 World Cup"]
}
```

### Tag Types
1. **People Tags**: Individual names (Trump, Messi, Biden, etc.)
2. **Topic Tags**: Themes (crypto, AI, politics, sports, economy)
3. **Category Tags**: Top-level (9 categories: Sports, Politics, etc.)
4. **Location Tags**: Geographic (USA, Europe, Argentina)
5. **Event Tags**: Specific events (2026 World Cup, Election 2024)

---

## Score Calculation Logic

### User-Topic Score Formula
```python
def calculate_topic_score(user_id, topic, interaction_history):
    """
    Calculate affinity score for a topic (0-100 scale)
    """
    base_score = 0.0
    total_interactions = 0
    
    for interaction in interaction_history:
        # Weight by action type
        action_weight = ACTION_WEIGHTS[interaction.type]
        
        # Weight by recency (exponential decay)
        days_ago = (now - interaction.timestamp).days
        recency_weight = math.exp(-days_ago / 30)  # 30-day half-life
        
        # Weight by engagement depth
        if interaction.type == 'dwell':
            depth_weight = min(1.0, interaction.seconds / 60)
        else:
            depth_weight = 1.0
        
        # Composite score update
        delta = action_weight * recency_weight * depth_weight
        base_score += delta
        total_interactions += 1
    
    # Normalize to 0-100 scale with sigmoid
    normalized_score = 100 / (1 + math.exp(-base_score + 5))
    
    # Boost for high interaction count (confidence)
    confidence_boost = min(1.0, total_interactions / 10)
    
    final_score = normalized_score * (0.7 + 0.3 * confidence_boost)
    
    return round(final_score, 2)
```

### Action Weights (Configuration)
```python
ACTION_WEIGHTS = {
    'position': 1.00,      # Bet placed
    'share': 0.85,         # Market shared
    'comment': 0.75,       # Comment posted
    'dwell_60+': 0.60,     # 60+ seconds spent
    'dwell_30': 0.45,      # 30-60 seconds
    'dwell_15': 0.30,      # 15-30 seconds
    'return_visit': 0.50,  # Came back to market
    'view': 0.20,          # Initial view
    'scroll_past': -0.05   # Saw but didn't click
}
```

---

## Personalized Ranking Algorithm

### Feed Ranking Formula
```python
def personalize_feed(user_id, markets):
    """
    Rank markets based on user affinity + belief intensity
    """
    ranked_markets = []
    
    for market in markets:
        # 1. Base score: Belief Intensity (global ranking)
        belief_intensity = calculate_belief_intensity(market)
        
        # 2. User affinity score
        category_score = get_user_score(user_id, 'category', market.category)
        
        tag_scores = [get_user_score(user_id, 'tag', tag) 
                      for tag in market.tags]
        avg_tag_score = sum(tag_scores) / len(tag_scores) if tag_scores else 0
        
        # 3. Composite affinity
        affinity = (
            category_score * 0.4 +
            avg_tag_score * 0.6
        )
        
        # 4. Apply diversity penalty (don't show too much of same category)
        diversity_penalty = calculate_diversity_penalty(user_id, market.category)
        
        # 5. Final personalized score
        personalized_score = (
            belief_intensity * 0.50 +
            affinity * 0.45 +
            diversity_penalty * 0.05
        )
        
        ranked_markets.append({
            'market': market,
            'score': personalized_score,
            'breakdown': {
                'belief_intensity': belief_intensity,
                'affinity': affinity,
                'category_score': category_score,
                'tag_score': avg_tag_score,
                'diversity': diversity_penalty
            }
        })
    
    ranked_markets.sort(key=lambda x: x['score'], reverse=True)
    return ranked_markets
```

### Diversity Penalty
Prevent filter bubbles by penalizing overrepresentation:
```python
def calculate_diversity_penalty(user_id, category):
    """
    Reduce score if user has seen too much of this category recently
    """
    recent_views = get_recent_views(user_id, hours=24)
    category_count = sum(1 for v in recent_views if v.category == category)
    
    # Penalty curve
    if category_count < 3:
        return 1.0  # No penalty
    elif category_count < 5:
        return 0.8  # Small penalty
    elif category_count < 8:
        return 0.6  # Medium penalty
    else:
        return 0.4  # Large penalty (still shown, but deprioritized)
```

---

## Cold Start Problem

### New User Strategy
Users with no history get:
1. **Global ranking** (pure belief intensity) for first 10 views
2. **Rapid learning** from first interactions (2x weight on first 20 actions)
3. **Category sampling** (ensure exposure to all 9 categories in first session)

```python
def get_feed_for_new_user(user_id):
    """
    Special feed strategy for users with < 20 interactions
    """
    markets = get_all_markets()
    
    # First 10 markets: pure global ranking
    global_top = rank_by_belief_intensity(markets)[:10]
    
    # Next 10 markets: one from each category (sampling)
    category_samples = []
    for category in CATEGORIES:
        top_in_category = get_top_market_by_category(category)
        category_samples.append(top_in_category)
    
    return {
        'hero': global_top[0],
        'featured': global_top[1:5],
        'grid': global_top[5:9] + category_samples[:4],
        'stream': category_samples[4:]
    }
```

---

## Learning Interface (Observation Tool)

### Purpose
**NOT for manual intervention**, but for:
- Observing learning patterns
- Understanding user behavior
- Testing algorithm changes
- Debugging scoring issues

### Interface Sections

#### 1. **User Profile Viewer**
```
┌─────────────────────────────────────────┐
│ User: Politics Junkie (user_001)        │
│ Created: 5 days ago | 127 interactions  │
├─────────────────────────────────────────┤
│ TOP CATEGORIES (last 30 days)           │
│  Politics     ████████████████ 87       │
│  Economics    █████████        52       │
│  World        ████              31       │
│  Crime        ███               19       │
├─────────────────────────────────────────┤
│ TOP TAGS (last 30 days)                 │
│  Trump        ████████████████ 92       │
│  Election     ██████████████   81       │
│  Biden        ████████         58       │
│  Deportation  ██████           43       │
├─────────────────────────────────────────┤
│ RECENT ACTIONS (last 24h)               │
│  🔥 BET   "Trump deportation 250K+"     │
│  👀 VIEW  "Biden approval rating"        │
│  ⏱️  30s   "Congress spending bill"      │
│  💬 COMMENT "Will Trump win 2024?"      │
└─────────────────────────────────────────┘
```

#### 2. **Score Evolution Timeline**
```
Politics Category Score (user_001)
100 ┤                               ╭─
 90 ┤                          ╭────╯
 80 ┤                     ╭────╯
 70 ┤               ╭─────╯
 60 ┤          ╭────╯
 50 ┤     ╭────╯
 40 ┤─────╯
    └─────────────────────────────────────
    Jan 1  Jan 10  Jan 20  Jan 30  Feb 10

Events:
• Jan 5: First Trump market bet (+15)
• Jan 12: 3x election market views (+8)
• Jan 20: Shared "Biden speech" (+12)
• Jan 28: 60s dwell on "Congress" (+6)
• Feb 3: Another Trump bet (+10)
```

#### 3. **Action Impact Analyzer**
```
Action: BET on "Will Messi win World Cup?"
User: Sports Fan (user_003)
Time: 2026-02-11 07:00:00

SCORE UPDATES:
Category: Sports
  Before: 78 → After: 88 (+10) ✅

Tags:
  Messi:       42 → 62 (+20) ✅
  World Cup:   35 → 55 (+20) ✅
  Soccer:      58 → 78 (+20) ✅
  Argentina:   12 → 32 (+20) ✅

Topics:
  Int'l Sports:    41 → 56 (+15) ✅
  Major Events:    28 → 43 (+15) ✅

Co-occurrence Created:
  Sports + Entertainment → +0.05
  (user often bets on both)
```

#### 4. **Algorithm Performance Dashboard**
```
┌─────────────────────────────────────────┐
│ PERSONALIZATION METRICS                  │
├─────────────────────────────────────────┤
│ Engagement Rate                          │
│   Personalized: 32.4% ████████          │
│   Global Rank:  18.7% ████              │
│   Lift:         +73%  ✅                │
├─────────────────────────────────────────┤
│ Avg Time Per Market                      │
│   Personalized: 42 sec ████████████     │
│   Global Rank:  28 sec ███████          │
│   Lift:         +50%  ✅                │
├─────────────────────────────────────────┤
│ Return Visit Rate                        │
│   Personalized: 8.2% ████               │
│   Global Rank:  4.1% ██                 │
│   Lift:         +100% ✅                │
└─────────────────────────────────────────┘
```

#### 5. **Tag Co-Occurrence Heatmap**
```
        Trump  Bitcoin  Sports  AI  Ukraine
Trump    100     35      12    18     42
Bitcoin   35    100      08    61     14
Sports    12     08     100    09     11
AI        18     61      09   100     19
Ukraine   42     14      11    19    100

Reading: "Users who engage with Trump markets 
have 42% overlap with Ukraine markets"
```

---

## Implementation Plan

### Phase 1: Core Tracking (Week 1)
- [ ] Implement action tracking middleware
- [ ] Store all interactions in `user_interactions` table
- [ ] Build score update functions
- [ ] Add recency decay scheduler (daily cron)

### Phase 2: Scoring Engine (Week 1-2)
- [ ] Implement action weight system
- [ ] Build user-topic score calculator
- [ ] Add diversity penalty logic
- [ ] Create personalized feed ranker

### Phase 3: Learning Interface (Week 2)
- [ ] User profile viewer page
- [ ] Score evolution timeline charts
- [ ] Action impact analyzer
- [ ] Algorithm performance dashboard
- [ ] Tag co-occurrence heatmap

### Phase 4: Testing & Tuning (Week 2-3)
- [ ] Simulate user behavior (bots)
- [ ] Test algorithm with test users
- [ ] Tune action weights based on results
- [ ] A/B test personalized vs global ranking

---

## Questions for Discussion

1. **Action Weights**: Are the proposed weights appropriate?
   - Should positions be weighted even higher (1.5x)?
   - Should scroll-past penalty be stronger?

2. **Decay Rate**: 5% per week?
   - Too fast (interests change overnight)?
   - Too slow (old interests linger too long)?

3. **Cold Start**: First 10 markets as global ranking?
   - Or aggressive category sampling from the start?

4. **Diversity**: How aggressive should diversity penalty be?
   - Current: 40% penalty after 8 views of same category in 24h
   - More strict? Less strict?

5. **Score Scale**: 0-100 or 0-1.0?
   - Current: 0-100 (easier to visualize)
   - Alternative: 0-1.0 (more flexible for formulas)

6. **Interface Access**: Who should see the learning interface?
   - Admins only?
   - Researchers?
   - Users (view-only their own profile)?

---

## Next Steps

**After this discussion:**
1. Refine weights and parameters based on your feedback
2. Implement core tracking system
3. Build scoring engine
4. Create learning interface
5. Test with simulated users
6. Deploy to production with gradual rollout

**Let's discuss any aspect of this design!**

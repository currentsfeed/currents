# 🧠 BRain Analytics Dashboard - Guide

**URL**: https://brain-analytics.loca.lt  
**Password**: `35.172.150.243`  
**Port**: 5557

---

## 🎯 Purpose

The BRain Analytics Dashboard helps you:
1. **Visualize** market data distributions
2. **Test** personalization strategies
3. **Tune** the ranking algorithm
4. **Understand** scoring breakdowns

---

## 📊 Features

### 1. **Data Visualization**

**Charts included:**
- Category Distribution (bar chart)
- Belief Intensity Distribution (bar chart)
- Volume Distribution (doughnut chart)  
- Probability Distribution (line chart)
- Top Tags (tag cloud)

**Use cases:**
- Understand market diversity
- Identify underrepresented categories
- Spot data quality issues
- Plan category expansions

---

### 2. **Personalization Simulator** 🎯

**How it works:**
Test how different user profiles affect market ranking.

**Inputs:**
- **Preferred Categories**: Select 1+ categories the user likes
- **Preferred Tags**: Select 1+ tags the user follows (trump, ai, deportation, etc.)
- **Volume Preference**: 
  - High: Boosts high-volume markets (>50K)
  - Medium: No bias
  - Low: Boosts low-volume markets (<20K)
- **Contestedness Preference**:
  - High: Boosts 50/50 markets (contested beliefs)
  - Medium: No bias
  - Low: Boosts clear winner markets (90/10)

**Output:**
- Top 20 personalized markets
- Personalized score vs base belief intensity
- See which markets got boosted/demoted

**Example use cases:**

**Scenario 1: Politics enthusiast**
```
Categories: Politics, Economics
Tags: trump, biden, election
Volume: High
Contestedness: High
→ Result: Highly-traded political races with uncertain outcomes
```

**Scenario 2: Niche AI investor**
```
Categories: Technology, Crypto
Tags: ai, gaming
Volume: Low
Contestedness: Medium
→ Result: Smaller AI/gaming markets others missed
```

**Scenario 3: Sports bettor**
```
Categories: Sports
Tags: (none)
Volume: High
Contestedness: High
→ Result: Big sports events with competitive odds
```

---

### 3. **Algorithm Playground** 🔬

**How it works:**
Adjust the weights in the belief intensity formula and see how rankings change.

**Current formula:**
```
belief_intensity = (volume_score × 0.6) + (contestedness × 0.4)

Where:
  volume_score = volume_24h / 10000
  contestedness = 1 - |0.5 - probability| × 2
```

**Interactive sliders:**
- **Volume Weight**: 0.0 - 1.0 (default: 0.6)
- **Contestedness Weight**: 0.0 - 1.0 (default: 0.4)

**Experiments to try:**

**Experiment 1: Pure volume ranking**
```
Volume Weight: 1.0
Contestedness Weight: 0.0
→ Result: Biggest markets rise to top (like Polymarket homepage)
```

**Experiment 2: Pure contestedness ranking**
```
Volume Weight: 0.0
Contestedness Weight: 1.0
→ Result: Most uncertain markets rise (50/50 battles)
```

**Experiment 3: Balanced**
```
Volume Weight: 0.5
Contestedness Weight: 0.5
→ Result: Equal weight to size and uncertainty
```

**Experiment 4: Volume-heavy**
```
Volume Weight: 0.8
Contestedness Weight: 0.2
→ Result: Favor popular markets, still surface some interesting contests
```

**Use cases:**
- Test different philosophies (volume vs engagement)
- Find optimal weights for your audience
- Discover hidden gems with low weight on volume
- Simulate what competitors might rank

---

### 4. **Market Scoring Breakdown** (API)

**Endpoint:** `GET /api/market-breakdown/<market_id>`

**Returns:**
```json
{
  "market": {
    "market_id": "517311",
    "title": "Will Trump deport 250,000-500,000 people?",
    "category": "Politics",
    "tags": ["trump", "deportation", "legal"]
  },
  "scoring": {
    "volume_24h": 375000,
    "volume_score": 37.5,
    "volume_contribution": 22.5,
    "probability": 0.90,
    "contestedness": 0.2,
    "contestedness_contribution": 0.08,
    "belief_intensity": 22.58
  },
  "metadata": {
    "participant_count": 2368,
    "created_at": "2025-12-14T..."
  }
}
```

**Use case:**
- Debug why a specific market ranks high/low
- Understand scoring components
- Build explanations for users ("This market ranks high because...")

---

## 💡 Personalization Strategy Development

### Step 1: Understand the Data
1. Open https://brain-analytics.loca.lt
2. Review all 4 distribution charts
3. Note which categories/tags are most common
4. Identify gaps in coverage

### Step 2: Define User Personas
Think about your target users:

**Persona: Crypto Trader**
- Categories: Crypto, Economics, Technology
- Tags: ai, revenue, budget
- Volume: High (wants liquid markets)
- Contestedness: Medium

**Persona: Political Analyst**
- Categories: Politics, Crime
- Tags: trump, biden, election
- Volume: Medium
- Contestedness: High (loves uncertainty)

**Persona: Pop Culture Fan**
- Categories: Entertainment, Sports
- Tags: (none, general interest)
- Volume: Medium
- Contestedness: Medium

### Step 3: Test Personas
1. Use Personalization Simulator
2. Input persona preferences
3. Review results
4. Refine preferences based on output quality

### Step 4: Implement Logic
Once you find combinations that work:

**Add to `app.py` or new `personalization.py`:**
```python
def get_personalized_feed(user_profile):
    """
    user_profile = {
        'categories': ['Politics', 'Economics'],
        'tags': ['trump', 'ai'],
        'volume_preference': 'high',
        'contestedness_preference': 'medium'
    }
    """
    markets = brain.get_all_markets()
    
    for market in markets:
        score = market['belief_intensity']
        
        # Category boost
        if market['category'] in user_profile['categories']:
            score *= 1.5
        
        # Tag boost
        user_tags = set(user_profile['tags'])
        market_tags = set(market['tags'])
        overlap = len(user_tags & market_tags)
        if overlap > 0:
            score *= (1 + overlap * 0.3)
        
        # Volume/contestedness preferences
        # ... (see brain_analytics.py for full logic)
        
        market['personalized_score'] = score
    
    markets.sort(key=lambda x: x['personalized_score'], reverse=True)
    return markets[:20]
```

---

## 🧪 A/B Testing Framework

**Goal:** Compare personalized vs standard feed

**Approach 1: Manual comparison**
1. Get standard ranking (current homepage)
2. Run personalization for User Profile A
3. Compare top 10 results
4. Note differences

**Approach 2: Track user engagement**
```python
# Add to user_interactions table
cursor.execute("""
    INSERT INTO user_interactions 
    (user_id, market_id, interaction_type, feed_type, timestamp)
    VALUES (?, ?, 'click', ?, ?)
""", (user_id, market_id, 'personalized', datetime.now()))
```

**Metrics to track:**
- Click-through rate (personalized vs standard)
- Time spent per market
- Position placed per market viewed
- Scroll depth

---

## 🚀 Next Steps

### Short-term (Demo)
1. ✅ Use analytics to understand current data
2. ✅ Test 3-5 user personas
3. ⬜ Document best personalization settings
4. ⬜ Add simple personalization (1-2 categories) to demo

### Medium-term (Post-demo)
1. Add user interaction tracking
2. Implement collaborative filtering
3. A/B test personalized feed
4. Build user preference UI (let users pick categories)

### Long-term (Production)
1. ML-based personalization
2. Real-time learning from user behavior
3. Content-based + collaborative filtering
4. Explanation UI ("Why this market?" tooltips)

---

## 📞 API Reference

### GET /api/personalize
Test personalization with user profile

**Request:**
```bash
curl -X POST https://brain-analytics.loca.lt/api/personalize \\
  -H "Content-Type: application/json" \\
  -d '{
    "categories": ["Politics", "Economics"],
    "tags": ["trump", "ai"],
    "volume_preference": "high",
    "contestedness_preference": "medium",
    "limit": 20
  }'
```

**Response:**
```json
{
  "markets": [...],
  "profile": {...},
  "total": 100
}
```

---

### GET /api/algorithm-test
Test different algorithm weights

**Request:**
```bash
curl -X POST https://brain-analytics.loca.lt/api/algorithm-test \\
  -H "Content-Type: application/json" \\
  -d '{
    "volume_weight": 0.8,
    "contested_weight": 0.2,
    "limit": 20
  }'
```

**Response:**
```json
{
  "markets": [...],
  "weights": {
    "volume": 0.8,
    "contested": 0.2
  },
  "total": 100
}
```

---

### GET /api/market-breakdown/<market_id>
Get detailed scoring breakdown

**Request:**
```bash
curl https://brain-analytics.loca.lt/api/market-breakdown/517311
```

**Response:**
```json
{
  "market": {...},
  "scoring": {
    "volume_24h": 375000,
    "volume_score": 37.5,
    "volume_contribution": 22.5,
    "probability": 0.90,
    "contestedness": 0.2,
    "contestedness_contribution": 0.08,
    "belief_intensity": 22.58
  },
  "metadata": {...}
}
```

---

## 🎓 Tips & Best Practices

1. **Start broad, then narrow**
   - Test with no filters first
   - Add 1-2 categories
   - Then add specific tags

2. **Balance personalization strength**
   - Too weak: Same results as standard feed
   - Too strong: Echo chamber (only sees politics)
   - Sweet spot: 1.5x category boost, 1.3x tag boost

3. **Consider user intent**
   - Discovery mode: Lower personalization
   - Focus mode: Higher personalization

4. **Test edge cases**
   - User with no preferences (new user)
   - User who likes everything (power user)
   - User with conflicting preferences (Sports + Politics)

5. **Monitor data quality**
   - Are tags accurate?
   - Are categories balanced?
   - Is volume data fresh?

---

**Questions? Feature requests? Let's iterate! 🚀**

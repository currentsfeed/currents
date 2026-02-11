# 🧠 Personalized Learning - How Currents Learns Your Preferences

## Overview

Currents uses **collaborative filtering** and **content-based filtering** to learn what types of markets interest you. The more you interact, the smarter your feed becomes.

## How It Works

### 1. 📊 Tracking Your Interactions

Every time you interact with a market, we record:

**Interaction Types**:
- **View** - You saw a market card
- **Click** - You opened the market detail page
- **Time Spent** - How long you stayed on a page
- **Position Taken** - You placed a bet/prediction

**Data Captured** (in `user_interactions` table):
```sql
CREATE TABLE user_interactions (
    interaction_id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,              -- Your unique identifier
    market_id TEXT NOT NULL,            -- Which market you interacted with
    interaction_type TEXT NOT NULL,     -- 'view', 'click', 'position', etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT                       -- Extra context (time spent, etc.)
)
```

**Example**:
```
User: roy_123
Market: "Russia-Ukraine Ceasefire before GTA VI?"
Action: clicked
Time: 2026-02-10 05:15:00
Duration: 45 seconds
```

### 2. 🎯 Content-Based Filtering

We analyze **what** you interact with:

**Market Attributes**:
- **Category**: Politics, Crypto, Sports, World, Technology, etc.
- **Tags**: Specific topics (ukraine, bitcoin, nfl, trump, etc.)
- **Probability Range**: Do you prefer close races (45-55%) or clear winners?
- **Volume**: High-liquidity markets vs niche topics
- **Market Type**: Binary (Yes/No) vs Multi-option
- **Contestedness**: How divided is the crowd?

**Your Preference Profile**:
```python
{
    "categories": {
        "World": 0.35,      # 35% of your clicks are World events
        "Politics": 0.30,   # 30% Politics
        "Crypto": 0.20,     # 20% Crypto
        "Sports": 0.15      # 15% Sports
    },
    "probability_sweet_spot": 0.45,  # You engage most with 40-50% markets
    "volume_preference": "high",      # You prefer high-volume markets
    "contestedness_preference": 0.7   # You like contested markets
}
```

### 3. 🤝 Collaborative Filtering

We find **users like you** and recommend what they engage with:

**How It Works**:
1. Build a matrix of users × markets
2. Find users with similar interaction patterns
3. Recommend markets they liked that you haven't seen

**Example**:
```
You (roy_123):        [1, 0, 1, 0, 1]  (markets you clicked)
Similar user:         [1, 1, 1, 0, 1]
Recommendation:       market #2 (they clicked, you didn't)
```

**User Similarity**:
- Users who click the same markets as you
- Users with similar category preferences
- Users with similar probability preferences

### 4. 🔮 Personalized Ranking

Your feed is re-ranked based on your profile:

**Default BRain Score**:
```python
belief_intensity = volume_score * 0.6 + contestedness * 0.4
```

**Your Personalized Score**:
```python
personalized_score = (
    belief_intensity * 0.4 +           # Base BRain signal
    category_match * 0.3 +              # How much you like this category
    collaborative_signal * 0.2 +        # Similar users' engagement
    recency_boost * 0.1                # Recent topics you've shown interest in
)
```

**Adjustments**:
- ✅ **Boost**: Markets in your preferred categories
- ✅ **Boost**: Markets similar users engaged with
- ✅ **Boost**: Markets with your preferred probability range
- ⬇️ **Demote**: Categories you consistently skip
- ⬇️ **Demote**: Markets you've already seen (freshness)

## Current Status

### Database Schema

**user_interactions** table schema:
```sql
sqlite3 brain.db "PRAGMA table_info(user_interactions);"
```

*Note: This table may not exist yet - it will be created when tracking is implemented.*

### What's Implemented

✅ **Markets Database**: 100 fresh Polymarket markets  
✅ **Categories**: Automatic categorization (World, Politics, Crypto, etc.)  
✅ **Tags**: Multiple tags per market  
✅ **BRain Algorithm**: Base ranking by belief intensity  
✅ **Database Viewer**: Inspect all data in real-time

### What's Coming

🔜 **User Tracking**: Record views, clicks, time spent  
🔜 **Preference Analysis**: Build your content profile  
🔜 **Collaborative Signals**: Find similar users  
🔜 **Personalized Feed**: Custom-ranked markets for you  
🔜 **A/B Testing**: Measure personalization quality

## How to Enable Tracking

### Step 1: Create User Interactions Table

```sql
CREATE TABLE IF NOT EXISTS user_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    market_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL,  -- 'view', 'click', 'position', 'share'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    device TEXT,
    duration_seconds INTEGER,
    metadata TEXT,  -- JSON for extra data
    FOREIGN KEY (market_id) REFERENCES markets (market_id)
);

CREATE INDEX idx_user_interactions_user ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_market ON user_interactions(market_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp);
```

### Step 2: Track Frontend Interactions

Add JavaScript to track:
```javascript
// Track view
window.addEventListener('load', () => {
    fetch('/api/track', {
        method: 'POST',
        body: JSON.stringify({
            user_id: getUserId(),
            market_id: getMarketId(),
            interaction_type: 'view',
            timestamp: new Date().toISOString()
        })
    });
});

// Track click
marketCard.addEventListener('click', () => {
    fetch('/api/track', {
        method: 'POST',
        body: JSON.stringify({
            user_id: getUserId(),
            market_id: market.id,
            interaction_type: 'click'
        })
    });
});
```

### Step 3: Build User Profile

```python
def get_user_profile(user_id):
    """Analyze user's interaction history"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get category preferences
    cursor.execute("""
        SELECT m.category, COUNT(*) as interactions
        FROM user_interactions ui
        JOIN markets m ON ui.market_id = m.market_id
        WHERE ui.user_id = ?
        GROUP BY m.category
        ORDER BY interactions DESC
    """, (user_id,))
    
    categories = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Get probability preferences
    cursor.execute("""
        SELECT AVG(m.probability) as avg_prob
        FROM user_interactions ui
        JOIN markets m ON ui.market_id = m.market_id
        WHERE ui.user_id = ?
    """, (user_id,))
    
    avg_probability = cursor.fetchone()[0]
    
    return {
        'categories': categories,
        'probability_sweet_spot': avg_probability
    }
```

### Step 4: Personalize Feed

```python
def get_personalized_feed(user_id):
    """Get markets ranked for this specific user"""
    profile = get_user_profile(user_id)
    markets = get_all_markets()
    
    for market in markets:
        # Base BRain score
        score = calculate_belief_intensity(market)
        
        # Category boost
        if market.category in profile['categories']:
            category_boost = profile['categories'][market.category] / 100
            score *= (1 + category_boost)
        
        # Probability preference
        prob_distance = abs(market.probability - profile['probability_sweet_spot'])
        if prob_distance < 0.1:
            score *= 1.2  # 20% boost for sweet spot
        
        market['personalized_score'] = score
    
    # Sort by personalized score
    markets.sort(key=lambda x: x['personalized_score'], reverse=True)
    return markets
```

## Example Queries

### See Your Interaction History
```sql
SELECT 
    ui.timestamp,
    ui.interaction_type,
    m.title as market_title,
    m.category
FROM user_interactions ui
JOIN markets m ON ui.market_id = m.market_id
WHERE ui.user_id = 'roy_123'
ORDER BY ui.timestamp DESC
LIMIT 20;
```

### Your Top Categories
```sql
SELECT 
    m.category,
    COUNT(*) as interactions,
    AVG(m.probability) as avg_probability
FROM user_interactions ui
JOIN markets m ON ui.market_id = m.market_id
WHERE ui.user_id = 'roy_123'
GROUP BY m.category
ORDER BY interactions DESC;
```

### Markets Similar Users Liked
```sql
-- Users similar to you
WITH similar_users AS (
    SELECT DISTINCT ui2.user_id
    FROM user_interactions ui1
    JOIN user_interactions ui2 
        ON ui1.market_id = ui2.market_id 
        AND ui1.user_id != ui2.user_id
    WHERE ui1.user_id = 'roy_123'
    GROUP BY ui2.user_id
    HAVING COUNT(*) > 3  -- At least 3 markets in common
)
-- What they engaged with that you haven't
SELECT 
    m.title,
    m.category,
    COUNT(DISTINCT ui.user_id) as similar_user_count
FROM user_interactions ui
JOIN markets m ON ui.market_id = m.market_id
WHERE ui.user_id IN (SELECT user_id FROM similar_users)
  AND ui.market_id NOT IN (
      SELECT market_id FROM user_interactions WHERE user_id = 'roy_123'
  )
GROUP BY m.market_id
ORDER BY similar_user_count DESC
LIMIT 10;
```

## Privacy & Data

**What We Track**:
- Market views and clicks (anonymous user ID)
- Time spent on pages
- Categories engaged with
- Interaction patterns

**What We DON'T Track**:
- Personal information beyond user ID
- Position amounts or wallet balances
- Any off-platform behavior

**Data Retention**:
- Interactions stored for personalization
- Can be deleted on request
- Used only for improving your feed

## Testing Personalization

### Simulate User Behavior
```python
# Add fake interactions for testing
def simulate_user(user_id, preferences):
    """Generate realistic interaction history"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get markets matching preferences
    for category in preferences['favorite_categories']:
        cursor.execute("""
            SELECT market_id FROM markets
            WHERE category = ?
            ORDER BY RANDOM()
            LIMIT 5
        """, (category,))
        
        for (market_id,) in cursor.fetchall():
            cursor.execute("""
                INSERT INTO user_interactions (user_id, market_id, interaction_type)
                VALUES (?, ?, 'click')
            """, (user_id, market_id))
    
    conn.commit()
```

### A/B Test
```python
# Compare personalized vs non-personalized feed
def ab_test(user_id):
    standard_feed = get_brain_feed()  # Default BRain ranking
    personalized_feed = get_personalized_feed(user_id)  # Your custom feed
    
    # Show which markets moved up/down
    for i, market in enumerate(personalized_feed[:10]):
        standard_rank = standard_feed.index(market)
        print(f"{market.title}: #{standard_rank} → #{i} ({'↑' if standard_rank > i else '↓'})")
```

## Next Steps

1. **Implement Tracking**: Add frontend JavaScript to record interactions
2. **Create User Profiles**: Analyze interaction patterns
3. **Build Recommender**: Use collaborative filtering
4. **Test & Iterate**: Measure engagement lift
5. **Privacy Controls**: Let users opt-out or reset preferences

---

**Ready to start tracking?** The database schema is ready, the algorithm framework exists, and the foundation is solid. Just need to connect the dots!

*Last updated: 2026-02-10*

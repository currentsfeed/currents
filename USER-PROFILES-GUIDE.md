# 👥 BRain User Profiles - Guide

**Feature**: User scoring and preference tracking for personalization  
**Access**: https://brain-analytics.loca.lt/users  
**Password**: `35.172.150.243`

---

## 🎯 Purpose

The User Profiles system tracks individual user preferences and scoring across:
- **Categories** (Politics, Sports, Crypto, etc.)
- **Tags** (trump, ai, gaming, etc.)
- **Behavioral preferences** (volume, contestedness)

This data powers the personalization engine to surface relevant markets for each user.

---

## 📊 Test Users (6 Profiles)

### 1. **Politics Junkie** (user_001)
**Categories:**
- Politics: 0.95
- Economics: 0.60
- Crime: 0.40

**Tags:**
- trump: 0.90
- biden: 0.75
- election: 0.85
- deportation: 0.70

**Preferences:**
- Volume: High (0.9)
- Contestedness: High (0.9)

**Profile**: Loves political markets, especially contested races. Prefers high-volume, uncertain outcomes.

---

### 2. **Crypto Trader** (user_002)
**Categories:**
- Crypto: 0.95
- Technology: 0.80
- Economics: 0.70

**Tags:**
- ai: 0.85
- gaming: 0.60
- revenue: 0.75
- budget: 0.50

**Preferences:**
- Volume: High (0.9)
- Contestedness: Medium (0.5)

**Profile**: Crypto enthusiast who also follows tech/AI. Wants liquid markets.

---

### 3. **Sports Fan** (user_003)
**Categories:**
- Sports: 0.90
- Entertainment: 0.65
- Technology: 0.30

**Tags:**
- basketball: 0.85
- gaming: 0.70

**Preferences:**
- Volume: Medium (0.5)
- Contestedness: High (0.9)

**Profile**: Sports bettor who loves close games and upsets.

---

### 4. **Tech Enthusiast** (user_004)
**Categories:**
- Technology: 0.95
- Crypto: 0.70
- Economics: 0.50

**Tags:**
- ai: 0.95
- gaming: 0.80
- revenue: 0.60

**Preferences:**
- Volume: Medium (0.5)
- Contestedness: Medium (0.5)

**Profile**: Deeply interested in AI and tech trends. Balanced approach.

---

### 5. **Balanced Investor** (user_005)
**Categories:**
- Economics: 0.80
- Politics: 0.70
- Crypto: 0.60
- Technology: 0.65

**Tags:**
- trump: 0.55
- ai: 0.70
- budget: 0.80
- revenue: 0.75

**Preferences:**
- Volume: High (0.9)
- Contestedness: Low (0.3)

**Profile**: Diversified interests, prefers clear winners in high-volume markets.

---

### 6. **Pop Culture Watcher** (user_006)
**Categories:**
- Entertainment: 0.95
- Sports: 0.60
- Culture: 0.80

**Tags:**
- gaming: 0.75
- rihanna: 0.85

**Preferences:**
- Volume: Low (0.3)
- Contestedness: Medium (0.5)

**Profile**: Follows entertainment and culture. Less interested in high-volume markets.

---

## 🎨 UI Features

### User List Page (`/users`)
- Grid view of all users
- Displays name, user_id, last active
- Click to view detailed profile
- Navigation to analytics dashboard

### User Detail Page (`/users/<user_id>`)

**Sections:**
1. **Header**
   - User avatar (first letter)
   - Display name and ID
   - Last active timestamp

2. **Category Preferences**
   - Bar chart visualization
   - Score (0.0-1.0)
   - Interaction count
   - Last updated date

3. **Tag Preferences**
   - Bar chart visualization
   - Tag badges with scores
   - Sorted by score (highest first)

4. **Behavioral Preferences**
   - Volume preference (low/medium/high)
   - Contestedness preference (clear winners vs 50/50)
   - Visual indicators

5. **Charts**
   - Polar area chart (categories)
   - Horizontal bar chart (tags)
   - Interactive with Chart.js

6. **Actions**
   - Test Personalization button
   - Link to analytics dashboard
   - Back to user list

---

## 🔧 API Endpoints

### GET /api/users
List all users

**Response:**
```json
{
  "users": [
    {
      "user_id": "user_001",
      "display_name": "Politics Junkie",
      "created_at": "2026-02-10T...",
      "last_active": "2026-02-10T..."
    }
  ],
  "total": 6
}
```

---

### GET /api/users/<user_id>
Get detailed user profile

**Response:**
```json
{
  "user_id": "user_001",
  "display_name": "Politics Junkie",
  "scores": {
    "category": [
      {
        "topic": "Politics",
        "score": 0.95,
        "interactions": 0,
        "last_updated": "2026-02-10T..."
      }
    ],
    "tag": [
      {
        "topic": "trump",
        "score": 0.90,
        "interactions": 0,
        "last_updated": "2026-02-10T..."
      }
    ],
    "preference": [
      {
        "topic": "volume",
        "score": 0.9,
        "interactions": 0,
        "last_updated": "2026-02-10T..."
      }
    ]
  },
  "recent_interactions": []
}
```

---

### POST /api/users/<user_id>/update-score
Update user topic score

**Request:**
```json
{
  "topic_type": "category",
  "topic_value": "Politics",
  "delta": 0.1
}
```

**Response:**
Updated user profile (same as GET)

---

## 💡 Use Cases

### 1. Understanding User Behavior
**Question**: "Who are my most engaged users?"
- Sort by interaction count
- View category distribution
- Identify power users

### 2. Testing Personalization
**Question**: "Will this user like this market?"
- Check user's category scores
- Match against market category/tags
- Calculate personalized score

### 3. Building User Segments
**Question**: "How many crypto traders do we have?"
- Filter users by category scores
- Create segments: crypto_score > 0.7
- Target with specific features

### 4. Improving Recommendations
**Question**: "Why did this user not engage?"
- Compare user preferences vs shown markets
- Identify mismatches
- Tune personalization weights

---

## 🔬 Scoring System

### Score Range: 0.0 - 1.0
- **0.0**: No interest
- **0.3**: Low interest
- **0.5**: Moderate interest
- **0.7**: High interest
- **1.0**: Maximum interest

### Score Updates
Scores increase with interactions:
```python
new_score = min(1.0, current_score + delta)
```

Default delta: **0.1** per interaction

### Interaction Types
- **view**: Market page view
- **click**: Market card click
- **position**: Position placed
- **share**: Market shared
- **comment**: Market discussion

Each interaction type can have different delta values.

---

## 🚀 Future Enhancements

### Short-term
1. **Real interaction tracking**
   - Hook up to frontend
   - Track clicks, views, positions
   - Update scores in real-time

2. **Interaction history**
   - Show last 20 interactions per user
   - Timestamp, market, action
   - Link to markets

3. **Score decay**
   - Reduce scores over time if no interactions
   - Keep profiles fresh
   - Prevent stale preferences

### Medium-term
1. **Collaborative filtering**
   - Find similar users
   - Recommend based on similar profiles
   - "Users like you also liked..."

2. **A/B testing**
   - Control group vs personalized
   - Measure engagement lift
   - Optimize weights

3. **User controls**
   - Let users set preferences
   - Adjust category weights
   - Opt out of tracking

### Long-term
1. **Machine learning**
   - Train recommendation model
   - Predict user preferences
   - Dynamic weight tuning

2. **Real-time personalization**
   - Update feed as user browses
   - Learn from session behavior
   - Instant feedback loop

---

## 🧪 Testing Workflow

### 1. Browse Users
```
Visit: https://brain-analytics.loca.lt/users
See 6 test user profiles
Click on any user
```

### 2. View Profile
```
Click: "Politics Junkie"
See all scores: Categories, Tags, Preferences
View charts: Polar area + bar charts
```

### 3. Test Personalization
```
Click: "Test Personalization" button
Returns to main analytics
Runs personalization with user's preferences
Shows ranked markets for that profile
```

### 4. Compare Users
```
Open multiple tabs
View different user profiles
Compare scoring patterns
Identify user segments
```

### 5. API Testing
```bash
# Get all users
curl https://brain-analytics.loca.lt/api/users | jq

# Get specific user
curl https://brain-analytics.loca.lt/api/users/user_001 | jq

# Update score
curl -X POST https://brain-analytics.loca.lt/api/users/user_001/update-score \\
  -H "Content-Type: application/json" \\
  -d '{"topic_type": "category", "topic_value": "Politics", "delta": 0.1}'
```

---

## 📐 Database Schema

### `user_profiles`
```sql
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    display_name TEXT,
    created_at TEXT,
    last_active TEXT,
    profile_data TEXT  -- JSON blob
);
```

### `user_topic_scores`
```sql
CREATE TABLE user_topic_scores (
    user_id TEXT,
    topic_type TEXT,     -- 'category', 'tag', 'preference'
    topic_value TEXT,    -- 'Politics', 'trump', 'volume'
    score REAL,          -- 0.0 - 1.0
    interactions INTEGER DEFAULT 0,
    last_updated TEXT,
    PRIMARY KEY (user_id, topic_type, topic_value)
);
```

### `user_interactions`
```sql
CREATE TABLE user_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    market_id TEXT,
    interaction_type TEXT,  -- 'view', 'click', 'position'
    timestamp TEXT,
    metadata TEXT  -- JSON blob
);
```

---

## 🎯 Key Metrics

### User Engagement
- Total users
- Active users (last 7 days)
- Avg interactions per user
- Top categories by user count

### Personalization Quality
- Click-through rate (personalized vs standard)
- Position rate (personalized vs standard)
- Time on page (personalized vs standard)
- Return rate

### Scoring Distribution
- Avg score per category
- Users with high scores (>0.7)
- Users with balanced scores (<0.3 diff)
- Users with single focus (1 category >0.8)

---

**Created**: 2026-02-10  
**Feature**: User profiles and scoring system for personalization  
**Status**: Live with 6 test users

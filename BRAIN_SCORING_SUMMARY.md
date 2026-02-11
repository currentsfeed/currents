# BRain Scoring System Summary
**Date:** Feb 11, 2026 07:07 UTC

## Current Scoring System

### Market Ranking (Belief Intensity)
```python
belief_intensity = volume_score * 0.6 + contestedness * 0.4
```

**Components:**
- **Volume Score** (60% weight): Logarithmic scoring of 24h trading volume
  - Scaled 0-100 based on market activity
  - Higher volume = more belief signals
  
- **Contestedness** (40% weight): How divided opinions are
  - Binary markets: Closeness to 50/50 split
  - Multi-option markets: Entropy across all options
  - More contested = more interesting

### User Affinity Scoring (Personalization)
Currently in `user_profiles.py` with 6 test users:

**User Profile Structure:**
```python
{
    "user_id": "user_001",
    "name": "Politics Junkie",
    "category_scores": {
        "Politics": 95,
        "Economics": 70,
        "World": 60,
        ...
    },
    "tag_scores": {
        "Trump": 90,
        "Congress": 85,
        ...
    },
    "historical_interactions": [
        {
            "market_id": "...",
            "action": "view|bet|share",
            "timestamp": "...",
            "engagement_seconds": 120
        }
    ]
}
```

**Personalization Formula:**
```python
# For each market, calculate user affinity
affinity_score = (
    category_match * 0.4 +
    tag_match * 0.3 +
    historical_pattern * 0.3
)

# Final personalized ranking
personalized_score = belief_intensity * 0.5 + affinity_score * 0.5
```

### Content Scoring (Not Yet Implemented)
Ideas for content quality scoring:
1. **Editorial Quality**: Has description, verified sources
2. **Image Quality**: Real photos vs AI-generated
3. **Market Liquidity**: Sufficient betting pool
4. **Time Relevance**: Resolution date proximity
5. **Social Engagement**: Comments, shares, saves

### Tag Affinity System
**Current Tags:**
- **People Tags**: Individual names (Trump, Messi, Djokovic, etc.)
- **Topic Tags**: Broader themes (cryptocurrency, sports, politics, etc.)
- **Category Tags**: 9 main categories (Sports, Politics, Crypto, etc.)

**User-Tag Scoring:**
```python
# Explicit scores (user preferences)
user.tag_scores["Trump"] = 90

# Implicit scores (learned from behavior)
# If user views 5 Trump markets:
inferred_score = avg_engagement_time * frequency * recency_weight
```

## Database Tables
### markets
- market_id, title, description, category
- probability, volume_24h, created_at, resolution_date
- image_url, editorial_description
- market_type (binary/multiple), top_options (JSON)

### users
- user_id, name, email, created_at
- preferences (JSON: category/tag scores)

### user_interactions
- user_id, market_id, action_type, timestamp
- engagement_seconds, position_size

### user_tag_affinity
- user_id, tag_name, tag_type (person/topic/category)
- affinity_score (0-100)
- last_updated

### trending_cache
- market_id, belief_intensity, rank
- updated_at, cache_ttl

## Next Steps for Roy's Scoring System
1. **Content Quality Scoring**:
   - Rate markets based on editorial descriptions
   - Image quality (professional photos vs AI)
   - Verified sources
   - Market liquidity thresholds

2. **Tag Affinity Learning**:
   - Track which tags user engages with
   - Build implicit preference scores
   - Weight by recency and engagement depth

3. **Cross-Tag Patterns**:
   - "Users who like X also like Y"
   - Category co-occurrence patterns
   - Tag clustering

4. **Scoring Dashboard**:
   - Visualize user profiles
   - Show tag affinity distributions
   - Test personalization algorithms
   - A/B test different weight combinations

## Questions for Roy
1. Do you need the full 50-page BRain spec again?
2. What specific scoring dimensions do you want to prioritize?
   - Content quality?
   - User-tag affinity?
   - Cross-market patterns?
3. Should scoring be:
   - Explicit (users rate content/tags)?
   - Implicit (learned from behavior)?
   - Hybrid?
4. Do you want a scoring admin interface in the database viewer?

## Files
- `brain.py` - Core BRain class with ranking logic
- `user_profiles.py` - User affinity data and test profiles
- `db_viewer.py` - Database viewer on port 5556
- `analytics_dashboard.py` - Analytics on port 5557 (distribution charts)
- `brain.db` - SQLite database (156 markets, 6 test users)

## Access
- **Database Viewer**: https://proliferative-daleyza-benthonic.ngrok-free.dev/brain-viewer
  - Username: admin
  - Password: demo2026
- **Main Site**: https://proliferative-daleyza-benthonic.ngrok-free.dev

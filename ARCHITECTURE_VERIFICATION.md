# Architecture Verification for Team Handoff

**Date:** 2026-02-13  
**Status:** ✅ Production-Ready  
**Demo:** https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## ✅ Confirmed: Data Structure & Architecture

### 1. Data Source

**Current Setup:**
- **326 real Polymarket markets** stored in local SQLite database (`brain.db`)
- Markets scraped from Polymarket using their API
- Data structure follows **Rain Protocol** format (ready for future integration)

**Config Toggle (`config.py`):**
```python
USE_RAIN_API = False  # Currently using local DB
RAIN_API_URL = 'http://localhost:5000/api/v1'  # Mock Rain API (port 5000)
```

**When USE_RAIN_API = True:**
- Fetches markets from Rain Protocol API
- `rain_client.py` converts Rain data to BRain format
- Currently using **mock Rain API** (`rain_api_mock.py`) for development

### 2. BRain Personalization Algorithm

**✅ CONFIRMED: BRain is running for personalization**

**Location:** `personalization.py`

**Algorithm (from 50-page spec):**
```python
# Belief Intensity (core ranking)
belief_intensity = volume_score * 0.6 + contestedness * 0.4

# Final Score (with personalization)
final_score = (
    belief_intensity +
    TRENDING_WEIGHT * trending_score +
    RISING_WEIGHT * rising_score +
    PERSONAL_WEIGHT * personal_score +
    news_boost +
    sports_boost
)
```

**Components:**
1. **Belief Intensity** - Volume (60%) + Contestedness (40%)
2. **Trending Score** - Recent engagement (85% interest + 15% volume)
3. **Rising Score** - Velocity of change
4. **Personal Score** - User's tag affinity (learned from interactions)
5. **News Boost** - Fresh news items prioritized
6. **Sports Boost** - Upcoming games (next 2-3 days)

### 3. Database Schema

**✅ CONFIRMED: Follows BRain spec**

**Tables:**
- `markets` - Market data (Rain Protocol compatible)
- `market_options` - Multi-option market outcomes
- `market_tags` - People tags (trump, musk) + topic tags (ai, crypto)
- `market_history` - Probability evolution over time
- `users` - User profiles
- `interactions` - User engagement tracking
- `user_profiles` - Learned preferences (tag-level)
- `trending_cache` - Computed trending scores
- `geography_tracking` - Location-based trending

**Market Schema (Rain-compatible):**
```sql
CREATE TABLE markets (
    market_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    probability REAL,
    volume_24h REAL,
    volume_total REAL,
    image_url TEXT,
    created_at TEXT,
    resolution_date TEXT,
    status TEXT DEFAULT 'open',
    market_type TEXT DEFAULT 'binary',
    editorial_description TEXT
);
```

### 4. Data Flow

```
Polymarket API
    ↓
Local DB (brain.db) ← 326 markets
    ↓
Personalization Engine (personalization.py)
    ├─ Belief Intensity (BRain algorithm)
    ├─ Trending Score (compute_trending.py)
    ├─ Personal Score (user_profiles table)
    └─ Category Diversity (max 3 per category in top 9)
    ↓
Flask API (app.py)
    ├─ Desktop: index-v2.html (grid layout)
    └─ Mobile: feed_mobile.html (TikTok feed)
    ↓
User Interaction
    ↓
Tracking (tracking_engine.py)
    ↓
Update user_profiles (tag-level learning)
```

### 5. Key Features Implemented

**✅ BRain Personalization:**
- Tag-level learning (90% tags, 10% category)
- Behavioral tracking (views, bookmarks, shares)
- Score decay over time
- Geographic trending (localized by country)

**✅ Feed Diversity:**
- Maximum 3 markets per category in top 9
- Minimum 4 different categories
- Guaranteed multi-option market in top 9

**✅ Fresh Content Priority:**
- News categories boosted (Politics, Entertainment, World)
- Sports games boosted (upcoming 2-3 days, 0.5 boost)
- Hero rotation from visual categories

**✅ Mobile Experience:**
- TikTok-style vertical feed
- Auto-detects mobile User-Agent
- Desktop fallback with `?desktop=1`
- All buttons working (like, share, info, wallet, menu)

### 6. Mock Rain API

**Status:** Ready for integration

**Location:** `rain_api_mock.py` (port 5000)

**Endpoints:**
- `GET /api/v1/markets` - List all markets
- `GET /api/v1/markets/:id` - Get market details
- `POST /api/v1/orders` - Place trade (simulated)
- `GET /api/v1/user/:address` - Get user data
- `POST /api/v1/positions` - Get user positions

**When to switch:**
1. Set `USE_RAIN_API=true` in environment
2. Point `RAIN_API_URL` to real Rain Protocol API
3. `rain_client.py` handles data conversion

### 7. Production Deployment

**Current Setup:**
- **Ngrok tunnel:** Auto-refreshes every 30 minutes
- **Systemd service:** Auto-restarts on crash
- **Health monitoring:** 90-minute checks

**URLs:**
- Main site: https://proliferative-daleyza-benthonic.ngrok-free.dev
- Database viewer: https://proliferative-daleyza-benthonic.ngrok-free.dev/brain-viewer
- Analytics: Port 5557 (not publicly exposed)

**Ports:**
- 5555: Main Flask app (Currents)
- 5556: Database viewer
- 5557: Analytics dashboard
- 5000: Mock Rain API (when enabled)

### 8. Testing Users

**Available test users:**
- `user1`, `user2`, `user3`, `user4`, `roy`
- Set with `?user=user2` parameter
- Tracks interactions separately
- Builds different personalized feeds

### 9. Analytics & Monitoring

**Tools:**
- `db_viewer.py` - Database inspector
- `brain_analytics.py` - Data distributions, personalization simulator
- `tracking_engine.py` - Event tracking
- `compute_trending.py` - Trending score updates (cron: every 30 min)

### 10. Documentation

**Complete documentation in workspace:**
- `MASTER-REFERENCE.md` - Overview
- `BRAIN_SPEC.md` - BRain algorithm details
- `PERSONALIZATION_SPEC.md` - Learning system
- `RAIN_PROTOCOL.md` - Rain integration plan
- `API.md` - BRain API endpoints
- 50+ other docs covering all aspects

---

## 🎯 Key Takeaways for Team

1. **✅ BRain algorithm is fully implemented** - Belief intensity + personalization working
2. **✅ Data structure follows Rain Protocol** - Ready for integration when available
3. **✅ Mock Rain API ready** - Switch with environment variable
4. **✅ 326 real markets** - Fresh Polymarket data
5. **✅ Mobile + Desktop working** - Production-ready
6. **✅ Tag-level learning** - Not category-level (as per spec)
7. **✅ Comprehensive tracking** - All interactions captured
8. **✅ Auto-restart + monitoring** - Production stability

---

## 🚀 Ready for Demo

**Status:** All systems operational  
**Data:** 326 markets, BRain personalization, tag-level learning  
**Mobile:** TikTok feed working perfectly  
**Desktop:** Grid layout with hero/featured/stream  
**Architecture:** Rain-compatible, ready for API switch

**Questions?** All code, docs, and data are in:
`/home/ubuntu/.openclaw/workspace/currents-full-local/`

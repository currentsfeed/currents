# 🌊 Currents - Master Reference

**Project**: Currents - Belief-driven prediction market discovery platform  
**Owner**: Roy Shaham (@royshaham)  
**Location**: `/home/ubuntu/.openclaw/workspace/currents-full-local/`  
**Last Updated**: 2026-02-10

---

## 🔑 Access Credentials

### Localtunnel Password
**Password**: `35.172.150.243`  
(Used for both Currents and Database Viewer)

### Live URLs

**Currents Frontend**: https://poor-hands-slide.loca.lt  
**Database Viewer**: https://brain-db-viewer.loca.lt  
**BRain Analytics**: https://brain-analytics.loca.lt

*(Tunnels need to be restarted after server restart)*

---

## 🚀 Quick Start (After Restart)

### Start Everything
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# 1. Start Rain API Mock (port 5000) - optional
python3 rain_api_mock.py > /tmp/rain-mock.log 2>&1 &

# 2. Start Currents App (port 5555)
python3 app.py > /tmp/currents-app.log 2>&1 &

# 3. Start Database Viewer (port 5556)
python3 db_viewer.py > /tmp/db-viewer.log 2>&1 &

# 4. Start BRain Analytics Dashboard (port 5557)
python3 brain_analytics.py > /tmp/brain-analytics.log 2>&1 &

# 6. Start Localtunnel for Currents
nohup lt --port 5555 --subdomain poor-hands-slide > /tmp/currents-tunnel.log 2>&1 &

# 7. Start Localtunnel for Database Viewer
nohup lt --port 5556 --subdomain brain-db-viewer > /tmp/db-viewer-tunnel.log 2>&1 &

# 8. Start Localtunnel for BRain Analytics
nohup lt --port 5557 --subdomain brain-analytics > /tmp/analytics-tunnel.log 2>&1 &

# Check status
sleep 3
curl -s http://localhost:5555/health
curl -s http://localhost:5556/ | grep -o "<title>[^<]*</title>"
```

### Stop Everything
```bash
# Kill all processes
pkill -f "python3 app.py"
pkill -f "python3 db_viewer.py"
pkill -f "python3 rain_api_mock.py"
pkill -f "lt --port"
```

### Automatic Tunnel Refresh (Prevents 503 Errors)
**Localtunnel connections are automatically refreshed every 30 minutes** to prevent 503 errors.

**Status**: ✅ Active (managed by OpenClaw cron)

**Manual refresh** (if needed):
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
./refresh-tunnels.sh
```

**Refresh log**:
```bash
tail -f /tmp/tunnel-refresh.log
```

**Disable auto-refresh** (if needed):
Contact OpenClaw agent to disable the cron job.

---

## 📊 Database

### Location
`/home/ubuntu/.openclaw/workspace/currents-full-local/brain.db`

### Current State
- **100 markets** (fresh from Polymarket)
- **Categories**: Sports (44), Economics (15), Crypto (10), Politics (10), Crime (9), Entertainment (8), Technology (3), Culture (1)
- **Tags**: Multiple tags per market (trump, ai, deportation, gaming, etc.)
- **History**: Probability evolution data points

### Refresh Markets
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
python3 populate_polymarket_fresh.py  # Fetches 100 fresh markets
```

### Recategorize (if needed)
```bash
python3 recategorize_markets.py  # Fixes categories and tags
```

---

## 🏗️ Architecture

### Data Source Modes

**Local Database** (Current):
```python
# config.py
USE_RAIN_API = False
```

**Rain API Mock**:
```python
# config.py
USE_RAIN_API = True
```

### Ports
- **5000**: Rain API Mock (optional)
- **5555**: Currents Frontend
- **5556**: Database Viewer

---

## 📁 Key Files

### Application
- `app.py` - Main Flask app (homepage, market detail)
- `api.py` - BRain API endpoints
- `db_viewer.py` - Database inspection UI
- `rain_api_mock.py` - Mock Rain Protocol API
- `rain_client.py` - Rain API client library
- `config.py` - Configuration (API toggle, settings)

### Database Scripts
- `populate_polymarket_fresh.py` - Fetch 100 fresh markets from Polymarket
- `populate_polymarket_fixed.py` - Fixed version with proper option parsing
- `recategorize_markets.py` - Fix categories and add rich tags

### Templates
- `templates/base.html` - Base template with header/footer
- `templates/index-v2.html` - Homepage (hero + grid + stream)
- `templates/detail.html` - Market detail page

### Documentation
- `MASTER-REFERENCE.md` - This file (master reference)
- `PERSONALIZATION.md` - How personalization will work
- `CATEGORIES-EXPLAINED.md` - Category system explained
- `DATABASE-VIEWER.md` - Database viewer docs
- `INTEGRATION.md` - Rain API integration docs
- `UPDATE-2026-02-10.md` - Latest update summary
- `README.md` - Project overview
- `API.md` - BRain API documentation

### Database
- `brain.db` - SQLite database with markets, tags, history

---

## 🧠 Personalization (Ready, Not Yet Active)

### What's Missing
1. `user_interactions` table creation
2. Frontend JavaScript tracking
3. API endpoint `/api/track`
4. User profile builder

### How It Will Work
```python
# Track interactions
user_interactions = {
    user_id: "roy_123",
    market_id: "market_xyz",
    interaction_type: "click",  # view, click, position
    timestamp: "2026-02-10T05:20:00Z"
}

# Build profile
user_profile = {
    categories: {"World": 0.35, "Politics": 0.30},
    tags: {"trump": 15, "ukraine": 12, "ai": 8},
    probability_sweet_spot: 0.48
}

# Personalized ranking
personalized_score = (
    belief_intensity * 0.4 +      # Base BRain
    category_match * 0.3 +         # Favorite topics
    collaborative_signal * 0.2 +   # Similar users
    recency_boost * 0.1            # Recent interests
)
```

---

## 🎯 Categories & Tags

### Categories (9)
1. **Sports** (44) - FIFA, NFL, NBA, Olympics
2. **Economics** (15) - Revenue, budget, tariffs
3. **Crypto** (10) - Bitcoin, Ethereum, DeFi
4. **Politics** (10) - Trump, elections, government
5. **Crime** (9) - Trials, convictions
6. **Entertainment** (8) - Gaming, music, movies
7. **Technology** (3) - AI, OpenAI, hardware
8. **Culture** (1) - Religion
9. **Predictions** (rare) - Misc/unusual

### Top Tags
- `trump` (11)
- `ai` (18)
- `deportation` (10)
- `gaming` (9)
- `legal` (9)
- `elon` (8)
- `budget` (8)

---

## 🔍 Useful Commands

### Check Status
```bash
# Check if apps are running
ps aux | grep -E "app.py|db_viewer.py|rain_api_mock" | grep -v grep

# Check if tunnels are running
ps aux | grep "lt --port" | grep -v grep

# Test local endpoints
curl http://localhost:5555/health
curl http://localhost:5556/ | grep title
curl http://localhost:5000/api/v1/health  # if Rain mock running
```

### View Logs
```bash
tail -f /tmp/currents-app.log      # Currents app
tail -f /tmp/db-viewer.log          # Database viewer
tail -f /tmp/rain-mock.log          # Rain API mock
tail -f /tmp/currents-tunnel.log    # Currents tunnel
tail -f /tmp/db-viewer-tunnel.log   # DB viewer tunnel
```

### Database Queries
```bash
# Connect to database
sqlite3 /home/ubuntu/.openclaw/workspace/currents-full-local/brain.db

# Useful queries
SELECT category, COUNT(*) FROM markets GROUP BY category;
SELECT tag, COUNT(*) FROM market_tags GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 20;
SELECT title FROM markets WHERE category = 'Politics' LIMIT 5;
```

### API Testing
```bash
# Homepage feed
curl http://localhost:5555/api/homepage | jq

# List markets
curl "http://localhost:5555/api/v1/markets?limit=5" | jq

# Get market detail
curl "http://localhost:5555/api/v1/markets/market_id" | jq

# Filter by category
curl "http://localhost:5555/api/v1/markets?category=Politics" | jq
```

---

## 🌐 External Services

### Polymarket API
- URL: `https://gamma-api.polymarket.com/markets`
- Used to fetch fresh markets
- No auth required
- Limit: ~100 markets per request

### Localtunnel
- Service: https://localtunnel.me
- Stable subdomains: `poor-hands-slide`, `brain-db-viewer`
- Password protection: `35.172.150.243`
- Needs restart after server reboot

---

## 📝 Version History

### v24 (2026-02-10)
- ✅ 100 fresh Polymarket markets
- ✅ Better categorization (no more "Markets" catch-all)
- ✅ Rich tagging (trump, ai, deportation, etc.)
- ✅ Database viewer shows market questions
- ✅ Footer link to database viewer
- ✅ Comprehensive documentation

### v23 (2026-02-09)
- ✅ Rain API integration
- ✅ Mock Rain Protocol API
- ✅ Config-based data source toggle
- ✅ Fixed market options (Democrat/Republican, not Yes/No)

### v22 (2026-02-09)
- ✅ Expandable options on cards
- ✅ Multi-option market support
- ✅ The Stream section
- ✅ Bottom widgets

### Earlier versions (v1-v21)
- See `CHANGELOG.md` for full history

---

## 🎓 Learning Resources

**How BRain Works**:
- Read `PERSONALIZATION.md` for algorithm details
- Read `CATEGORIES-EXPLAINED.md` for tagging system
- Read `API.md` for endpoint documentation

**How to Extend**:
1. Add new categories: Edit `recategorize_markets.py`
2. Add new data sources: Edit `populate_polymarket_fresh.py`
3. Add new UI features: Edit `templates/index-v2.html`
4. Add new API endpoints: Edit `api.py`

---

## 🐛 Troubleshooting

### Tunnels Not Working
```bash
# Kill old tunnels
pkill -f "lt --port"

# Restart both
nohup lt --port 5555 --subdomain poor-hands-slide > /tmp/currents-tunnel.log 2>&1 &
nohup lt --port 5556 --subdomain brain-db-viewer > /tmp/db-viewer-tunnel.log 2>&1 &

# Wait and check
sleep 3
cat /tmp/currents-tunnel.log
cat /tmp/db-viewer-tunnel.log
```

### App Not Starting
```bash
# Check if port is in use
lsof -ti:5555

# Kill process on port
lsof -ti:5555 | xargs kill

# Check logs for errors
tail -20 /tmp/currents-app.log
```

### Database Issues
```bash
# Verify database exists
ls -lh brain.db

# Check table count
sqlite3 brain.db "SELECT name FROM sqlite_master WHERE type='table';"

# Refresh data
python3 populate_polymarket_fresh.py
```

---

## ✅ Current Status

**Everything Working**:
- ✅ 100 fresh markets loaded
- ✅ Proper categorization (9 categories)
- ✅ Rich tagging system
- ✅ Database viewer enhanced
- ✅ Both tunnels live
- ✅ Footer link working
- ✅ All documentation complete

**Ready for Next Steps**:
- 🔜 User interaction tracking
- 🔜 Personalized ranking
- 🔜 Collaborative filtering
- 🔜 Real Rain Protocol API connection (when available)

---

## 👤 Owner Info

**Name**: Roy Shaham  
**Telegram**: @royshaham  
**GitHub**: roy481977  
**Project**: Currents (discovery UI) + BRain (ranking) for Rain protocol

---

**Last Updated**: 2026-02-10 05:26 UTC  
**Status**: ✅ Fully Operational  
**Next Session**: Just run the Quick Start commands above!

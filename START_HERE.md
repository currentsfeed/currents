# 🌊 Currents + Rain Protocol - START HERE

**Welcome!** This is your 2-week demo of Currents, a belief-driven prediction market platform powered by Rain Protocol.

## 📦 What's Inside

This demo includes:

1. **🌧️  Mock Rain API** - Simulates Rain Protocol with fake data
2. **🧠 BRain Intelligence** - Ranking algorithm (belief intensity)
3. **🌊 Currents UI** - Beautiful discovery interface
4. **📡 REST APIs** - Both Rain and BRain exposed as APIs

## 🚀 Quick Start (3 commands)

```bash
# Terminal 1: Start Mock Rain Protocol
python3 rain_api_mock.py

# Terminal 2: Start BRain + Currents  
export USE_RAIN_API=true
python3 -m flask run --host=0.0.0.0 --port=5555

# Browser: Open UI
http://localhost:5555
```

**That's it!** You now have:
- Mock Rain API on port 5000
- Currents UI on port 5555
- 7 fake markets with realistic data

## 📚 Documentation

Pick your path:

### For Quick Demo
→ **[QUICKSTART_RAIN.md](QUICKSTART_RAIN.md)** - 5-minute setup guide

### For Understanding Architecture
→ **[RAIN_INTEGRATION.md](RAIN_INTEGRATION.md)** - How BRain integrates with Rain

### For API Details
→ **[API.md](API.md)** - BRain API reference  
→ **Rain Mock API** - See rain_api_mock.py docstrings

### For Development
→ **[README.md](README.md)** - Project overview  
→ **[CHANGELOG.md](CHANGELOG.md)** - Version history

## 🎯 Testing

### Test Rain Mock API
```bash
python3 test_rain_mock.py
```

### Test BRain API
```bash
python3 test_api.py
```

### Manual Testing
```bash
# Rain API
curl http://localhost:5000/api/v1/health
curl http://localhost:5000/api/v1/markets

# BRain API
curl http://localhost:5555/api/v1/health
curl http://localhost:5555/api/v1/feed
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Currents UI                   │ 
│  (Web interface, visualizations)        │
│              Port 5555                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          BRain Intelligence             │
│  (Ranking algorithm, belief intensity)  │
│         REST API: /api/v1/*             │
└──────────────┬──────────────────────────┘
               │
               │ RainClient (rain_client.py)
               │
┌──────────────▼──────────────────────────┐
│      Mock Rain Protocol API             │
│  (Markets, trades, positions, stats)    │
│              Port 5000                  │
└─────────────────────────────────────────┘
```

**When Real Rain API is Ready**:
Just change `RAIN_API_URL` → No code changes!

## 📊 What's Included

### Markets (7 total)
- **5 Binary**: Bitcoin, Trump, GPT-5, Recession, Ukraine
- **2 Multi-Option**: World Cup (7 countries), $5T Market Cap (5 companies)

### Data
- Realistic volumes ($50k-$800k per market)
- Participant counts (1k-30k)
- Price history (20 data points per market)
- Recent trades (10 per market)
- User positions
- Leaderboard (fake traders)
- Platform statistics

### Features
- ✅ Hero section (featured market)
- ✅ Grid (8 top markets)
- ✅ Stream feed (extended list)
- ✅ Multi-option market support
- ✅ Expandable options
- ✅ Belief Currents visualization
- ✅ Category filtering
- ✅ Bottom widgets (trending, leaderboard)

## 🔄 Integration Pattern

This setup establishes the **real integration pattern**:

1. **Rain API** provides market data
2. **BRain** fetches, ranks, and curates
3. **Currents** displays beautiful UI
4. **When real Rain launches** → just swap the URL!

## 🎨 UI Highlights

- **Belief Currents**: Time-based gradient showing opinion evolution
- **Dynamic Colors**: Each option gets unique color (blue/purple/green/yellow)
- **Expandable Options**: Click "+2 more" to reveal hidden options
- **Multi-Option Support**: Markets with 5+ outcomes (World Cup, etc.)
- **Responsive**: Works on desktop/tablet
- **Figma-Matched**: Design matches provided mockups

## 🔧 Configuration

All settings in `config.py`:

```python
USE_RAIN_API = True  # Toggle Rain API vs local DB
RAIN_API_URL = "http://localhost:5000/api/v1"  # Rain endpoint
PORT = 5555  # BRain/Currents port
```

Environment variables override:
```bash
export USE_RAIN_API=true
export RAIN_API_URL=https://api.rain.xyz/v1  # When real API is ready
```

## 🐛 Troubleshooting

### Nothing works
```bash
# Check both services are running
curl http://localhost:5000/api/v1/health  # Rain
curl http://localhost:5555/api/v1/health  # BRain

# Restart if needed
pkill -f rain_api_mock.py
pkill -f "flask run"
```

### Markets not showing
```bash
# Test Rain directly
curl http://localhost:5000/api/v1/markets

# Check config
python3 -c "import config; print(config.USE_RAIN_API)"
```

### Port already in use
```bash
# Find process
lsof -i :5000
lsof -i :5555

# Kill and restart
pkill -f python3
```

## 📞 Support

Check documentation in order:
1. **[QUICKSTART_RAIN.md](QUICKSTART_RAIN.md)** - Setup help
2. **[RAIN_INTEGRATION.md](RAIN_INTEGRATION.md)** - Integration details
3. **[API.md](API.md)** - API reference

## 🎯 Demo Day Checklist

Before showing to Rain team/investors:

- [ ] Both services running (port 5000 & 5555)
- [ ] Run test suites (both pass)
- [ ] Open UI in browser (looks good)
- [ ] Click around (no errors)
- [ ] Expand options (works smoothly)
- [ ] Show API responses (`curl` commands)
- [ ] Explain integration pattern

**Key talking points**:
- ✅ Mock API simulates real Rain perfectly
- ✅ When real API launches, just change URL
- ✅ BRain ranking makes markets discoverable
- ✅ Belief Currents show opinion evolution
- ✅ Ready for Rain protocol integration

## 🚀 Next Steps

After demo approval:

1. **Connect to Real Rain API** (when available)
2. **Add More BRain Features**:
   - Personalized feeds
   - Search
   - Advanced filtering
   - Real-time updates
3. **Scale Infrastructure**:
   - Caching (Redis)
   - Load balancing
   - CDN for images
4. **Mobile App** (React Native)

---

## 📝 File Guide

**Start Here**:
- `START_HERE.md` ← You are here!
- `QUICKSTART_RAIN.md` ← Run this first

**Core Files**:
- `rain_api_mock.py` - Mock Rain Protocol
- `rain_client.py` - Rain API client
- `app.py` - BRain + Currents
- `api.py` - BRain REST API

**Documentation**:
- `RAIN_INTEGRATION.md` - Integration guide
- `API.md` - BRain API reference
- `README.md` - Project overview
- `CHANGELOG.md` - Version history

**Testing**:
- `test_rain_mock.py` - Test Rain integration
- `test_api.py` - Test BRain API

**Config**:
- `config.py` - Settings (Rain URL, ports, etc.)
- `brain.db` - SQLite database (fallback)

**UI**:
- `templates/index-v2.html` - Homepage
- `templates/base.html` - Layout
- `templates/detail.html` - Market detail

---

**🎉 You're all set!**

Pick a guide above and start exploring. The quick start is 3 commands away.

**Built with 🌧️ + 🧠 + 🌊 for Rain Protocol**

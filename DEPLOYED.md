# ✅ Your APIs Are Deployed!

## 🌐 Public URLs

Both services are now **publicly accessible** and can be used from anywhere:

### 🧠 BRain API + Currents UI
**URL**: `https://brain-currents.loca.lt`  
**Password**: `35.172.150.243`

**What it provides**:
- REST API for market intelligence
- Belief intensity ranking
- Curated feeds (hero/grid/stream)
- Web UI for visualization

**Endpoints**:
```
GET  /api/v1/health
GET  /api/v1/markets
GET  /api/v1/markets/{id}
GET  /api/v1/feed
GET  /api/v1/categories
GET  /api/v1/trending
```

---

### 🌧️  Mock Rain Protocol API
**URL**: `https://rain-mock-api.loca.lt`  
**Password**: `35.172.150.243`

**What it provides**:
- Simulates Rain Protocol with fake data
- 7 prediction markets (binary + multi-option)
- Trading history, positions, leaderboard
- Platform statistics

**Endpoints**:
```
GET  /api/v1/health
GET  /api/v1/markets
GET  /api/v1/markets/{id}
GET  /api/v1/user/{id}/positions
GET  /api/v1/trades
GET  /api/v1/leaderboard
GET  /api/v1/stats
```

---

## 🚀 Quick Test

### From Command Line

```bash
# Test BRain
curl https://brain-currents.loca.lt/api/v1/health

# Test Rain
curl https://rain-mock-api.loca.lt/api/v1/health

# Get markets
curl https://brain-currents.loca.lt/api/v1/feed
```

### From Browser

1. Visit: `https://brain-currents.loca.lt`
2. Enter password: `35.172.150.243`
3. You'll see the Currents UI

For API calls:
- `https://brain-currents.loca.lt/api/v1/health`
- `https://rain-mock-api.loca.lt/api/v1/health`

---

## 💻 For Frontend Development

### JavaScript

```javascript
const BRAIN_API = "https://brain-currents.loca.lt/api/v1";

// Get feed
fetch(`${BRAIN_API}/feed`)
  .then(res => res.json())
  .then(data => {
    console.log("Hero:", data.hero[0]);
    console.log("Grid:", data.grid);
  });

// Get crypto markets
fetch(`${BRAIN_API}/markets?category=Crypto`)
  .then(res => res.json())
  .then(data => {
    console.log("Crypto markets:", data.markets);
  });
```

### Python

```python
import requests

BRAIN_API = "https://brain-currents.loca.lt/api/v1"

# Get feed
response = requests.get(f"{BRAIN_API}/feed")
feed = response.json()

print(f"Hero: {feed['hero'][0]['title']}")
print(f"Grid markets: {len(feed['grid'])}")
```

### React

```jsx
import { useEffect, useState } from 'react';

const BRAIN_API = "https://brain-currents.loca.lt/api/v1";

function Markets() {
  const [feed, setFeed] = useState(null);
  
  useEffect(() => {
    fetch(`${BRAIN_API}/feed`)
      .then(res => res.json())
      .then(data => setFeed(data));
  }, []);
  
  if (!feed) return <div>Loading...</div>;
  
  return (
    <div>
      <h1>{feed.hero[0].title}</h1>
      <div className="grid">
        {feed.grid.map(market => (
          <div key={market.market_id}>
            <h3>{market.title}</h3>
            <p>{(market.probability * 100).toFixed(1)}%</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 📊 What's Available

### BRain API (50 markets)
- **45 binary markets**: Bitcoin, Trump, GPT-5, S&P 500, etc.
- **5 multi-option markets**: Eurovision, Oscars, Super Bowl, NBA MVP, Fed Chair

### Rain Mock API (7 markets)
- **5 binary markets**: Bitcoin $150k, GPT-5, Trump, Recession, Ukraine
- **2 multi-option markets**: World Cup (7 countries), $5T market cap (5 companies)

### Features
- ✅ Ranked by belief intensity
- ✅ Real-time (mock) data
- ✅ Price history
- ✅ Trading data
- ✅ User positions
- ✅ Leaderboard

---

## 🔧 Architecture

```
┌─────────────────────────────────┐
│   Your Frontend (Anywhere)      │
│   React / Vue / Plain JS        │
└────────────┬────────────────────┘
             │ HTTPS
             ▼
┌─────────────────────────────────┐
│  https://brain-currents.loca.lt │ ← BRain API
│  • Market intelligence           │
│  • Belief intensity ranking     │
│  • Curated feeds                │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ https://rain-mock-api.loca.lt   │ ← Rain Protocol (Mock)
│  • Prediction markets            │
│  • Trades, positions             │
│  • Platform stats                │
└─────────────────────────────────┘
```

---

## 🎯 Integration Pattern

This setup **establishes the real integration pattern** for when Rain launches:

**Today** (Mock):
```javascript
const RAIN_API = "https://rain-mock-api.loca.lt/api/v1";
```

**Tomorrow** (Real):
```javascript
const RAIN_API = "https://api.rain.xyz/v1";
```

**BRain stays the same** - your frontend never changes!

---

## 📖 Documentation

- **[PUBLIC_ENDPOINTS.md](PUBLIC_ENDPOINTS.md)** - Complete API reference
- **[RAIN_INTEGRATION.md](RAIN_INTEGRATION.md)** - Integration guide
- **[API.md](API.md)** - BRain API docs
- **[START_HERE.md](START_HERE.md)** - Project overview

---

## ⚠️ Important Notes

### Password Protection

First time you visit each URL, enter password: `35.172.150.243`

Your browser will remember it for future requests.

### CORS Enabled

Both APIs support CORS, so you can call them from:
- Any website
- Browser JavaScript
- Mobile apps
- Desktop apps

### Temporary URLs

These localtunnel URLs are temporary. For production:
- Deploy to Railway / Render / Fly.io
- Use custom domain
- Add proper rate limiting

---

## 🐛 Troubleshooting

### "503 Service Unavailable"

The tunnel may have reset. Test:
```bash
curl https://brain-currents.loca.lt/api/v1/health
```

If down, contact server admin to restart tunnels.

### CORS Errors

Make sure you're using `https://` (not `http://`).

Both APIs have CORS enabled for all origins.

### Slow Response

Localtunnel adds ~200ms latency. This is fine for development.

For production, deploy to a proper cloud service.

---

## 🚀 Next Steps

1. **Build your frontend** against these APIs
2. **Test the integration** with real data
3. **When satisfied**, deploy to production infrastructure
4. **When Rain launches**, just change the Rain API URL

---

## 📞 Quick Reference

**BRain/Currents**: https://brain-currents.loca.lt  
**Mock Rain API**: https://rain-mock-api.loca.lt  
**Password**: `35.172.150.243`

**Test Commands**:
```bash
# BRain health
curl https://brain-currents.loca.lt/api/v1/health

# Get feed
curl https://brain-currents.loca.lt/api/v1/feed

# Rain health
curl https://rain-mock-api.loca.lt/api/v1/health

# Rain markets
curl https://rain-mock-api.loca.lt/api/v1/markets
```

---

**🎉 Everything is ready for frontend development!**

You can now build your Currents website against these public APIs from anywhere.

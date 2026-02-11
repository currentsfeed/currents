# 🌐 Public API Endpoints

Your BRain and Mock Rain APIs are now **publicly accessible**!

## 🚀 Live URLs

### BRain API + Currents UI
**Base URL**: `https://brain-currents.loca.lt`

**API Endpoints**:
- Health: `https://brain-currents.loca.lt/api/v1/health`
- Markets: `https://brain-currents.loca.lt/api/v1/markets`
- Feed: `https://brain-currents.loca.lt/api/v1/feed`
- Categories: `https://brain-currents.loca.lt/api/v1/categories`
- Trending: `https://brain-currents.loca.lt/api/v1/trending`

**Web UI**:
- Homepage: `https://brain-currents.loca.lt/`

---

### Mock Rain Protocol API
**Base URL**: `https://rain-mock-api.loca.lt`

**API Endpoints**:
- Health: `https://rain-mock-api.loca.lt/api/v1/health`
- Markets: `https://rain-mock-api.loca.lt/api/v1/markets`
- Market Detail: `https://rain-mock-api.loca.lt/api/v1/markets/{id}`
- User Positions: `https://rain-mock-api.loca.lt/api/v1/user/{id}/positions`
- Trades: `https://rain-mock-api.loca.lt/api/v1/trades`
- Leaderboard: `https://rain-mock-api.loca.lt/api/v1/leaderboard`
- Platform Stats: `https://rain-mock-api.loca.lt/api/v1/stats`

---

## 🧪 Test Commands

### Test BRain API

```bash
# Health check
curl https://brain-currents.loca.lt/api/v1/health

# Get feed
curl https://brain-currents.loca.lt/api/v1/feed

# Get crypto markets
curl "https://brain-currents.loca.lt/api/v1/markets?category=Crypto&limit=5"

# Get trending
curl https://brain-currents.loca.lt/api/v1/trending
```

### Test Mock Rain API

```bash
# Health check
curl https://rain-mock-api.loca.lt/api/v1/health

# List all markets
curl https://rain-mock-api.loca.lt/api/v1/markets

# Get specific market
curl https://rain-mock-api.loca.lt/api/v1/markets/rain_binary_1

# Platform stats
curl https://rain-mock-api.loca.lt/api/v1/stats

# Leaderboard
curl https://rain-mock-api.loca.lt/api/v1/leaderboard

# Recent trades
curl https://rain-mock-api.loca.lt/api/v1/trades
```

---

## 🔌 Frontend Integration

### JavaScript Example

```javascript
// Fetch from BRain API
const BRAIN_API = "https://brain-currents.loca.lt/api/v1";

// Get feed
fetch(`${BRAIN_API}/feed`)
  .then(res => res.json())
  .then(data => {
    console.log("Hero market:", data.hero[0]);
    console.log("Grid markets:", data.grid.length);
  });

// Get crypto markets
fetch(`${BRAIN_API}/markets?category=Crypto`)
  .then(res => res.json())
  .then(data => {
    data.markets.forEach(m => {
      console.log(m.title, m.probability);
    });
  });
```

### Python Example

```python
import requests

BRAIN_API = "https://brain-currents.loca.lt/api/v1"
RAIN_API = "https://rain-mock-api.loca.lt/api/v1"

# Get BRain feed
response = requests.get(f"{BRAIN_API}/feed")
feed = response.json()
print(f"Hero: {feed['hero'][0]['title']}")

# Get Rain markets
response = requests.get(f"{RAIN_API}/markets")
markets = response.json()['markets']
print(f"Found {len(markets)} Rain markets")
```

---

## 📊 Response Examples

### BRain API - Feed

```bash
curl https://brain-currents.loca.lt/api/v1/feed
```

Response:
```json
{
  "hero": [
    {
      "market_id": "m_eth_flip",
      "title": "Will Ethereum flip Bitcoin by market cap in 2026?",
      "belief_intensity": 18.82,
      "probability": 0.28,
      "volume_24h": 310000,
      "category": "Crypto"
    }
  ],
  "grid": [...],
  "stream": [...]
}
```

### Rain Mock API - Markets

```bash
curl https://rain-mock-api.loca.lt/api/v1/markets?limit=1
```

Response:
```json
{
  "markets": [
    {
      "market_id": "rain_binary_1",
      "title": "Will Bitcoin hit $150,000 by July 2025?",
      "category": "Crypto",
      "market_type": "binary",
      "probability": 0.66,
      "volume_24h": 222537,
      "liquidity": 582373,
      "chain": "ethereum",
      "contract_address": "0xabc123...",
      "outcomes": [
        {"name": "Yes", "probability": 0.66},
        {"name": "No", "probability": 0.34}
      ]
    }
  ]
}
```

---

## 🔐 CORS

Both APIs have CORS enabled for all origins, so you can call them from:
- ✅ Any website
- ✅ Browser JavaScript
- ✅ React/Vue/Angular apps
- ✅ Mobile apps
- ✅ Desktop apps

---

## 🎯 Use Cases

### 1. Build Custom Dashboard

```html
<!DOCTYPE html>
<html>
<head>
  <title>Currents Dashboard</title>
</head>
<body>
  <h1>Top Markets</h1>
  <div id="markets"></div>
  
  <script>
    fetch('https://brain-currents.loca.lt/api/v1/feed')
      .then(res => res.json())
      .then(data => {
        const html = data.grid.map(m => `
          <div>
            <h3>${m.title}</h3>
            <p>Probability: ${(m.probability * 100).toFixed(1)}%</p>
            <p>Volume: $${m.volume_24h.toLocaleString()}</p>
          </div>
        `).join('');
        document.getElementById('markets').innerHTML = html;
      });
  </script>
</body>
</html>
```

### 2. Monitor Rain Protocol

```python
import requests
import time

RAIN_API = "https://rain-mock-api.loca.lt/api/v1"

while True:
    # Get platform stats
    stats = requests.get(f"{RAIN_API}/stats").json()
    print(f"Volume 24h: ${stats['total_volume_24h']:,.0f}")
    print(f"Active users: {stats['active_users_24h']:,}")
    
    # Get recent trades
    trades = requests.get(f"{RAIN_API}/trades?limit=5").json()['trades']
    for trade in trades:
        print(f"  {trade['side'].upper()} {trade['outcome']}: ${trade['amount']:.2f}")
    
    time.sleep(60)  # Update every minute
```

### 3. Track Specific Markets

```javascript
const BRAIN_API = "https://brain-currents.loca.lt/api/v1";

async function trackMarket(marketId) {
  const response = await fetch(`${BRAIN_API}/markets/${marketId}`);
  const data = await response.json();
  const market = data.market;
  
  console.log(`${market.title}`);
  console.log(`  Current: ${(market.probability * 100).toFixed(1)}%`);
  console.log(`  Belief Intensity: ${market.belief_intensity.toFixed(2)}`);
  
  // Check every 30 seconds
  setTimeout(() => trackMarket(marketId), 30000);
}

trackMarket('m_eth_flip');
```

---

## 🚨 Important Notes

### Localtunnel Password

These URLs require password authentication on first visit:

**Password**: `35.172.150.243`

After entering the password once, your browser will remember it.

### Rate Limiting

Currently: **No rate limiting**  
Recommended for production: **100 requests/minute**

### Persistence

These tunnels are temporary and will reset if:
- Server restarts
- Network interruption
- Process crash

For production, deploy to:
- Railway (https://railway.app)
- Render (https://render.com)
- Fly.io (https://fly.io)
- Vercel (API routes)

---

## 🔄 Switching to Real Rain API

When the real Rain Protocol API is ready:

**Step 1**: Update BRain configuration
```bash
export RAIN_API_URL=https://api.rain.xyz/v1
```

**Step 2**: Restart BRain
```bash
pkill -f "flask run"
python3 -m flask run --host=0.0.0.0 --port=5555
```

**That's it!** BRain will automatically fetch from the real Rain API instead of the mock.

Your frontend code doesn't need to change at all - it still calls:
```
https://brain-currents.loca.lt/api/v1/*
```

---

## 📖 Full API Documentation

- **BRain API**: See [API.md](API.md)
- **Rain Mock API**: See [RAIN_INTEGRATION.md](RAIN_INTEGRATION.md)

---

## 🐛 Troubleshooting

### "503 Service Unavailable"

Tunnel may have reset. Check status:
```bash
curl https://brain-currents.loca.lt/api/v1/health
curl https://rain-mock-api.loca.lt/api/v1/health
```

If down, restart tunnels (see server admin).

### CORS Error

Both APIs have CORS enabled. If you see CORS errors:
1. Check the API is actually accessible
2. Make sure you're using HTTPS (not HTTP)
3. Check browser console for actual error

### Slow Responses

Localtunnel adds ~100-300ms latency. For faster responses:
- Deploy to proper cloud service
- Use CDN
- Add caching layer (Redis)

---

## 📞 Support

Questions? Check:
1. [QUICKSTART_RAIN.md](QUICKSTART_RAIN.md)
2. [RAIN_INTEGRATION.md](RAIN_INTEGRATION.md)
3. [API.md](API.md)

---

**🎉 Your APIs are now live and accessible from anywhere!**

Start building your frontend against these URLs.

# Rain API - Quick Start Guide

## 🚀 Quick Start (30 seconds)

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Start both services
python3 brain_rain_service.py

# Or start individually:
python3 rain_api_standalone.py &    # Port 5001
python3 app.py                       # Port 5555
```

## ✅ Verify It's Working

```bash
# Check service status
python3 brain_rain_service.py status

# Test Rain API
curl http://localhost:5001/health
curl http://localhost:5001/api/v1/stats

# Run full integration test
python3 test_rain_integration.py
```

## 📊 What's Where

| Data | Location | Access |
|------|----------|--------|
| Market metadata | `rain.db` | Rain API (port 5001) |
| Market images | `brain.db` | BRain App (port 5555) |
| User data | `brain.db` | BRain App (port 5555) |
| Interactions | `brain.db` | BRain App (port 5555) |

## 🔌 API Endpoints

### Get Markets
```bash
curl "http://localhost:5001/api/v1/markets?limit=10&status=open"
```

### Get Single Market
```bash
curl "http://localhost:5001/api/v1/markets/MARKET_ID"
```

### Get Multiple Markets
```bash
curl -X POST http://localhost:5001/api/v1/markets/batch \
  -H "Content-Type: application/json" \
  -d '{"market_ids": ["id1", "id2", "id3"]}'
```

### Get Stats
```bash
curl "http://localhost:5001/api/v1/stats"
```

## 🧠 Using Rain Client in Python

```python
from rain_client_brain import rain_client

# Get markets
markets = rain_client.get_markets(limit=10)

# Get single market
market = rain_client.get_market('market_id')

# Get batch
markets = rain_client.get_markets_batch(['id1', 'id2'])

# Health check
if rain_client.health_check():
    print("Rain API is healthy")
```

## 🔧 Troubleshooting

### Rain API won't start
```bash
# Check if port 5001 is in use
lsof -i :5001

# Kill existing process
kill $(lsof -t -i :5001)

# Restart
python3 rain_api_standalone.py
```

### Integration test fails
```bash
# Make sure Rain API is running
curl http://localhost:5001/health

# Check logs
tail -f rain_api.log
```

## 📝 Key Files

- `rain.db` - Market data database (153 markets)
- `rain_api_standalone.py` - Rain API service
- `rain_client_brain.py` - Python client wrapper
- `personalization.py` - Uses Rain API for market data
- `brain_rain_service.py` - Service manager
- `test_rain_integration.py` - Integration tests

## 📖 Full Documentation

See `RAIN_SEPARATION_COMPLETE.md` for complete documentation.

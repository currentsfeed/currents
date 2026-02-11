# Quick Start: Rain Protocol Integration

Get Currents running with the mock Rain API in 3 minutes.

## 🚀 Step 1: Start Mock Rain API

```bash
cd currents-full-local/
python3 rain_api_mock.py
```

**Expected output**:
```
🌧️  Rain Protocol Mock API starting...
📊 Generated 7 fake markets
🚀 Running on http://0.0.0.0:5000
```

**Test it**:
```bash
curl http://localhost:5000/api/v1/health
# Should return: {"status": "ok", ...}
```

---

## 🧪 Step 2: Test Rain Integration

```bash
# In a new terminal
python3 test_rain_mock.py
```

**Expected output**:
```
🌧️  Testing Mock Rain Protocol API
======================================================================
✅ Health Check
✅ List Markets (5 found)
✅ Market Details
✅ Multi-Option Markets
✅ BRain Conversion
✅ All tests passed!
```

---

## 🌐 Step 3: Start BRain with Rain API

```bash
# Configure to use Rain API
export USE_RAIN_API=true
export RAIN_API_URL=http://localhost:5000/api/v1

# Start BRain/Currents
python3 -m flask run --host=0.0.0.0 --port=5555
```

**Expected output**:
```
📡 Data Source: Rain API
🌧️  Rain API URL: http://localhost:5000/api/v1
* Running on http://0.0.0.0:5555
```

---

## ✅ Step 4: Verify Everything Works

### Check BRain API

```bash
# BRain health (should mention Rain)
curl http://localhost:5555/api/v1/health

# Get feed from BRain (fetches from Rain API)
curl http://localhost:5555/api/v1/feed
```

### Check UI

Open browser: `http://localhost:5555`

You should see:
- Markets from Rain API displayed
- Hero section working
- Grid cards populated

---

## 🔄 Switch Between Mock and Database

### Use Mock Rain API (Recommended for demo)

```bash
export USE_RAIN_API=true
export RAIN_API_URL=http://localhost:5000/api/v1
python3 -m flask run --port 5555
```

### Use Local Database (Fallback)

```bash
export USE_RAIN_API=false
python3 -m flask run --port 5555
```

---

## 📊 What's Running?

After following the steps above, you'll have:

```
Port 5000: Mock Rain Protocol API (fake markets, trades, stats)
Port 5555: BRain + Currents (UI + intelligence layer)
```

**Data Flow**:
```
Rain Mock (5000) → BRain Client → BRain API (5555) → Currents UI
```

---

## 🧪 Test Endpoints

### Rain API (Port 5000)

```bash
# Markets
curl "http://localhost:5000/api/v1/markets?limit=3"

# Market detail
curl "http://localhost:5000/api/v1/markets/rain_binary_1"

# Platform stats
curl "http://localhost:5000/api/v1/stats"

# Leaderboard
curl "http://localhost:5000/api/v1/leaderboard"
```

### BRain API (Port 5555)

```bash
# Health
curl "http://localhost:5555/api/v1/health"

# Feed
curl "http://localhost:5555/api/v1/feed"

# Markets (processed by BRain)
curl "http://localhost:5555/api/v1/markets?category=Crypto"
```

---

## 🎯 Quick Demo Script

Run this to see everything in action:

```bash
#!/bin/bash

echo "🌧️  Starting Rain Mock API..."
python3 rain_api_mock.py > /tmp/rain.log 2>&1 &
RAIN_PID=$!

sleep 2

echo "🧪 Testing Rain API..."
curl -s http://localhost:5000/api/v1/health | jq .

echo ""
echo "🚀 Starting BRain..."
export USE_RAIN_API=true
export RAIN_API_URL=http://localhost:5000/api/v1
python3 -m flask run --host=0.0.0.0 --port=5555 > /tmp/brain.log 2>&1 &
BRAIN_PID=$!

sleep 3

echo "✅ Testing BRain integration..."
curl -s http://localhost:5555/api/v1/health | jq .

echo ""
echo "📊 Fetching feed from BRain (via Rain)..."
curl -s "http://localhost:5555/api/v1/feed" | jq '.hero[0].title'

echo ""
echo "✅ Everything is running!"
echo "   Rain Mock: http://localhost:5000"
echo "   BRain/UI:  http://localhost:5555"
echo ""
echo "Press Ctrl+C to stop"

# Cleanup on exit
trap "kill $RAIN_PID $BRAIN_PID" EXIT
wait
```

Save as `start_demo.sh`, then:

```bash
chmod +x start_demo.sh
./start_demo.sh
```

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Kill existing processes
pkill -f rain_api_mock.py
pkill -f "flask run"

# Or use different ports
python3 rain_api_mock.py --port 5001
```

### Connection Refused

```bash
# Make sure Rain API is running
curl http://localhost:5000/api/v1/health

# Check BRain config
python3 -c "import config; print(config.USE_RAIN_API, config.RAIN_API_URL)"
```

### No Markets Showing

```bash
# Test Rain API directly
curl "http://localhost:5000/api/v1/markets?limit=1"

# Check BRain logs
tail -f /tmp/brain.log
```

---

## 🎓 Next Steps

1. **Explore the mock data**: See `rain_api_mock.py` for fake market generation
2. **Test the client**: Use `rain_client.py` to integrate with your own apps
3. **Read the integration guide**: See `RAIN_INTEGRATION.md` for full details
4. **When real Rain API is ready**: Just change `RAIN_API_URL` and it works!

---

**🎉 That's it! You now have a working Rain Protocol integration.**

The beauty of this setup:
- ✅ Mock API simulates real Rain protocol
- ✅ BRain consumes it exactly like it will consume the real API
- ✅ When real API is ready, just change the URL
- ✅ Zero code changes needed for the switch!

# Rain Protocol Integration Guide

This guide explains how Currents/BRain integrates with the Rain Protocol API (both mock and real).

## 🌧️ Overview

**Rain Protocol** provides the underlying prediction market data and trading infrastructure. **BRain** is the intelligence layer that ranks markets by "belief intensity" and creates curated feeds.

```
┌─────────────┐      ┌──────────┐      ┌──────────┐
│ Rain Protocol│ ────>│  BRain   │ ────>│ Currents │
│   (Markets)  │      │(Ranking) │      │   (UI)   │
└─────────────┘      └──────────┘      └──────────┘
```

## 📁 Files

- **`rain_api_mock.py`**: Mock Rain API (runs on port 5000)
- **`rain_client.py`**: Python client for Rain API
- **`config.py`**: Configuration (toggle mock vs real)
- **`test_rain_mock.py`**: Test suite for Rain integration

## 🚀 Quick Start

### 1. Start Mock Rain API

```bash
# Start on port 5000
python3 rain_api_mock.py

# Check it's running
curl http://localhost:5000/api/v1/health
```

### 2. Configure BRain

```bash
# Use Rain API (default)
export USE_RAIN_API=true
export RAIN_API_URL=http://localhost:5000/api/v1

# Or use local database (fallback)
export USE_RAIN_API=false
```

### 3. Test Integration

```bash
# Run comprehensive test suite
python3 test_rain_mock.py
```

## 📊 Mock Rain API Endpoints

All endpoints are prefixed with `/api/v1`

### Health Check
```bash
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "service": "Rain Protocol Mock API",
  "version": "v1-mock",
  "markets_count": 7
}
```

---

### List Markets
```bash
GET /markets?status=open&category=Crypto&limit=10
```

**Query Parameters**:
- `status`: open | closed | resolved
- `category`: Politics | Crypto | Sports | etc.
- `market_type`: binary | multiple
- `limit`: Number of results
- `offset`: Pagination

**Response**:
```json
{
  "markets": [
    {
      "market_id": "rain_binary_1",
      "title": "Will Bitcoin hit $150,000 by July 2025?",
      "description": "...",
      "category": "Crypto",
      "market_type": "binary",
      "probability": 0.66,
      "volume_24h": 222537,
      "volume_total": 5123456,
      "liquidity": 582373,
      "participant_count": 17044,
      "creator": "0x1234...5678",
      "created_at": "2026-01-15T12:00:00",
      "resolution_date": "2025-07-31T23:59:59",
      "status": "open",
      "chain": "ethereum",
      "contract_address": "0xabc123...",
      "fee_percentage": 2.0,
      "min_bet": 10.0,
      "max_bet": 100000.0,
      "outcomes": [
        {
          "name": "Yes",
          "probability": 0.66,
          "backing": 660000
        },
        {
          "name": "No",
          "probability": 0.34,
          "backing": 340000
        }
      ]
    }
  ],
  "total": 7,
  "limit": 10,
  "offset": 0
}
```

---

### Get Market Details
```bash
GET /markets/{market_id}
```

**Response**: Market object with additional fields:
- `price_history`: Array of historical probability points
- `recent_trades`: Last 10 trades on this market

---

### Get User Positions
```bash
GET /user/{user_id}/positions
```

**Response**:
```json
{
  "user_id": "0x1234...5678",
  "positions": [
    {
      "position_id": "pos_123456",
      "market_id": "rain_binary_1",
      "market_title": "Will Bitcoin hit $150,000...",
      "outcome": "Yes",
      "shares": 100,
      "avg_price": 0.55,
      "current_value": 6600.0,
      "pnl": 1100.0,
      "pnl_percentage": 20.0
    }
  ],
  "total_value": 15000.0,
  "total_pnl": 2500.0
}
```

---

### List Recent Trades
```bash
GET /trades?limit=50
```

**Response**:
```json
{
  "trades": [
    {
      "trade_id": "trade_789012",
      "timestamp": "2026-02-09T20:30:00",
      "market_id": "rain_binary_1",
      "market_title": "Will Bitcoin hit $150,000...",
      "user": "0xabcd...1234",
      "outcome": "Yes",
      "amount": 500.0,
      "price": 0.66,
      "side": "buy"
    }
  ]
}
```

---

### Get Leaderboard
```bash
GET /leaderboard?limit=10
```

**Response**:
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": "0x1234...5678",
      "username": "trader_123",
      "total_profit": 25000.0,
      "total_volume": 150000.0,
      "win_rate": 0.68,
      "markets_traded": 42,
      "reputation_score": 95
    }
  ]
}
```

---

### Platform Statistics
```bash
GET /stats
```

**Response**:
```json
{
  "total_markets": 7,
  "total_volume_24h": 1500000,
  "total_volume_all_time": 50000000,
  "total_liquidity": 5000000,
  "total_users": 45000,
  "active_users_24h": 3200,
  "markets_resolved_24h": 3,
  "avg_market_volume": 214285.71
}
```

## 🔄 BRain Integration

### RainClient Usage

```python
from rain_client import get_rain_client

# Initialize client
client = get_rain_client("http://localhost:5000/api/v1")

# Check health
health = client.health()

# List markets
markets = client.list_markets(
    category="Crypto",
    market_type="binary",
    limit=10
)

# Get market details
market = client.get_market("rain_binary_1")

# Convert to BRain format
brain_market = client.convert_to_brain_format(market)
```

### Format Conversion

Rain API returns markets with blockchain-specific fields (contract address, chain, liquidity). BRain converts these to its internal format:

**Rain Format** → **BRain Format**:
- `contract_address` → (discarded, not needed for ranking)
- `chain` → (discarded)
- `liquidity` → (discarded)
- `outcomes` → `top_options` (top 5 for multi-option)
- Adds `belief_intensity` score
- Adds `image_url` (generated from hash)

### Belief Intensity Calculation

```python
def calculate_belief_intensity(market):
    volume_score = market['volume_24h'] / 10000
    prob = market['probability']
    contestedness = 1 - abs(0.5 - prob) * 2
    return volume_score * 0.6 + contestedness * 0.4
```

## 🔧 Configuration

### Environment Variables

```bash
# Use Rain API (recommended)
export USE_RAIN_API=true
export RAIN_API_URL=http://localhost:5000/api/v1

# Use local database (fallback)
export USE_RAIN_API=false

# Other settings
export DEBUG=false
export HOST=0.0.0.0
export PORT=5555
```

### Config File

Edit `config.py`:

```python
USE_RAIN_API = True  # Toggle Rain API vs database
RAIN_API_URL = "http://localhost:5000/api/v1"  # Rain API endpoint
```

## 🧪 Testing

### Run Test Suite

```bash
# Test all Rain API endpoints
python3 test_rain_mock.py

# Test specific functionality
python3 -c "
from rain_client import get_rain_client
client = get_rain_client()
print(client.health())
"
```

### Manual Testing

```bash
# Health check
curl http://localhost:5000/api/v1/health

# List markets
curl "http://localhost:5000/api/v1/markets?limit=5" | jq .

# Get market
curl "http://localhost:5000/api/v1/markets/rain_binary_1" | jq .

# Platform stats
curl http://localhost:5000/api/v1/stats | jq .
```

## 🚀 Deployment Scenarios

### Scenario 1: Local Development (Current)

```
┌─────────────────┐
│  Rain Mock API  │ :5000
└────────┬────────┘
         │
┌────────▼────────┐
│  BRain + Flask  │ :5555
└────────┬────────┘
         │
┌────────▼────────┐
│  Currents UI    │
└─────────────────┘
```

**Setup**:
1. `python3 rain_api_mock.py` (port 5000)
2. `export USE_RAIN_API=true`
3. `python3 -m flask run --port 5555`

---

### Scenario 2: Real Rain Protocol (Future)

```
┌─────────────────┐
│  Rain Protocol  │ rain.xyz/api/v1
│  (Production)   │
└────────┬────────┘
         │ (HTTPS)
┌────────▼────────┐
│  BRain + Flask  │ :5555
└────────┬────────┘
         │
┌────────▼────────┐
│  Currents UI    │
└─────────────────┘
```

**Setup**:
1. `export RAIN_API_URL=https://api.rain.xyz/v1`
2. `export USE_RAIN_API=true`
3. `python3 -m flask run --port 5555`

---

### Scenario 3: Fallback to Database

```
┌─────────────────┐
│  SQLite (local) │
└────────┬────────┘
         │
┌────────▼────────┐
│  BRain + Flask  │ :5555
└────────┬────────┘
         │
┌────────▼────────┐
│  Currents UI    │
└─────────────────┘
```

**Setup**:
1. `export USE_RAIN_API=false`
2. `python3 -m flask run --port 5555`

## 📝 Mock Data

The mock API generates fake but realistic data:

### Markets
- 5 binary markets (Bitcoin, Trump, GPT-5, Recession, Ukraine)
- 2 multi-option markets (World Cup, $5T market cap)
- Random volumes, probabilities, participant counts
- Ethereum contract addresses (fake)

### Trades
- Random buy/sell trades
- Realistic amounts ($10-$5000)
- Recent timestamps (last 5 hours)

### Users
- Ethereum addresses (0x...)
- Random profit/loss
- Win rates (45-75%)

## 🔜 Next Steps

### When Real Rain API is Ready

1. **Update URL**:
   ```bash
   export RAIN_API_URL=https://api.rain.xyz/v1
   ```

2. **Authentication** (if required):
   ```python
   # In rain_client.py
   self.session.headers.update({
       'Authorization': f'Bearer {API_KEY}'
   })
   ```

3. **Handle Rate Limiting**:
   ```python
   # Add retry logic
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry
   ```

4. **Cache Responses**:
   ```python
   # Add caching layer (Redis)
   import redis
   cache = redis.Redis()
   ```

### BRain Enhancements

- [ ] Personalized ranking based on user interactions
- [ ] Real-time websocket updates from Rain
- [ ] Advanced filtering (tags, creators, chains)
- [ ] Historical belief current analysis
- [ ] Cross-chain market aggregation

---

## 🐛 Troubleshooting

### Mock API Not Starting

```bash
# Check if port 5000 is available
lsof -i :5000

# Kill existing process
pkill -f rain_api_mock.py

# Restart
python3 rain_api_mock.py
```

### Connection Refused

```bash
# Check API is running
curl http://localhost:5000/api/v1/health

# Check BRain config
python3 -c "import config; print(config.RAIN_API_URL)"
```

### Format Mismatch

If Rain API format changes:

1. Update `rain_client.py` conversion logic
2. Update mock data in `rain_api_mock.py`
3. Run tests: `python3 test_rain_mock.py`

---

## 📚 Resources

- **Rain Protocol**: (placeholder for real docs)
- **BRain API**: See `API.md`
- **Currents UI**: See `README.md`

---

**Built with 🌧️  + 🧠 for the Rain ecosystem**

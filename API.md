# BRain API Documentation

**Base URL**: `http://localhost:5555/api/v1` (development)  
**Version**: v1  
**Authentication**: None (for now)

## Overview

The BRain API provides RESTful access to the Currents belief intelligence layer. It ranks markets by "belief intensity" (a combination of volume and contestedness) and provides personalized feeds.

---

## Endpoints

### Health Check

```http
GET /api/v1/health
```

**Response**:
```json
{
  "status": "ok",
  "service": "BRain API",
  "version": "v1",
  "timestamp": "2026-02-09T21:00:00.000000"
}
```

---

### List Markets

```http
GET /api/v1/markets
```

**Query Parameters**:
- `category` (string, optional): Filter by category (Politics, Crypto, Sports, Technology, Markets, Economics, World, Entertainment)
- `market_type` (string, optional): Filter by type (`binary` or `multiple`)
- `limit` (integer, optional): Number of results (default: 20, max: 100)
- `offset` (integer, optional): Pagination offset (default: 0)
- `sort` (string, optional): Sort order (`belief_intensity`, `volume`, `probability`) (default: `belief_intensity`)

**Example Request**:
```bash
curl "http://localhost:5555/api/v1/markets?category=Crypto&limit=5"
```

**Response**:
```json
{
  "markets": [
    {
      "market_id": "m_eth_flip",
      "title": "Will Ethereum flip Bitcoin by market cap in 2026?",
      "description": "Whether ETH market capitalization will exceed BTC market cap at any point",
      "category": "Crypto",
      "market_type": "binary",
      "probability": 0.28,
      "volume_24h": 310000.0,
      "volume_total": 5600000.0,
      "participant_count": 15200,
      "belief_intensity": 18.82,
      "image_url": "https://...",
      "created_at": "2026-02-04 21:13:35",
      "tags": []
    }
  ],
  "total": 45,
  "limit": 5,
  "offset": 0
}
```

---

### Get Market Details

```http
GET /api/v1/markets/{market_id}
```

**Path Parameters**:
- `market_id` (string, required): Unique market identifier

**Example Request**:
```bash
curl "http://localhost:5555/api/v1/markets/m_eth_flip"
```

**Response**:
```json
{
  "market": {
    "market_id": "m_eth_flip",
    "title": "Will Ethereum flip Bitcoin by market cap in 2026?",
    "description": "Whether ETH market capitalization will exceed BTC market cap at any point",
    "category": "Crypto",
    "market_type": "binary",
    "probability": 0.28,
    "volume_24h": 310000.0,
    "volume_total": 5600000.0,
    "participant_count": 15200,
    "belief_intensity": 18.82,
    "probability_history": [
      {
        "probability": 0.25,
        "volume": 50000,
        "timestamp": "2026-02-04 21:13:35"
      },
      {
        "probability": 0.28,
        "volume": 310000,
        "timestamp": "2026-02-09 20:00:00"
      }
    ],
    "tags": ["crypto", "ethereum", "bitcoin"]
  }
}
```

For **multi-option markets**, response includes `options` array:
```json
{
  "market": {
    "market_id": "m_superbowl2027",
    "market_type": "multiple",
    "options": [
      {
        "option_id": "nfl_chiefs",
        "option_text": "Kansas City Chiefs",
        "probability": 0.09
      },
      {
        "option_id": "nfl_49ers",
        "option_text": "San Francisco 49ers",
        "probability": 0.08
      }
    ]
  }
}
```

---

### Get Feed

```http
GET /api/v1/feed
```

Returns markets ranked by belief intensity, organized into hero/grid/stream sections.

**Query Parameters**:
- `personalized` (boolean, optional): Enable personalized ranking (coming soon)

**Example Request**:
```bash
curl "http://localhost:5555/api/v1/feed"
```

**Response**:
```json
{
  "hero": [
    {
      "market_id": "m_superbowl2027",
      "title": "Who will win Super Bowl LXI (2027)?",
      "belief_intensity": 18.67,
      "top_options": [
        {"option_text": "Other Team", "probability": 0.22},
        {"option_text": "Kansas City Chiefs", "probability": 0.09}
      ]
    }
  ],
  "grid": [
    /* 8 markets ranked by belief_intensity */
  ],
  "stream": [
    /* 21 more markets */
  ]
}
```

---

### Get Categories

```http
GET /api/v1/categories
```

Returns list of all categories with market counts.

**Response**:
```json
{
  "categories": [
    {"category": "Politics", "count": 12},
    {"category": "Crypto", "count": 8},
    {"category": "Sports", "count": 7},
    {"category": "Technology", "count": 6}
  ]
}
```

---

### Get Trending

```http
GET /api/v1/trending
```

Returns markets with highest recent activity (24h volume).

**Response**:
```json
{
  "trending": [
    {
      "market_id": "m_eth_flip",
      "title": "Will Ethereum flip Bitcoin by market cap in 2026?",
      "volume_24h": 310000.0
    }
  ]
}
```

---

## Coming Soon

### Search Markets
```http
GET /api/v1/search?q=query
```
Full-text search across market titles and descriptions.

### Personalized Feed
```http
GET /api/v1/user/{user_id}/feed
```
Feed personalized based on user interactions and preferences.

---

## BRain Algorithm

**Belief Intensity** is calculated as:

```
belief_intensity = (volume_score * 0.6) + (contestedness * 0.4)

where:
  volume_score = volume_24h / 10000
  contestedness = 1 - |0.5 - probability| * 2
```

This algorithm surfaces markets that are:
1. **High volume** (lots of activity)
2. **Contested** (probability near 50%, not obvious)

Markets with both qualities create the most interesting belief currents.

---

## Error Responses

**404 Not Found**:
```json
{
  "error": "Market not found"
}
```

**400 Bad Request**:
```json
{
  "error": "Invalid parameter value"
}
```

---

## Rate Limiting

Currently: **No rate limiting** (development)  
Production: **100 requests/minute** (planned)

---

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for all origins in development.

---

## Example Use Cases

### 1. Build a Custom Dashboard
```javascript
// Fetch crypto markets
fetch('http://localhost:5555/api/v1/markets?category=Crypto&limit=10')
  .then(res => res.json())
  .then(data => {
    data.markets.forEach(market => {
      console.log(`${market.title}: ${market.probability}`)
    });
  });
```

### 2. Monitor Trending Topics
```python
import requests

response = requests.get('http://localhost:5555/api/v1/trending')
trending = response.json()['trending']

for market in trending:
    print(f"{market['title']} - {market['volume_24h']} volume")
```

### 3. Track Specific Market
```bash
# Watch probability changes
watch -n 60 'curl -s http://localhost:5555/api/v1/markets/m_eth_flip | jq ".market.probability"'
```

---

## Changelog

### v1 (2026-02-09)
- Initial release
- Basic CRUD endpoints
- BRain ranking algorithm
- Feed generation
- Category filtering

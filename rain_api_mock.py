"""
Mock Rain Protocol API
Simulates the Rain protocol endpoints with fake data
This establishes the integration pattern for the real API

Run on port 5000: python3 rain_api_mock.py
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Fake data store
FAKE_MARKETS = {}
FAKE_POSITIONS = {}
FAKE_TRADES = []
FAKE_USERS = {}

def generate_fake_markets():
    """Generate fake market data"""
    markets = []
    
    # Binary markets
    binary_topics = [
        ("Will Bitcoin hit $150,000 by July 2025?", "Crypto", 0.66),
        ("Will Trump win the 2024 election?", "Politics", 0.58),
        ("Will OpenAI release GPT-5 in 2026?", "Technology", 0.71),
        ("Will recession hit US in 2026?", "Economics", 0.44),
        ("Will Ukraine retake Crimea by 2025?", "World", 0.23),
    ]
    
    for i, (title, category, prob) in enumerate(binary_topics):
        market_id = f"rain_binary_{i+1}"
        markets.append({
            "market_id": market_id,
            "title": title,
            "description": f"Prediction market: {title}",
            "category": category,
            "market_type": "binary",
            "probability": prob,
            "volume_24h": random.randint(50000, 500000),
            "volume_total": random.randint(1000000, 10000000),
            "liquidity": random.randint(100000, 1000000),
            "participant_count": random.randint(1000, 20000),
            "creator": f"0x{random.randint(1000, 9999):04x}...{random.randint(1000, 9999):04x}",
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "resolution_date": (datetime.now() + timedelta(days=random.randint(30, 180))).isoformat(),
            "status": "open",
            "chain": "ethereum",
            "contract_address": f"0x{random.randint(100000000, 999999999):09x}",
            "fee_percentage": 2.0,
            "min_bet": 10.0,
            "max_bet": 100000.0,
            "outcomes": [
                {"name": "Yes", "probability": prob, "backing": prob * 1000000},
                {"name": "No", "probability": 1-prob, "backing": (1-prob) * 1000000}
            ]
        })
    
    # Multi-option markets
    multi_markets = [
        {
            "title": "Who will win the 2026 World Cup?",
            "category": "Sports",
            "options": [
                ("Brazil", 0.18),
                ("France", 0.16),
                ("Argentina", 0.15),
                ("England", 0.12),
                ("Spain", 0.10),
                ("Germany", 0.08),
                ("Other", 0.21)
            ]
        },
        {
            "title": "Which company will reach $5T market cap first?",
            "category": "Markets",
            "options": [
                ("Apple", 0.35),
                ("Microsoft", 0.30),
                ("Nvidia", 0.20),
                ("Google", 0.10),
                ("Other", 0.05)
            ]
        }
    ]
    
    for i, market_spec in enumerate(multi_markets):
        market_id = f"rain_multi_{i+1}"
        outcomes = [
            {
                "name": opt[0],
                "probability": opt[1],
                "backing": opt[1] * 2000000
            }
            for opt in market_spec["options"]
        ]
        
        markets.append({
            "market_id": market_id,
            "title": market_spec["title"],
            "description": f"Prediction market: {market_spec['title']}",
            "category": market_spec["category"],
            "market_type": "multiple",
            "probability": market_spec["options"][0][1],  # Top option
            "volume_24h": random.randint(100000, 800000),
            "volume_total": random.randint(2000000, 15000000),
            "liquidity": random.randint(200000, 2000000),
            "participant_count": random.randint(2000, 30000),
            "creator": f"0x{random.randint(1000, 9999):04x}...{random.randint(1000, 9999):04x}",
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "resolution_date": (datetime.now() + timedelta(days=random.randint(60, 365))).isoformat(),
            "status": "open",
            "chain": "ethereum",
            "contract_address": f"0x{random.randint(100000000, 999999999):09x}",
            "fee_percentage": 2.5,
            "min_bet": 10.0,
            "max_bet": 100000.0,
            "outcomes": outcomes
        })
    
    return {m["market_id"]: m for m in markets}

# Initialize fake data
FAKE_MARKETS = generate_fake_markets()

@app.route('/api/v1/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "ok",
        "service": "Rain Protocol Mock API",
        "version": "v1-mock",
        "timestamp": datetime.utcnow().isoformat(),
        "markets_count": len(FAKE_MARKETS)
    })

@app.route('/api/v1/markets', methods=['GET'])
def list_markets():
    """
    List all markets
    Query params: status, category, market_type, limit, offset
    """
    status = request.args.get('status', 'open')
    category = request.args.get('category')
    market_type = request.args.get('market_type')
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    # Filter markets
    filtered = list(FAKE_MARKETS.values())
    
    if status:
        filtered = [m for m in filtered if m['status'] == status]
    if category:
        filtered = [m for m in filtered if m['category'] == category]
    if market_type:
        filtered = [m for m in filtered if m['market_type'] == market_type]
    
    # Sort by volume (most active first)
    filtered.sort(key=lambda x: x['volume_24h'], reverse=True)
    
    # Paginate
    paginated = filtered[offset:offset + limit]
    
    return jsonify({
        "markets": paginated,
        "total": len(filtered),
        "limit": limit,
        "offset": offset
    })

@app.route('/api/v1/markets/<market_id>', methods=['GET'])
def get_market(market_id):
    """Get market details"""
    if market_id not in FAKE_MARKETS:
        return jsonify({"error": "Market not found"}), 404
    
    market = FAKE_MARKETS[market_id].copy()
    
    # Add fake price history
    history = []
    start_prob = market['outcomes'][0]['probability']
    for i in range(20):
        timestamp = datetime.now() - timedelta(hours=20-i)
        prob = start_prob + random.uniform(-0.1, 0.1)
        prob = max(0.05, min(0.95, prob))  # Keep in range
        history.append({
            "timestamp": timestamp.isoformat(),
            "probability": round(prob, 4),
            "volume": random.randint(1000, 50000)
        })
    
    market['price_history'] = history
    
    # Add recent trades
    trades = []
    for i in range(10):
        trades.append({
            "trade_id": f"trade_{random.randint(100000, 999999)}",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
            "user": f"0x{random.randint(1000, 9999):04x}...{random.randint(1000, 9999):04x}",
            "outcome": random.choice(market['outcomes'])['name'],
            "amount": round(random.uniform(10, 1000), 2),
            "price": round(random.uniform(0.3, 0.7), 4),
            "side": random.choice(["buy", "sell"])
        })
    
    market['recent_trades'] = sorted(trades, key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({"market": market})

@app.route('/api/v1/user/<user_id>/positions', methods=['GET'])
def get_user_positions(user_id):
    """Get user positions"""
    # Generate fake positions
    positions = []
    for market_id, market in list(FAKE_MARKETS.items())[:3]:
        positions.append({
            "position_id": f"pos_{random.randint(100000, 999999)}",
            "market_id": market_id,
            "market_title": market['title'],
            "outcome": market['outcomes'][0]['name'],
            "shares": random.randint(10, 1000),
            "avg_price": round(random.uniform(0.3, 0.7), 4),
            "current_value": round(random.uniform(100, 5000), 2),
            "pnl": round(random.uniform(-500, 1000), 2),
            "pnl_percentage": round(random.uniform(-20, 50), 2)
        })
    
    return jsonify({
        "user_id": user_id,
        "positions": positions,
        "total_value": sum(p['current_value'] for p in positions),
        "total_pnl": sum(p['pnl'] for p in positions)
    })

@app.route('/api/v1/trades', methods=['GET'])
def list_trades():
    """Get recent trades across all markets"""
    limit = int(request.args.get('limit', 50))
    
    # Generate fake recent trades
    trades = []
    for _ in range(limit):
        market_id = random.choice(list(FAKE_MARKETS.keys()))
        market = FAKE_MARKETS[market_id]
        
        trades.append({
            "trade_id": f"trade_{random.randint(100000, 999999)}",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 300))).isoformat(),
            "market_id": market_id,
            "market_title": market['title'],
            "user": f"0x{random.randint(1000, 9999):04x}...{random.randint(1000, 9999):04x}",
            "outcome": random.choice(market['outcomes'])['name'],
            "amount": round(random.uniform(10, 5000), 2),
            "price": round(random.uniform(0.2, 0.8), 4),
            "side": random.choice(["buy", "sell"])
        })
    
    trades.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({"trades": trades})

@app.route('/api/v1/leaderboard', methods=['GET'])
def leaderboard():
    """Get top traders"""
    limit = int(request.args.get('limit', 10))
    
    # Generate fake leaderboard
    traders = []
    for i in range(limit):
        traders.append({
            "rank": i + 1,
            "user_id": f"0x{random.randint(1000, 9999):04x}...{random.randint(1000, 9999):04x}",
            "username": f"trader_{random.randint(100, 999)}",
            "total_profit": round(random.uniform(1000, 50000), 2),
            "total_volume": round(random.uniform(10000, 500000), 2),
            "win_rate": round(random.uniform(0.45, 0.75), 2),
            "markets_traded": random.randint(5, 100),
            "reputation_score": random.randint(50, 100)
        })
    
    return jsonify({"leaderboard": traders})

@app.route('/api/v1/stats', methods=['GET'])
def platform_stats():
    """Get platform-wide statistics"""
    return jsonify({
        "total_markets": len(FAKE_MARKETS),
        "total_volume_24h": sum(m['volume_24h'] for m in FAKE_MARKETS.values()),
        "total_volume_all_time": sum(m['volume_total'] for m in FAKE_MARKETS.values()),
        "total_liquidity": sum(m['liquidity'] for m in FAKE_MARKETS.values()),
        "total_users": random.randint(10000, 100000),
        "active_users_24h": random.randint(1000, 10000),
        "markets_resolved_24h": random.randint(1, 10),
        "avg_market_volume": round(sum(m['volume_24h'] for m in FAKE_MARKETS.values()) / len(FAKE_MARKETS), 2)
    })

@app.route('/api/v1/trade', methods=['POST'])
def place_trade():
    """Simulated trade placement - checks balance but doesn't execute on chain"""
    data = request.get_json()
    
    # Required fields
    market_id = data.get('market_id')
    outcome = data.get('outcome')
    amount = float(data.get('amount', 0))
    wallet_address = data.get('wallet_address')
    wallet_balance = float(data.get('wallet_balance', 0))
    
    # Validation
    if not all([market_id, outcome, amount, wallet_address]):
        return jsonify({
            "success": False,
            "error": "Missing required fields: market_id, outcome, amount, wallet_address"
        }), 400
    
    # Check if enough balance
    if amount > wallet_balance:
        return jsonify({
            "success": False,
            "error": f"Insufficient balance. You have {wallet_balance} ETH but need {amount} ETH",
            "balance_check": False
        }), 400
    
    # Simulate successful trade
    trade_id = f"trade_{random.randint(100000, 999999)}"
    execution_price = round(random.uniform(0.4, 0.7), 4)
    shares = round(amount / execution_price, 2)
    
    # Store fake trade
    fake_trade = {
        "trade_id": trade_id,
        "market_id": market_id,
        "outcome": outcome,
        "amount": amount,
        "shares": shares,
        "execution_price": execution_price,
        "wallet_address": wallet_address,
        "timestamp": datetime.now().isoformat(),
        "status": "simulated"  # Not a real blockchain transaction
    }
    FAKE_TRADES.append(fake_trade)
    
    return jsonify({
        "success": True,
        "trade": fake_trade,
        "balance_check": True,
        "message": f"Trade simulated successfully! Bought {shares} shares of '{outcome}' for {amount} ETH"
    }), 200

if __name__ == '__main__':
    print("🌧️  Rain Protocol Mock API starting...")
    print("📊 Generated {} fake markets".format(len(FAKE_MARKETS)))
    print("🚀 Running on http://0.0.0.0:5000")
    print("📖 Endpoints:")
    print("   GET  /api/v1/health")
    print("   GET  /api/v1/markets")
    print("   GET  /api/v1/markets/{market_id}")
    print("   GET  /api/v1/user/{user_id}/positions")
    print("   GET  /api/v1/trades")
    print("   GET  /api/v1/leaderboard")
    print("   GET  /api/v1/stats")
    print("   POST /api/v1/trade (simulated trading)")
    app.run(host='0.0.0.0', port=5000, debug=False)

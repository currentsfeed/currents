#!/usr/bin/env python3
"""
Rain API - Standalone Market Data Service
Port 5000 - Provides market data to BRain personalization engine
"""
from flask import Flask, jsonify, request
import sqlite3
from typing import Optional, List
import os

app = Flask(__name__)
RAIN_DB = 'rain.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(RAIN_DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Rain API', 'version': '1.0'})

@app.route('/api/v1/markets', methods=['GET'])
def get_markets():
    """
    Get markets with filters
    Query params:
    - status: open/closed/all (default: open)
    - category: filter by category
    - limit: max results (default: 100)
    - offset: pagination offset (default: 0)
    - ids: comma-separated market IDs
    """
    status = request.args.get('status', 'open')
    category = request.args.get('category')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    ids = request.args.get('ids')  # comma-separated
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Build query
    query = """
        SELECT m.*,
               GROUP_CONCAT(DISTINCT mt.tag) as tags
        FROM markets m
        LEFT JOIN market_tags mt ON m.market_id = mt.market_id
    """
    
    conditions = []
    params = []
    
    if status != 'all':
        conditions.append("m.status = ?")
        params.append(status)
    
    if category:
        conditions.append("m.category = ?")
        params.append(category)
    
    if ids:
        id_list = [id.strip() for id in ids.split(',')]
        placeholders = ','.join('?' * len(id_list))
        conditions.append(f"m.market_id IN ({placeholders})")
        params.extend(id_list)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " GROUP BY m.market_id ORDER BY m.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    
    markets = []
    for row in cursor.fetchall():
        market = dict(row)
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        markets.append(market)
    
    conn.close()
    
    return jsonify({
        'markets': markets,
        'count': len(markets),
        'limit': limit,
        'offset': offset
    })

@app.route('/api/v1/markets/<market_id>', methods=['GET'])
def get_market(market_id: str):
    """Get single market by ID with full details including options"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get market
    cursor.execute("""
        SELECT m.*,
               GROUP_CONCAT(DISTINCT mt.tag) as tags
        FROM markets m
        LEFT JOIN market_tags mt ON m.market_id = mt.market_id
        WHERE m.market_id = ?
        GROUP BY m.market_id
    """, (market_id,))
    
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Market not found'}), 404
    
    market = dict(row)
    market['tags'] = market['tags'].split(',') if market['tags'] else []
    
    # Get options if multi-option market
    if market.get('market_type') == 'multi':
        cursor.execute("""
            SELECT * FROM market_options
            WHERE market_id = ?
            ORDER BY position
        """, (market_id,))
        
        market['options'] = [dict(opt) for opt in cursor.fetchall()]
    else:
        market['options'] = []
    
    # Get probability history (last 24 hours)
    cursor.execute("""
        SELECT probability, volume, timestamp
        FROM probability_history
        WHERE market_id = ?
        ORDER BY timestamp DESC
        LIMIT 100
    """, (market_id,))
    
    market['probability_history'] = [dict(h) for h in cursor.fetchall()]
    
    conn.close()
    
    return jsonify(market)

@app.route('/api/v1/markets/batch', methods=['POST'])
def get_markets_batch():
    """
    Get multiple markets by IDs
    Body: {"market_ids": ["id1", "id2", ...]}
    """
    data = request.get_json()
    market_ids = data.get('market_ids', [])
    
    if not market_ids:
        return jsonify({'error': 'No market_ids provided'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    placeholders = ','.join('?' * len(market_ids))
    query = f"""
        SELECT m.*,
               GROUP_CONCAT(DISTINCT mt.tag) as tags
        FROM markets m
        LEFT JOIN market_tags mt ON m.market_id = mt.market_id
        WHERE m.market_id IN ({placeholders})
        GROUP BY m.market_id
    """
    
    cursor.execute(query, market_ids)
    
    markets = []
    for row in cursor.fetchall():
        market = dict(row)
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        markets.append(market)
    
    conn.close()
    
    return jsonify({
        'markets': markets,
        'count': len(markets)
    })

@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    """Get list of all categories with counts"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM markets
        WHERE status = 'open'
        GROUP BY category
        ORDER BY count DESC
    """)
    
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'categories': categories})

@app.route('/api/v1/tags', methods=['GET'])
def get_tags():
    """Get list of all tags with counts"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT mt.tag, COUNT(DISTINCT mt.market_id) as count
        FROM market_tags mt
        JOIN markets m ON mt.market_id = m.market_id
        WHERE m.status = 'open'
        GROUP BY mt.tag
        ORDER BY count DESC
        LIMIT 100
    """)
    
    tags = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'tags': tags})

@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Get overall Rain API statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM markets WHERE status = 'open'")
    open_markets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM markets WHERE status = 'closed'")
    closed_markets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT category) FROM markets")
    categories = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT tag) FROM market_tags")
    tags = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'open_markets': open_markets,
        'closed_markets': closed_markets,
        'total_markets': open_markets + closed_markets,
        'categories': categories,
        'tags': tags
    })

if __name__ == '__main__':
    # Check if rain.db exists
    if not os.path.exists(RAIN_DB):
        print(f"ERROR: {RAIN_DB} not found!")
        print("Run migrate_to_rain.py first")
        exit(1)
    
    print("🌧️  Starting Rain API on http://localhost:5001")
    print(f"📊 Database: {RAIN_DB}")
    app.run(host='0.0.0.0', port=5001, debug=False)

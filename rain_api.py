#!/usr/bin/env python3
"""
Rain Protocol API (Mock)
Port 5000 - Market data source of truth
Separate from BRain intelligence layer
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import logging
from typing import List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Allow all origins (this is a mock API)

DB_PATH = 'rain.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row) -> dict:
    """Convert sqlite3.Row to dict"""
    return dict(zip(row.keys(), row))

@app.route('/api/v1/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM markets")
        count = cursor.fetchone()['count']
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'service': 'Rain Protocol API',
            'version': '1.0.0',
            'markets_count': count
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/v1/markets', methods=['GET'])
def get_markets():
    """
    Get list of markets with optional filters
    Query params:
      - category: Filter by category
      - status: Filter by status (open, closed, resolved)
      - limit: Max number of results (default 100)
      - offset: Pagination offset (default 0)
      - search: Search in title/description
    """
    try:
        # Get query parameters
        category = request.args.get('category')
        status = request.args.get('status', 'open')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        search = request.args.get('search')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM markets WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if search:
            query += " AND (title LIKE ? OR description LIKE ?)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        markets = [dict_from_row(row) for row in cursor.fetchall()]
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM markets WHERE 1=1"
        count_params = []
        if category:
            count_query += " AND category = ?"
            count_params.append(category)
        if status:
            count_query += " AND status = ?"
            count_params.append(status)
        if search:
            count_query += " AND (title LIKE ? OR description LIKE ?)"
            count_params.extend([search_term, search_term])
        
        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']
        
        conn.close()
        
        logger.info(f"GET /api/v1/markets - returned {len(markets)}/{total} markets")
        
        return jsonify({
            'markets': markets,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'returned': len(markets)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in get_markets: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/markets/<market_id>', methods=['GET'])
def get_market(market_id: str):
    """Get single market by ID with options if multi-option"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get market
        cursor.execute("SELECT * FROM markets WHERE market_id = ?", (market_id,))
        market_row = cursor.fetchone()
        
        if not market_row:
            conn.close()
            return jsonify({'error': 'Market not found'}), 404
        
        market = dict_from_row(market_row)
        
        # Get options if multi-option market
        if market.get('market_type') == 'multiple':
            cursor.execute("""
                SELECT * FROM market_options 
                WHERE market_id = ? 
                ORDER BY probability DESC
            """, (market_id,))
            options = [dict_from_row(row) for row in cursor.fetchall()]
            market['options'] = options
        
        # Get tags
        cursor.execute("SELECT tag FROM market_tags WHERE market_id = ?", (market_id,))
        tags = [row['tag'] for row in cursor.fetchall()]
        if tags:
            market['tags'] = tags
        
        conn.close()
        
        logger.info(f"GET /api/v1/markets/{market_id} - found")
        return jsonify(market)
        
    except Exception as e:
        logger.error(f"Error in get_market: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/markets/batch', methods=['POST'])
def get_markets_batch():
    """
    Get multiple markets by IDs
    Body: {"market_ids": ["id1", "id2", ...]}
    """
    try:
        data = request.get_json()
        market_ids = data.get('market_ids', [])
        
        if not market_ids:
            return jsonify({'error': 'market_ids required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build query with placeholders
        placeholders = ','.join('?' * len(market_ids))
        query = f"SELECT * FROM markets WHERE market_id IN ({placeholders})"
        
        cursor.execute(query, market_ids)
        markets = [dict_from_row(row) for row in cursor.fetchall()]
        
        # Get options for multi-option markets
        for market in markets:
            if market.get('market_type') == 'multiple':
                cursor.execute("""
                    SELECT * FROM market_options 
                    WHERE market_id = ? 
                    ORDER BY probability DESC
                """, (market['market_id'],))
                market['options'] = [dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        logger.info(f"POST /api/v1/markets/batch - returned {len(markets)}/{len(market_ids)} markets")
        
        return jsonify({
            'markets': markets,
            'requested': len(market_ids),
            'found': len(markets)
        })
        
    except Exception as e:
        logger.error(f"Error in get_markets_batch: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/markets/<market_id>/history', methods=['GET'])
def get_market_history(market_id: str):
    """Get probability history for a market"""
    try:
        limit = int(request.args.get('limit', 100))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if market exists
        cursor.execute("SELECT 1 FROM markets WHERE market_id = ?", (market_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Market not found'}), 404
        
        # Get history
        cursor.execute("""
            SELECT probability, timestamp 
            FROM probability_history 
            WHERE market_id = ? 
            ORDER BY timestamp ASC
            LIMIT ?
        """, (market_id, limit))
        
        history = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'market_id': market_id,
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        logger.error(f"Error in get_market_history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    """Get list of all categories with market counts"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM markets
            WHERE status = 'open'
            GROUP BY category
            ORDER BY count DESC
        """)
        
        categories = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'categories': categories,
            'total': len(categories)
        })
        
    except Exception as e:
        logger.error(f"Error in get_categories: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🌊 RAIN PROTOCOL API")
    print("="*80)
    print("Port: 5000")
    print("Database: rain.db")
    print("CORS: Enabled (all origins)")
    print("\nEndpoints:")
    print("  GET  /api/v1/health")
    print("  GET  /api/v1/markets")
    print("  GET  /api/v1/markets/:id")
    print("  POST /api/v1/markets/batch")
    print("  GET  /api/v1/markets/:id/history")
    print("  GET  /api/v1/categories")
    print("="*80 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

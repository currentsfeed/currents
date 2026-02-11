"""
BRain API - RESTful endpoints for Currents intelligence layer
Provides ranked belief currents, market data, and personalization
"""
from flask import Blueprint, jsonify, request
import sqlite3
import os
from datetime import datetime
from brain_algorithm import calculate_belief_intensity

api = Blueprint('api', __name__, url_prefix='/api/v1')

DB_PATH = os.path.join(os.path.dirname(__file__), 'brain.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'BRain API',
        'version': 'v1',
        'timestamp': datetime.utcnow().isoformat()
    })

@api.route('/markets', methods=['GET'])
def list_markets():
    """
    GET /api/v1/markets
    Query params:
      - category: Filter by category (Politics, Crypto, Sports, etc.)
      - market_type: Filter by type (binary, multiple)
      - limit: Number of results (default 20, max 100)
      - offset: Pagination offset
      - sort: Sort order (belief_intensity, volume, probability)
    """
    # Parse and validate query parameters
    try:
        category = request.args.get('category')
        market_type = request.args.get('market_type')
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        sort_by = request.args.get('sort', 'belief_intensity')
        
        # Validate pagination
        if limit < 1 or offset < 0:
            return jsonify({'error': 'Invalid pagination parameters'}), 400
        
        # Validate sort_by
        allowed_sorts = {'belief_intensity', 'volume', 'probability'}
        if sort_by not in allowed_sorts:
            return jsonify({'error': f'Invalid sort field. Allowed: {", ".join(allowed_sorts)}'}), 400
            
    except ValueError as e:
        return jsonify({'error': f'Invalid query parameters: {str(e)}'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Build query
    query = """
        SELECT m.*, 
               GROUP_CONCAT(DISTINCT mt.tag) as tags
        FROM markets m
        LEFT JOIN market_tags mt ON m.market_id = mt.market_id
        WHERE m.status = 'open'
    """
    params = []
    
    if category:
        query += " AND m.category = ?"
        params.append(category)
    
    if market_type:
        query += " AND m.market_type = ?"
        params.append(market_type)
    
    query += " GROUP BY m.market_id"
    
    cursor.execute(query, params)
    
    # Fetch and rank markets
    markets = []
    for row in cursor.fetchall():
        market = dict(row)
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        market['belief_intensity'] = calculate_belief_intensity(market)
        
        # Fetch options for multi-option markets
        if market.get('market_type') == 'multiple':
            cursor.execute("""
                SELECT option_id, option_text, probability
                FROM market_options
                WHERE market_id = ?
                ORDER BY probability DESC
            """, (market['market_id'],))
            market['options'] = [dict(opt) for opt in cursor.fetchall()]
        
        markets.append(market)
    
    # Sort
    if sort_by == 'belief_intensity':
        markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
    elif sort_by == 'volume':
        markets.sort(key=lambda x: x['volume_24h'], reverse=True)
    elif sort_by == 'probability':
        markets.sort(key=lambda x: x['probability'], reverse=True)
    
    # Paginate
    paginated = markets[offset:offset + limit]
    
    conn.close()
    
    return jsonify({
        'markets': paginated,
        'total': len(markets),
        'limit': limit,
        'offset': offset
    })

@api.route('/markets/<market_id>', methods=['GET'])
def get_market(market_id):
    """
    GET /api/v1/markets/{market_id}
    Returns detailed market information including history
    """
    conn = get_db()
    cursor = conn.cursor()
    
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
    market['belief_intensity'] = calculate_belief_intensity(market)
    
    # Get probability history
    cursor.execute("""
        SELECT probability, volume, timestamp
        FROM probability_history
        WHERE market_id = ?
        ORDER BY timestamp ASC
    """, (market_id,))
    market['probability_history'] = [dict(row) for row in cursor.fetchall()]
    
    # Get options for multi-option markets
    if market.get('market_type') == 'multiple':
        cursor.execute("""
            SELECT option_id, option_text, probability
            FROM market_options
            WHERE market_id = ?
            ORDER BY probability DESC
        """, (market_id,))
        market['options'] = [dict(opt) for opt in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({'market': market})

@api.route('/feed', methods=['GET'])
def get_feed():
    """
    GET /api/v1/feed
    Returns ranked feed: hero, grid, stream
    Query params:
      - personalized: Boolean (future: user-based ranking)
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.*, 
               GROUP_CONCAT(DISTINCT mt.tag) as tags
        FROM markets m
        LEFT JOIN market_tags mt ON m.market_id = mt.market_id
        WHERE m.status = 'open'
        GROUP BY m.market_id
    """)
    
    markets = []
    for row in cursor.fetchall():
        market = dict(row)
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        market['belief_intensity'] = calculate_belief_intensity(market)
        
        # Fetch options for multi-option markets
        if market.get('market_type') == 'multiple':
            cursor.execute("""
                SELECT option_id, option_text, probability
                FROM market_options
                WHERE market_id = ?
                ORDER BY probability DESC
                LIMIT 5
            """, (market['market_id'],))
            market['top_options'] = [dict(opt) for opt in cursor.fetchall()]
        
        markets.append(market)
    
    markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
    
    conn.close()
    
    return jsonify({
        'hero': markets[0:1] if markets else [],
        'grid': markets[1:9] if len(markets) > 1 else [],
        'stream': markets[9:30] if len(markets) > 9 else []
    })

@api.route('/categories', methods=['GET'])
def get_categories():
    """
    GET /api/v1/categories
    Returns list of categories with market counts
    """
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

@api.route('/trending', methods=['GET'])
def get_trending():
    """
    GET /api/v1/trending
    Returns markets with highest recent activity
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.*
        FROM markets m
        WHERE m.status = 'open'
        ORDER BY m.volume_24h DESC
        LIMIT 10
    """)
    
    trending = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'trending': trending})

# Future endpoints (stubs for now)
@api.route('/search', methods=['GET'])
def search():
    """
    GET /api/v1/search?q=query
    Search markets by title/description
    """
    query = request.args.get('q', '')
    # TODO: Implement full-text search
    return jsonify({'results': [], 'query': query})

@api.route('/user/<user_id>/feed', methods=['GET'])
def personalized_feed(user_id):
    """
    GET /api/v1/user/{user_id}/feed
    Personalized feed based on user interactions
    """
    # TODO: Implement personalization algorithm
    return jsonify({'message': 'Personalization coming soon', 'user_id': user_id})

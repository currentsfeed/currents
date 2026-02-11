"""
Currents Full Stack - Local Development
Combines BRain database + Flask API + Frontend
Supports both local SQLite and Rain Protocol API
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import logging
from collections import defaultdict

# Import config and Rain client
from config import USE_RAIN_API, RAIN_API_URL
from rain_client import RainClient
from brain_algorithm import calculate_belief_intensity
from tracking_engine import tracker
from personalization import personalizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS configuration - only allow specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://*.loca.lt",      # For localtunnel deployment
            "http://localhost:*",     # For local development
            "http://127.0.0.1:*"      # For local development
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Register API blueprint
from api import api as api_blueprint
app.register_blueprint(api_blueprint)

# Database path (used when USE_RAIN_API = False)
DB_PATH = os.path.join(os.path.dirname(__file__), 'brain.db')

# Initialize Rain client (used when USE_RAIN_API = True)
rain_client = RainClient(RAIN_API_URL) if USE_RAIN_API else None

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}", exc_info=True)
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return "Internal server error", 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return "Something went wrong", 500

# Request/response logging
@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"{request.method} {request.path}")

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.debug(f"{request.method} {request.path} -> {response.status_code}")
    return response

# Template filters
@app.template_filter('format_number')
def format_number(value):
    """Format numbers with commas"""
    try:
        return "{:,}".format(int(value))
    except:
        return value

@app.template_filter('category_color')
def category_color(category):
    """Return colored background with black text for category badges"""
    colors = {
        'Sports': 'bg-green-400 text-black',
        'Politics': 'bg-orange-400 text-black',
        'Economics': 'bg-blue-400 text-black',
        'Technology': 'bg-purple-400 text-black',
        'Entertainment': 'bg-pink-400 text-black',
        'Crypto': 'bg-yellow-400 text-black',
        'Crime': 'bg-red-400 text-black',
        'World': 'bg-cyan-400 text-black',
        'Culture': 'bg-indigo-400 text-black',
    }
    return colors.get(category, 'bg-orange-400 text-black')

@app.template_filter('option_color')
def option_color(index):
    """Return diverse gradient colors for multi-option markets"""
    colors = [
        'from-blue-500 to-blue-400',      # Blue
        'from-purple-500 to-purple-400',  # Purple
        'from-green-500 to-green-400',    # Green
        'from-yellow-500 to-yellow-400',  # Yellow
        'from-red-500 to-red-400',        # Red
        'from-pink-500 to-pink-400',      # Pink
        'from-indigo-500 to-indigo-400',  # Indigo
        'from-teal-500 to-teal-400',      # Teal
    ]
    return colors[index % len(colors)]

# REMOVED DUPLICATE - category_color filter already defined above (line 99)

@app.template_filter('belief_gradient')
def belief_gradient(market):
    """Generate dynamic gradient based on market behavior and option colors"""
    import hashlib
    
    # For multi-option markets, use the actual option colors
    if market.get('market_type') == 'multiple' and market.get('top_options'):
        # Get color hex codes for each option
        color_map = {
            0: '#3B82F6',  # blue-500
            1: '#A855F7',  # purple-500
            2: '#10B981',  # green-500
            3: '#EAB308',  # yellow-500
            4: '#EF4444',  # red-500
            5: '#EC4899',  # pink-500
            6: '#6366F1',  # indigo-500
            7: '#14B8A6',  # teal-500
        }
        
        # Create gradient showing transitions between top 3 options
        opts = market['top_options'][:3]
        if len(opts) >= 3:
            c1 = color_map[0]  # First option color
            c2 = color_map[1]  # Second option color
            c3 = color_map[2]  # Third option color
            
            # Gradient shows evolution: started with option 3, moved to 2, now leading is 1
            return f"linear-gradient(to right, {c3} 0%, {c2} 35%, {c1} 70%, {c1} 100%)"
        else:
            return "linear-gradient(to right, #3B82F6 0%, #A855F7 50%, #10B981 100%)"
    
    # For binary markets, use traditional Yes/No colors
    seed = int(hashlib.md5(market['market_id'].encode()).hexdigest()[:8], 16)
    prob = market['probability']
    
    patterns = {
        'strong_yes': "linear-gradient(to right, #F59E0B 0%, #10B981 15%, #10B981 60%, #22C55E 100%)",
        'rising_yes': "linear-gradient(to right, #EF4444 0%, #F59E0B 25%, #10B981 60%, #22C55E 100%)",
        'contested': "linear-gradient(to right, #EF4444 0%, #F59E0B 20%, #10B981 40%, #F59E0B 60%, #EF4444 80%, #F59E0B 100%)",
        'declining_no': "linear-gradient(to right, #10B981 0%, #F59E0B 30%, #EF4444 70%, #DC2626 100%)",
        'strong_no': "linear-gradient(to right, #F59E0B 0%, #EF4444 20%, #EF4444 60%, #DC2626 100%)",
        'volatile': "linear-gradient(to right, #10B981 0%, #F59E0B 15%, #EF4444 30%, #F59E0B 50%, #10B981 70%, #F59E0B 85%, #EF4444 100%)",
    }
    
    if prob > 0.75:
        options = ['strong_yes', 'rising_yes']
    elif prob > 0.6:
        options = ['rising_yes', 'strong_yes']
    elif prob > 0.4:
        options = ['contested', 'volatile']
    elif prob > 0.25:
        options = ['declining_no', 'contested']
    else:
        options = ['strong_no', 'declining_no']
    
    pattern_key = options[seed % len(options)]
    return patterns[pattern_key]

@app.template_filter('timeline_points')
def timeline_points(created_at):
    """Generate 5 evenly-spaced timeline points from market start to now"""
    from datetime import datetime, timedelta
    
    try:
        # Parse created_at
        if isinstance(created_at, str):
            start = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        else:
            start = created_at
        
        now = datetime.now()
        delta = now - start
        total_hours = delta.total_seconds() / 3600
        
        # Calculate 3 evenly-spaced points between start and now
        point1 = start + (delta * 0.25)
        point2 = start + (delta * 0.50)
        point3 = start + (delta * 0.75)
        
        # Format based on time span
        if total_hours < 24:
            # Show hours for markets created today
            fmt = lambda dt: f"{int((dt - start).total_seconds() / 3600)}h"
            return [
                'Start',
                fmt(point1),
                fmt(point2),
                fmt(point3),
                'Now'
            ]
        elif delta.days < 7:
            # Show as "Mon", "Tue", etc. for recent markets
            fmt = "%a"
            return [
                'Start',
                point1.strftime(fmt),
                point2.strftime(fmt),
                point3.strftime(fmt),
                'Now'
            ]
        elif delta.days < 60:
            # Show as "Jan 5", "Jan 15", etc.
            fmt = "%b %-d"
            return [
                'Start',
                point1.strftime(fmt),
                point2.strftime(fmt),
                point3.strftime(fmt),
                'Now'
            ]
        else:
            # Show as "Jan", "Feb", etc. for older markets
            fmt = "%b"
            return [
                'Start',
                point1.strftime(fmt),
                point2.strftime(fmt),
                point3.strftime(fmt),
                'Now'
            ]
    except Exception as e:
        return ['Start', '25%', '50%', '75%', 'Now']

class BRain:
    """BRain intelligence layer - supports both local DB and Rain API"""
    
    def _get_conn(self):
        """Get database connection (local mode only)"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_homepage_feed(self):
        """Get ranked markets for homepage"""
        if USE_RAIN_API and rain_client:
            # Use Rain API
            try:
                rain_markets = rain_client.list_markets()
                if not rain_markets:
                    return {'hero': [], 'grid': [], 'stream': []}
                
                # Convert to BRain format
                markets = [rain_client.convert_to_brain_format(m) for m in rain_markets]
                
                # Calculate belief intensity
                for market in markets:
                    market['belief_intensity'] = calculate_belief_intensity(market)
                
                # Sort by belief intensity
                markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
                
                # ALWAYS ensure at least one multi-option market in hero or grid (for testing)
                top_9 = markets[:9] if len(markets) >= 9 else markets
                has_multi = any(m.get('market_type') == 'multiple' for m in top_9)
                
                if not has_multi and len(markets) > 9:
                    # Find first multi-option market outside top 9
                    multi_market = next((m for m in markets[9:] if m.get('market_type') == 'multiple'), None)
                    if multi_market:
                        # Remove it from its position and insert at position 8 (last grid slot)
                        markets.remove(multi_market)
                        markets.insert(8, multi_market)
                
                return {
                    'hero': markets[0:1] if markets else [],
                    'grid': markets[1:9] if len(markets) > 1 else [],
                    'stream': markets[9:20] if len(markets) > 9 else []
                }
            except Exception as e:
                logger.error(f"Error getting Rain API feed: {e}", exc_info=True)
                return {'hero': [], 'grid': [], 'stream': []}
        else:
            # Use local database
            conn = None
            try:
                conn = self._get_conn()
                cursor = conn.cursor()
                
                # Main query - fetch all markets
                cursor.execute("""
                    SELECT m.market_id, m.title, m.description, m.editorial_description, m.category, 
                           m.language, m.probability, m.volume_24h, m.volume_total, m.participant_count,
                           m.image_url, m.status, m.created_at, m.resolution_date, m.resolved, 
                           m.outcome, m.market_type,
                           GROUP_CONCAT(DISTINCT mt.tag) as tags
                    FROM markets m
                    LEFT JOIN market_tags mt ON m.market_id = mt.market_id
                    WHERE m.status = 'open'
                    GROUP BY m.market_id
                """)
                
                markets = [dict(row) for row in cursor.fetchall()]
                
                # Batch fetch options for multi-option markets (FIX N+1!)
                multi_ids = [m['market_id'] for m in markets if m.get('market_type') == 'multiple']
                options_by_market = defaultdict(list)
                
                if multi_ids:
                    placeholders = ','.join('?' * len(multi_ids))
                    cursor.execute(f"""
                        SELECT market_id, option_id, option_text, probability
                        FROM market_options
                        WHERE market_id IN ({placeholders})
                        ORDER BY market_id, probability DESC
                    """, multi_ids)
                    
                    for row in cursor.fetchall():
                        options_by_market[row['market_id']].append(dict(row))
                
                # Process markets
                for market in markets:
                    market['tags'] = market['tags'].split(',') if market['tags'] else []
                    market['belief_intensity'] = calculate_belief_intensity(market)
                    
                    # Add options if multi-option market
                    if market['market_id'] in options_by_market:
                        market['top_options'] = options_by_market[market['market_id']][:5]
                
                # Sort by belief intensity
                markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
                
                # ALWAYS prioritize visually interesting categories for hero (Roy's feedback)
                visual_categories = ['Sports', 'Entertainment', 'Technology', 'Crypto']
                visual_markets = [m for m in markets if m['category'] in visual_categories]
                
                logger.info(f"🎨 Hero selection: Found {len(visual_markets)} visual markets")
                logger.info(f"🎨 Current top market: {markets[0]['title'][:40]} ({markets[0]['category']})")
                
                if visual_markets:
                    # Use highest-belief-intensity visual market as hero
                    hero_market = visual_markets[0]
                    logger.info(f"🎨 Promoting to hero: {hero_market['title'][:40]} ({hero_market['category']})")
                    markets.remove(hero_market)
                    markets.insert(0, hero_market)
                
                # ALWAYS ensure at least one multi-option market in hero or grid (for testing)
                top_9 = markets[:9] if len(markets) >= 9 else markets
                has_multi = any(m.get('market_type') == 'multiple' for m in top_9)
                
                if not has_multi and len(markets) > 9:
                    # Find first multi-option market outside top 9
                    multi_market = next((m for m in markets[9:] if m.get('market_type') == 'multiple'), None)
                    if multi_market:
                        # Remove it from its position and insert at position 8 (last grid slot)
                        markets.remove(multi_market)
                        markets.insert(8, multi_market)
                
                return {
                    'hero': markets[0:1] if markets else [],
                    'grid': markets[1:13] if len(markets) > 1 else [],
                    'stream': markets[13:40] if len(markets) > 13 else []
                }
            
            except Exception as e:
                logger.error(f"Error getting homepage feed: {e}", exc_info=True)
                return {'hero': [], 'grid': [], 'stream': []}
            
            finally:
                if conn:
                    try:
                        conn.close()
                    except:
                        pass
    
    def get_market_detail(self, market_id):
        """Get market details with history"""
        if USE_RAIN_API and rain_client:
            # Use Rain API
            rain_market = rain_client.get_market(market_id)
            if not rain_market:
                return None
            
            # Convert to BRain format
            market = rain_client.convert_to_brain_format(rain_market)
            
            # Calculate outcomes from options
            if market.get('top_options'):
                market['outcomes'] = [
                    {'name': opt['option_text'], 'probability': opt['probability']}
                    for opt in market['top_options']
                ]
            else:
                market['outcomes'] = [
                    {'name': 'Yes', 'probability': market['probability']},
                    {'name': 'No', 'probability': 1 - market['probability']}
                ]
            
            return market
        else:
            # Use local database
            conn = self._get_conn()
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
                return None
            
            market = dict(row)
            market['tags'] = market['tags'].split(',') if market['tags'] else []
            
            # Get probability history
            cursor.execute("""
                SELECT probability, volume, timestamp
                FROM probability_history
                WHERE market_id = ?
                ORDER BY timestamp ASC
            """, (market_id,))
            
            market['probability_history'] = [dict(row) for row in cursor.fetchall()]
            
            # Calculate outcomes
            market['outcomes'] = [
                {'name': 'Yes', 'probability': market['probability']},
                {'name': 'No', 'probability': 1 - market['probability']}
            ]
            
            conn.close()
            return market
    
    def get_related_markets(self, market_id, limit=3):
        """Find related markets by tags"""
        if USE_RAIN_API and rain_client:
            # Use Rain API - simple implementation: just get other markets
            # In production, Rain API would have a related markets endpoint
            all_markets = rain_client.list_markets()
            if not all_markets:
                return []
            
            # Filter out current market and convert to BRain format
            related = [
                rain_client.convert_to_brain_format(m) 
                for m in all_markets 
                if m.get('market_id') != market_id
            ][:limit]
            
            return related
        else:
            # Use local database
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute("SELECT tag FROM market_tags WHERE market_id = ?", (market_id,))
            target_tags = set(row['tag'] for row in cursor.fetchall())
            
            if not target_tags:
                conn.close()
                return []
            
            cursor.execute("""
                SELECT m.*, 
                       COUNT(DISTINCT mt.tag) as tag_overlap,
                       GROUP_CONCAT(DISTINCT mt.tag) as tags
                FROM markets m
                JOIN market_tags mt ON m.market_id = mt.market_id
                WHERE mt.tag IN ({})
                  AND m.market_id != ?
                  AND m.status = 'open'
                GROUP BY m.market_id
                ORDER BY tag_overlap DESC
                LIMIT ?
            """.format(','.join('?' * len(target_tags))), (*target_tags, market_id, limit))
            
            related = [dict(row) for row in cursor.fetchall()]
            for m in related:
                m['tags'] = m['tags'].split(',') if m['tags'] else []
            
            conn.close()
            return related

# Initialize BRain
brain = BRain()

# Routes
@app.route('/')
def index():
    """Homepage - Personalized Feed"""
    # Check for URL parameter (?user=user2) to set cookie
    url_user = request.args.get('user')
    
    # Get user key: prioritize URL param, then test user cookie, then regular user key
    test_user = request.cookies.get('currents_test_user')
    user_key = url_user or test_user or request.headers.get('X-User-Key') or request.cookies.get('currents_user_key') or None
    
    # Get personalized feed
    feed = personalizer.get_personalized_feed(user_key=user_key, limit=20)
    
    logger.info(f"Homepage: user={user_key}, test_mode={test_user is not None}, personalized={feed.get('personalized', False)}")
    
    # Create response
    response = app.make_response(render_template('index-v2.html',
                         hero=feed['hero'],
                         grid=feed['grid'],
                         stream=feed['stream'],
                         personalized=feed.get('personalized', False),
                         user_key=user_key,
                         test_mode=(test_user is not None)))
    
    # If URL parameter provided, set cookie for future visits
    if url_user and url_user in ['roy', 'user2', 'user3', 'user4']:
        response.set_cookie('currents_test_user', url_user, max_age=7*24*60*60)  # 7 days
        logger.info(f"Set cookie for user: {url_user}")
    
    return response

@app.route('/market/<market_id>')
def market_detail(market_id):
    """Market detail page"""
    # Validate market_id
    if not market_id or len(market_id) > 100:
        logger.warning(f"Invalid market_id: {market_id}")
        return "Invalid market ID", 400
    
    try:
        market = brain.get_market_detail(market_id)
        if not market:
            logger.info(f"Market not found: {market_id}")
            return "Market not found", 404
        
        related = brain.get_related_markets(market_id)
        return render_template('detail.html',
                             market=market,
                             related=related)
    except Exception as e:
        logger.error(f"Error loading market {market_id}: {e}", exc_info=True)
        return "Error loading market", 500

@app.route('/api/homepage')
def api_homepage():
    """API: Get homepage feed"""
    return jsonify(brain.get_homepage_feed())

@app.route('/api/markets/<market_id>')
def api_market(market_id):
    """API: Get market details"""
    # Validate market_id
    if not market_id or len(market_id) > 100:
        return jsonify({"error": "Invalid market ID"}), 400
    
    try:
        market = brain.get_market_detail(market_id)
        if not market:
            return jsonify({"error": "Market not found"}), 404
        return jsonify(market)
    except Exception as e:
        logger.error(f"API error getting market {market_id}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/wallet-demo')
def wallet_demo():
    """Wallet v2 demo page"""
    return render_template('wallet_v2.html')

@app.route('/wallet-transactions')
def wallet_transactions():
    """Transaction demo page"""
    return render_template('demo_transaction.html')

@app.route('/connect-wallet')
def connect_wallet():
    """Simple MetaMask connection (WORKING)"""
    return render_template('wallet_simple.html')

@app.route('/wallet')
def wallet_minimal():
    """Minimal wallet - NO external libraries needed"""
    return render_template('wallet_minimal.html')

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "ok", "service": "currents-local"})

@app.route('/filter-test')
def filter_test():
    """Test page for Jinja filters"""
    feed = brain.get_homepage_feed()
    return render_template('filter_test.html', hero=feed['hero'])

@app.route('/api/track', methods=['POST'])
def track_interaction():
    """
    Track user interaction event
    """
    try:
        data = request.get_json()
        
        # Get or create user_key (use IP as fallback for now)
        user_key = data.get('user_key') or request.headers.get('X-User-Key') or request.remote_addr
        
        market_id = data.get('market_id')
        event_type = data.get('event_type')
        dwell_ms = data.get('dwell_ms')
        section = data.get('section')
        position = data.get('position')
        
        if not market_id or not event_type:
            return jsonify({"error": "market_id and event_type required"}), 400
        
        # Record interaction
        interaction_id = tracker.record_interaction(
            user_key=user_key,
            market_id=market_id,
            event_type=event_type,
            dwell_ms=dwell_ms,
            section=section,
            position=position
        )
        
        logger.info(f"Tracked: {event_type} on {market_id} by {user_key}")
        
        return jsonify({
            "success": True,
            "interaction_id": interaction_id
        })
    
    except Exception as e:
        logger.error(f"Track error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/track/batch', methods=['POST'])
def track_batch():
    """
    Track multiple events in batch
    """
    try:
        data = request.get_json()
        user_key = data.get('user_key') or request.remote_addr
        events = data.get('events', [])
        
        interaction_ids = []
        for event in events:
            interaction_id = tracker.record_interaction(
                user_key=user_key,
                market_id=event.get('market_id'),
                event_type=event.get('event_type'),
                dwell_ms=event.get('dwell_ms'),
                section=event.get('section'),
                position=event.get('position')
            )
            interaction_ids.append(interaction_id)
        
        logger.info(f"Tracked batch: {len(events)} events by {user_key}")
        
        return jsonify({
            "success": True,
            "interaction_ids": interaction_ids
        })
    
    except Exception as e:
        logger.error(f"Batch track error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tracking-admin')
def tracking_admin():
    """Admin dashboard for behavioral learning"""
    return render_template('tracking_admin.html')

@app.route('/api/admin/users')
def admin_users():
    """Get list of all users"""
    users = tracker.get_all_users()
    return jsonify(users)

@app.route('/api/admin/profile/<user_key>')
def admin_profile(user_key):
    """Get user profile with scores"""
    profile = tracker.get_user_profile(user_key)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    return jsonify(profile)

@app.route('/api/admin/evolution/<user_key>/<topic_type>/<topic_value>')
def admin_evolution(user_key, topic_type, topic_value):
    """Get score evolution history"""
    history = tracker.get_score_evolution(user_key, topic_type, topic_value)
    return jsonify(history)

@app.route('/brain-viewer')
@app.route('/brain-viewer/<path:subpath>')
def brain_viewer(subpath=''):
    """Proxy to BRain Database Viewer on port 5556"""
    import requests
    from flask import request, Response
    
    # Forward request to database viewer
    url = f'http://localhost:5556/{subpath}'
    
    # Copy query parameters
    if request.query_string:
        url += f'?{request.query_string.decode()}'
    
    # Forward request with auth
    try:
        resp = requests.get(
            url,
            auth=('admin', 'demo2026'),
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            allow_redirects=False
        )
        
        # Return response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Database Viewer not available. Make sure db_viewer.py is running on port 5556. Error: {e}", 503

if __name__ == '__main__':
    print("🌊 Currents starting...")
    
    # Check data source
    if USE_RAIN_API:
        print(f"📡 Data source: Rain Protocol API ({RAIN_API_URL})")
        # Test Rain API connection
        if rain_client:
            test_markets = rain_client.list_markets()
            if test_markets:
                print(f"✅ Rain API: Connected ({len(test_markets)} markets available)")
            else:
                print("⚠️  Rain API: Connection failed or no markets available")
                print("💡 Make sure rain_api_mock.py is running on port 5000")
        else:
            print("❌ Rain API client not initialized")
            exit(1)
    else:
        print("📊 Data source: Local SQLite database")
        if not os.path.exists(DB_PATH):
            print("⚠️  Database not found! Run setup.sh first.")
            exit(1)
        print("✅ BRain database: OK")
    
    # Use PORT from environment (for production) or default to 5555
    # Note: Rain API mock runs on 5000, so we use 5555 for the main app
    port = int(os.environ.get('PORT', 5555))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Server: http://{host}:{port}")
    print("")
    
    app.run(host=host, port=port, debug=debug)

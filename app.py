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
import time
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Import config and Rain client
from config import USE_RAIN_API, RAIN_API_URL, BRAIN_V1_ENABLED
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

# Geo-IP lookup cache (to avoid repeated API calls)
GEO_CACHE = {}

# Rate limiting for waitlist submissions
# Format: {ip_address: [timestamp1, timestamp2, ...]}
WAITLIST_RATE_LIMIT = defaultdict(list)
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
RATE_LIMIT_MAX = 3  # Max 3 submissions per hour per IP

def get_country_from_ip(ip_address):
    """
    Get country code from IP address using ip-api.com (free, supports IPv6)
    Falls back to 'UNKNOWN' if lookup fails
    """
    # Skip private IPs
    if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        return 'LOCAL'
    
    # Check cache
    if ip_address in GEO_CACHE:
        return GEO_CACHE[ip_address]
    
    try:
        # Use ip-api.com free API (no key needed, supports IPv6, 45 req/min limit)
        response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=countryCode', timeout=2)
        if response.status_code == 200:
            data = response.json()
            country_code = data.get('countryCode')
            if country_code and len(country_code) == 2:
                GEO_CACHE[ip_address] = country_code
                logger.info(f"Geo lookup: {ip_address} -> {country_code}")
                return country_code
    except Exception as e:
        logger.warning(f"Geo lookup failed for {ip_address}: {e}")
    
    return 'UNKNOWN'

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

# Robots.txt route (block crawlers during development)
@app.route('/robots.txt')
def robots():
    """Serve robots.txt file to block web crawlers"""
    from flask import send_from_directory
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

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

@app.template_filter('market_rules')
def market_rules(market):
    """Generate market-specific resolution rules"""
    from market_rules_generator import get_market_rules
    return get_market_rules(market)

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
    """Homepage - Personalized Feed (Mobile: TikTok feed, Desktop: Grid)"""
    # Check for bypass parameter (from "Go to site" link)
    bypass_redirect = request.args.get('bypass')
    
    # If bypass parameter is present, set cookie and continue
    if bypass_redirect:
        from flask import make_response, redirect
        response = make_response(redirect('/'))
        # Set cookie that lasts for 7 days
        response.set_cookie('currents_bypass_coming_soon', 'true', max_age=7*24*60*60)
        return response
    
    # Check if user has bypass cookie (from clicking "Go to site")
    has_bypass = request.cookies.get('currents_bypass_coming_soon') == 'true'
    
    # Coming Soon redirect DISABLED - keep page but don't redirect
    # if not has_bypass:
    #     from flask import redirect
    #     return redirect('/coming-soon')
    
    # Check for URL parameter (?user=user2) to set cookie
    url_user = request.args.get('user')
    
    # Get user key: prioritize URL param, then test user cookie, then regular user key
    test_user = request.cookies.get('currents_test_user')
    user_key = url_user or test_user or request.headers.get('X-User-Key') or request.cookies.get('currents_user_key') or None
    
    # Generate anonymous user key if none exists
    if not user_key:
        import random
        import string
        user_key = 'anon_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    
    # Detect mobile device from User-Agent
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(x in user_agent for x in ['mobile', 'android', 'iphone', 'ipad', 'tablet'])
    
    # Force desktop mode with ?desktop=1 parameter (for menu link)
    force_desktop = request.args.get('desktop') == '1'
    
    # Check for special Yaniv market access parameter (?yaniv=1)
    show_yaniv = request.args.get('yaniv') == '1'
    
    # Get user's country for geo-based trending
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    user_country = get_country_from_ip(client_ip)
    
    # OVERRIDE: user4 is always from Japan
    if user_key == 'user4':
        user_country = 'JP'
        logger.info(f"🇯🇵 User4 country override: JP (always Japanese)")
    
    logger.info(f"User location: IP={client_ip}, Country={user_country}")
    
    # Check if BRain v1 is enabled
    if BRAIN_V1_ENABLED:
        # BRain v1 personalized feed
        try:
            from feed_composer import feed_composer
            from impression_tracker import impression_tracker
            
            # Get limit based on device
            limit = 50 if is_mobile and not force_desktop else 30
            
            # Compose feed with BRain v1
            result = feed_composer.compose_feed(
                user_key=user_key,
                geo_bucket=user_country,
                limit=limit,
                exclude_ids=[],
                debug=False
            )
            
            # Extract markets from items
            all_markets = [item['market'] for item in result['items']]
            
            # HERO MARKET OVERRIDE - DISABLED (Joni is now normal market)
            # Joni market will appear in normal personalized feed position
            joni_market_id = 'joni-token-april-2026'
            
            # Remove Joni market from list (will re-add only for Israeli users)
            # DISABLED - no longer removing or promoting Joni
            joni_market = None
            if False:
                for market in all_markets[:]:  # Create copy to safely remove during iteration
                    if market.get('market_id') == joni_market_id:
                        joni_market = market
                        all_markets.remove(market)
                        break
            
            # Only show Joni market to users from Israel
            # DISABLED
            if False:  # was: user_country == 'IL'
                # If Joni market not in list, fetch it from database
                if not joni_market:
                    try:
                        conn = sqlite3.connect('brain.db')
                        conn.row_factory = sqlite3.Row
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT * FROM markets WHERE market_id = ?
                        """, (joni_market_id,))
                        row = cursor.fetchone()
                        if row:
                            joni_market = dict(row)
                            # Fetch options for multi-choice market
                            cursor.execute("""
                                SELECT * FROM market_options WHERE market_id = ? ORDER BY position
                            """, (joni_market_id,))
                            options = [dict(opt) for opt in cursor.fetchall()]
                            joni_market['outcomes'] = options
                        conn.close()
                    except Exception as e:
                        logger.error(f"Error fetching Joni hero market: {e}")
                
                # Insert Joni market as first (hero position)
                if joni_market:
                    all_markets.insert(0, joni_market)
                    logger.info(f"🇮🇱 HERO OVERRIDE (Israel only): Joni market promoted to position 0")
            else:
                # Non-Israeli users: Joni market already removed from list
                logger.info(f"🌍 Joni market hidden for non-Israeli user: country={user_country}")
            
            # GEO-FILTER JAPANESE MARKETS: Show only to JP users
            if user_country != 'JP':
                # Remove all Japanese markets (japan-* prefix)
                japanese_markets = [m for m in all_markets if m.get('market_id', '').startswith('japan-')]
                for jp_market in japanese_markets:
                    all_markets.remove(jp_market)
                if japanese_markets:
                    logger.info(f"🌍 Filtered {len(japanese_markets)} Japanese markets for non-JP user: country={user_country}")
            else:
                logger.info(f"🇯🇵 Japanese user detected - showing all JP markets")
            
            # YANIV MARKET SPECIAL ACCESS: Show only with ?yaniv=1 URL parameter
            yaniv_market_id = 'yaniv-rain-march-2026'
            yaniv_market = None
            
            # Remove Yaniv market from list (will re-add only if show_yaniv=True)
            for market in all_markets[:]:  # Create copy to safely remove during iteration
                if market.get('market_id') == yaniv_market_id:
                    yaniv_market = market
                    all_markets.remove(market)
                    break
            
            # If show_yaniv parameter present, show as hero market
            if show_yaniv:
                # If Yaniv market not in list, fetch it from database
                if not yaniv_market:
                    try:
                        conn = sqlite3.connect('brain.db')
                        conn.row_factory = sqlite3.Row
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT * FROM markets WHERE market_id = ?
                        """, (yaniv_market_id,))
                        row = cursor.fetchone()
                        if row:
                            yaniv_market = dict(row)
                        conn.close()
                    except Exception as e:
                        logger.error(f"Error fetching Yaniv hero market: {e}")
                
                # Insert Yaniv market as first (hero position)
                if yaniv_market:
                    all_markets.insert(0, yaniv_market)
                    logger.info(f"🔐 HERO OVERRIDE (Special access): Yaniv market promoted to position 0")
            else:
                # Normal users: Yaniv market hidden
                if yaniv_market:
                    logger.info(f"🔒 Yaniv market hidden (no ?yaniv=1 parameter)")
            
            # IRAN ATTACK MARKET: Visible to all users, trending in Israel
            # (No geo-filtering - appears in normal feed based on personalization)
            
            # Log impressions server-side
            shown_ids = [item['market_id'] for item in result['items']]
            impression_tracker.log_impressions(user_key, shown_ids)
            
            logger.info(f"BRain v1 feed: user={user_key}, geo={user_country}, items={len(all_markets)}, quotas={result['meta']['quotas_used']}")
            
        except Exception as e:
            logger.error(f"BRain v1 feed error, falling back to old system: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to old system
            feed = personalizer.get_personalized_feed(user_key=user_key, limit=50 if is_mobile else 20, user_country=user_country)
            all_markets = []
            if feed['hero']:
                all_markets.extend(feed['hero'])
            if feed['grid']:
                all_markets.extend(feed['grid'])
            if feed['stream']:
                all_markets.extend(feed['stream'])
    else:
        # Old system (v159)
        logger.info(f"Using old personalizer (BRain v1 disabled)")
        feed = personalizer.get_personalized_feed(user_key=user_key, limit=50 if is_mobile else 20, user_country=user_country)
        all_markets = []
        if feed['hero']:
            all_markets.extend(feed['hero'])
        if feed['grid']:
            all_markets.extend(feed['grid'])
        if feed['stream']:
            all_markets.extend(feed['stream'])
    
    # HERO MARKET OVERRIDE - DISABLED (Joni is now normal market)
    # Joni market will appear in normal personalized feed position
    joni_market_id = 'joni-token-april-2026'
    
    # Remove Joni market from list (will re-add only for Israeli users)
    # DISABLED - no longer removing or promoting Joni
    joni_market = None
    if False:
        for market in all_markets[:]:  # Create copy to safely remove during iteration
            if market.get('market_id') == joni_market_id:
                joni_market = market
                all_markets.remove(market)
                break
    
    # Only show Joni market to users from Israel
    # DISABLED
    if False:  # was: user_country == 'IL'
        # If Joni market not in list, fetch it from database
        if not joni_market:
            try:
                conn = sqlite3.connect('brain.db')
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM markets WHERE market_id = ?
                """, (joni_market_id,))
                row = cursor.fetchone()
                if row:
                    joni_market = dict(row)
                    # Fetch options for multi-choice market
                    cursor.execute("""
                        SELECT * FROM market_options WHERE market_id = ? ORDER BY position
                    """, (joni_market_id,))
                    options = [dict(opt) for opt in cursor.fetchall()]
                    joni_market['outcomes'] = options
                conn.close()
            except Exception as e:
                logger.error(f"Error fetching Joni hero market: {e}")
        
        # Insert Joni market as first (hero position)
        if joni_market:
            all_markets.insert(0, joni_market)
            logger.info(f"🇮🇱 HERO OVERRIDE (Israel only): Joni market promoted to position 0")
    else:
        # Non-Israeli users: Joni market already removed from list
        logger.info(f"🌍 Joni market hidden for non-Israeli user: country={user_country}")
    
    # GEO-FILTER JAPANESE MARKETS: Show only to JP users
    if user_country != 'JP':
        # Remove all Japanese markets (japan-* prefix)
        japanese_markets = [m for m in all_markets if m.get('market_id', '').startswith('japan-')]
        for jp_market in japanese_markets:
            all_markets.remove(jp_market)
        if japanese_markets:
            logger.info(f"🌍 Filtered {len(japanese_markets)} Japanese markets for non-JP user: country={user_country}")
    else:
        logger.info(f"🇯🇵 Japanese user detected - showing all JP markets")
    
    # YANIV MARKET SPECIAL ACCESS (FALLBACK): Show only with ?yaniv=1 URL parameter
    yaniv_market_id = 'yaniv-rain-march-2026'
    yaniv_market = None
    
    # Remove Yaniv market from list (will re-add only if show_yaniv=True)
    for market in all_markets[:]:  # Create copy to safely remove during iteration
        if market.get('market_id') == yaniv_market_id:
            yaniv_market = market
            all_markets.remove(market)
            break
    
    # If show_yaniv parameter present, show as hero market
    if show_yaniv:
        # If Yaniv market not in list, fetch it from database
        if not yaniv_market:
            try:
                conn = sqlite3.connect('brain.db')
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM markets WHERE market_id = ?
                """, (yaniv_market_id,))
                row = cursor.fetchone()
                if row:
                    yaniv_market = dict(row)
                conn.close()
            except Exception as e:
                logger.error(f"Error fetching Yaniv hero market: {e}")
        
        # Insert Yaniv market as first (hero position)
        if yaniv_market:
            all_markets.insert(0, yaniv_market)
            logger.info(f"🔐 HERO OVERRIDE (Special access - fallback): Yaniv market promoted to position 0")
    else:
        # Normal users: Yaniv market hidden
        if yaniv_market:
            logger.info(f"🔒 Yaniv market hidden (no ?yaniv=1 parameter - fallback)")
    
    # IRAN ATTACK MARKET: Visible to all users, trending in Israel
    # (No geo-filtering - appears in normal feed based on personalization)
    
    # Mobile users get TikTok feed (unless ?desktop=1)
    if is_mobile and not force_desktop:
        logger.info(f"Mobile detected - serving TikTok feed: user={user_key}")
        
        response = app.make_response(render_template('feed_mobile.html',
                             markets=all_markets,
                             user_key=user_key))
    else:
        # Desktop users get grid layout
        logger.info(f"Desktop mode - serving grid: user={user_key}, test_mode={test_user is not None}")
        
        # Split markets into hero/grid/stream for desktop layout
        hero = all_markets[:1] if all_markets else []
        grid = all_markets[1:9] if len(all_markets) > 1 else []
        stream = all_markets[9:] if len(all_markets) > 9 else []
        
        # Create response
        response = app.make_response(render_template('index-v2.html',
                             hero=hero,
                             grid=grid,
                             stream=stream,
                             personalized=True,
                             user_key=user_key,
                             test_mode=(test_user is not None)))
    
    # If URL parameter provided, set cookie for future visits
    if url_user and url_user in ['user1', 'user2', 'user3', 'user4', 'roy']:
        response.set_cookie('currents_test_user', url_user, max_age=7*24*60*60)  # 7 days
        logger.info(f"Set cookie for user: {url_user}")
    
    return response


@app.route('/feed')
def feed_mobile():
    """TikTok-style vertical scrolling feed (MOBILE ONLY)"""
    # Get user key for personalization
    test_user = request.cookies.get('currents_test_user')
    user_key = test_user or request.headers.get('X-User-Key') or request.cookies.get('currents_user_key') or None
    
    # Generate anonymous user key if none exists
    if not user_key:
        import random
        import string
        user_key = 'anon_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    
    # Check for special Yaniv market access parameter (?yaniv=1)
    show_yaniv = request.args.get('yaniv') == '1'
    
    # Get user's country for geo-based trending
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    user_country = get_country_from_ip(client_ip)
    
    # OVERRIDE: user4 is always from Japan
    if user_key == 'user4':
        user_country = 'JP'
        logger.info(f"🇯🇵 User4 country override: JP (always Japanese)")
    
    # Check if BRain v1 is enabled
    if BRAIN_V1_ENABLED:
        # BRain v1 personalized feed
        try:
            from feed_composer import feed_composer
            from impression_tracker import impression_tracker
            
            # Compose feed with BRain v1
            result = feed_composer.compose_feed(
                user_key=user_key,
                geo_bucket=user_country,
                limit=50,
                exclude_ids=[],
                debug=False
            )
            
            # Extract markets from items
            all_markets = [item['market'] for item in result['items']]
            
            # HERO MARKET OVERRIDE - DISABLED (Joni is now normal market)
            # Joni market will appear in normal personalized feed position
            joni_market_id = 'joni-token-april-2026'
            
            # Remove Joni market from list (will re-add only for Israeli users)
            # DISABLED - no longer removing or promoting Joni
            joni_market = None
            if False:
                for market in all_markets[:]:  # Create copy to safely remove during iteration
                    if market.get('market_id') == joni_market_id:
                        joni_market = market
                        all_markets.remove(market)
                        break
            
            # Only show Joni market to users from Israel
            # DISABLED
            if False:  # was: user_country == 'IL'
                # If Joni market not in list, fetch it from database
                if not joni_market:
                    try:
                        conn = sqlite3.connect('brain.db')
                        conn.row_factory = sqlite3.Row
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT * FROM markets WHERE market_id = ?
                        """, (joni_market_id,))
                        row = cursor.fetchone()
                        if row:
                            joni_market = dict(row)
                            # Fetch options for multi-choice market
                            cursor.execute("""
                                SELECT * FROM market_options WHERE market_id = ? ORDER BY position
                            """, (joni_market_id,))
                            options = [dict(opt) for opt in cursor.fetchall()]
                            joni_market['outcomes'] = options
                        conn.close()
                    except Exception as e:
                        logger.error(f"Error fetching Joni hero market: {e}")
                
                # Insert Joni market as first (hero position)
                if joni_market:
                    all_markets.insert(0, joni_market)
                    logger.info(f"🇮🇱 HERO OVERRIDE (mobile, Israel only): Joni market promoted to position 0")
            else:
                # Non-Israeli users: Joni market already removed from list
                logger.info(f"🌍 Joni market hidden for non-Israeli mobile user: country={user_country}")
            
            # GEO-FILTER JAPANESE MARKETS: Show only to JP users
            if user_country != 'JP':
                # Remove all Japanese markets (japan-* prefix)
                japanese_markets = [m for m in all_markets if m.get('market_id', '').startswith('japan-')]
                for jp_market in japanese_markets:
                    all_markets.remove(jp_market)
                if japanese_markets:
                    logger.info(f"🌍 Filtered {len(japanese_markets)} Japanese markets for non-JP mobile user: country={user_country}")
            else:
                logger.info(f"🇯🇵 Japanese mobile user detected - showing all JP markets")
            
            # YANIV MARKET SPECIAL ACCESS (MOBILE): Show only with ?yaniv=1 URL parameter
            yaniv_market_id = 'yaniv-rain-march-2026'
            yaniv_market = None
            
            # Remove Yaniv market from list (will re-add only if show_yaniv=True)
            for market in all_markets[:]:  # Create copy to safely remove during iteration
                if market.get('market_id') == yaniv_market_id:
                    yaniv_market = market
                    all_markets.remove(market)
                    break
            
            # If show_yaniv parameter present, show as hero market
            if show_yaniv:
                # If Yaniv market not in list, fetch it from database
                if not yaniv_market:
                    try:
                        conn = sqlite3.connect('brain.db')
                        conn.row_factory = sqlite3.Row
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT * FROM markets WHERE market_id = ?
                        """, (yaniv_market_id,))
                        row = cursor.fetchone()
                        if row:
                            yaniv_market = dict(row)
                        conn.close()
                    except Exception as e:
                        logger.error(f"Error fetching Yaniv hero market: {e}")
                
                # Insert Yaniv market as first (hero position)
                if yaniv_market:
                    all_markets.insert(0, yaniv_market)
                    logger.info(f"🔐 HERO OVERRIDE (Mobile special access): Yaniv market promoted to position 0")
            else:
                # Normal users: Yaniv market hidden
                if yaniv_market:
                    logger.info(f"🔒 Yaniv market hidden (no ?yaniv=1 parameter - mobile)")
            
            # IRAN ATTACK MARKET: Visible to all users, trending in Israel
            # (No geo-filtering - appears in normal feed based on personalization)
            
            # Log impressions server-side
            shown_ids = [item['market_id'] for item in result['items']]
            impression_tracker.log_impressions(user_key, shown_ids)
            
            logger.info(f"BRain v1 mobile feed: user={user_key}, geo={user_country}, items={len(all_markets)}")
            
        except Exception as e:
            logger.error(f"BRain v1 feed error, falling back: {e}")
            # Fallback to old system
            feed = personalizer.get_personalized_feed(user_key=user_key, limit=50, user_country=user_country)
            all_markets = []
            if feed['hero']:
                all_markets.extend(feed['hero'])
            if feed['grid']:
                all_markets.extend(feed['grid'])
            if feed['stream']:
                all_markets.extend(feed['stream'])
    else:
        # Old system (v159)
        feed = personalizer.get_personalized_feed(user_key=user_key, limit=50, user_country=user_country)
        all_markets = []
        if feed['hero']:
            all_markets.extend(feed['hero'])
        if feed['grid']:
            all_markets.extend(feed['grid'])
        if feed['stream']:
            all_markets.extend(feed['stream'])
    
    logger.info(f"Mobile Feed: user={user_key}, markets={len(all_markets)}")
    
    return render_template('feed_mobile.html',
                         markets=all_markets,
                         user_key=user_key)

@app.route('/alt')
def index_alt():
    """Alternative Homepage - Full Card Images with Text Overlay"""
    # Check for URL parameter (?user=user2) to set cookie
    url_user = request.args.get('user')
    
    # Get user key: prioritize URL param, then test user cookie, then regular user key
    test_user = request.cookies.get('currents_test_user')
    user_key = url_user or test_user or request.headers.get('X-User-Key') or request.cookies.get('currents_user_key') or None
    
    # Get user's country for geo-based trending
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    user_country = get_country_from_ip(client_ip)
    
    # Get personalized feed
    feed = personalizer.get_personalized_feed(user_key=user_key, limit=20, user_country=user_country)
    
    logger.info(f"Alternative Homepage: user={user_key}, test_mode={test_user is not None}, personalized={feed.get('personalized', False)}")
    
    # Create response
    response = app.make_response(render_template('index-alt.html',
                         hero=feed['hero'],
                         grid=feed['grid'],
                         stream=feed['stream'],
                         personalized=feed.get('personalized', False),
                         user_key=user_key,
                         test_mode=(test_user is not None)))
    
    # If URL parameter provided, set cookie for future visits
    if url_user and url_user in ['user1', 'user2', 'user3', 'user4', 'roy']:
        response.set_cookie('currents_test_user', url_user, max_age=7*24*60*60)  # 7 days
        logger.info(f"Set cookie for user: {url_user}")
    
    return response


@app.route('/markets')
def all_markets():
    """All Markets page with category filtering"""
    # Get user key
    test_user = request.cookies.get('currents_test_user')
    user_key = test_user or request.headers.get('X-User-Key') or request.cookies.get('currents_user_key') or None
    
    # Get category filter from URL (if any)
    category_filter = request.args.get('category')
    
    # Detect mobile
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(x in user_agent for x in ['mobile', 'android', 'iphone', 'ipad', 'tablet'])
    force_desktop = request.args.get('desktop') == '1'
    
    # Get user's country for personalization
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    user_country = get_country_from_ip(client_ip)
    
    logger.info(f"All Markets: user={user_key}, category={category_filter}, mobile={is_mobile and not force_desktop}")
    
    # Render appropriate template
    if is_mobile and not force_desktop:
        return render_template('markets_mobile.html',
                             user_key=user_key,
                             category_filter=category_filter)
    else:
        return render_template('markets.html',
                             user_key=user_key,
                             category_filter=category_filter)


@app.route('/api/markets/feed', methods=['POST'])
def api_markets_feed():
    """API: Get paginated markets feed with category filtering"""
    try:
        data = request.json or {}
        user_key = data.get('user_key')
        category = data.get('category')  # None = all markets
        offset = data.get('offset', 0)
        limit = data.get('limit', 60)
        
        # Get ALL markets from database
        conn = brain._get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Filter by category if specified
        if category and category != 'all':
            cursor.execute("""
                SELECT * FROM markets 
                WHERE status = 'open' AND category = ?
                ORDER BY created_at DESC
            """, (category,))
            all_markets = [dict(row) for row in cursor.fetchall()]
        else:
            # For "all" category, implement round-robin distribution for diversity
            cursor.execute("""
                SELECT * FROM markets 
                WHERE status = 'open'
                ORDER BY created_at DESC
            """)
            all_markets_raw = [dict(row) for row in cursor.fetchall()]
            
            # Group by category
            from collections import defaultdict
            markets_by_category = defaultdict(list)
            for market in all_markets_raw:
                markets_by_category[market['category']].append(market)
            
            # Round-robin distribution for perfect diversity
            all_markets = []
            categories = list(markets_by_category.keys())
            max_per_category = max(len(markets) for markets in markets_by_category.values())
            
            for i in range(max_per_category):
                for cat in categories:
                    if i < len(markets_by_category[cat]):
                        all_markets.append(markets_by_category[cat][i])
        
        conn.close()
        
        # FILTER OUT YANIV MARKET: Hidden from All Markets page (API endpoint)
        # Only accessible via main feed with ?yaniv=1 parameter
        yaniv_market_id = 'yaniv-rain-march-2026'
        all_markets = [m for m in all_markets if m.get('market_id') != yaniv_market_id]
        
        # Paginate
        total = len(all_markets)
        paginated = all_markets[offset:offset + limit]
        has_more = offset + limit < total
        
        logger.info(f"Markets feed: category={category}, offset={offset}, limit={limit}, total={total}, returned={len(paginated)}")
        
        return jsonify({
            'markets': paginated,
            'total': total,
            'has_more': has_more
        })
            
    except Exception as e:
        logger.error(f"Markets feed error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


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
        
        # DISABLED: Auto-fetch creates mock content from placeholder API endpoints
        # Re-enable when web_search/web_fetch tools are properly integrated
        # from article_fetcher import should_refresh_article
        # try:
        #     if should_refresh_article(market):
        #         # Trigger background fetch (non-blocking)
        #         import threading
        #         def fetch_bg():
        #             from article_fetcher import fetch_article_for_market
        #             fetch_article_for_market(market_id, market['title'])
        #         
        #         thread = threading.Thread(target=fetch_bg)
        #         thread.daemon = True
        #         thread.start()
        # except Exception as e:
        #     logger.warning(f"Article fetch trigger failed: {e}")
        
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

@app.route('/my-location')
def my_location():
    """Show detected IP and country for debugging"""
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    
    country = get_country_from_ip(client_ip)
    
    return jsonify({
        "ip": client_ip,
        "country": country,
        "israel_detected": country == 'IL',
        "geo_boost_active": country == 'IL'
    })

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
        
        # Get geo location from IP
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            # X-Forwarded-For can be comma-separated list, get first IP
            client_ip = client_ip.split(',')[0].strip()
        geo_country = get_country_from_ip(client_ip)
        
        # Record interaction
        interaction_id = tracker.record_interaction(
            user_key=user_key,
            market_id=market_id,
            event_type=event_type,
            dwell_ms=dwell_ms,
            section=section,
            position=position,
            geo_country=geo_country
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
        
        # Get geo location once for batch
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        geo_country = get_country_from_ip(client_ip)
        
        interaction_ids = []
        for event in events:
            interaction_id = tracker.record_interaction(
                user_key=user_key,
                market_id=event.get('market_id'),
                event_type=event.get('event_type'),
                dwell_ms=event.get('dwell_ms'),
                section=event.get('section'),
                position=event.get('position'),
                geo_country=geo_country
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

@app.route('/api/trade', methods=['POST'])
def api_trade():
    """
    Simulated trading endpoint (replaces mock Rain API)
    Client-side JavaScript calls this to simulate trades
    """
    try:
        data = request.get_json()
        
        # Extract trade parameters
        market_id = data.get('market_id')
        outcome = data.get('outcome')
        amount = data.get('amount', 0)
        wallet_address = data.get('wallet_address')
        wallet_balance = data.get('wallet_balance', 0)
        
        # Validation
        if not market_id or not outcome or not wallet_address:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: market_id, outcome, wallet_address'
            }), 400
        
        if amount <= 0:
            return jsonify({
                'success': False,
                'error': 'Amount must be greater than 0'
            }), 400
        
        if amount > wallet_balance:
            return jsonify({
                'success': False,
                'error': f'Insufficient balance. You have {wallet_balance} USDT but need {amount} USDT'
            }), 400
        
        # Get market probability from database
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        cursor.execute("SELECT probability, title FROM markets WHERE market_id = ?", (market_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({
                'success': False,
                'error': f'Market not found: {market_id}'
            }), 404
        
        probability, market_title = row
        
        # Calculate simulated trade details
        # For YES: price = probability, for NO: price = 1 - probability
        if outcome.upper() == 'YES':
            execution_price = probability
        elif outcome.upper() == 'NO':
            execution_price = 1 - probability
        else:
            execution_price = probability  # Default
        
        # Calculate shares (simplified: amount / price)
        shares = round(amount / max(execution_price, 0.01), 2)
        
        # Simulated trade result
        trade_result = {
            'trade_id': f'sim_{int(time.time() * 1000)}',
            'market_id': market_id,
            'market_title': market_title,
            'outcome': outcome,
            'amount': amount,
            'shares': shares,
            'execution_price': round(execution_price, 4),
            'timestamp': datetime.now().isoformat(),
            'status': 'simulated',
            'wallet_address': wallet_address
        }
        
        app.logger.info(f"Simulated trade: {wallet_address} bought {shares} shares of {outcome} on {market_id} for {amount} USDT")
        
        return jsonify({
            'success': True,
            'trade': trade_result,
            'message': 'Trade simulated successfully (no real transaction occurred)'
        })
        
    except Exception as e:
        app.logger.error(f"Trade error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Trade failed: {str(e)}'
        }), 500

# ============================================
# Web Search/Fetch API (for article fetcher)
# ============================================

@app.route('/api/web-search', methods=['POST'])
def api_web_search():
    """Search the web using integrated web_search"""
    try:
        data = request.json
        query = data.get('query', '')
        count = data.get('count', 5)
        
        if not query:
            return jsonify({'error': 'Query required'}), 400
        
        # Placeholder - in production this would call actual web_search tool
        # For now, return mock results
        return jsonify({
            'results': [
                {
                    'title': f'Article about {query}',
                    'url': f'https://example.com/article-{query.lower().replace(" ", "-")}',
                    'snippet': f'This is a comprehensive article about {query}...'
                }
            ]
        })
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/web-fetch', methods=['POST'])
def api_web_fetch():
    """Fetch content from URL"""
    try:
        data = request.json
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL required'}), 400
        
        # Placeholder - in production this would call actual web_fetch tool
        # For now, return mock content
        return jsonify({
            'content': f'# Full article content from {url}\n\nThis is a detailed article about the topic...'
        })
    except Exception as e:
        logger.error(f"Web fetch error: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================
# BRain v1 API Endpoints
# ============================================

@app.route('/api/brain/feed', methods=['POST'])
def api_brain_feed():
    """
    BRain v1 - Get personalized feed with quota enforcement
    
    POST /api/brain/feed
    {
        "user_key": "wallet_or_userid_or_cookie",
        "geo_country": "IL",
        "limit": 30,
        "cursor": null,
        "context": {"surface": "home"},
        "exclude_market_ids": ["m123"],
        "debug": false
    }
    
    Returns ranked feed + logs impressions server-side
    """
    # Check if BRain v1 is enabled
    if not BRAIN_V1_ENABLED:
        return jsonify({
            'error': 'BRain v1 is disabled. Use /api/homepage for old system.',
            'rollback': True
        }), 503
    
    try:
        # Import BRain v1 components
        from feed_composer import feed_composer
        from impression_tracker import impression_tracker
        
        data = request.get_json()
        
        user_key = data.get('user_key')
        if not user_key:
            return jsonify({'error': 'user_key required'}), 400
        
        geo_country = data.get('geo_country')
        if not geo_country:
            # Try to get from IP
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if client_ip:
                client_ip = client_ip.split(',')[0].strip()
            geo_country = get_country_from_ip(client_ip)
        
        limit = data.get('limit', 30)
        exclude_ids = data.get('exclude_market_ids', [])
        debug = data.get('debug', False)
        
        # Compose feed
        result = feed_composer.compose_feed(
            user_key=user_key,
            geo_bucket=geo_country,
            limit=limit,
            exclude_ids=exclude_ids,
            debug=debug
        )
        
        # Log impressions server-side
        shown_market_ids = [item['market_id'] for item in result['items']]
        impression_tracker.log_impressions(user_key, shown_market_ids)
        
        app.logger.info(f"[BRain v1] Feed: user={user_key}, geo={geo_country}, items={len(result['items'])}")
        
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"BRain feed error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/brain/user/<user_key>', methods=['GET'])
def api_brain_user(user_key):
    """
    BRain v1 - Get user profile for debugging
    
    Returns long-term + session state
    """
    # Check if BRain v1 is enabled
    if not BRAIN_V1_ENABLED:
        return jsonify({
            'error': 'BRain v1 is disabled',
            'rollback': True
        }), 503
    
    try:
        from session_manager import session_manager
        import sqlite3
        
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        # Get long-term scores
        cursor.execute("""
            SELECT topic_type, topic_value, score
            FROM user_topic_scores
            WHERE user_key = ?
            ORDER BY score DESC
        """, (user_key,))
        
        long_term = defaultdict(list)
        for row in cursor.fetchall():
            topic_type, topic_value, score = row
            long_term[topic_type].append({
                'value': topic_value,
                'score': score
            })
        
        # Get session state
        session_weights = session_manager.get_session_weights(user_key)
        
        # Get interaction counts
        cutoff_7d = (datetime.now() - timedelta(days=7)).isoformat()
        cutoff_30d = (datetime.now() - timedelta(days=30)).isoformat()
        
        cursor.execute("""
            SELECT COUNT(*) FROM user_interactions
            WHERE user_key = ? AND event_type != 'impression' AND ts > ?
        """, (user_key, cutoff_7d))
        interactions_7d = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM user_interactions
            WHERE user_key = ? AND event_type != 'impression' AND ts > ?
        """, (user_key, cutoff_30d))
        interactions_30d = cursor.fetchone()[0]
        
        # Get recently shown markets
        cursor.execute("""
            SELECT market_id, impressions_24h, last_shown_at
            FROM user_market_impressions
            WHERE user_key = ?
            ORDER BY last_shown_at DESC
            LIMIT 20
        """, (user_key,))
        
        recent_shown = [
            {
                'market_id': row[0],
                'impressions_24h': row[1],
                'last_shown_at': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return jsonify({
            'user_key': user_key,
            'long_term': {
                'categories': long_term['category'][:10],
                'tags': long_term['tag'][:20]
            },
            'session': session_weights,
            'interactions': {
                '7d': interactions_7d,
                '30d': interactions_30d
            },
            'recent_shown': recent_shown
        })
        
    except Exception as e:
        app.logger.error(f"BRain user error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/brain/trending', methods=['GET'])
def api_brain_trending():
    """
    BRain v1 - Get trending markets
    
    GET /api/brain/trending?scope=global&geo_country=IL&window=1h
    """
    # Check if BRain v1 is enabled
    if not BRAIN_V1_ENABLED:
        return jsonify({
            'error': 'BRain v1 is disabled',
            'rollback': True
        }), 503
    
    try:
        scope = request.args.get('scope', 'global')
        geo_country = request.args.get('geo_country', '')
        limit = int(request.args.get('limit', 50))
        
        # Build geo_bucket
        if scope == 'local' and geo_country:
            geo_bucket = geo_country
        else:
            geo_bucket = 'GLOBAL'
        
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.market_id, m.title, m.category,
                   v.trades_1h, v.views_1h, v.odds_change_1h
            FROM market_velocity_rollups v
            JOIN markets m ON v.market_id = m.market_id
            WHERE v.geo_bucket = ?
            ORDER BY (v.trades_1h * 0.7 + v.views_1h * 0.3) DESC
            LIMIT ?
        """, (geo_bucket, limit))
        
        trending = [
            {
                'market_id': row[0],
                'title': row[1],
                'category': row[2],
                'trades_1h': row[3],
                'views_1h': row[4],
                'odds_change_1h': row[5]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return jsonify({
            'trending': trending,
            'geo_bucket': geo_bucket
        })
        
    except Exception as e:
        app.logger.error(f"BRain trending error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/coming-soon')
def coming_soon():
    """Coming Soon / Waiting List page"""
    # Get user IP (handle proxy headers from ngrok)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()
    
    # Check if user is from Israel
    country_code = get_country_from_ip(user_ip)
    show_site_link = (country_code == 'IL')
    
    logger.info(f"Coming Soon page: IP={user_ip}, Country={country_code}, ShowLink={show_site_link}")
    
    return render_template('coming_soon.html', show_site_link=show_site_link)


@app.route('/api/waitlist/submit', methods=['POST'])
def waitlist_submit():
    """
    Submit waitlist entry with belief choice and email
    Handles test email override and duplicate checking
    """
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        belief_choice = data.get('belief_choice', '').upper()
        device_type = data.get('device_type', 'unknown')
        locale = data.get('locale', 'en-US')
        
        # Validate belief choice
        if belief_choice not in ['YES', 'NO', 'MARCH', 'APRIL', 'MAY', 'LATER']:
            return jsonify({'error': 'Invalid belief choice'}), 400
        
        # Check for test email override
        is_test = (email == 'testtt')
        
        # Email validation (skip for test email)
        if not is_test:
            if not email or '@' not in email or '.' not in email.split('@')[1]:
                return jsonify({'error': 'Please enter a valid email address'}), 400
        
        # Get request metadata
        user_agent = request.headers.get('User-Agent', '')
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        # Rate limiting (skip for test email)
        if not is_test:
            current_time = time.time()
            
            # Clean old timestamps outside the window
            WAITLIST_RATE_LIMIT[ip_address] = [
                ts for ts in WAITLIST_RATE_LIMIT[ip_address] 
                if current_time - ts < RATE_LIMIT_WINDOW
            ]
            
            # Check if limit exceeded
            if len(WAITLIST_RATE_LIMIT[ip_address]) >= RATE_LIMIT_MAX:
                app.logger.warning(f"⚠️  Rate limit exceeded for IP: {ip_address}")
                return jsonify({
                    'error': 'Too many submissions from this location. Please try again in an hour.'
                }), 429
            
            # Add current timestamp
            WAITLIST_RATE_LIMIT[ip_address].append(current_time)
        
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        # Check for duplicates (skip for test email)
        if not is_test:
            cursor.execute("""
                SELECT id FROM waitlist_submissions 
                WHERE email = ? AND is_test_submission = 0
            """, (email,))
            
            existing = cursor.fetchone()
            if existing:
                conn.close()
                return jsonify({
                    'error': 'This email is already on the Currents waiting list.',
                    'secondary': 'We\'ll notify you when the outcome is known.'
                }), 409
        
        # Insert submission
        cursor.execute("""
            INSERT INTO waitlist_submissions 
            (email, belief_choice, device_type, locale, is_test_submission, user_agent, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (email, belief_choice, device_type, locale, 1 if is_test else 0, user_agent, ip_address))
        
        submission_id = cursor.lastrowid
        
        # Get waitlist position (count of ALL submissions + 0 to start at 50 with seed data)
        cursor.execute("""
            SELECT COUNT(*) FROM waitlist_submissions
        """)
        total_count = cursor.fetchone()[0]
        waitlist_position = total_count
        
        # Get belief percentages (all submissions including test)
        cursor.execute("""
            SELECT belief_choice, COUNT(*) as count
            FROM waitlist_submissions
            GROUP BY belief_choice
        """)
        belief_counts = {row[0]: row[1] for row in cursor.fetchall()}
        march_count = belief_counts.get('MARCH', 0)
        april_count = belief_counts.get('APRIL', 0)
        may_count = belief_counts.get('MAY', 0)
        later_count = belief_counts.get('LATER', 0)
        total = march_count + april_count + may_count + later_count
        
        march_percentage = round((march_count / total * 100)) if total > 0 else 25
        april_percentage = round((april_count / total * 100)) if total > 0 else 25
        may_percentage = round((may_count / total * 100)) if total > 0 else 25
        later_percentage = round((later_count / total * 100)) if total > 0 else 25
        
        conn.commit()
        conn.close()
        
        app.logger.info(f"✅ Waitlist submission: {email} → {belief_choice} (test={is_test}, id={submission_id}, position={waitlist_position}, march={march_percentage}%, april={april_percentage}%, may={may_percentage}%, later={later_percentage}%)")
        
        # TODO: Send confirmation email
        # If is_test=True, send to roy@rain.one
        # Otherwise send to the actual email
        
        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'belief': belief_choice,
            'position': waitlist_position,
            'march_percentage': march_percentage,
            'april_percentage': april_percentage,
            'may_percentage': may_percentage,
            'later_percentage': later_percentage
        }), 200
        
    except Exception as e:
        app.logger.error(f"❌ Waitlist submission error: {str(e)}")
        return jsonify({'error': 'An error occurred. Please try again.'}), 500


@app.route('/api/waitlist/percentages')
def waitlist_percentages():
    """Get current belief percentages (for displaying on buttons)"""
    try:
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        # Get belief counts (all submissions including test)
        cursor.execute("""
            SELECT belief_choice, COUNT(*) as count
            FROM waitlist_submissions
            GROUP BY belief_choice
        """)
        belief_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        march_count = belief_counts.get('MARCH', 0)
        april_count = belief_counts.get('APRIL', 0)
        may_count = belief_counts.get('MAY', 0)
        later_count = belief_counts.get('LATER', 0)
        total = march_count + april_count + may_count + later_count
        
        march_percentage = round((march_count / total * 100)) if total > 0 else 25
        april_percentage = round((april_count / total * 100)) if total > 0 else 25
        may_percentage = round((may_count / total * 100)) if total > 0 else 25
        later_percentage = round((later_count / total * 100)) if total > 0 else 25
        
        return jsonify({
            'march_percentage': march_percentage,
            'april_percentage': april_percentage,
            'may_percentage': may_percentage,
            'later_percentage': later_percentage,
            'march_count': march_count,
            'april_count': april_count,
            'may_count': may_count,
            'later_count': later_count,
            'total_submissions': total
        })
        
    except Exception as e:
        app.logger.error(f"Waitlist percentages error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/waitlist/stats')
def waitlist_stats():
    """Get waitlist statistics (for admin/monitoring)"""
    try:
        conn = sqlite3.connect('brain.db')
        cursor = conn.cursor()
        
        # Total submissions (excluding test)
        cursor.execute("""
            SELECT COUNT(*) FROM waitlist_submissions 
            WHERE is_test_submission = 0
        """)
        total = cursor.fetchone()[0]
        
        # YES count
        cursor.execute("""
            SELECT COUNT(*) FROM waitlist_submissions 
            WHERE belief_choice = 'YES' AND is_test_submission = 0
        """)
        yes_count = cursor.fetchone()[0]
        
        # NO count
        cursor.execute("""
            SELECT COUNT(*) FROM waitlist_submissions 
            WHERE belief_choice = 'NO' AND is_test_submission = 0
        """)
        no_count = cursor.fetchone()[0]
        
        # Device breakdown
        cursor.execute("""
            SELECT device_type, COUNT(*) 
            FROM waitlist_submissions 
            WHERE is_test_submission = 0
            GROUP BY device_type
        """)
        devices = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return jsonify({
            'total': total,
            'yes': yes_count,
            'no': no_count,
            'yes_percentage': round(yes_count / total * 100, 1) if total > 0 else 0,
            'no_percentage': round(no_count / total * 100, 1) if total > 0 else 0,
            'devices': devices
        })
        
    except Exception as e:
        app.logger.error(f"Waitlist stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/diagnostic')
def diagnostic():
    """Diagnostic page for troubleshooting mobile feed"""
    return render_template('diagnostic.html')

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


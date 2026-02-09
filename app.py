"""
Currents Full Stack - Local Development
Combines BRain database + Flask API + Frontend
"""
from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'brain.db')

class BRain:
    """BRain intelligence layer"""
    
    def _get_conn(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def calculate_belief_intensity(self, market):
        """Calculate belief intensity score"""
        volume_score = market['volume_24h'] / 10000
        prob = market['probability']
        contestedness = 1 - abs(0.5 - prob) * 2
        return volume_score * 0.6 + contestedness * 0.4
    
    def get_homepage_feed(self):
        """Get ranked markets for homepage"""
        conn = self._get_conn()
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
            market['belief_intensity'] = self.calculate_belief_intensity(market)
            markets.append(market)
        
        markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
        
        conn.close()
        
        return {
            'hero': markets[0:1] if markets else [],
            'grid': markets[1:9] if len(markets) > 1 else [],
            'stream': markets[9:20] if len(markets) > 9 else []
        }
    
    def get_market_detail(self, market_id):
        """Get market details with history"""
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
    """Homepage"""
    feed = brain.get_homepage_feed()
    return render_template('index.html',
                         hero=feed['hero'],
                         grid=feed['grid'],
                         stream=feed['stream'])

@app.route('/market/<market_id>')
def market_detail(market_id):
    """Market detail page"""
    market = brain.get_market_detail(market_id)
    if not market:
        return "Market not found", 404
    
    related = brain.get_related_markets(market_id)
    return render_template('detail.html',
                         market=market,
                         related=related)

@app.route('/api/homepage')
def api_homepage():
    """API: Get homepage feed"""
    return jsonify(brain.get_homepage_feed())

@app.route('/api/markets/<market_id>')
def api_market(market_id):
    """API: Get market details"""
    market = brain.get_market_detail(market_id)
    if not market:
        return jsonify({"error": "Market not found"}), 404
    return jsonify(market)

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "ok", "service": "currents-local"})

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print("⚠️  Database not found! Run setup.sh first.")
        exit(1)
    
    print("🌊 Currents starting...")
    print("📊 BRain database: OK")
    
    # Use PORT from environment (for production) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Server: http://{host}:{port}")
    print("")
    
    app.run(host=host, port=port, debug=debug)

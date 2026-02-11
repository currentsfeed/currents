"""
BRain Analytics Dashboard
Interactive visualization and personalization testing tool
"""
from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime
from collections import defaultdict, Counter
from user_profiles import get_all_users, get_user_profile, update_user_score

app = Flask(__name__)
DB_PATH = 'brain.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_belief_intensity(volume_24h, probability, volume_weight=0.6, contested_weight=0.4):
    """Calculate belief intensity with configurable weights"""
    volume_score = volume_24h / 10000
    contestedness = 1 - abs(0.5 - probability) * 2
    return (volume_score * volume_weight) + (contestedness * contested_weight)

@app.route('/')
def index():
    """Main analytics dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all markets with full data
    cursor.execute("""
        SELECT m.*,
               GROUP_CONCAT(DISTINCT mt.tag) as tags
        FROM markets m
        LEFT JOIN market_tags mt ON m.market_id = mt.market_id
        WHERE m.status = 'open'
        GROUP BY m.market_id
    """)
    
    markets = [dict(row) for row in cursor.fetchall()]
    
    # Calculate belief intensity for each
    for market in markets:
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        market['belief_intensity'] = calculate_belief_intensity(
            market['volume_24h'], 
            market['probability']
        )
    
    # Analytics
    category_dist = Counter(m['category'] for m in markets)
    tag_dist = Counter(tag for m in markets for tag in m['tags'])
    
    # Belief intensity distribution
    bi_ranges = {
        '0-5': 0,
        '5-10': 0,
        '10-15': 0,
        '15-20': 0,
        '20+': 0
    }
    for m in markets:
        bi = m['belief_intensity']
        if bi < 5:
            bi_ranges['0-5'] += 1
        elif bi < 10:
            bi_ranges['5-10'] += 1
        elif bi < 15:
            bi_ranges['10-15'] += 1
        elif bi < 20:
            bi_ranges['15-20'] += 1
        else:
            bi_ranges['20+'] += 1
    
    # Volume distribution
    volume_ranges = {
        '0-10K': 0,
        '10-50K': 0,
        '50-100K': 0,
        '100-500K': 0,
        '500K+': 0
    }
    for m in markets:
        vol = m['volume_24h']
        if vol < 10000:
            volume_ranges['0-10K'] += 1
        elif vol < 50000:
            volume_ranges['10-50K'] += 1
        elif vol < 100000:
            volume_ranges['50-100K'] += 1
        elif vol < 500000:
            volume_ranges['100-500K'] += 1
        else:
            volume_ranges['500K+'] += 1
    
    # Probability distribution
    prob_ranges = {
        '0-20%': 0,
        '20-40%': 0,
        '40-60%': 0,
        '60-80%': 0,
        '80-100%': 0
    }
    for m in markets:
        prob = m['probability'] * 100
        if prob < 20:
            prob_ranges['0-20%'] += 1
        elif prob < 40:
            prob_ranges['20-40%'] += 1
        elif prob < 60:
            prob_ranges['40-60%'] += 1
        elif prob < 80:
            prob_ranges['60-80%'] += 1
        else:
            prob_ranges['80-100%'] += 1
    
    conn.close()
    
    return render_template('analytics.html',
                         total_markets=len(markets),
                         markets=markets[:50],  # Top 50 for table
                         category_dist=dict(category_dist.most_common()),
                         tag_dist=dict(tag_dist.most_common(20)),
                         bi_ranges=bi_ranges,
                         volume_ranges=volume_ranges,
                         prob_ranges=prob_ranges)

@app.route('/api/personalize', methods=['POST'])
def personalize():
    """
    Test personalization algorithm with custom user profile
    
    POST data:
    {
        "categories": ["Sports", "Politics"],
        "tags": ["trump", "ai"],
        "volume_preference": "high|medium|low",
        "contestedness_preference": "high|medium|low",
        "limit": 20
    }
    """
    data = request.json
    
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
    
    markets = [dict(row) for row in cursor.fetchall()]
    
    # Calculate scores
    for market in markets:
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        market['belief_intensity'] = calculate_belief_intensity(
            market['volume_24h'],
            market['probability']
        )
        
        # Personalization score
        score = market['belief_intensity']
        
        # Category boost
        if data.get('categories') and market['category'] in data['categories']:
            score *= 1.5
        
        # Tag boost
        user_tags = set(data.get('tags', []))
        market_tags = set(market['tags'])
        tag_overlap = len(user_tags & market_tags)
        if tag_overlap > 0:
            score *= (1 + tag_overlap * 0.3)
        
        # Volume preference
        vol_pref = data.get('volume_preference', 'medium')
        if vol_pref == 'high' and market['volume_24h'] > 50000:
            score *= 1.2
        elif vol_pref == 'low' and market['volume_24h'] < 20000:
            score *= 1.2
        
        # Contestedness preference
        contestedness = 1 - abs(0.5 - market['probability']) * 2
        contest_pref = data.get('contestedness_preference', 'medium')
        if contest_pref == 'high' and contestedness > 0.6:
            score *= 1.3
        elif contest_pref == 'low' and contestedness < 0.4:
            score *= 1.2
        
        market['personalized_score'] = score
    
    # Sort by personalized score
    markets.sort(key=lambda x: x['personalized_score'], reverse=True)
    
    limit = data.get('limit', 20)
    
    conn.close()
    
    return jsonify({
        'markets': markets[:limit],
        'profile': data,
        'total': len(markets)
    })

@app.route('/api/algorithm-test', methods=['POST'])
def algorithm_test():
    """
    Test different algorithm weights
    
    POST data:
    {
        "volume_weight": 0.6,
        "contested_weight": 0.4,
        "limit": 20
    }
    """
    data = request.json
    
    volume_weight = float(data.get('volume_weight', 0.6))
    contested_weight = float(data.get('contested_weight', 0.4))
    
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
    
    markets = [dict(row) for row in cursor.fetchall()]
    
    for market in markets:
        market['tags'] = market['tags'].split(',') if market['tags'] else []
        market['belief_intensity'] = calculate_belief_intensity(
            market['volume_24h'],
            market['probability'],
            volume_weight,
            contested_weight
        )
    
    markets.sort(key=lambda x: x['belief_intensity'], reverse=True)
    
    limit = data.get('limit', 20)
    
    conn.close()
    
    return jsonify({
        'markets': markets[:limit],
        'weights': {
            'volume': volume_weight,
            'contested': contested_weight
        },
        'total': len(markets)
    })

@app.route('/api/market-breakdown/<market_id>')
def market_breakdown(market_id):
    """Get detailed scoring breakdown for a market"""
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
    
    market = dict(cursor.fetchone())
    market['tags'] = market['tags'].split(',') if market['tags'] else []
    
    # Calculate components
    volume_score = market['volume_24h'] / 10000
    contestedness = 1 - abs(0.5 - market['probability']) * 2
    belief_intensity = calculate_belief_intensity(market['volume_24h'], market['probability'])
    
    breakdown = {
        'market': market,
        'scoring': {
            'volume_24h': market['volume_24h'],
            'volume_score': round(volume_score, 2),
            'volume_contribution': round(volume_score * 0.6, 2),
            'probability': market['probability'],
            'contestedness': round(contestedness, 2),
            'contestedness_contribution': round(contestedness * 0.4, 2),
            'belief_intensity': round(belief_intensity, 2)
        },
        'metadata': {
            'category': market['category'],
            'tags': market['tags'],
            'participant_count': market['participant_count'],
            'created_at': market['created_at']
        }
    }
    
    conn.close()
    
    return jsonify(breakdown)

@app.route('/users')
def users_list():
    """User profiles list page"""
    users = get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def user_detail(user_id):
    """User profile detail page"""
    profile = get_user_profile(user_id)
    return render_template('user_detail.html', profile=profile)

@app.route('/api/users')
def api_users_list():
    """API: Get all users"""
    users = get_all_users()
    return jsonify({'users': users, 'total': len(users)})

@app.route('/api/users/<user_id>')
def api_user_detail(user_id):
    """API: Get user profile with scores"""
    profile = get_user_profile(user_id)
    return jsonify(profile)

@app.route('/api/users/<user_id>/update-score', methods=['POST'])
def api_update_user_score(user_id):
    """API: Update user topic score"""
    data = request.json
    topic_type = data.get('topic_type')
    topic_value = data.get('topic_value')
    delta = float(data.get('delta', 0.1))
    
    update_user_score(user_id, topic_type, topic_value, delta)
    
    # Return updated profile
    profile = get_user_profile(user_id)
    return jsonify(profile)

if __name__ == '__main__':
    print("🧠 Starting BRain Analytics Dashboard...")
    print("📊 URL: http://0.0.0.0:5557")
    print("🔬 Features:")
    print("   - Visual data distributions")
    print("   - Personalization simulator")
    print("   - Algorithm playground")
    print("   - Market scoring breakdown")
    print("")
    app.run(host='0.0.0.0', port=5557, debug=False)

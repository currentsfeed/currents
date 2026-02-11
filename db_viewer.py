#!/usr/bin/env python3
"""
Simple Database Viewer for BRain
View all tables, data, and relationships
"""
from flask import Flask, render_template_string, request
from flask_httpauth import HTTPBasicAuth
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = 'brain.db'

# Authentication setup
auth = HTTPBasicAuth()

# Get credentials from environment
VIEWER_USER = os.getenv('VIEWER_USER', 'admin')
VIEWER_PASS = os.getenv('VIEWER_PASS', 'demo2026')

@auth.verify_password
def verify_password(username, password):
    """Verify database viewer password"""
    if username == VIEWER_USER and password == VIEWER_PASS:
        return username
    return None

@auth.error_handler
def auth_error(status):
    """Return error for unauthorized access"""
    return "Unauthorized Access", 401

# HTML Template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BRain Database Viewer</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0e1a;
            color: #e5e7eb;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            font-size: 32px;
            margin-bottom: 10px;
            background: linear-gradient(to right, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { color: #6b7280; margin-bottom: 30px; font-size: 14px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #1f2937;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #374151;
        }
        .stat-label { color: #9ca3af; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-value { font-size: 32px; font-weight: bold; margin-top: 5px; }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #374151;
            padding-bottom: 10px;
        }
        .tab {
            padding: 10px 20px;
            background: #1f2937;
            border: 1px solid #374151;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            text-decoration: none;
            color: #9ca3af;
            transition: all 0.2s;
        }
        .tab:hover { background: #374151; color: #e5e7eb; }
        .tab.active {
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }
        .table-container {
            background: #1f2937;
            border-radius: 10px;
            border: 1px solid #374151;
            overflow: hidden;
        }
        .table-header {
            padding: 15px 20px;
            background: #111827;
            border-bottom: 1px solid #374151;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .table-title { font-size: 18px; font-weight: 600; }
        .table-count { color: #6b7280; font-size: 14px; }
        .table-wrapper { overflow-x: auto; }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #374151;
        }
        th {
            background: #111827;
            color: #9ca3af;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: sticky;
            top: 0;
        }
        td { font-size: 14px; }
        tr:hover td { background: #374151; }
        .null { color: #6b7280; font-style: italic; }
        .number { color: #34d399; font-family: monospace; }
        .text { color: #e5e7eb; }
        .truncate {
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .boolean { 
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        .boolean.true { background: #065f46; color: #10b981; }
        .boolean.false { background: #7f1d1d; color: #ef4444; }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            background: #1e40af;
            color: #60a5fa;
        }
        .filter-bar {
            margin-bottom: 20px;
            padding: 15px;
            background: #1f2937;
            border-radius: 8px;
            border: 1px solid #374151;
        }
        .filter-bar input, .filter-bar select {
            padding: 8px 12px;
            background: #111827;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #e5e7eb;
            margin-right: 10px;
        }
        .filter-bar button {
            padding: 8px 16px;
            background: #3b82f6;
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
            font-weight: 600;
        }
        .filter-bar button:hover { background: #2563eb; }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        .pagination a {
            padding: 8px 12px;
            background: #1f2937;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #9ca3af;
            text-decoration: none;
        }
        .pagination a:hover { background: #374151; }
        .pagination a.active { background: #3b82f6; color: white; border-color: #3b82f6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌊 BRain Database Viewer</h1>
        <p class="subtitle">Real-time view of all database tables and data</p>
        
        <!-- Stats -->
        <div class="stats">
            {% for stat in stats %}
            <div class="stat-card">
                <div class="stat-label">{{ stat.label }}</div>
                <div class="stat-value">{{ stat.value }}</div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Tabs -->
        <div class="tabs">
            {% for tab in tables %}
            <a href="?table={{ tab }}" class="tab {% if current_table == tab %}active{% endif %}">
                {{ tab }}
            </a>
            {% endfor %}
        </div>
        
        <!-- Filter Bar -->
        <div class="filter-bar">
            <form method="GET" style="display: flex; align-items: center;">
                <input type="hidden" name="table" value="{{ current_table }}">
                <input type="text" name="search" placeholder="Search..." value="{{ search }}" style="flex: 1;">
                <input type="number" name="limit" placeholder="Limit" value="{{ limit }}" style="width: 100px;">
                <button type="submit">Filter</button>
            </form>
        </div>
        
        <!-- Table -->
        {% if data %}
        <div class="table-container">
            <div class="table-header">
                <div class="table-title">{{ current_table }}</div>
                <div class="table-count">{{ data|length }} rows</div>
            </div>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            {% for col in columns %}
                            <th>{{ col }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in data %}
                        <tr>
                            {% for col in columns %}
                            <td>
                                {% set val = row[col] %}
                                {% if val is none %}
                                    <span class="null">NULL</span>
                                {% elif val is number %}
                                    <span class="number">{{ val }}</span>
                                {% elif val is sameas true or val is sameas false %}
                                    <span class="boolean {{ 'true' if val else 'false' }}">{{ val }}</span>
                                {% elif val|string|length > 100 %}
                                    <span class="text truncate" title="{{ val }}">{{ val }}</span>
                                {% else %}
                                    <span class="text">{{ val }}</span>
                                {% endif %}
                            </td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        {% else %}
        <div class="table-container">
            <div class="table-header">
                <div class="table-title">{{ current_table }}</div>
                <div class="table-count">0 rows</div>
            </div>
            <div style="padding: 40px; text-align: center; color: #6b7280;">
                No data in this table
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_stats():
    """Get database statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = []
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Markets count
    if 'markets' in tables:
        cursor.execute("SELECT COUNT(*) FROM markets")
        stats.append({"label": "Markets", "value": cursor.fetchone()[0]})
    
    # History points
    if 'probability_history' in tables:
        cursor.execute("SELECT COUNT(*) FROM probability_history")
        stats.append({"label": "History Points", "value": cursor.fetchone()[0]})
    
    # Tags
    if 'market_tags' in tables:
        cursor.execute("SELECT COUNT(*) FROM market_tags")
        stats.append({"label": "Tags", "value": cursor.fetchone()[0]})
    
    # Options
    if 'market_options' in tables:
        cursor.execute("SELECT COUNT(*) FROM market_options")
        stats.append({"label": "Market Options", "value": cursor.fetchone()[0]})
    
    # User interactions (if table exists)
    if 'user_interactions' in tables:
        cursor.execute("SELECT COUNT(*) FROM user_interactions")
        stats.append({"label": "User Interactions", "value": cursor.fetchone()[0]})
        
        cursor.execute("SELECT COUNT(DISTINCT user_key) FROM user_interactions")
        stats.append({"label": "Users", "value": cursor.fetchone()[0]})
    
    conn.close()
    return stats

def get_tables():
    """Get all table names"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def get_table_data(table, search=None, limit=100):
    """Get data from a specific table"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if table has market_id column (join with markets table for context)
    cursor.execute(f"PRAGMA table_info({table})")
    table_columns = [row[1] for row in cursor.fetchall()]
    has_market_id = 'market_id' in table_columns
    
    # Build query
    if has_market_id and table != 'markets':
        # Join with markets table to show market question
        query = f"""
            SELECT {table}.*, markets.title as market_question
            FROM {table}
            LEFT JOIN markets ON {table}.market_id = markets.market_id
        """
        columns = table_columns + ['market_question']
    else:
        query = f"SELECT * FROM {table}"
        columns = table_columns
    
    if search:
        # Simple search across all columns
        search_conditions = [f"{col} LIKE ?" for col in columns if col != 'market_question']
        if has_market_id and table != 'markets':
            search_conditions.append("markets.title LIKE ?")
        
        query += " WHERE " + " OR ".join(search_conditions)
        params = [f"%{search}%"] * len(search_conditions)
        cursor.execute(f"{query} LIMIT {limit}", params)
    else:
        cursor.execute(f"{query} LIMIT {limit}")
    
    rows = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return columns, rows

@app.route('/')
@auth.login_required
def index():
    # Get query params
    current_table = request.args.get('table', 'markets')
    search = request.args.get('search', '')
    limit = int(request.args.get('limit', 100))
    
    # Get data
    stats = get_stats()
    tables = get_tables()
    
    if current_table in tables:
        columns, data = get_table_data(current_table, search if search else None, limit)
    else:
        columns, data = [], []
    
    return render_template_string(
        TEMPLATE,
        stats=stats,
        tables=tables,
        current_table=current_table,
        columns=columns,
        data=data,
        search=search,
        limit=limit
    )

if __name__ == '__main__':
    print("🔍 Starting BRain Database Viewer...")
    print("📊 URL: http://0.0.0.0:5556")
    print(f"🔐 Username: {VIEWER_USER}")
    print(f"🔑 Password: {VIEWER_PASS}")
    print("")
    app.run(host='0.0.0.0', port=5556, debug=False)

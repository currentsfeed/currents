#!/bin/bash
# Setup BRain local database

echo "🧠 Setting up BRain local database..."
echo ""

# Create database and schema
echo "📦 Creating database schema..."
sqlite3 brain.db < schema.sql

# Seed data
echo "🌱 Seeding sample data..."
python3 seed_data.py

# Test BRain
echo "🧪 Testing BRain..."
python3 brain.py

echo ""
echo "✅ BRain database is ready!"
echo ""
echo "📁 Files created:"
echo "   brain.db          - SQLite database"
echo "   schema.sql        - Database schema"
echo "   seed_data.py      - Data population script"
echo "   brain.py          - BRain logic class"
echo ""
echo "🚀 Next steps:"
echo "   1. Explore the database: sqlite3 brain.db"
echo "   2. Query markets: SELECT * FROM markets;"
echo "   3. Run Python: python3 brain.py"
echo ""

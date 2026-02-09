#!/bin/bash
# Render.com build script

echo "🔨 Building Currents..."

# Install Python dependencies
pip install -r requirements.txt

# Create database schema
echo "📊 Creating database schema..."
sqlite3 brain.db < schema.sql

# Seed database with sample data
echo "🌱 Seeding database..."
python seed_data.py

echo "✅ Build complete!"

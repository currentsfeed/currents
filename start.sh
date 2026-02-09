#!/bin/bash
# Start Currents Full Stack Locally

echo "🌊 Starting Currents..."
echo ""

# Check if database exists
if [ ! -f "brain.db" ]; then
    echo "📦 Setting up database for the first time..."
    sqlite3 brain.db < schema.sql
    python3 seed_data.py
    echo ""
fi

# Check Python dependencies
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip3 install flask
    echo ""
fi

# Start the app
echo "🚀 Starting server..."
echo ""
python3 app.py

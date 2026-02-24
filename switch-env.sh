#!/bin/bash
# Switch between production and development environments

if [ "$1" == "production" ] || [ "$1" == "prod" ]; then
    echo "🔄 Switching to PRODUCTION environment..."
    cp .env.production .env
    echo "✅ Environment set to PRODUCTION"
    echo "   - Database: production.db"
    echo "   - Domain: currents.global"
    echo "   - Debug: OFF"
    echo ""
    echo "⚠️  Remember to:"
    echo "   1. git checkout main"
    echo "   2. sudo systemctl restart currents"
    
elif [ "$1" == "development" ] || [ "$1" == "dev" ]; then
    echo "🔄 Switching to DEVELOPMENT environment..."
    cp .env.development .env
    echo "✅ Environment set to DEVELOPMENT"
    echo "   - Database: brain.db"
    echo "   - Domain: localhost"
    echo "   - Debug: ON"
    echo ""
    echo "⚠️  Remember to:"
    echo "   1. git checkout dev"
    echo "   2. sudo systemctl restart currents"
    
else
    echo "❌ Usage: ./switch-env.sh [production|dev]"
    echo ""
    echo "Examples:"
    echo "  ./switch-env.sh production   # Switch to production config"
    echo "  ./switch-env.sh dev          # Switch to development config"
    echo ""
    
    if [ -f .env ]; then
        echo "Current .env file exists. To see which environment:"
        echo "  grep ENV= .env"
    else
        echo "No .env file found. Run this script to create one."
    fi
    exit 1
fi

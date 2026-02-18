"""
Configuration for Currents
Toggle between Rain API sources and other settings
"""
import os

# Data source configuration
USE_RAIN_API = os.getenv('USE_RAIN_API', 'false').lower() == 'true'
RAIN_API_URL = os.getenv('RAIN_API_URL', 'http://localhost:5000/api/v1')

# BRain v1 personalization toggle
BRAIN_V1_ENABLED = os.getenv('BRAIN_V1_ENABLED', 'true').lower() == 'true'  # Set to False to rollback to v159

# Database fallback
DB_PATH = os.path.join(os.path.dirname(__file__), 'brain.db')

# Application settings
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5555))

# BRain algorithm parameters
BELIEF_INTENSITY_VOLUME_WEIGHT = 0.6
BELIEF_INTENSITY_CONTESTED_WEIGHT = 0.4
VOLUME_NORMALIZATION = 10000

# Feed configuration
HERO_COUNT = 1
GRID_COUNT = 8
STREAM_COUNT = 21

print(f"📡 Data Source: {'Rain API' if USE_RAIN_API else 'Local Database'}")
if USE_RAIN_API:
    print(f"🌧️  Rain API URL: {RAIN_API_URL}")

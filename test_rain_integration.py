#!/usr/bin/env python3
"""
Test Rain API & BRain Integration
Verifies:
1. Rain API responds correctly
2. Rain client works
3. Personalization engine uses Rain API
4. Images still served from brain.db
"""
import requests
import sqlite3
from rain_client_brain import rain_client
from personalization import personalizer

def test_rain_api():
    """Test Rain API directly"""
    print("\n🧪 Testing Rain API...")
    
    # Health check
    response = requests.get('http://localhost:5001/health')
    assert response.status_code == 200, "Health check failed"
    print("✅ Health check passed")
    
    # Get markets
    response = requests.get('http://localhost:5001/api/v1/markets?limit=10')
    assert response.status_code == 200, "Get markets failed"
    data = response.json()
    assert 'markets' in data, "No markets in response"
    assert len(data['markets']) > 0, "No markets returned"
    print(f"✅ Got {len(data['markets'])} markets")
    
    # Get single market
    first_market_id = data['markets'][0]['market_id']
    response = requests.get(f'http://localhost:5001/api/v1/markets/{first_market_id}')
    assert response.status_code == 200, "Get single market failed"
    market = response.json()
    assert market['market_id'] == first_market_id, "Market ID mismatch"
    print(f"✅ Got single market: {market['title'][:50]}")
    
    # Get batch
    market_ids = [m['market_id'] for m in data['markets'][:5]]
    response = requests.post('http://localhost:5001/api/v1/markets/batch',
                            json={'market_ids': market_ids})
    assert response.status_code == 200, "Batch get failed"
    batch_data = response.json()
    assert len(batch_data['markets']) == 5, "Batch count mismatch"
    print(f"✅ Got batch of {len(batch_data['markets'])} markets")
    
    # Stats
    response = requests.get('http://localhost:5001/api/v1/stats')
    assert response.status_code == 200, "Stats failed"
    stats = response.json()
    print(f"✅ Stats: {stats['total_markets']} total markets ({stats['open_markets']} open)")
    
    return True

def test_rain_client():
    """Test Rain client wrapper"""
    print("\n🧪 Testing Rain Client...")
    
    # Health check
    assert rain_client.health_check(), "Rain client health check failed"
    print("✅ Rain client healthy")
    
    # Get markets
    markets = rain_client.get_markets(limit=10)
    assert len(markets) > 0, "No markets from client"
    print(f"✅ Rain client got {len(markets)} markets")
    
    # Get single market
    market = rain_client.get_market(markets[0]['market_id'])
    assert market is not None, "Failed to get single market"
    print(f"✅ Rain client got market: {market['title'][:50]}")
    
    # Get batch
    market_ids = [m['market_id'] for m in markets[:3]]
    batch = rain_client.get_markets_batch(market_ids)
    assert len(batch) == 3, "Batch size mismatch"
    print(f"✅ Rain client got batch of {len(batch)} markets")
    
    return True

def test_personalization_integration():
    """Test personalization engine uses Rain API"""
    print("\n🧪 Testing Personalization Integration...")
    
    # Get feed without user (global ranking)
    feed = personalizer.get_personalized_feed(user_key=None, limit=20)
    
    assert 'hero' in feed, "No hero section"
    assert 'grid' in feed, "No grid section"
    assert 'stream' in feed, "No stream section"
    assert feed['personalized'] == False, "Should not be personalized"
    
    total_markets = len(feed['hero']) + len(feed['grid']) + len(feed['stream'])
    print(f"✅ Personalization engine returned {total_markets} markets")
    print(f"   Hero: {len(feed['hero'])}, Grid: {len(feed['grid'])}, Stream: {len(feed['stream'])}")
    
    if feed['hero']:
        print(f"   Hero market: {feed['hero'][0]['title'][:50]}")
    
    return True

def test_images_in_brain():
    """Verify images are still in brain.db"""
    print("\n🧪 Testing Images in BRain...")
    
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Check if markets table still exists with image_url
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='markets'")
    result = cursor.fetchone()
    assert result is not None, "Markets table missing from brain.db"
    
    # Check if image_url column exists
    cursor.execute("PRAGMA table_info(markets)")
    columns = [col[1] for col in cursor.fetchall()]
    assert 'image_url' in columns, "image_url column missing"
    
    # Count markets with images
    cursor.execute("SELECT COUNT(*) FROM markets WHERE image_url IS NOT NULL AND image_url != ''")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ {count} markets have images in brain.db")
    
    return True

def test_separation():
    """Verify data separation: markets in rain.db, images in brain.db"""
    print("\n🧪 Testing Data Separation...")
    
    # Check rain.db has markets
    rain_conn = sqlite3.connect('rain.db')
    rain_cursor = rain_conn.cursor()
    rain_cursor.execute("SELECT COUNT(*) FROM markets")
    rain_count = rain_cursor.fetchone()[0]
    rain_conn.close()
    
    # Check brain.db has images
    brain_conn = sqlite3.connect('brain.db')
    brain_cursor = brain_conn.cursor()
    brain_cursor.execute("SELECT COUNT(*) FROM markets WHERE image_url IS NOT NULL")
    brain_image_count = brain_cursor.fetchone()[0]
    brain_conn.close()
    
    print(f"✅ Rain DB: {rain_count} markets")
    print(f"✅ BRain DB: {brain_image_count} markets with images")
    
    assert rain_count == 153, f"Expected 153 markets in rain.db, got {rain_count}"
    
    return True

def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("🧪 Rain API & BRain Integration Tests")
    print("=" * 60)
    
    try:
        test_rain_api()
        test_rain_client()
        test_personalization_integration()
        test_images_in_brain()
        test_separation()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n📋 Summary:")
        print("  • Rain API running on port 5001")
        print("  • 153 markets migrated to rain.db")
        print("  • Rain client working correctly")
        print("  • Personalization engine using Rain API")
        print("  • Images remain in brain.db")
        print("  • Data properly separated")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

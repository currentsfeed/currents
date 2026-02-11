#!/usr/bin/env python3
"""
Test script for BRain API
Demonstrates various endpoint usage
"""
import requests
import json

BASE_URL = "http://localhost:5555/api/v1"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_health():
    print_section("Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(json.dumps(response.json(), indent=2))

def test_markets_list():
    print_section("List Markets (Crypto, limit=3)")
    response = requests.get(f"{BASE_URL}/markets", params={
        'category': 'Crypto',
        'limit': 3,
        'sort': 'belief_intensity'
    })
    data = response.json()
    print(f"Total crypto markets: {data['total']}")
    for market in data['markets']:
        print(f"\n📊 {market['title']}")
        print(f"   Probability: {market['probability']*100:.1f}%")
        print(f"   Volume 24h: ${market['volume_24h']:,.0f}")
        print(f"   Belief Intensity: {market['belief_intensity']:.2f}")

def test_market_detail():
    print_section("Market Detail - Ethereum Flip")
    response = requests.get(f"{BASE_URL}/markets/m_eth_flip")
    market = response.json()['market']
    print(f"\n{market['title']}")
    print(f"Description: {market['description']}")
    print(f"Category: {market['category']}")
    print(f"Probability: {market['probability']*100:.1f}%")
    print(f"Participants: {market['participant_count']:,}")
    print(f"Total Volume: ${market['volume_total']:,.0f}")

def test_feed():
    print_section("Feed (Hero + Grid Preview)")
    response = requests.get(f"{BASE_URL}/feed")
    data = response.json()
    
    print("\n🌟 HERO:")
    if data['hero']:
        hero = data['hero'][0]
        print(f"   {hero['title']}")
        print(f"   Belief Intensity: {hero['belief_intensity']:.2f}")
    
    print("\n📱 GRID (Top 5):")
    for i, market in enumerate(data['grid'][:5], 1):
        print(f"   {i}. {market['title'][:50]}...")
        print(f"      BI: {market['belief_intensity']:.2f}")

def test_categories():
    print_section("Categories")
    response = requests.get(f"{BASE_URL}/categories")
    categories = response.json()['categories']
    for cat in categories:
        print(f"   {cat['category']:20} {cat['count']:3} markets")

def test_trending():
    print_section("Trending (Top Volume)")
    response = requests.get(f"{BASE_URL}/trending")
    trending = response.json()['trending']
    for i, market in enumerate(trending[:5], 1):
        print(f"   {i}. {market['title'][:50]}")
        print(f"      Volume 24h: ${market['volume_24h']:,.0f}")

def test_multi_option():
    print_section("Multi-Option Market - Super Bowl")
    response = requests.get(f"{BASE_URL}/markets/m_superbowl2027")
    market = response.json()['market']
    print(f"\n{market['title']}")
    print(f"\nTop Options:")
    for opt in market.get('options', [])[:5]:
        prob_pct = opt['probability'] * 100
        bar = '█' * int(prob_pct / 2)
        print(f"   {opt['option_text']:25} {prob_pct:5.1f}% {bar}")

if __name__ == "__main__":
    try:
        test_health()
        test_markets_list()
        test_market_detail()
        test_feed()
        test_categories()
        test_trending()
        test_multi_option()
        
        print(f"\n{'='*60}")
        print("  ✅ All API tests completed successfully!")
        print('='*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("   Make sure Flask is running: python3 -m flask run --port=5555")
    except Exception as e:
        print(f"\n❌ Error: {e}")

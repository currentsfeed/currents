#!/usr/bin/env python3
"""
Test script for Mock Rain Protocol API
Demonstrates integration with Rain client
"""
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace/currents-full-local')

from rain_client import get_rain_client
import json

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)

def test_health():
    print_section("Health Check")
    client = get_rain_client()
    health = client.health()
    print(json.dumps(health, indent=2))
    print(f"✅ Rain API is {'UP' if health.get('status') == 'ok' else 'DOWN'}")

def test_list_markets():
    print_section("List Markets (All)")
    client = get_rain_client()
    markets = client.list_markets(limit=5)
    
    print(f"Found {len(markets)} markets\n")
    for market in markets:
        print(f"📊 {market['title']}")
        print(f"   ID: {market['market_id']}")
        print(f"   Type: {market['market_type']}")
        print(f"   Category: {market['category']}")
        print(f"   Probability: {market['probability']*100:.1f}%")
        print(f"   Volume 24h: ${market['volume_24h']:,.0f}")
        print(f"   Participants: {market['participant_count']:,}")
        print()

def test_get_market_detail():
    print_section("Market Detail - Binary Market")
    client = get_rain_client()
    
    # Get first market
    markets = client.list_markets(limit=1)
    if markets:
        market_id = markets[0]['market_id']
        market = client.get_market(market_id)
        
        if market:
            print(f"\n{market['title']}")
            print(f"Description: {market['description']}")
            print(f"\nOutcomes:")
            for outcome in market['outcomes']:
                print(f"  - {outcome['name']}: {outcome['probability']*100:.1f}% (backing: ${outcome['backing']:,.0f})")
            
            print(f"\nContract: {market['contract_address']}")
            print(f"Chain: {market['chain']}")
            print(f"Fee: {market['fee_percentage']}%")
            print(f"Min bet: ${market['min_bet']}")
            print(f"Max bet: ${market['max_bet']}")
            
            print(f"\nRecent Trades ({len(market.get('recent_trades', []))}):")
            for trade in market.get('recent_trades', [])[:3]:
                print(f"  {trade['timestamp'][:19]} - {trade['side'].upper()} {trade['outcome']}: ${trade['amount']:.2f}")

def test_multi_option_market():
    print_section("Multi-Option Market")
    client = get_rain_client()
    
    markets = client.list_markets(market_type='multiple', limit=1)
    if markets:
        market = markets[0]
        print(f"\n{market['title']}")
        print(f"Type: {market['market_type']}")
        print(f"\nOptions:")
        for opt in market['outcomes']:
            prob_pct = opt['probability'] * 100
            bar = '█' * int(prob_pct / 2)
            print(f"  {opt['name']:20} {prob_pct:5.1f}% {bar}")

def test_brain_conversion():
    print_section("BRain Format Conversion")
    client = get_rain_client()
    
    # Get a market and convert to BRain format
    markets = client.list_markets(limit=1)
    if markets:
        rain_market = markets[0]
        brain_market = client.convert_to_brain_format(rain_market)
        
        print("Rain Format → BRain Format")
        print(f"\nOriginal Rain fields:")
        print(f"  - contract_address: {rain_market['contract_address']}")
        print(f"  - chain: {rain_market['chain']}")
        print(f"  - liquidity: ${rain_market['liquidity']:,}")
        print(f"  - outcomes: {len(rain_market['outcomes'])} options")
        
        print(f"\nBRain format:")
        print(f"  - market_id: {brain_market['market_id']}")
        print(f"  - belief_intensity: {brain_market['belief_intensity']:.2f}")
        print(f"  - top_options: {len(brain_market.get('top_options', []))} options" if brain_market.get('top_options') else "  - binary market")
        print(f"  - image_url: {brain_market['image_url'][:50]}...")

def test_user_positions():
    print_section("User Positions")
    client = get_rain_client()
    
    user_id = "0x1234...5678"
    data = client.get_user_positions(user_id)
    
    print(f"User: {data['user_id']}")
    print(f"Total Value: ${data['total_value']:,.2f}")
    print(f"Total P&L: ${data['total_pnl']:,.2f}\n")
    
    print("Positions:")
    for pos in data['positions']:
        pnl_color = "🟢" if pos['pnl'] > 0 else "🔴"
        print(f"  {pnl_color} {pos['market_title'][:40]}")
        print(f"     Outcome: {pos['outcome']}")
        print(f"     Shares: {pos['shares']} @ ${pos['avg_price']:.4f}")
        print(f"     Value: ${pos['current_value']:.2f}")
        print(f"     P&L: ${pos['pnl']:.2f} ({pos['pnl_percentage']:+.1f}%)")
        print()

def test_recent_trades():
    print_section("Recent Trades")
    client = get_rain_client()
    
    trades = client.list_trades(limit=10)
    
    print(f"Last {len(trades)} trades:\n")
    for trade in trades[:5]:
        side_emoji = "🟢" if trade['side'] == "buy" else "🔴"
        print(f"{side_emoji} {trade['timestamp'][:19]}")
        print(f"   Market: {trade['market_title'][:40]}")
        print(f"   {trade['side'].upper()} {trade['outcome']}: ${trade['amount']:.2f} @ ${trade['price']:.4f}")
        print(f"   User: {trade['user']}")
        print()

def test_leaderboard():
    print_section("Leaderboard")
    client = get_rain_client()
    
    leaderboard = client.get_leaderboard(limit=5)
    
    print("Top Traders:\n")
    for trader in leaderboard:
        print(f"#{trader['rank']} {trader['username']} ({trader['user_id']})")
        print(f"   Profit: ${trader['total_profit']:,.2f}")
        print(f"   Volume: ${trader['total_volume']:,.2f}")
        print(f"   Win Rate: {trader['win_rate']*100:.1f}%")
        print(f"   Markets: {trader['markets_traded']}")
        print()

def test_platform_stats():
    print_section("Platform Statistics")
    client = get_rain_client()
    
    stats = client.get_platform_stats()
    
    print(f"📊 Platform Stats\n")
    print(f"Total Markets: {stats['total_markets']}")
    print(f"Volume (24h): ${stats['total_volume_24h']:,.0f}")
    print(f"Volume (All-Time): ${stats['total_volume_all_time']:,.0f}")
    print(f"Total Liquidity: ${stats['total_liquidity']:,.0f}")
    print(f"Total Users: {stats['total_users']:,}")
    print(f"Active Users (24h): {stats['active_users_24h']:,}")
    print(f"Markets Resolved (24h): {stats['markets_resolved_24h']}")
    print(f"Avg Market Volume: ${stats['avg_market_volume']:,.2f}")

if __name__ == "__main__":
    try:
        print("\n🌧️  Testing Mock Rain Protocol API")
        print("="*70)
        
        test_health()
        test_list_markets()
        test_get_market_detail()
        test_multi_option_market()
        test_brain_conversion()
        test_user_positions()
        test_recent_trades()
        test_leaderboard()
        test_platform_stats()
        
        print(f"\n{'='*70}")
        print("  ✅ All Rain API tests completed successfully!")
        print('='*70)
        print("\n💡 Next steps:")
        print("   1. Start BRain with USE_RAIN_API=true")
        print("   2. BRain will fetch from mock Rain API")
        print("   3. When real Rain API is ready, just change RAIN_API_URL")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

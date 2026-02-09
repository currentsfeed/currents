"""
Seed the BRain database with sample markets and data
"""
import sqlite3
import json
from datetime import datetime, timedelta
import random

# Sample markets
MARKETS = [
    {
        "market_id": "m_001",
        "title": "Will the US attack Iran by January 31st?",
        "description": "Resolves YES if the United States conducts a military strike against targets in Iran before January 31, 2026.",
        "category": "Politics",
        "tags": ["US", "Iran", "Military", "Conflict", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.64,
        "volume_24h": 45000,
        "volume_total": 320000,
        "participant_count": 1234,
        "image_url": "https://images.unsplash.com/photo-1526450840302-d7f96aca0e29?w=800"
    },
    {
        "market_id": "m_002",
        "title": "Will Bitcoin hit $100k by March 2026?",
        "description": "Resolves YES if Bitcoin trades at or above $100,000 USD on any major exchange before March 31, 2026.",
        "category": "Crypto",
        "tags": ["Bitcoin", "BTC", "Crypto", "Price"],
        "taxonomy": ["Finance/Cryptocurrency/Bitcoin"],
        "probability": 0.79,
        "volume_24h": 89000,
        "volume_total": 1200000,
        "participant_count": 3456,
        "image_url": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=800"
    },
    {
        "market_id": "m_003",
        "title": "Will TikTok be banned in the US by end of 2026?",
        "description": "Resolves YES if TikTok is officially banned in the United States before December 31, 2026.",
        "category": "Technology",
        "tags": ["TikTok", "US", "Tech", "Politics", "Social Media"],
        "taxonomy": ["Technology/Social Media", "Politics/US Policy"],
        "probability": 0.41,
        "volume_24h": 34000,
        "volume_total": 230000,
        "participant_count": 1890,
        "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800"
    },
    {
        "market_id": "m_004",
        "title": "Will Israel strike Iran by March 2026?",
        "description": "Resolves YES if Israel conducts a military strike against targets in Iran before March 31, 2026.",
        "category": "Politics",
        "tags": ["Israel", "Iran", "Military", "Conflict", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.58,
        "volume_24h": 38000,
        "volume_total": 280000,
        "participant_count": 1120,
        "image_url": "https://images.unsplash.com/photo-1457364887197-9150188c107b?w=800"
    },
    {
        "market_id": "m_005",
        "title": "Will SpaceX launch Starship to orbit in Q1 2026?",
        "description": "Resolves YES if SpaceX successfully launches Starship to orbit before March 31, 2026.",
        "category": "Technology",
        "tags": ["SpaceX", "Starship", "Space", "Technology", "Elon Musk"],
        "taxonomy": ["Technology/Space/Commercial"],
        "probability": 0.82,
        "volume_24h": 42000,
        "volume_total": 310000,
        "participant_count": 1678,
        "image_url": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=800"
    },
    {
        "market_id": "m_006",
        "title": "Will LeBron James score 40+ points in his next game?",
        "description": "Resolves YES if LeBron James scores 40 or more points in his next regular season or playoff game.",
        "category": "Sports",
        "tags": ["NBA", "Basketball", "LeBron", "Lakers"],
        "taxonomy": ["Sports/Basketball/NBA"],
        "probability": 0.23,
        "volume_24h": 12000,
        "volume_total": 45000,
        "participant_count": 567,
        "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800"
    },
    {
        "market_id": "m_007",
        "title": "Will the Fed cut rates in January 2025?",
        "description": "Resolves YES if the Federal Reserve announces an interest rate cut in January 2025.",
        "category": "Economics",
        "tags": ["Fed", "Interest Rates", "Economics", "US", "Monetary Policy"],
        "taxonomy": ["Finance/Economics/Monetary Policy"],
        "probability": 0.73,
        "volume_24h": 56000,
        "volume_total": 450000,
        "participant_count": 2345,
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
    },
    {
        "market_id": "m_008",
        "title": "Will Gaza conflict end by March 2026?",
        "description": "Resolves YES if a ceasefire is reached and maintained for 30+ days before March 31, 2026.",
        "category": "Politics",
        "tags": ["Gaza", "Israel", "Palestine", "Conflict", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.35,
        "volume_24h": 29000,
        "volume_total": 180000,
        "participant_count": 1050,
        "image_url": "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=800"
    },
    # US POLITICS
    {
        "market_id": "m_009",
        "title": "Will Trump win the 2024 Republican nomination?",
        "description": "Resolves YES if Donald Trump secures the Republican Party nomination for the 2024 presidential election.",
        "category": "Politics",
        "tags": ["Trump", "Republican", "US", "Election", "2024"],
        "taxonomy": ["Politics/US Politics/Elections"],
        "probability": 0.88,
        "volume_24h": 125000,
        "volume_total": 2100000,
        "participant_count": 5678,
        "image_url": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=800"
    },
    {
        "market_id": "m_010",
        "title": "Will Biden run for reelection in 2024?",
        "description": "Resolves YES if Joe Biden is the Democratic nominee for the 2024 presidential election.",
        "category": "Politics",
        "tags": ["Biden", "Democrat", "US", "Election", "2024"],
        "taxonomy": ["Politics/US Politics/Elections"],
        "probability": 0.67,
        "volume_24h": 98000,
        "volume_total": 1450000,
        "participant_count": 4321,
        "image_url": "https://images.unsplash.com/photo-1577511131218-68818ecaf7c7?w=800"
    },
    {
        "market_id": "m_011",
        "title": "Will the US government shut down in 2026?",
        "description": "Resolves YES if the US federal government experiences a shutdown lasting at least 24 hours during 2026.",
        "category": "Politics",
        "tags": ["US", "Government", "Shutdown", "Congress", "Budget"],
        "taxonomy": ["Politics/US Politics/Domestic Policy"],
        "probability": 0.52,
        "volume_24h": 67000,
        "volume_total": 485000,
        "participant_count": 2890,
        "image_url": "https://images.unsplash.com/photo-1555532538-686a574b4353?w=800"
    },
    # INTERNATIONAL POLITICS
    {
        "market_id": "m_012",
        "title": "Will Russia and Ukraine reach a peace deal in 2026?",
        "description": "Resolves YES if Russia and Ukraine sign a formal peace agreement before December 31, 2026.",
        "category": "Politics",
        "tags": ["Russia", "Ukraine", "War", "Peace", "Europe"],
        "taxonomy": ["Politics/International Relations/Europe"],
        "probability": 0.28,
        "volume_24h": 82000,
        "volume_total": 920000,
        "participant_count": 3456,
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=800"
    },
    {
        "market_id": "m_013",
        "title": "Will China invade Taiwan by end of 2026?",
        "description": "Resolves YES if China initiates a military invasion of Taiwan before December 31, 2026.",
        "category": "Politics",
        "tags": ["China", "Taiwan", "Military", "Conflict", "Asia"],
        "taxonomy": ["Politics/International Relations/Asia"],
        "probability": 0.15,
        "volume_24h": 105000,
        "volume_total": 1560000,
        "participant_count": 4890,
        "image_url": "https://images.unsplash.com/photo-1589519160732-57fc498494f8?w=800"
    },
    {
        "market_id": "m_014",
        "title": "Will Netanyahu remain Israel PM through 2026?",
        "description": "Resolves YES if Benjamin Netanyahu is still Prime Minister of Israel on December 31, 2026.",
        "category": "Politics",
        "tags": ["Israel", "Netanyahu", "Politics", "Middle East"],
        "taxonomy": ["Politics/International Relations/Middle East"],
        "probability": 0.61,
        "volume_24h": 43000,
        "volume_total": 295000,
        "participant_count": 1890,
        "image_url": "https://images.unsplash.com/photo-1488229297570-58520851e868?w=800"
    },
    # CRYPTO MARKETS
    {
        "market_id": "m_015",
        "title": "Will Ethereum hit $5,000 by June 2026?",
        "description": "Resolves YES if Ethereum trades at or above $5,000 USD on any major exchange before June 30, 2026.",
        "category": "Crypto",
        "tags": ["Ethereum", "ETH", "Crypto", "Price"],
        "taxonomy": ["Finance/Cryptocurrency/Ethereum"],
        "probability": 0.71,
        "volume_24h": 112000,
        "volume_total": 1680000,
        "participant_count": 5234,
        "image_url": "https://images.unsplash.com/photo-1622630998477-20aa696ecb05?w=800"
    },
    {
        "market_id": "m_016",
        "title": "Will a Bitcoin ETF be approved in 2026?",
        "description": "Resolves YES if the SEC approves a spot Bitcoin ETF in the United States during 2026.",
        "category": "Crypto",
        "tags": ["Bitcoin", "ETF", "SEC", "Regulation", "US"],
        "taxonomy": ["Finance/Cryptocurrency/Regulation"],
        "probability": 0.84,
        "volume_24h": 95000,
        "volume_total": 1250000,
        "participant_count": 4567,
        "image_url": "https://images.unsplash.com/photo-1605792657660-596af9009e82?w=800"
    },
    {
        "market_id": "m_017",
        "title": "Will Solana flip Ethereum in market cap by end of 2026?",
        "description": "Resolves YES if Solana's market capitalization exceeds Ethereum's at any point before December 31, 2026.",
        "category": "Crypto",
        "tags": ["Solana", "Ethereum", "Altcoins", "Market Cap", "Crypto"],
        "taxonomy": ["Finance/Cryptocurrency/Altcoins"],
        "probability": 0.19,
        "volume_24h": 78000,
        "volume_total": 645000,
        "participant_count": 3210,
        "image_url": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800"
    },
    {
        "market_id": "m_018",
        "title": "Will Dogecoin hit $1 in 2026?",
        "description": "Resolves YES if Dogecoin trades at or above $1.00 USD on any major exchange during 2026.",
        "category": "Crypto",
        "tags": ["Dogecoin", "DOGE", "Altcoins", "Meme Coins"],
        "taxonomy": ["Finance/Cryptocurrency/Altcoins"],
        "probability": 0.34,
        "volume_24h": 56000,
        "volume_total": 420000,
        "participant_count": 2345,
        "image_url": "https://images.unsplash.com/photo-1621504450181-5d356f61d307?w=800"
    },
    # SPORTS
    {
        "market_id": "m_019",
        "title": "Will the Lakers make the NBA playoffs in 2026?",
        "description": "Resolves YES if the Los Angeles Lakers qualify for the 2026 NBA playoffs.",
        "category": "Sports",
        "tags": ["NBA", "Lakers", "Basketball", "Playoffs"],
        "taxonomy": ["Sports/Basketball/NBA"],
        "probability": 0.76,
        "volume_24h": 34000,
        "volume_total": 289000,
        "participant_count": 1567,
        "image_url": "https://images.unsplash.com/photo-1504450758481-7338eba7524a?w=800"
    },
    {
        "market_id": "m_020",
        "title": "Will the Chiefs win Super Bowl LX?",
        "description": "Resolves YES if the Kansas City Chiefs win Super Bowl LX in February 2026.",
        "category": "Sports",
        "tags": ["NFL", "Chiefs", "Super Bowl", "Football"],
        "taxonomy": ["Sports/Football/NFL"],
        "probability": 0.22,
        "volume_24h": 89000,
        "volume_total": 1120000,
        "participant_count": 4678,
        "image_url": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800"
    },
    {
        "market_id": "m_021",
        "title": "Will Real Madrid win Champions League 2026?",
        "description": "Resolves YES if Real Madrid wins the 2025-26 UEFA Champions League.",
        "category": "Sports",
        "tags": ["Soccer", "Champions League", "Real Madrid", "Football"],
        "taxonomy": ["Sports/Soccer/Champions League"],
        "probability": 0.31,
        "volume_24h": 67000,
        "volume_total": 890000,
        "participant_count": 3890,
        "image_url": "https://images.unsplash.com/photo-1522778526097-ce0a22ceb253?w=800"
    },
    {
        "market_id": "m_022",
        "title": "Will Messi score 30+ goals in 2026?",
        "description": "Resolves YES if Lionel Messi scores 30 or more goals across all competitions in calendar year 2026.",
        "category": "Sports",
        "tags": ["Soccer", "Messi", "Goals", "MLS"],
        "taxonomy": ["Sports/Soccer/MLS"],
        "probability": 0.48,
        "volume_24h": 45000,
        "volume_total": 345000,
        "participant_count": 2123,
        "image_url": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800"
    },
    {
        "market_id": "m_023",
        "title": "Will Steph Curry break the all-time 3-point record by mid-2026?",
        "description": "Resolves YES if Stephen Curry becomes the all-time leader in career 3-pointers made before June 30, 2026.",
        "category": "Sports",
        "tags": ["NBA", "Steph Curry", "Basketball", "Records"],
        "taxonomy": ["Sports/Basketball/NBA"],
        "probability": 0.89,
        "volume_24h": 23000,
        "volume_total": 178000,
        "participant_count": 1234,
        "image_url": "https://images.unsplash.com/photo-1519861531473-9200262188bf?w=800"
    },
    # TECHNOLOGY
    {
        "market_id": "m_024",
        "title": "Will OpenAI release GPT-5 in 2026?",
        "description": "Resolves YES if OpenAI officially releases a model called GPT-5 or announces its availability before December 31, 2026.",
        "category": "Technology",
        "tags": ["AI", "OpenAI", "GPT", "Machine Learning"],
        "taxonomy": ["Technology/Artificial Intelligence/LLMs"],
        "probability": 0.68,
        "volume_24h": 145000,
        "volume_total": 1890000,
        "participant_count": 6789,
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800"
    },
    {
        "market_id": "m_025",
        "title": "Will Tesla's self-driving be approved for unsupervised use in 2026?",
        "description": "Resolves YES if Tesla receives regulatory approval for fully unsupervised self-driving in any US state during 2026.",
        "category": "Technology",
        "tags": ["Tesla", "Self-Driving", "AI", "Autonomous Vehicles", "Elon Musk"],
        "taxonomy": ["Technology/Automotive/Autonomous Vehicles"],
        "probability": 0.42,
        "volume_24h": 87000,
        "volume_total": 920000,
        "participant_count": 4123,
        "image_url": "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800"
    },
    {
        "market_id": "m_026",
        "title": "Will SpaceX catch Starship booster successfully 3+ times by June 2026?",
        "description": "Resolves YES if SpaceX successfully catches the Starship Super Heavy booster at least 3 times before June 30, 2026.",
        "category": "Technology",
        "tags": ["SpaceX", "Starship", "Space", "Elon Musk"],
        "taxonomy": ["Technology/Space/Commercial"],
        "probability": 0.73,
        "volume_24h": 56000,
        "volume_total": 678000,
        "participant_count": 2890,
        "image_url": "https://images.unsplash.com/photo-1541185933-55cd36c90d51?w=800"
    },
    {
        "market_id": "m_027",
        "title": "Will Apple release an AI hardware product in 2026?",
        "description": "Resolves YES if Apple announces or releases a standalone AI-focused hardware device before December 31, 2026.",
        "category": "Technology",
        "tags": ["Apple", "AI", "Hardware", "Tech"],
        "taxonomy": ["Technology/Consumer Electronics/AI"],
        "probability": 0.55,
        "volume_24h": 72000,
        "volume_total": 845000,
        "participant_count": 3567,
        "image_url": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800"
    },
    {
        "market_id": "m_028",
        "title": "Will Google's Gemini surpass GPT-4 on benchmarks by mid-2026?",
        "description": "Resolves YES if Google's Gemini model achieves higher scores than GPT-4 on majority of major AI benchmarks before June 30, 2026.",
        "category": "Technology",
        "tags": ["AI", "Google", "Gemini", "GPT", "Machine Learning"],
        "taxonomy": ["Technology/Artificial Intelligence/LLMs"],
        "probability": 0.59,
        "volume_24h": 91000,
        "volume_total": 1120000,
        "participant_count": 4567,
        "image_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800"
    },
    # ECONOMICS
    {
        "market_id": "m_029",
        "title": "Will the Fed raise rates in Q1 2026?",
        "description": "Resolves YES if the Federal Reserve announces an interest rate increase between January 1 and March 31, 2026.",
        "category": "Economics",
        "tags": ["Fed", "Interest Rates", "Economics", "Monetary Policy"],
        "taxonomy": ["Finance/Economics/Monetary Policy"],
        "probability": 0.38,
        "volume_24h": 103000,
        "volume_total": 1340000,
        "participant_count": 5234,
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
    },
    {
        "market_id": "m_030",
        "title": "Will US enter recession in 2026?",
        "description": "Resolves YES if the US economy experiences two consecutive quarters of negative GDP growth during 2026.",
        "category": "Economics",
        "tags": ["Recession", "US", "GDP", "Economy"],
        "taxonomy": ["Finance/Economics/Macroeconomics"],
        "probability": 0.44,
        "volume_24h": 118000,
        "volume_total": 1670000,
        "participant_count": 6234,
        "image_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800"
    },
    {
        "market_id": "m_031",
        "title": "Will S&P 500 hit 6000 by end of 2026?",
        "description": "Resolves YES if the S&P 500 index closes at or above 6000 at any point before December 31, 2026.",
        "category": "Economics",
        "tags": ["Stock Market", "S&P 500", "Investing", "Markets"],
        "taxonomy": ["Finance/Markets/Equities"],
        "probability": 0.62,
        "volume_24h": 134000,
        "volume_total": 1980000,
        "participant_count": 7123,
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
    },
    {
        "market_id": "m_032",
        "title": "Will inflation fall below 2% in US by end of 2026?",
        "description": "Resolves YES if the US CPI inflation rate falls below 2.0% year-over-year before December 31, 2026.",
        "category": "Economics",
        "tags": ["Inflation", "CPI", "US", "Economy"],
        "taxonomy": ["Finance/Economics/Inflation"],
        "probability": 0.51,
        "volume_24h": 87000,
        "volume_total": 1120000,
        "participant_count": 4678,
        "image_url": "https://images.unsplash.com/photo-1579621970795-87facc2f976d?w=800"
    },
    {
        "market_id": "m_033",
        "title": "Will oil prices exceed $100/barrel in 2026?",
        "description": "Resolves YES if WTI crude oil futures trade above $100 per barrel at any point during 2026.",
        "category": "Economics",
        "tags": ["Oil", "Energy", "Commodities", "Markets"],
        "taxonomy": ["Finance/Commodities/Energy"],
        "probability": 0.47,
        "volume_24h": 76000,
        "volume_total": 890000,
        "participant_count": 3890,
        "image_url": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800"
    }
]

def seed_database(db_path='brain.db'):
    """Populate database with sample data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🌱 Seeding BRain database...")
    
    # Insert markets
    for market in MARKETS:
        cursor.execute("""
            INSERT OR REPLACE INTO markets 
            (market_id, title, description, category, probability, volume_24h, 
             volume_total, participant_count, image_url, status, created_at, resolution_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', datetime('now', '-7 days'), datetime('now', '+30 days'))
        """, (
            market['market_id'],
            market['title'],
            market['description'],
            market['category'],
            market['probability'],
            market['volume_24h'],
            market['volume_total'],
            market['participant_count'],
            market['image_url']
        ))
        
        # Insert tags
        for tag in market['tags']:
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market['market_id'], tag))
        
        # Insert taxonomy
        for taxonomy in market['taxonomy']:
            cursor.execute("""
                INSERT OR IGNORE INTO market_taxonomy (market_id, taxonomy_path)
                VALUES (?, ?)
            """, (market['market_id'], taxonomy))
        
        # Generate probability history (last 7 days)
        base_prob = market['probability']
        for days_ago in range(7, 0, -1):
            # Random walk around base probability
            variation = random.uniform(-0.05, 0.05)
            prob = max(0.05, min(0.95, base_prob + variation))
            
            cursor.execute("""
                INSERT INTO probability_history (market_id, probability, volume, timestamp)
                VALUES (?, ?, ?, datetime('now', '-' || ? || ' days'))
            """, (market['market_id'], prob, market['volume_24h'] * random.uniform(0.5, 1.5), days_ago))
    
    # Create sample users
    sample_users = ['user_001', 'user_002', 'user_003']
    for user_id in sample_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, anon_id)
            VALUES (?, ?)
        """, (user_id, f'anon_{user_id}'))
    
    # Generate sample interactions
    for _ in range(50):
        user_id = random.choice(sample_users)
        market = random.choice(MARKETS)
        event_type = random.choice(['view', 'view', 'view', 'click', 'trade'])
        
        cursor.execute("""
            INSERT INTO interactions (user_id, market_id, event_type, timestamp)
            VALUES (?, ?, ?, datetime('now', '-' || ? || ' hours'))
        """, (user_id, market['market_id'], event_type, random.randint(1, 168)))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Seeded {len(MARKETS)} markets with tags, taxonomy, and history")
    print(f"✅ Created {len(sample_users)} sample users with 50 interactions")
    print(f"✅ Database ready at: {db_path}")

if __name__ == '__main__':
    seed_database()

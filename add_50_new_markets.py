#!/usr/bin/env python3
"""
Add 50 new diverse markets to Currents for BRain personalization testing
All markets include editorial descriptions and image search keywords
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Define all 50 new markets with complete data
NEW_MARKETS = [
    # POLITICS (8 markets)
    {
        "market_id": f"new_{60001}",
        "title": "Will Trump's approval rating exceed 50% by March 2026?",
        "category": "Politics",
        "editorial_description": "Trump's second term started with strong base support but independents remain skeptical. His first 100 days will define whether he can build a broader coalition or double down on his base.",
        "image_keywords": "polling politics approval rating government"
    },
    {
        "market_id": f"new_{60002}",
        "title": "Will VP Vance run for President in 2028?",
        "category": "Politics",
        "editorial_description": "JD Vance's national profile has skyrocketed, but questions about Trump's succession plan create intrigue. Early 2028 positioning begins now with staffing and donor cultivation.",
        "image_keywords": "campaign politics presidential election"
    },
    {
        "market_id": f"new_{60003}",
        "title": "Will Senate flip to Democrats in 2026 midterms?",
        "category": "Politics",
        "editorial_description": "Republicans hold a slim Senate majority entering 2026 midterms, with several purple-state senators up for reelection. Historical midterm dynamics favor the opposition party.",
        "image_keywords": "senate congress capitol building election"
    },
    {
        "market_id": f"new_{60004}",
        "title": "Will Newsom announce 2028 presidential run by July 2026?",
        "category": "Politics",
        "editorial_description": "California's governor has been building national infrastructure and appearing on cable news non-stop. An early announcement would clear the Democratic field or spark a contested primary.",
        "image_keywords": "california governor politics campaign"
    },
    {
        "market_id": f"new_{60005}",
        "title": "Will AOC challenge Schumer in 2028 Senate primary?",
        "category": "Politics",
        "editorial_description": "Alexandria Ocasio-Cortez has transformed from backbencher to progressive powerhouse. Taking on Schumer would be the ultimate establishment challenge in deep-blue New York.",
        "image_keywords": "congress politics progressive senate"
    },
    {
        "market_id": f"new_{60006}",
        "title": "Will Supreme Court overturn same-sex marriage by 2027?",
        "category": "Politics",
        "editorial_description": "Conservative legal groups are openly strategizing to bring new cases challenging Obergefell. The court's willingness to revisit precedent after Dobbs has activists on both sides mobilizing.",
        "image_keywords": "supreme court washington dc legal"
    },
    {
        "market_id": f"new_{60007}",
        "title": "Will Trump pardon January 6 defendants by June 2026?",
        "category": "Politics",
        "editorial_description": "Trump promised pardons on the campaign trail, calling Jan 6 defendants 'hostages.' The scope and timing of clemency will test limits of presidential pardon power and political tolerance.",
        "image_keywords": "washington dc capitol politics justice"
    },
    {
        "market_id": f"new_{60008}",
        "title": "Will federal abortion ban pass Congress by 2027?",
        "category": "Politics",
        "editorial_description": "Pro-life activists are pushing for a national 15-week ban with narrow exceptions. Moderate Republicans are caught between base demands and swing district voters who favor abortion access.",
        "image_keywords": "congress politics healthcare legislation"
    },
    
    # SPORTS (10 markets)
    {
        "market_id": f"new_{60009}",
        "title": "Will Caitlin Clark win MVP in 2026 WNBA season?",
        "category": "Sports",
        "editorial_description": "Clark's rookie season shattered viewership records and elevated women's basketball. Her sophomore campaign will determine if she's a transcendent superstar or beneficiary of hype.",
        "image_keywords": "wnba basketball women sports mvp"
    },
    {
        "market_id": f"new_{60010}",
        "title": "Will Lionel Messi win 2026 World Cup with Argentina?",
        "category": "Sports",
        "editorial_description": "Messi's final World Cup arrives after his fairy-tale 2022 victory. At 39, he's defying age with Inter Miami but international soccer at altitude tests even legends.",
        "image_keywords": "messi world cup soccer argentina"
    },
    {
        "market_id": f"new_{60011}",
        "title": "Will Yankees win 2026 World Series?",
        "category": "Sports",
        "editorial_description": "Judge and Soto form baseball's most dangerous duo, but championship drought dating to 2009 weighs heavy. The Steinbrenner family is demanding October success after years of playoff disappointments.",
        "image_keywords": "yankees baseball world series stadium"
    },
    {
        "market_id": f"new_{60012}",
        "title": "Will Connor McDavid win his first Stanley Cup?",
        "category": "Sports",
        "editorial_description": "The best player of his generation still lacks the ultimate trophy. Edmonton's championship window is wide open, but McDavid's legacy hangs in the balance.",
        "image_keywords": "mcdavid oilers stanley cup ice hockey"
    },
    {
        "market_id": f"new_{60013}",
        "title": "Will Tiger Woods play in 2026 Masters?",
        "category": "Sports",
        "editorial_description": "Tiger's body continues betraying his competitive spirit, but Augusta's magic pulls him back year after year. His relationship with the Masters transcends normal athlete-event dynamics.",
        "image_keywords": "tiger woods golf masters augusta"
    },
    {
        "market_id": f"new_{60014}",
        "title": "Will Simone Biles compete in 2028 Olympics?",
        "category": "Sports",
        "editorial_description": "Biles returned triumphantly in 2024, but Los Angeles 2028 would make her 31—ancient for gymnastics. Her advocacy work may ultimately prove more impactful than more medals.",
        "image_keywords": "simone biles gymnastics olympics sports"
    },
    {
        "market_id": f"new_{60015}",
        "title": "Will Michigan repeat as College Football champions?",
        "category": "Sports",
        "editorial_description": "The Wolverines broke their title drought dramatically in 2023. Sustaining excellence in the NIL era requires both on-field coaching and off-field fundraising prowess.",
        "image_keywords": "michigan college football ncaa stadium"
    },
    {
        "market_id": f"new_{60016}",
        "title": "Will Saquon Barkley rush for 2,000 yards?",
        "category": "Sports",
        "editorial_description": "Barkley's Eagles debut was spectacular, reviving his career behind an elite offensive line. The 2,000-yard milestone remains NFL's rarest rushing achievement.",
        "image_keywords": "saquon barkley nfl football eagles"
    },
    {
        "market_id": f"new_{60017}",
        "title": "Will Jake Paul fight Canelo Alvarez?",
        "category": "Sports",
        "editorial_description": "Paul's boxing journey has gone from gimmick to genuine contender status. Taking on pound-for-pound king Canelo would be the ultimate test—or ultimate payday stunt.",
        "image_keywords": "jake paul boxing canelo fight ring"
    },
    {
        "market_id": f"new_{60018}",
        "title": "Will Novak Djokovic win another Grand Slam?",
        "category": "Sports",
        "editorial_description": "At 38, Djokovic's pursuit of records continues against Father Time and younger challengers. Each major could be his last chance to extend his Grand Slam lead.",
        "image_keywords": "djokovic tennis grand slam court"
    },
    
    # CRYPTO (7 markets)
    {
        "market_id": f"new_{60019}",
        "title": "Will Ethereum surpass $5,000 by June 2026?",
        "category": "Crypto",
        "editorial_description": "ETH has lagged Bitcoin's rally despite successful network upgrades. The flippening debate rages on as institutional adoption of smart contracts accelerates.",
        "image_keywords": "ethereum cryptocurrency blockchain digital"
    },
    {
        "market_id": f"new_{60020}",
        "title": "Will SEC approve Solana ETF by December 2026?",
        "category": "Crypto",
        "editorial_description": "Bitcoin and Ethereum ETFs opened the floodgates, but the SEC remains cautious on alt-coins. Solana's speed and ecosystem growth make it the next obvious candidate.",
        "image_keywords": "solana etf cryptocurrency blockchain"
    },
    {
        "market_id": f"new_{60021}",
        "title": "Will Coinbase stock hit $500 by end of 2026?",
        "category": "Crypto",
        "editorial_description": "Coinbase rode the crypto bull market to profitability but faces intensifying competition from BlackRock and traditional finance entering the space.",
        "image_keywords": "coinbase cryptocurrency exchange trading"
    },
    {
        "market_id": f"new_{60022}",
        "title": "Will USDC depeg below $0.95?",
        "category": "Crypto",
        "editorial_description": "Stablecoin trust is crypto's foundation, but banking crises and regulatory pressure create systemic risks. USDC's March 2023 depeg trauma still haunts the market.",
        "image_keywords": "usdc stablecoin cryptocurrency digital"
    },
    {
        "market_id": f"new_{60023}",
        "title": "Will NFT trading volume exceed $10B in Q2 2026?",
        "category": "Crypto",
        "editorial_description": "NFTs crashed from peak mania but never disappeared. Gaming integration and IP licensing deals are building sustainable utility beyond speculation.",
        "image_keywords": "nft digital art blockchain trading"
    },
    {
        "market_id": f"new_{60024}",
        "title": "Will SBF's sentence be reduced on appeal?",
        "category": "Crypto",
        "editorial_description": "Sam Bankman-Fried's 25-year sentence shocked crypto, but his legal team is arguing procedural errors. The appeals process will test DOJ's aggressive crypto enforcement strategy.",
        "image_keywords": "courthouse legal justice crypto"
    },
    {
        "market_id": f"new_{60025}",
        "title": "Will Ripple win SEC lawsuit by July 2026?",
        "category": "Crypto",
        "editorial_description": "The Ripple-SEC battle has dragged on for years, with billions in crypto regulation hanging on the outcome. A Ripple victory could greenlight dozens of alt-coins, while SEC win would consolidate power.",
        "image_keywords": "ripple xrp legal cryptocurrency regulation"
    },
    
    # TECHNOLOGY (8 markets)
    {
        "market_id": f"new_{60026}",
        "title": "Will Apple Vision Pro 2 launch by December 2026?",
        "category": "Technology",
        "editorial_description": "The Vision Pro's $3,500 price tag limited adoption despite impressive tech. Apple's playbook is iterative hardware improvements at lower price points—but spatial computing takes time to mature.",
        "image_keywords": "apple vision pro vr technology headset"
    },
    {
        "market_id": f"new_{60027}",
        "title": "Will ChatGPT reach 1 billion users?",
        "category": "Technology",
        "editorial_description": "ChatGPT revolutionized AI accessibility but competition from Google, Microsoft, and open-source models intensifies daily. The billion-user milestone would cement OpenAI's consumer dominance.",
        "image_keywords": "chatgpt ai openai technology"
    },
    {
        "market_id": f"new_{60028}",
        "title": "Will Tesla stock hit $500 by end of 2026?",
        "category": "Technology",
        "editorial_description": "Musk's political pivot and production delays have tested investor patience. Full self-driving promises and the Cybertruck's success will determine if Tesla can reignite growth.",
        "image_keywords": "tesla electric vehicle ev stock"
    },
    {
        "market_id": f"new_{60029}",
        "title": "Will SpaceX launch first manned Mars mission?",
        "category": "Technology",
        "editorial_description": "Starship test flights progress toward Musk's Mars ambitions, but manned missions require life support systems not yet demonstrated. Even Musk's optimistic timeline extends beyond 2026.",
        "image_keywords": "spacex rocket launch mars space"
    },
    {
        "market_id": f"new_{60030}",
        "title": "Will TikTok be banned in the US by end of 2026?",
        "category": "Technology",
        "editorial_description": "Congressional TikTok ban legislation passed but faces court challenges and ByteDance resistance. The app's 170 million US users represent massive political and economic leverage.",
        "image_keywords": "tiktok social media smartphone technology"
    },
    {
        "market_id": f"new_{60031}",
        "title": "Will Microsoft acquire Nintendo?",
        "category": "Technology",
        "editorial_description": "Microsoft's gaming ambitions grew with Activision-Blizzard, but Nintendo's fierce independence and Japanese corporate culture make acquisition nearly impossible. Stranger deals have happened.",
        "image_keywords": "microsoft nintendo gaming console"
    },
    {
        "market_id": f"new_{60032}",
        "title": "Will Sam Altman remain OpenAI CEO through 2026?",
        "category": "Technology",
        "editorial_description": "Altman survived his brief ouster but tensions with the board and safety concerns persist. OpenAI's explosive growth and AGI timeline create unprecedented leadership pressure.",
        "image_keywords": "sam altman openai ai ceo silicon valley"
    },
    {
        "market_id": f"new_{60033}",
        "title": "Will Google's Gemini beat GPT-5?",
        "category": "Technology",
        "editorial_description": "The AI race intensifies as Google throws its full resources behind Gemini. DeepMind's research pedigree meets Google's computational infrastructure in a battle for AI supremacy.",
        "image_keywords": "google gemini ai llm technology"
    },
    
    # ENTERTAINMENT (6 markets)
    {
        "market_id": f"new_{60034}",
        "title": "Will Barbie win Best Picture at 2026 Oscars?",
        "category": "Entertainment",
        "editorial_description": "The Barbie cultural phenomenon dominated 2023, but Academy voters historically snub blockbusters for prestige dramas. Greta Gerwig's direction and cultural impact could break the pattern.",
        "image_keywords": "barbie oscars movie awards hollywood"
    },
    {
        "market_id": f"new_{60035}",
        "title": "Will Taylor Swift marry Travis Kelce in 2026?",
        "category": "Entertainment",
        "editorial_description": "Pop culture's power couple has dominated tabloids for months. Swift's Eras Tour wraps and Kelce's NFL career timeline could align for America's most-watched wedding.",
        "image_keywords": "taylor swift celebrity couple entertainment"
    },
    {
        "market_id": f"new_{60036}",
        "title": "Will Beyoncé tour in 2026?",
        "category": "Entertainment",
        "editorial_description": "Queen Bey's Renaissance tour broke records, but touring's physical toll and her film/business empire expansion suggest she might step back from the road. Fans remain hopeful.",
        "image_keywords": "beyonce concert tour music performance"
    },
    {
        "market_id": f"new_{60037}",
        "title": "Will Succession win Emmy for Best Drama?",
        "category": "Entertainment",
        "editorial_description": "The Roy family saga concluded as prestige TV's crown jewel. Its final season sweep would cap one of television's most critically acclaimed runs in Emmy history.",
        "image_keywords": "succession emmy tv television awards"
    },
    {
        "market_id": f"new_{60038}",
        "title": "Will Avatar 3 outgross Avatar 2?",
        "category": "Entertainment",
        "editorial_description": "Cameron's Way of Water proved audiences still crave spectacle, but diminishing returns plagued franchise sequels. Avatar 3's underwater focus and production delays create uncertainty.",
        "image_keywords": "avatar movie cinema blockbuster"
    },
    {
        "market_id": f"new_{60039}",
        "title": "Will Disney+ subscriber count exceed Netflix?",
        "category": "Entertainment",
        "editorial_description": "Disney's streaming empire expanded rapidly but Netflix remains the industry leader. The streaming wars enter a mature phase where content quality trumps growth-at-any-cost.",
        "image_keywords": "disney plus netflix streaming video"
    },
    
    # ECONOMICS (6 markets)
    {
        "market_id": f"new_{60040}",
        "title": "Will unemployment rate exceed 5% by July 2026?",
        "category": "Economics",
        "editorial_description": "Labor market resilience has surprised economists, but higher interest rates traditionally lead to job losses. The Fed's soft landing attempt faces its sternest test in coming months.",
        "image_keywords": "unemployment jobs economy business"
    },
    {
        "market_id": f"new_{60041}",
        "title": "Will inflation drop below 2% target by December 2026?",
        "category": "Economics",
        "editorial_description": "The Fed's inflation fight has made progress but sticky service prices and wage growth complicate the final mile. Declaring victory too early risked 1970s-style resurgence.",
        "image_keywords": "inflation federal reserve economy finance"
    },
    {
        "market_id": f"new_{60042}",
        "title": "Will S&P 500 hit 7000 by end of 2026?",
        "category": "Economics",
        "editorial_description": "Markets surged on AI optimism and soft landing hopes, but valuations stretched. The path to 7000 requires sustained earnings growth without recession or major geopolitical shocks.",
        "image_keywords": "stock market sp500 wall street trading"
    },
    {
        "market_id": f"new_{60043}",
        "title": "Will housing prices fall 10% nationally by year-end?",
        "category": "Economics",
        "editorial_description": "Sky-high mortgage rates froze the housing market but prices remained sticky. A 10% correction would provide relief for buyers but devastate recent homeowners and construction industries.",
        "image_keywords": "housing real estate market prices"
    },
    {
        "market_id": f"new_{60044}",
        "title": "Will Fed cut rates by 1% or more in 2026?",
        "category": "Economics",
        "editorial_description": "Powell's Fed maintained higher-for-longer stance, but economic data could force aggressive cutting. The debate centers on whether cuts signal victory over inflation or panic over recession.",
        "image_keywords": "federal reserve interest rates economy"
    },
    {
        "market_id": f"new_{60045}",
        "title": "Will U.S. enter recession in 2026?",
        "category": "Economics",
        "editorial_description": "Recession calls have been wrong for two years, but inverted yield curves and tightening credit conditions historically precede downturns. The question is when, not if.",
        "image_keywords": "recession economy gdp business downturn"
    },
    
    # WORLD (5 markets)
    {
        "market_id": f"new_{60046}",
        "title": "Will Israel and Hamas reach ceasefire by March 2026?",
        "category": "World",
        "editorial_description": "The Gaza conflict drags on despite international pressure and humanitarian catastrophe. Ceasefire negotiations have repeatedly stalled over hostage releases and security guarantees.",
        "image_keywords": "peace talks diplomacy international israel"
    },
    {
        "market_id": f"new_{60047}",
        "title": "Will North Korea conduct nuclear test in 2026?",
        "category": "World",
        "editorial_description": "Kim Jong Un's weapons program accelerated despite sanctions. A seventh nuclear test would escalate regional tensions and test US-South Korea-Japan alliance coordination.",
        "image_keywords": "north korea nuclear military weapons"
    },
    {
        "market_id": f"new_{60048}",
        "title": "Will UK rejoin EU by 2027?",
        "category": "World",
        "editorial_description": "Brexit's economic pain has fueled rejoiner sentiment, but EU skepticism and UK politics complicate any return. Labour's election victory changed dynamics but not EU appetite for British drama.",
        "image_keywords": "brexit uk eu britain parliament london"
    },
    {
        "market_id": f"new_{60049}",
        "title": "Will India surpass China in population officially?",
        "category": "World",
        "editorial_description": "India likely already eclipsed China as world's most populous nation, but official census data lags. The demographic shift reshapes global economic and political power dynamics.",
        "image_keywords": "india china population demographics"
    },
    {
        "market_id": f"new_{60050}",
        "title": "Will Mexico legalize all drugs by end of 2026?",
        "category": "World",
        "editorial_description": "Mexico's progressive president pushed decriminalization amid cartel violence, but conservative opposition and US pressure create obstacles. Full legalization would be unprecedented globally.",
        "image_keywords": "mexico politics government policy"
    },
]

def add_markets_to_database():
    """Add all 50 new markets to the database with realistic probabilities"""
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    print(f"\n{'='*80}")
    print(f"ADDING 50 NEW MARKETS TO CURRENTS")
    print(f"{'='*80}\n")
    
    for i, market in enumerate(NEW_MARKETS, 1):
        # Generate realistic random data
        probability = random.uniform(0.15, 0.85)
        volume_24h = random.uniform(50000, 800000)
        volume_total = volume_24h * random.uniform(3, 15)
        participant_count = int(volume_total / random.uniform(500, 2000))
        
        # Resolution date (3-12 months out)
        resolution_days = random.randint(90, 365)
        resolution_date = (datetime.now() + timedelta(days=resolution_days)).strftime('%Y-%m-%d')
        
        # Placeholder image URL (will be replaced with real images)
        image_url = f"/static/images/market_{market['market_id']}.jpg"
        
        # Create description from resolution criteria (placeholder)
        description = f"This market will resolve based on official announcements and credible news sources by {resolution_date}."
        
        try:
            cursor.execute("""
                INSERT INTO markets (
                    market_id, title, description, category, 
                    probability, volume_24h, volume_total, participant_count,
                    image_url, editorial_description, resolution_date,
                    status, market_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                market['market_id'],
                market['title'],
                description,
                market['category'],
                probability,
                volume_24h,
                volume_total,
                participant_count,
                image_url,
                market['editorial_description'],
                resolution_date,
                'open',
                'binary'
            ))
            
            print(f"[{i}/50] ✅ Added: {market['title'][:60]}")
            print(f"        Category: {market['category']} | Probability: {probability:.1%}")
            
        except sqlite3.IntegrityError as e:
            print(f"[{i}/50] ⚠️  Skipped (exists): {market['title'][:60]}")
    
    conn.commit()
    
    # Print summary
    cursor.execute("SELECT COUNT(*) FROM markets")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM markets GROUP BY category ORDER BY COUNT(*) DESC")
    categories = cursor.fetchall()
    
    conn.close()
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total markets in database: {total}")
    print(f"\nCategory breakdown:")
    for cat, count in categories:
        print(f"  {cat}: {count} markets")
    
    print(f"\n✅ All 50 new markets added successfully!")
    print(f"\n📝 Next steps:")
    print(f"1. Get valid Pexels/Unsplash API key")
    print(f"2. Run image curation script to fetch topic-relevant images")
    print(f"3. Test BRain personalization with diverse market set")
    
    return total

if __name__ == '__main__':
    add_markets_to_database()

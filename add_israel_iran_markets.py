#!/usr/bin/env python3
"""
Add 30 Israel/Iran-related markets to the database
With images, belief currents, volume, descriptions, etc.
"""

import sqlite3
import os
import random
import requests
from datetime import datetime, timedelta
import time
import hashlib

# Unsplash API key
UNSPLASH_ACCESS_KEY = open('.unsplash_key').read().strip() if os.path.exists('.unsplash_key') else None

DB_PATH = 'brain.db'

# 30 Israel/Iran-related markets
MARKETS = [
    # Israel Politics
    {
        "title": "Will Netanyahu remain PM through 2025?",
        "description": "Will Benjamin Netanyahu continue to serve as Prime Minister of Israel for the entirety of 2025?",
        "editorial_description": "Netanyahu's coalition faces mounting pressure from judicial reform protests and coalition tensions.",
        "category": "Politics",
        "probability": 0.62,
        "tags": ["netanyahu", "israel", "politics"],
        "search_term": "israel parliament"
    },
    {
        "title": "Will Israel hold early elections in 2025?",
        "description": "Will Israel hold national elections before the scheduled 2026 election date?",
        "editorial_description": "Coalition instability and protests could trigger snap elections this year.",
        "category": "Politics",
        "probability": 0.44,
        "tags": ["israel", "elections", "politics"],
        "search_term": "israel voting"
    },
    {
        "title": "Will Israeli judicial reform pass in 2025?",
        "description": "Will the Israeli government successfully pass comprehensive judicial reform legislation in 2025?",
        "editorial_description": "Controversial judicial overhaul continues to divide Israeli society and politics.",
        "category": "Politics",
        "probability": 0.38,
        "tags": ["israel", "judicial", "reform"],
        "search_term": "israel protest"
    },
    
    # Iran Nuclear Program
    {
        "title": "Will Iran enrich uranium above 90% by July 2025?",
        "description": "Will Iran enrich uranium to weapons-grade levels (>90% purity) by July 2025?",
        "editorial_description": "Iran's nuclear program accelerates as JCPOA talks remain stalled.",
        "category": "World",
        "probability": 0.71,
        "tags": ["iran", "nuclear", "uranium"],
        "search_term": "iran nuclear facility"
    },
    {
        "title": "Will US/Iran revive nuclear deal in 2025?",
        "description": "Will the United States and Iran successfully revive the JCPOA nuclear agreement in 2025?",
        "editorial_description": "Diplomatic efforts continue despite years of impasse on nuclear negotiations.",
        "category": "Politics",
        "probability": 0.18,
        "tags": ["iran", "nuclear", "jcpoa", "usa"],
        "search_term": "iran flag"
    },
    {
        "title": "Will Iran test a nuclear device by 2026?",
        "description": "Will Iran conduct its first nuclear weapons test by the end of 2026?",
        "editorial_description": "Analysts warn Iran may be months away from breakout capability.",
        "category": "World",
        "probability": 0.24,
        "tags": ["iran", "nuclear", "weapons"],
        "search_term": "iran military"
    },
    
    # Israel-Iran Conflict
    {
        "title": "Will Israel strike Iranian nuclear sites in 2025?",
        "description": "Will Israel launch military strikes against Iranian nuclear facilities in 2025?",
        "editorial_description": "Israeli officials hint at unilateral action as diplomatic options narrow.",
        "category": "World",
        "probability": 0.33,
        "tags": ["israel", "iran", "military", "nuclear"],
        "search_term": "military aircraft"
    },
    {
        "title": "Will Iran directly attack Israel in 2025?",
        "description": "Will Iran launch a direct military attack on Israeli territory from Iranian soil in 2025?",
        "editorial_description": "Shadow war escalates with unprecedented April 2024 missile barrage still fresh.",
        "category": "World",
        "probability": 0.41,
        "tags": ["iran", "israel", "conflict"],
        "search_term": "missile launch"
    },
    {
        "title": "Will Israel-Iran engage in open warfare by 2026?",
        "description": "Will Israel and Iran be in a state of open, declared war by the end of 2026?",
        "editorial_description": "Regional tensions reach boiling point as proxy conflicts intensify.",
        "category": "World",
        "probability": 0.29,
        "tags": ["israel", "iran", "war"],
        "search_term": "war conflict"
    },
    
    # Gaza & Hamas
    {
        "title": "Will Gaza ceasefire last >90 days in 2025?",
        "description": "Will any Gaza ceasefire agreement hold for more than 90 consecutive days in 2025?",
        "editorial_description": "Fragile truces repeatedly collapse as humanitarian crisis deepens.",
        "category": "World",
        "probability": 0.36,
        "tags": ["gaza", "israel", "ceasefire"],
        "search_term": "gaza destruction"
    },
    {
        "title": "Will Hamas remain in power in Gaza through 2025?",
        "description": "Will Hamas maintain control of Gaza Strip governance throughout 2025?",
        "editorial_description": "Hamas faces military pressure but maintains administrative control amid war.",
        "category": "Politics",
        "probability": 0.67,
        "tags": ["hamas", "gaza", "israel"],
        "search_term": "gaza city"
    },
    {
        "title": "Will Israeli hostages all be released by July 2025?",
        "description": "Will all Israeli hostages held in Gaza be released by July 2025?",
        "editorial_description": "Over 100 hostages remain captive as negotiations stall repeatedly.",
        "category": "World",
        "probability": 0.21,
        "tags": ["hostages", "israel", "hamas"],
        "search_term": "protest signs"
    },
    
    # Hezbollah & Lebanon
    {
        "title": "Will Israel invade South Lebanon in 2025?",
        "description": "Will Israel launch a ground invasion of southern Lebanon in 2025?",
        "editorial_description": "Northern border exchanges escalate beyond October 7th skirmishes.",
        "category": "World",
        "probability": 0.48,
        "tags": ["israel", "lebanon", "hezbollah"],
        "search_term": "lebanon border"
    },
    {
        "title": "Will Hezbollah fire >1000 rockets at Israel in single day?",
        "description": "Will Hezbollah launch more than 1,000 rockets at Israel in a single day during 2025?",
        "editorial_description": "Hezbollah's massive arsenal threatens unprecedented escalation.",
        "category": "World",
        "probability": 0.52,
        "tags": ["hezbollah", "israel", "rockets"],
        "search_term": "rocket trail sky"
    },
    {
        "title": "Will Nasrallah be killed/removed by Dec 2025?",
        "description": "Will Hassan Nasrallah cease to be Hezbollah's leader (death or removal) by December 2025?",
        "editorial_description": "Israeli intelligence reportedly intensifies hunt for Hezbollah's longtime chief.",
        "category": "World",
        "probability": 0.27,
        "tags": ["nasrallah", "hezbollah", "israel"],
        "search_term": "hezbollah flag"
    },
    
    # Regional Powers
    {
        "title": "Will Saudi Arabia normalize relations with Israel in 2025?",
        "description": "Will Saudi Arabia and Israel establish formal diplomatic relations in 2025?",
        "editorial_description": "Abraham Accords expansion hinges on Palestinian state progress.",
        "category": "Politics",
        "probability": 0.31,
        "tags": ["saudi", "israel", "diplomacy"],
        "search_term": "saudi arabia"
    },
    {
        "title": "Will US strike Iranian targets in 2025?",
        "description": "Will the United States conduct military strikes against Iranian targets in 2025?",
        "editorial_description": "US warns of consequences for attacks on American forces in region.",
        "category": "World",
        "probability": 0.44,
        "tags": ["usa", "iran", "military"],
        "search_term": "us military"
    },
    {
        "title": "Will Iran close Strait of Hormuz for >7 days?",
        "description": "Will Iran successfully block the Strait of Hormuz to shipping for more than 7 consecutive days in 2025-26?",
        "editorial_description": "Tehran threatens oil chokepoint as tensions with West escalate.",
        "category": "World",
        "probability": 0.16,
        "tags": ["iran", "hormuz", "oil"],
        "search_term": "strait hormuz"
    },
    
    # Economy & Energy
    {
        "title": "Will oil hit $150/barrel due to Mideast conflict?",
        "description": "Will oil prices exceed $150 per barrel due to Middle East conflict escalation in 2025?",
        "editorial_description": "Energy markets jittery over potential supply disruptions.",
        "category": "Economics",
        "probability": 0.23,
        "tags": ["oil", "iran", "energy"],
        "search_term": "oil refinery"
    },
    {
        "title": "Will Iran sanctions be fully reimposed by US?",
        "description": "Will the US reimpose full pre-JCPOA sanctions on Iran by end of 2025?",
        "editorial_description": "Maximum pressure campaign could return as nuclear diplomacy fails.",
        "category": "Politics",
        "probability": 0.59,
        "tags": ["iran", "sanctions", "usa"],
        "search_term": "oil tanker"
    },
    
    # Israeli Society
    {
        "title": "Will >100K Israelis emigrate in 2025?",
        "description": "Will more than 100,000 Israelis emigrate from Israel in 2025?",
        "editorial_description": "Brain drain concerns grow amid political turmoil and security fears.",
        "category": "World",
        "probability": 0.34,
        "tags": ["israel", "emigration"],
        "search_term": "tel aviv"
    },
    {
        "title": "Will West Bank violence kill >500 in 2025?",
        "description": "Will Israeli-Palestinian violence in the West Bank result in more than 500 deaths in 2025?",
        "editorial_description": "West Bank sees deadliest period in decades as clashes intensify.",
        "category": "World",
        "probability": 0.46,
        "tags": ["westbank", "israel", "violence"],
        "search_term": "west bank"
    },
    {
        "title": "Will Israeli settlers surpass 1M in West Bank?",
        "description": "Will the number of Israeli settlers in the West Bank exceed 1 million by end of 2025?",
        "editorial_description": "Settlement expansion accelerates despite international condemnation.",
        "category": "Politics",
        "probability": 0.28,
        "tags": ["settlements", "westbank", "israel"],
        "search_term": "israeli settlement"
    },
    
    # International Relations
    {
        "title": "Will ICC issue Netanyahu arrest warrant?",
        "description": "Will the International Criminal Court issue an arrest warrant for Benjamin Netanyahu in 2025?",
        "editorial_description": "War crimes investigation advances as prosecutor seeks approval.",
        "category": "Politics",
        "probability": 0.42,
        "tags": ["netanyahu", "icc", "israel"],
        "search_term": "international court"
    },
    {
        "title": "Will UN Security Council vote for Palestinian state?",
        "description": "Will the UN Security Council vote to recognize Palestinian statehood in 2025?",
        "editorial_description": "US veto power faces test as international pressure mounts.",
        "category": "Politics",
        "probability": 0.37,
        "tags": ["palestine", "un", "statehood"],
        "search_term": "united nations"
    },
    {
        "title": "Will EU sanction Israeli officials in 2025?",
        "description": "Will the European Union impose sanctions on Israeli government officials in 2025?",
        "editorial_description": "European patience wears thin over settlement policy and Gaza operations.",
        "category": "Politics",
        "probability": 0.41,
        "tags": ["eu", "israel", "sanctions"],
        "search_term": "european union"
    },
    
    # Technology & Cyber
    {
        "title": "Will Iran launch major cyberattack on Israel?",
        "description": "Will Iran conduct a cyberattack causing >$1B damage to Israeli infrastructure in 2025-26?",
        "editorial_description": "Cyber warfare intensifies as both nations target critical systems.",
        "category": "Technology",
        "probability": 0.31,
        "tags": ["cyber", "iran", "israel"],
        "search_term": "cyber security"
    },
    {
        "title": "Will Israel hit Iranian nuclear scientist?",
        "description": "Will Israel assassinate a senior Iranian nuclear scientist in 2025?",
        "editorial_description": "Mossad operations continue targeting Iran's nuclear brain trust.",
        "category": "World",
        "probability": 0.39,
        "tags": ["mossad", "iran", "nuclear"],
        "search_term": "scientist lab"
    },
    
    # Wildcard Scenarios
    {
        "title": "Will Putin visit Tehran in 2025?",
        "description": "Will Russian President Vladimir Putin make an official state visit to Tehran in 2025?",
        "editorial_description": "Russia-Iran military partnership deepens amid mutual isolation.",
        "category": "Politics",
        "probability": 0.56,
        "tags": ["russia", "iran", "putin"],
        "search_term": "kremlin"
    },
    {
        "title": "Will Iran join BRICS officially in 2025?",
        "description": "Will Iran become a full member of the BRICS economic bloc in 2025?",
        "editorial_description": "Tehran seeks economic alternatives as Western sanctions bite.",
        "category": "Economics",
        "probability": 0.68,
        "tags": ["iran", "brics", "economics"],
        "search_term": "brics summit"
    },
]

def download_image(search_term, output_dir='static/images'):
    """Download image from Unsplash"""
    if not UNSPLASH_ACCESS_KEY:
        print(f"⚠️  No Unsplash API key - skipping image for '{search_term}'")
        return None
    
    try:
        # Search for relevant image
        url = 'https://api.unsplash.com/search/photos'
        params = {
            'query': search_term,
            'per_page': 1,
            'orientation': 'landscape'
        }
        headers = {
            'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data['results']:
            print(f"⚠️  No images found for '{search_term}'")
            return None
        
        photo = data['results'][0]
        image_url = photo['urls']['regular']
        
        # Download image
        img_response = requests.get(image_url, timeout=10)
        img_response.raise_for_status()
        
        # Generate filename
        filename = f"israel_iran_{hashlib.md5(search_term.encode()).hexdigest()[:8]}.jpg"
        filepath = os.path.join(output_dir, filename)
        
        # Save image
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(img_response.content)
        
        print(f"✅ Downloaded: {filename} ({search_term})")
        return f"/static/images/{filename}"
        
    except Exception as e:
        print(f"❌ Error downloading image for '{search_term}': {e}")
        return None

def generate_belief_history(current_prob, days_back=30):
    """Generate realistic probability history"""
    history = []
    now = datetime.now()
    
    # Start from a different probability
    start_prob = current_prob + random.uniform(-0.15, 0.15)
    start_prob = max(0.1, min(0.9, start_prob))
    
    for i in range(days_back):
        date = now - timedelta(days=days_back - i)
        # Gradually move toward current probability
        progress = i / days_back
        prob = start_prob + (current_prob - start_prob) * progress
        # Add some random noise
        prob += random.uniform(-0.05, 0.05)
        prob = max(0.05, min(0.95, prob))
        
        history.append({
            'date': date.isoformat(),
            'probability': round(prob, 3)
        })
    
    return history

def add_markets_to_db():
    """Add all markets to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🇮🇱 Adding 30 Israel/Iran Markets 🇮🇷\n")
    print("=" * 60)
    
    added_count = 0
    
    for market in MARKETS:
        # Generate market ID
        market_id = f"israel_iran_{hashlib.md5(market['title'].encode()).hexdigest()[:8]}"
        
        # Check if already exists
        cursor.execute("SELECT market_id FROM markets WHERE market_id = ?", (market_id,))
        if cursor.fetchone():
            print(f"⏭️  Skipping (exists): {market['title'][:50]}...")
            continue
        
        # Download image
        image_url = download_image(market['search_term'])
        if not image_url:
            # Use placeholder if download fails
            image_url = "/static/images/default.jpg"
        
        # Generate volumes
        volume_24h = random.randint(50000, 500000)
        volume_total = random.randint(volume_24h * 5, volume_24h * 20)
        
        # Generate belief history
        history = generate_belief_history(market['probability'])
        
        # Insert market
        created_at = (datetime.now() - timedelta(days=random.randint(10, 60))).isoformat()
        resolution_date = (datetime.now() + timedelta(days=random.randint(60, 365))).isoformat()
        
        cursor.execute("""
            INSERT INTO markets (
                market_id, title, description, category, probability,
                volume_24h, volume_total, image_url, created_at, resolution_date,
                status, market_type, editorial_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            market_id,
            market['title'],
            market['description'],
            market['category'],
            market['probability'],
            volume_24h,
            volume_total,
            image_url,
            created_at,
            resolution_date,
            'open',
            'binary',
            market['editorial_description']
        ))
        
        # Insert tags
        for tag in market['tags']:
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market_id, tag))
        
        # Insert belief history
        for point in history:
            cursor.execute("""
                INSERT INTO probability_history (market_id, timestamp, probability, volume)
                VALUES (?, ?, ?, ?)
            """, (market_id, point['date'], point['probability'], volume_24h))
        
        conn.commit()
        added_count += 1
        print(f"✅ Added: {market['title']}")
        
        # Rate limit for Unsplash API
        time.sleep(1)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"\n✨ Successfully added {added_count} markets!")
    print(f"📊 Total markets in database: {get_total_markets()}")
    print("\n🎯 Markets cover:")
    print("  • Israeli politics & elections")
    print("  • Iran nuclear program")
    print("  • Israel-Iran conflict scenarios")
    print("  • Gaza & Hamas situation")
    print("  • Hezbollah & Lebanon tensions")
    print("  • Regional diplomacy")
    print("  • Economic impacts")
    print("  • International law & UN")
    print("  • Cyber warfare")
    print("  • Geopolitical wildcards")

def get_total_markets():
    """Get total market count"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM markets")
    count = cursor.fetchone()[0]
    conn.close()
    return count

if __name__ == '__main__':
    add_markets_to_db()

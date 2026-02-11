#!/usr/bin/env python3
"""
Create upcoming sports markets (next 2-3 days)
Based on typical February schedules for major leagues
"""
import json
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = 'brain.db'

def get_resolution_date(days_ahead):
    """Get resolution date N days from now"""
    return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

# Upcoming sports markets (Feb 12-14, 2026)
SPORTS_MARKETS = [
    # NBA (Tuesday Feb 11, Wednesday Feb 12, Thursday Feb 13)
    {
        'id': 'nba-lakers-celtics-feb12',
        'title': 'Will Lakers defeat Celtics on Feb 12?',
        'description': 'Lakers vs Celtics at TD Garden. Lakers coming off 3-game win streak, Celtics leading Eastern Conference. Key matchup between LeBron and Tatum.',
        'category': 'Basketball',
        'subcategory': 'NBA',
        'probability': 0.42,
        'volume': 85000,
        'resolution_date': get_resolution_date(1),
        'tags': ['NBA', 'Lakers', 'Celtics', 'Basketball', 'LeBron James', 'Jayson Tatum'],
        'image': 'static/images/sports_nba_lakers_celtics.jpg'
    },
    {
        'id': 'nba-warriors-suns-feb12',
        'title': 'Will Warriors beat Suns by 5+ points on Feb 12?',
        'description': 'Warriors vs Suns at Chase Center. Curry averaging 28 PPG this month. Suns missing key players due to injury. Warriors favored at home.',
        'category': 'Basketball',
        'subcategory': 'NBA',
        'probability': 0.58,
        'volume': 92000,
        'resolution_date': get_resolution_date(1),
        'tags': ['NBA', 'Warriors', 'Suns', 'Basketball', 'Stephen Curry', 'Kevin Durant'],
        'image': 'static/images/sports_nba_warriors_suns.jpg'
    },
    {
        'id': 'nba-bucks-nets-feb13',
        'title': 'Will Giannis score 35+ points vs Nets on Feb 13?',
        'description': 'Bucks vs Nets at Barclays Center. Giannis averaging 32 PPG last 5 games. Nets defense struggling. Over/under set at 34.5 points.',
        'category': 'Basketball',
        'subcategory': 'NBA',
        'probability': 0.52,
        'volume': 78000,
        'resolution_date': get_resolution_date(2),
        'tags': ['NBA', 'Bucks', 'Nets', 'Basketball', 'Giannis Antetokounmpo', 'Player Props'],
        'image': 'static/images/sports_nba_bucks_nets.jpg'
    },
    {
        'id': 'nba-mavs-nuggets-feb13',
        'title': 'Will Mavericks upset Nuggets on Feb 13?',
        'description': 'Mavericks vs Nuggets at Ball Arena. Luka Doncic vs Nikola Jokic showdown. Nuggets 8-2 at home. Mavericks underdogs but playing well.',
        'category': 'Basketball',
        'subcategory': 'NBA',
        'probability': 0.38,
        'volume': 105000,
        'resolution_date': get_resolution_date(2),
        'tags': ['NBA', 'Mavericks', 'Nuggets', 'Basketball', 'Luka Doncic', 'Nikola Jokic'],
        'image': 'static/images/sports_nba_mavs_nuggets.jpg'
    },
    {
        'id': 'nba-heat-sixers-feb13',
        'title': 'Will Heat-76ers game go over 225.5 total points?',
        'description': 'Heat vs 76ers at Wells Fargo Center. Both teams averaging 115+ PPG. Fast-paced matchup. Over/under total set at 225.5 points.',
        'category': 'Basketball',
        'subcategory': 'NBA',
        'probability': 0.49,
        'volume': 67000,
        'resolution_date': get_resolution_date(2),
        'tags': ['NBA', 'Heat', '76ers', 'Basketball', 'Over/Under', 'Totals'],
        'image': 'static/images/sports_nba_heat_sixers.jpg'
    },
    
    # Premier League (Weekend Feb 14-15)
    {
        'id': 'epl-arsenal-liverpool-feb14',
        'title': 'Will Arsenal defeat Liverpool on Feb 14?',
        'description': 'Arsenal vs Liverpool at Emirates Stadium. Title race clash. Arsenal unbeaten at home. Liverpool in form with 5 straight wins. Match of the week.',
        'category': 'Soccer',
        'subcategory': 'Premier League',
        'probability': 0.45,
        'volume': 215000,
        'resolution_date': get_resolution_date(3),
        'tags': ['Soccer', 'Premier League', 'Arsenal', 'Liverpool', 'English Football'],
        'image': 'static/images/sports_epl_arsenal_liverpool.jpg'
    },
    {
        'id': 'epl-mancity-chelsea-feb15',
        'title': 'Will Man City win vs Chelsea on Feb 15?',
        'description': 'Manchester City vs Chelsea at Etihad Stadium. City chasing leaders. Haaland in red-hot form. Chelsea struggling for consistency.',
        'category': 'Soccer',
        'subcategory': 'Premier League',
        'probability': 0.68,
        'volume': 195000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Soccer', 'Premier League', 'Manchester City', 'Chelsea', 'Erling Haaland'],
        'image': 'static/images/sports_epl_city_chelsea.jpg'
    },
    {
        'id': 'epl-united-spurs-feb15',
        'title': 'Will Man United vs Tottenham end in draw?',
        'description': 'Manchester United vs Tottenham at Old Trafford. Classic rivalry match. Both teams inconsistent. Last 3 meetings ended in draws.',
        'category': 'Soccer',
        'subcategory': 'Premier League',
        'probability': 0.32,
        'volume': 142000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Soccer', 'Premier League', 'Manchester United', 'Tottenham', 'Draw'],
        'image': 'static/images/sports_epl_united_spurs.jpg'
    },
    {
        'id': 'epl-salah-hat-trick-feb14',
        'title': 'Will Mohamed Salah score hat-trick vs Arsenal?',
        'description': 'Salah vs Arsenal at Emirates. Salah has 3 hat-tricks vs Arsenal historically. Arsenal defense vulnerable. Long odds but possible.',
        'category': 'Soccer',
        'subcategory': 'Premier League',
        'probability': 0.08,
        'volume': 45000,
        'resolution_date': get_resolution_date(3),
        'tags': ['Soccer', 'Premier League', 'Mohamed Salah', 'Liverpool', 'Hat-trick', 'Player Props'],
        'image': 'static/images/sports_epl_salah.jpg'
    },
    
    # Champions League (Round of 16 - Feb 12-13)
    {
        'id': 'ucl-psg-barcelona-feb12',
        'title': 'Will PSG defeat Barcelona in Champions League on Feb 12?',
        'description': 'PSG vs Barcelona, Champions League Round of 16 first leg at Parc des Princes. Mbappe vs Lewandowski. High-stakes knockout match.',
        'category': 'Soccer',
        'subcategory': 'Champions League',
        'probability': 0.54,
        'volume': 325000,
        'resolution_date': get_resolution_date(1),
        'tags': ['Soccer', 'Champions League', 'PSG', 'Barcelona', 'UEFA', 'Kylian Mbappe'],
        'image': 'static/images/sports_ucl_psg_barca.jpg'
    },
    {
        'id': 'ucl-bayern-atletico-feb13',
        'title': 'Will Bayern Munich beat Atletico Madrid on Feb 13?',
        'description': 'Bayern Munich vs Atletico Madrid, Champions League Round of 16. Allianz Arena. Bayern dominant at home. Atletico defensive masters.',
        'category': 'Soccer',
        'subcategory': 'Champions League',
        'probability': 0.62,
        'volume': 285000,
        'resolution_date': get_resolution_date(2),
        'tags': ['Soccer', 'Champions League', 'Bayern Munich', 'Atletico Madrid', 'UEFA'],
        'image': 'static/images/sports_ucl_bayern_atletico.jpg'
    },
    {
        'id': 'ucl-both-teams-score-feb12',
        'title': 'Will both teams score in PSG vs Barcelona?',
        'description': 'Both teams to score in PSG vs Barcelona Champions League clash. Attacking lineups. High-scoring expected. BTTS odds at 1.65.',
        'category': 'Soccer',
        'subcategory': 'Champions League',
        'probability': 0.71,
        'volume': 156000,
        'resolution_date': get_resolution_date(1),
        'tags': ['Soccer', 'Champions League', 'BTTS', 'PSG', 'Barcelona', 'Goals'],
        'image': 'static/images/sports_ucl_btts.jpg'
    },
    
    # NHL (Multiple games per night)
    {
        'id': 'nhl-rangers-bruins-feb12',
        'title': 'Will Rangers defeat Bruins on Feb 12?',
        'description': 'Rangers vs Bruins at TD Garden. Atlantic Division rivalry. Rangers on 4-game win streak. Bruins strong at home. Goalie duel.',
        'category': 'Hockey',
        'subcategory': 'NHL',
        'probability': 0.44,
        'volume': 62000,
        'resolution_date': get_resolution_date(1),
        'tags': ['Hockey', 'NHL', 'Rangers', 'Bruins', 'Ice Hockey'],
        'image': 'static/images/sports_nhl_rangers_bruins.jpg'
    },
    {
        'id': 'nhl-oilers-avalanche-feb13',
        'title': 'Will Oilers-Avalanche game have 7+ total goals?',
        'description': 'Oilers vs Avalanche at Ball Arena. McDavid vs MacKinnon. Two highest-scoring teams. Over/under set at 6.5 goals.',
        'category': 'Hockey',
        'subcategory': 'NHL',
        'probability': 0.56,
        'volume': 71000,
        'resolution_date': get_resolution_date(2),
        'tags': ['Hockey', 'NHL', 'Oilers', 'Avalanche', 'Over/Under', 'Connor McDavid'],
        'image': 'static/images/sports_nhl_oilers_avs.jpg'
    },
    {
        'id': 'nhl-leafs-panthers-feb13',
        'title': 'Will Maple Leafs upset Panthers on Feb 13?',
        'description': 'Maple Leafs vs Panthers at FLA Live Arena. Panthers defending champions. Matthews scoring at will. Leafs underdogs.',
        'category': 'Hockey',
        'subcategory': 'NHL',
        'probability': 0.41,
        'volume': 58000,
        'resolution_date': get_resolution_date(2),
        'tags': ['Hockey', 'NHL', 'Maple Leafs', 'Panthers', 'Auston Matthews'],
        'image': 'static/images/sports_nhl_leafs_panthers.jpg'
    },
    
    # NPB (Japan Baseball - Spring Training)
    {
        'id': 'npb-giants-tigers-feb14',
        'title': 'Will Yomiuri Giants defeat Hanshin Tigers in spring game?',
        'description': 'Yomiuri Giants vs Hanshin Tigers spring training exhibition. Giants testing new lineup. Tigers have strong pitching. Preseason warmup.',
        'category': 'Baseball',
        'subcategory': 'NPB',
        'probability': 0.51,
        'volume': 35000,
        'resolution_date': get_resolution_date(3),
        'tags': ['Baseball', 'NPB', 'Japan', 'Yomiuri Giants', 'Hanshin Tigers', 'Japanese Baseball'],
        'image': 'static/images/sports_npb_giants_tigers.jpg'
    },
    {
        'id': 'npb-fighters-marines-feb14',
        'title': 'Will Hokkaido Fighters beat Chiba Marines by 2+ runs?',
        'description': 'Fighters vs Marines spring exhibition. Fighters strong preseason form. Marines rebuilding. Run line set at 1.5 runs.',
        'category': 'Baseball',
        'subcategory': 'NPB',
        'probability': 0.48,
        'volume': 28000,
        'resolution_date': get_resolution_date(3),
        'tags': ['Baseball', 'NPB', 'Japan', 'Hokkaido Fighters', 'Chiba Marines', 'Run Line'],
        'image': 'static/images/sports_npb_fighters_marines.jpg'
    },
    
    # La Liga (Spain)
    {
        'id': 'laliga-real-madrid-villarreal-feb15',
        'title': 'Will Real Madrid win vs Villarreal on Feb 15?',
        'description': 'Real Madrid vs Villarreal at Santiago Bernabéu. Madrid chasing Barcelona. Vinicius Jr in form. Villarreal tough opponent.',
        'category': 'Soccer',
        'subcategory': 'La Liga',
        'probability': 0.72,
        'volume': 175000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Soccer', 'La Liga', 'Real Madrid', 'Villarreal', 'Spain', 'Vinicius Jr'],
        'image': 'static/images/sports_laliga_madrid_villarreal.jpg'
    },
    {
        'id': 'laliga-barcelona-athletic-feb15',
        'title': 'Will Barcelona beat Athletic Bilbao on Feb 15?',
        'description': 'Barcelona vs Athletic Bilbao at Camp Nou. Barcelona league leaders. Athletic strong defense. Title race critical match.',
        'category': 'Soccer',
        'subcategory': 'La Liga',
        'probability': 0.65,
        'volume': 162000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Soccer', 'La Liga', 'Barcelona', 'Athletic Bilbao', 'Spain'],
        'image': 'static/images/sports_laliga_barca_athletic.jpg'
    },
    
    # Bundesliga (Germany)
    {
        'id': 'bundesliga-bayern-dortmund-feb15',
        'title': 'Will Bayern Munich defeat Borussia Dortmund on Feb 15?',
        'description': 'Der Klassiker: Bayern vs Dortmund at Allianz Arena. Germany\'s biggest rivalry. Bayern unbeaten. Dortmund in form. Title implications.',
        'category': 'Soccer',
        'subcategory': 'Bundesliga',
        'probability': 0.58,
        'volume': 185000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Soccer', 'Bundesliga', 'Bayern Munich', 'Borussia Dortmund', 'Germany', 'Der Klassiker'],
        'image': 'static/images/sports_bundesliga_bayern_dortmund.jpg'
    },
    
    # Serie A (Italy)
    {
        'id': 'seriea-inter-milan-feb15',
        'title': 'Will Inter Milan beat AC Milan in Derby della Madonnina?',
        'description': 'Inter vs AC Milan at San Siro. Milan derby. Inter top of table. Milan inconsistent. City bragging rights at stake.',
        'category': 'Soccer',
        'subcategory': 'Serie A',
        'probability': 0.55,
        'volume': 168000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Soccer', 'Serie A', 'Inter Milan', 'AC Milan', 'Italy', 'Derby'],
        'image': 'static/images/sports_seriea_inter_milan.jpg'
    },
    
    # Other Major Sports
    {
        'id': 'rugby-england-ireland-feb15',
        'title': 'Will England defeat Ireland in Six Nations on Feb 15?',
        'description': 'England vs Ireland at Twickenham. Six Nations Championship. Ireland defending champions. England home advantage. Physical battle.',
        'category': 'Rugby',
        'subcategory': 'Six Nations',
        'probability': 0.42,
        'volume': 82000,
        'resolution_date': get_resolution_date(4),
        'tags': ['Rugby', 'Six Nations', 'England', 'Ireland', 'Rugby Union'],
        'image': 'static/images/sports_rugby_england_ireland.jpg'
    },
    {
        'id': 'afl-preseason-feb14',
        'title': 'Will Richmond Tigers win AFL preseason match vs Collingwood?',
        'description': 'Richmond Tigers vs Collingwood Magpies AFL preseason. Australian Rules Football. Tigers testing new players. Collingwood favorites.',
        'category': 'Australian Football',
        'subcategory': 'AFL',
        'probability': 0.38,
        'volume': 25000,
        'resolution_date': get_resolution_date(3),
        'tags': ['AFL', 'Australian Football', 'Richmond Tigers', 'Collingwood', 'Australia'],
        'image': 'static/images/sports_afl_richmond_collingwood.jpg'
    }
]

def add_sports_markets():
    """Add sports markets to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    skipped = 0
    
    for market in SPORTS_MARKETS:
        # Check if exists
        cursor.execute("SELECT market_id FROM markets WHERE market_id = ?", (market['id'],))
        if cursor.fetchone():
            skipped += 1
            continue
        
        # Add market
        cursor.execute("""
            INSERT INTO markets (
                market_id, title, description, category, probability,
                volume_total, resolution_date, image_url, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            market['id'],
            market['title'],
            market['description'],
            market['category'],
            market['probability'],
            market['volume'],
            market['resolution_date'],
            market['image'],
            datetime.now().isoformat()
        ))
        
        # Add tags
        for tag in market['tags']:
            cursor.execute("""
                INSERT OR IGNORE INTO market_tags (market_id, tag)
                VALUES (?, ?)
            """, (market['id'], tag))
        
        # Add probability history (3 recent points)
        for i in range(3):
            days_ago = 2 - i
            prob_delta = random.uniform(-0.03, 0.03)
            hist_prob = max(0.1, min(0.9, market['probability'] + prob_delta))
            
            cursor.execute("""
                INSERT INTO probability_history (market_id, probability, timestamp)
                VALUES (?, ?, ?)
            """, (
                market['id'],
                hist_prob,
                (datetime.now() - timedelta(days=days_ago)).isoformat()
            ))
        
        added += 1
        print(f"✅ {market['title'][:60]}... ({market['category']})")
    
    conn.commit()
    conn.close()
    
    print()
    print(f"📊 Summary:")
    print(f"   Added: {added} sports markets")
    print(f"   Skipped: {skipped} (already exist)")
    print(f"   Total: {len(SPORTS_MARKETS)} sports markets")
    print()
    print("🏀 NBA: 5 markets")
    print("⚽ Premier League: 4 markets")
    print("⚽ Champions League: 3 markets")
    print("🏒 NHL: 3 markets")
    print("⚾ NPB (Japan): 2 markets")
    print("⚽ La Liga: 2 markets")
    print("⚽ Bundesliga: 1 market")
    print("⚽ Serie A: 1 market")
    print("🏉 Rugby: 1 market")
    print("🏈 AFL: 1 market")

if __name__ == '__main__':
    print("🏆 Creating upcoming sports markets (Feb 12-15, 2026)...")
    print()
    add_sports_markets()
    print()
    print("✅ Sports markets ready!")

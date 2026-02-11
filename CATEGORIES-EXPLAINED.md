# 📊 Categories & Tags Explained

## Why "Markets" Was Bad

**Before**: "Markets" was a catch-all for anything that didn't fit specific keywords. This meant:
- Elon budget cuts → "Markets" (should be Economics/Politics)
- GTA 6 pricing → "Markets" (should be Entertainment)
- Harvey Weinstein trial → "Markets" (should be Crime)
- Music albums → "Markets" (should be Entertainment)

**Problem**: "Markets" told you nothing about the content!

## New Category System

### 🎯 Specific Categories (checked first)

1. **Crime** (9 markets)
   - Legal cases, trials, convictions
   - Keywords: guilty, convicted, sentenced, trial, prison
   - Examples: 
     - "Rojas guilty in Texas illegal abortion case?"
     - "Will Harvey Weinstein be sentenced to prison?"

2. **Entertainment** (8 markets)
   - Gaming, music, movies
   - Keywords: GTA, gaming, album, music, movie, Netflix
   - Examples:
     - "Will GTA 6 cost $100+?"
     - "New Rihanna Album before GTA VI?"

3. **Culture** (1 market)
   - Religion, society
   - Keywords: Jesus, religion, church, god
   - Examples:
     - "Will Jesus Christ return before GTA VI?"

4. **Crypto** (10 markets)
   - Cryptocurrency, blockchain, DeFi
   - Keywords: bitcoin, crypto, ethereum, DeFi, NFT
   - Examples:
     - "Will Bitcoin hit $100k?"
     - "Ethereum surpass Bitcoin?"

5. **Technology** (3 markets)
   - AI, tech companies, product launches
   - Keywords: AI, OpenAI, Apple, Google, Microsoft, hardware
   - Examples:
     - "Will OpenAI launch new consumer hardware?"
     - "Apple Vision Pro sales?"

### 🏟️ Major Categories

6. **Sports** (44 markets)
   - All sports: FIFA, NFL, NBA, NHL, MLB, Olympics
   - Keywords: qualify, championship, world cup, football, basketball
   - Examples:
     - "Will Italy qualify for 2026 FIFA World Cup?"
     - "NBA Finals winner?"

7. **World** (geopolitics removed, merged into Politics)
   - International conflicts, geopolitics
   - Keywords: Iran, Ukraine, Russia, China, Taiwan, war, ceasefire
   - Examples:
     - "Russia-Ukraine Ceasefire before GTA VI?"
     - "Will China invade Taiwan?"

8. **Politics** (10 markets)
   - Government, elections, policy
   - Keywords: Trump, Biden, election, president, congress, deport
   - Examples:
     - "Will Trump deport 250,000-500,000 people?"
     - "Presidential election outcome?"

9. **Economics** (15 markets)
   - Revenue, tariffs, GDP, economic indicators
   - Keywords: revenue, tariff, tax, GDP, inflation, budget
   - Examples:
     - "Will Elon cut the budget by at least 10%?"
     - "US collect $1-2T in revenue in 2025?"

### 🔮 Default

10. **Predictions** (catch-all)
    - Only used when nothing else matches
    - For truly misc/unusual markets

## 🏷️ Tag System

Each market gets **multiple tags** for fine-grained filtering:

### Primary Tags
- Category tag (e.g., `sports`, `politics`, `crime`)

### People Tags
- `trump` (11 markets)
- `elon` (8 markets)
- `weinstein` (6 markets)
- `biden`, `rihanna`, etc.

### Topic Tags  
- `deportation` (10 markets)
- `ai` (18 markets)
- `gaming` (9 markets)
- `legal` (9 markets)
- `budget` (8 markets)
- `revenue` (7 markets)
- `ceasefire`, `invasion`, `tariffs`, etc.

### Why Multiple Tags?

**Example Market**: "Will Trump deport 250,000-500,000 people?"

**Category**: Politics  
**Tags**: `politics`, `trump`, `deportation`

**Benefits**:
- Search by person: "Show me all Trump markets"
- Search by topic: "Show me all deportation markets"
- Search by category: "Show me all Politics markets"

## 📊 Current Distribution

After recategorization:

```
Sports: 44 (FIFA qualifications, championships)
Economics: 15 (revenue, budget, tariffs)
Crypto: 10 (Bitcoin, Ethereum, DeFi)
Politics: 10 (Trump, deportation, elections)
Crime: 9 (trials, convictions)
Entertainment: 8 (GTA 6, music, movies)
Technology: 3 (AI, hardware, products)
Culture: 1 (religion)
```

## 🔍 How to Use

### In Database Viewer

1. **Browse by Category**:
   - Go to `markets` table
   - Search: "Politics" in category column

2. **Browse by Tag**:
   - Go to `market_tags` table
   - Search: "trump" or "deportation" or "ai"
   - See market questions in `market_question` column

3. **Find Person-Specific Markets**:
   - Search: "elon" → see all Elon Musk markets
   - Search: "trump" → see all Trump markets

### In API

```bash
# Get all Politics markets
curl "http://localhost:5555/api/v1/markets?category=Politics"

# Get all Trump-related markets  
curl "http://localhost:5555/api/v1/markets?tag=trump"

# Get all AI markets
curl "http://localhost:5555/api/v1/markets?tag=ai"
```

## 🎯 Personalization Use Cases

### Scenario 1: You Love Geopolitics

Your interaction history shows:
- 40% World category
- 30% Politics category
- Tags: ukraine, china, taiwan, iran

**Personalized Feed**:
- Boosts World & Politics markets
- Boosts markets with geopolitical tags
- Shows you conflict/ceasefire markets first

### Scenario 2: You're a Sports Fan

Your interaction history shows:
- 60% Sports category
- Tags: fifa, nba, world cup, qualify

**Personalized Feed**:
- Boosts Sports markets
- Shows FIFA/NBA markets prominently
- Hides politics/economics

### Scenario 3: You Follow Specific People

Your interaction history shows:
- Tags: trump (15 clicks), elon (12 clicks)

**Personalized Feed**:
- Boosts any market mentioning Trump or Elon
- Cross-category (Politics + Economics + Technology)
- "Trump tariffs" or "Elon budget cuts" rise to top

## 🔄 Re-Categorization

The categorization logic is in `recategorize_markets.py`.

**Order of checks** (important!):
1. Crime (specific) - guilty, convicted, trial
2. Entertainment (specific) - GTA, music, movies
3. Culture (specific) - religion, Jesus
4. Crypto (specific) - Bitcoin, Ethereum
5. Technology (specific) - AI, OpenAI, hardware
6. Sports (major) - FIFA, NFL, NBA
7. World (broad) - conflicts, wars
8. Politics (broad) - government, elections
9. Economics (broad) - revenue, taxes
10. Predictions (default) - everything else

**Why this order?**  
Specific categories are checked first to prevent broad keywords from catching everything. For example, "budget" appears in Economics keywords, but if a market is about "Elon budget cuts", we want Politics to catch it first via "elon" keyword.

## ✅ Summary

**Old System**:
- ❌ "Markets" = meaningless catch-all
- ❌ No detailed tags
- ❌ Can't filter effectively

**New System**:
- ✅ 9 specific categories
- ✅ Multiple tags per market
- ✅ Person tags (trump, elon, etc.)
- ✅ Topic tags (deportation, ai, etc.)
- ✅ Perfect for personalization

**Result**: You can now find exactly what you're interested in, and the system can learn your preferences across categories AND tags!

---

*Updated: 2026-02-10*

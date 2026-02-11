# Currents - Belief-Driven Prediction Market Discovery

A full-stack prediction market platform with intelligent ranking powered by the **BRain** algorithm.

**✨ NEW: Rain Protocol Integration** - Now supports both Rain API and local database! See [INTEGRATION.md](INTEGRATION.md) for details.

## 🌊 What is Currents?

Currents surfaces the most interesting prediction markets using "belief intensity" - a combination of trading volume and contestedness. It shows you where collective belief is in motion, not just static probabilities.

## 📡 Data Sources

Currents supports two data sources (toggle in `config.py`):

1. **Rain Protocol API** (Default) - Live data from Rain markets
2. **Local SQLite Database** - 50 curated markets for development

Current setup: **Rain API Mock** with 7 markets (5 binary, 2 multi-option)

## 🧠 BRain Intelligence Layer

The **BRain** ranking algorithm calculates:

```
belief_intensity = (volume_score * 0.6) + (contestedness * 0.4)

where:
  volume_score = volume_24h / 10000
  contestedness = 1 - |0.5 - probability| * 2
```

This surfaces markets that are both **highly traded** and **highly contested** - the most interesting belief currents.

## 📊 Current Status

- **50 Total Markets**: 45 binary + 5 multi-option
- **Categories**: Politics (11), Technology (10), Sports (10), Crypto (7), Economics (7), World (2), Entertainment (2), Markets (1)
- **Features**: Hero section, grid view, stream feed, expandable options, bottom widgets

## 🚀 Quick Start

### Run Locally

```bash
# Navigate to project
cd currents-full-local/

# Start Flask server
python3 -m flask run --host=0.0.0.0 --port=5555

# Visit in browser
http://localhost:5555
```

### Test API

```bash
# Run API test suite
python3 test_api.py

# Or test endpoints manually
curl http://localhost:5555/api/v1/health
curl http://localhost:5555/api/v1/feed
curl "http://localhost:5555/api/v1/markets?category=Crypto&limit=5"
```

## 📁 Project Structure

```
currents-full-local/
├── app.py              # Main Flask application
├── api.py              # BRain API endpoints (v1)
├── brain.db            # SQLite database (markets, options, history)
├── templates/
│   ├── base.html       # Base template with header/footer
│   └── index-v2.html   # Homepage with hero/grid/stream
├── API.md              # Complete API documentation
├── test_api.py         # API test suite
├── VERSION.md          # Version history
└── README.md           # This file
```

## 🔌 API Endpoints

Base URL: `http://localhost:5555/api/v1`

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/markets` | GET | List all markets (filterable) |
| `/markets/{id}` | GET | Get market details |
| `/feed` | GET | Get ranked feed (hero/grid/stream) |
| `/categories` | GET | List categories with counts |
| `/trending` | GET | Top volume markets |

### Example Requests

```bash
# Get crypto markets
curl "http://localhost:5555/api/v1/markets?category=Crypto&limit=5"

# Get specific market
curl "http://localhost:5555/api/v1/markets/m_eth_flip"

# Get ranked feed
curl "http://localhost:5555/api/v1/feed"

# Get trending markets
curl "http://localhost:5555/api/v1/trending"
```

See [API.md](API.md) for complete documentation.

## 🎨 UI Features

### Hero Section
- Large featured market with full details
- Belief Currents timeline (color-coded gradient)
- Top 3 options (multi-option markets)
- Expandable "+2 more options"

### Grid (8 markets)
- Category badges (color-coded)
- Probability badges (shows leading option for multi-option)
- Compact Belief Currents chart
- Uniform card heights

### The Stream
- 3-column grid of additional markets
- Compact card layout
- Quick stats (voices, votes)

### Bottom Widgets
- **On The Rise** 📈: High-probability markets gaining momentum
- **Most Contested** ⚔️: Markets near 50/50
- **Explore Currents** 🧭: Browse by category

## 📈 Market Types

### Binary Markets
Yes/No questions with single probability:
- "Will Bitcoin hit $100k by March 2026?"
- Shows: Yes %, No %, Trend

### Multi-Option Markets
Multiple mutually-exclusive outcomes:
- "Who will win Super Bowl LXI?"
- Shows: Top 3-5 options with probabilities
- Expandable to show more options

## 🔧 Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite (with full schema)
- **Frontend**: HTML, Tailwind CSS, Jinja2
- **API**: RESTful JSON with CORS
- **Fonts**: Inter (Google Fonts)

## 🎯 Next Steps

### Immediate
1. ✅ Add real markets from Polymarket/Kalshi
2. ✅ Build BRain API structure
3. 🔄 Deploy to accessible URL

### Near-term
- Personalized feeds based on user interactions
- Search functionality
- User profiles and portfolios
- Historical probability charts
- Mobile optimization

### Long-term
- Real-time websocket updates
- Rain protocol integration
- Social features (comments, shares)
- Advanced analytics dashboard

## 📊 Database Schema

### markets
- Binary and multi-option market metadata
- Probabilities, volumes, participants
- Categories, images, descriptions

### market_options
- Options for multi-outcome markets
- Individual probabilities per option

### probability_history
- Time-series probability data
- Volume snapshots

### market_tags
- Flexible tagging system

## 🌐 Deployment

Currently running locally. For production:

1. Use production WSGI server (gunicorn/uwsgi)
2. Configure reverse proxy (nginx)
3. Set up SSL/TLS
4. Configure CORS for specific origins
5. Add rate limiting
6. Set up monitoring

## 📝 Version History

- **v21** (2026-02-09): Expandable options + The Stream section
- **v20** (2026-02-09): Dynamic belief current colors + Figma matching
- **v19** (2026-02-09): Multi-color options + category badges
- **v18** (2026-02-09): Layout fixes (hero + grid heights)
- **v17** (2026-02-09): Multi-option markets + dynamic sentiments
- **v16** (2026-02-09): Rain logo + dynamic timelines
- **v15** (2026-02-09): Version numbering + BELIEF CURRENTS

See [VERSION.md](VERSION.md) for detailed changelog.

## 📖 Documentation

- [API.md](API.md) - Complete API reference
- [VERSION.md](VERSION.md) - Detailed version history
- [test_api.py](test_api.py) - API usage examples

## 🤝 Contributing

This is a demo project. For production deployment:
1. Connect to real prediction market data sources
2. Implement user authentication
3. Add caching layer (Redis)
4. Set up proper monitoring
5. Add comprehensive test suite

## 📄 License

Demonstration project for the Rain protocol ecosystem.

---

**Built with 🌊 by Currents + BRain**  
*Powered by Rain Protocol*

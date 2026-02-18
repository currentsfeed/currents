# Currents

**Belief-driven prediction market discovery platform**

Currents is a personalized feed for prediction markets, using behavioral learning to surface the most relevant markets to each user.

---

## 🚀 Features

- **BRain v1 Personalization**: Tag-level behavioral learning
- **Mobile-First UX**: TikTok-style vertical feed on mobile, grid layout on desktop
- **353 Markets**: Sports, Technology, Politics, Economics, World events, Crypto, Entertainment, Culture
- **Real-Time Trending**: Geographic-based trending with local/global blend
- **Wallet Integration**: Arbitrum network support via WalletConnect
- **Waitlist System**: Email collection with belief-based questions

---

## 📦 Tech Stack

- **Backend**: Python 3.11 + Flask
- **Database**: SQLite (with BRain v1 personalization engine)
- **Frontend**: HTML/CSS/JS (Tailwind CSS)
- **Deployment**: nginx + systemd + Let's Encrypt SSL
- **Network**: Arbitrum One (Chain ID 42161)

---

## 🏗️ Architecture

### Core Components:

- **app.py**: Flask application with routing and API endpoints
- **feed_composer.py**: BRain v1 feed composition (quota-based personalization)
- **impression_tracker.py**: User interaction tracking
- **compute_trending.py**: Trending market calculation
- **brain_v1_config.json**: Configurable personalization parameters

### Key Features:

1. **Personalization Engine (BRain v1)**:
   - 40% personal interests
   - 25% global trending
   - 12% local trending
   - 8% fresh markets
   - 15% exploration

2. **Category Diversity**:
   - 9 main categories
   - Maximum 15% per category in candidate pools
   - Round-robin distribution in feeds

3. **Geo-Targeting**:
   - IP-based country detection
   - Region-specific markets (Japan, Israel)
   - User overrides for testing

4. **Special Access Markets**:
   - URL parameter-based visibility
   - Hero position override system

---

## 🚀 Quick Deployment

### Prerequisites:
- Ubuntu 22.04 server
- Domain name
- 2GB RAM minimum

### One-Command Deploy:
```bash
./deploy-production.sh YOUR_DOMAIN.com
```

### What It Does:
- Installs Python 3.11, nginx, certbot
- Sets up virtual environment
- Configures nginx reverse proxy
- Obtains SSL certificate (Let's Encrypt)
- Creates systemd service (auto-restart)
- Starts application

**Total time**: 15 minutes

---

## 📚 Documentation

- **START_HERE.md**: Deployment overview
- **DIGITALOCEAN_SETUP.md**: Complete step-by-step guide
- **PRODUCTION_DEPLOYMENT_GUIDE.md**: Platform options and architecture
- **CREDENTIALS_CHECKLIST.md**: Account and access tracking
- **DEPLOYMENT_v205.md**: Latest deployment notes

---

## 🗄️ Database Schema

### Key Tables:

- **markets**: Market data (353 total)
- **market_tags**: Tag associations for personalization
- **user_interactions**: Clicks, trades, hides
- **user_market_impressions**: Feed impression tracking
- **user_taste**: Aggregated user preferences
- **trending_cache**: Pre-computed trending scores
- **waitlist_submissions**: Coming soon page signups

---

## 🌍 Market Distribution

- **Sports**: 134 markets
- **Technology**: 48 markets
- **Politics**: 42 markets
- **Economics**: 34 markets
- **World**: 32 markets
- **Crypto**: 23 markets
- **Entertainment**: 16 markets
- **Culture**: 14 markets
- **Crime**: 9 markets
- **Business**: 1 market

---

## ⚙️ Configuration

### Environment Variables:
```bash
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5555
HOST=0.0.0.0
DATABASE_PATH=brain.db
```

### BRain v1 Config:
Edit `brain_v1_config.json` to tune:
- Quota weights (personal/trending/fresh/exploration)
- Category caps and diversity rules
- Cooldown and frequency penalties
- Trending decay rates

---

## 🔧 Management Commands

```bash
# View logs
sudo journalctl -u currents.service -f

# Restart application
sudo systemctl restart currents.service

# Check status
sudo systemctl status currents.service

# Restart nginx
sudo systemctl restart nginx

# Database location
/var/www/currents/brain.db
```

---

## 🌐 Production URLs

### Main Site:
- `https://YOUR_DOMAIN.com`
- `https://www.YOUR_DOMAIN.com`

### API Endpoints:
- `GET /` - Main feed (mobile: TikTok, desktop: grid)
- `GET /markets` - All markets page with category filter
- `GET /market/<id>` - Market detail page
- `POST /api/markets/feed` - Paginated markets API
- `POST /api/brain/feed` - BRain v1 personalized feed
- `GET /coming-soon` - Waitlist page

---

## 📊 Monitoring

### Health Checks:
- Systemd auto-restart on crash
- Log rotation via journald
- Nginx access/error logs

### Recommended:
- Uptime monitoring (UptimeRobot, StatusCake)
- Error tracking (Sentry)
- Analytics (Plausible, Simple Analytics)

---

## 🔒 Security

- SSL/TLS via Let's Encrypt (auto-renewal)
- Firewall: UFW or cloud platform firewall
- Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)
- SSH key authentication recommended
- Rate limiting on API endpoints

---

## 💰 Operating Costs

**Monthly**:
- Server (2GB): $12/month
- Backups: $2/month
- Domain: ~$1.25/month
- **Total**: ~$15/month

**One-time**:
- Domain registration: $10-15/year
- SSL certificate: $0 (Let's Encrypt)

---

## 🚀 Latest Updates (v205)

**February 18, 2026**:
- ✅ Removed 23 past-event sports markets
- ✅ Added 20 new upcoming sports markets (Feb 19-24)
- ✅ Added special access market system
- ✅ Geo-targeting for regional content
- ✅ Category diversity enforcement
- ✅ Comprehensive backup system

---

## 📝 License

Proprietary - Rain Protocol Ltd.

---

## 🤝 Support

For deployment issues, see documentation:
- DIGITALOCEAN_SETUP.md (step-by-step)
- PRODUCTION_DEPLOYMENT_GUIDE.md (overview)
- CREDENTIALS_CHECKLIST.md (setup tracking)

---

**Built with belief. Measured in certainty.**

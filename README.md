# Currents - Full Local Stack

Complete working Currents demo running entirely on your computer.

## 🎯 What This Is

A fully integrated local setup:
- ✅ SQLite database (BRain)
- ✅ Flask backend (API + web server)
- ✅ HTML/CSS frontend (Tailwind)
- ✅ All connected and working

## 🚀 Quick Start

### One Command:
```bash
./start.sh
```

Then open: **http://localhost:5000**

That's it! Everything runs automatically.

---

## 📋 Manual Setup (if needed)

### Step 1: Install Flask
```bash
pip3 install flask
```

### Step 2: Create Database
```bash
sqlite3 brain.db < schema.sql
python3 seed_data.py
```

### Step 3: Run Server
```bash
python3 app.py
```

### Step 4: Open Browser
Go to: http://localhost:5000

---

## 🗂️ Project Structure

```
currents-full-local/
├── app.py              # Flask app (backend + frontend)
├── brain.db            # SQLite database (created by setup)
├── schema.sql          # Database structure
├── seed_data.py        # Populate sample data
├── start.sh            # One-command startup
├── requirements.txt    # Python dependencies
├── templates/          # HTML pages
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   └── detail.html     # Market detail
└── README.md           # This file
```

---

## 🧠 How It Works

### 1. Database Layer (BRain)
SQLite database with:
- 8 pre-loaded markets
- Probability history
- Tags and taxonomy
- User tracking tables

### 2. Backend (Flask)
Python app that:
- Queries database
- Runs ranking algorithm
- Serves web pages
- Provides JSON API

### 3. Frontend (Templates)
HTML pages that:
- Display ranked markets
- Show detail pages
- Use Tailwind CSS for styling

---

## 📊 Features

### Homepage
- **Hero section:** Top market by belief intensity
- **Grid section:** Next 8 markets
- **Stream section:** Additional markets

### Market Detail Page
- Full market information
- Probability history chart
- Related markets (tag-based)
- Current belief (Yes/No outcomes)

### API Endpoints
- `GET /` - Homepage
- `GET /market/<id>` - Market detail
- `GET /api/homepage` - JSON feed
- `GET /api/markets/<id>` - JSON market detail

---

## 🛠️ Customization

### Add More Markets

Edit `seed_data.py` and add to the `MARKETS` list:

```python
{
    "market_id": "m_009",
    "title": "Your question here?",
    "category": "Politics",
    "tags": ["tag1", "tag2"],
    "probability": 0.65,
    "volume_24h": 50000,
    # ... more fields
}
```

Then run:
```bash
python3 seed_data.py
```

### Change Ranking Algorithm

Edit `app.py`, function `calculate_belief_intensity()`:

```python
def calculate_belief_intensity(self, market):
    volume_score = market['volume_24h'] / 10000
    prob = market['probability']
    contestedness = 1 - abs(0.5 - prob) * 2
    
    # Adjust these weights:
    return volume_score * 0.7 + contestedness * 0.3
```

### Modify Templates

Edit files in `templates/`:
- `index.html` - Homepage layout
- `detail.html` - Market detail page
- `base.html` - Shared header/footer

---

## 🔧 Troubleshooting

### "Database not found"
Run: `./start.sh` (it creates the DB automatically)

### "Flask not installed"
Run: `pip3 install flask`

### "Port 5000 already in use"
Change port in `app.py`:
```python
app.run(host='127.0.0.1', port=8080, debug=True)
```

### Can't access from other devices
Change host in `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 🎯 What to Do Next

### Today:
1. Run `./start.sh`
2. Open http://localhost:5000
3. Click around, explore markets
4. Check detail pages

### This Week:
1. Add 10+ more markets
2. Customize the design
3. Tweak ranking algorithm
4. Test on mobile (responsive)

### Next Week:
1. Connect to real Rain API
2. Deploy to public hosting
3. Add user authentication
4. Build personalization

---

## 📝 Tips

- **Database:** Use `sqlite3 brain.db` to explore data
- **Logs:** Check terminal for errors/requests
- **Reload:** Changes to Python files auto-reload
- **Reset:** Delete `brain.db` and run `./start.sh` again

---

**You have a complete working system!** 🚀

Everything runs locally, no internet needed (except for Tailwind CSS from CDN).

Questions? Check the code - it's all documented and readable.

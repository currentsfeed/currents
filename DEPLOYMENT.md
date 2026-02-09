# Currents Deployment Guide

## Quick Deploy to Render.com (Recommended - 5 minutes)

### Option 1: Via GitHub (Easiest)

1. **Create a GitHub repository:**
   - Go to https://github.com/new
   - Name it: `currents-demo`
   - Make it Public
   - Don't add README, .gitignore, or license
   - Click "Create repository"

2. **Push code to GitHub:**
   ```bash
   cd /home/ubuntu/.openclaw/workspace/currents-full-local
   git remote add origin https://github.com/YOUR_USERNAME/currents-demo.git
   git push -u origin master
   ```

3. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/Login (use GitHub)
   - Click "New +" → "Web Service"
   - Connect your `currents-demo` repository
   - Configure:
     - **Name:** currents-demo
     - **Runtime:** Python 3
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - Click "Create Web Service"

4. **Wait 2-3 minutes** for deployment

5. **Your app will be live at:** `https://currents-demo.onrender.com`

---

## Option 2: Via Fly.io (Alternative)

1. **Install flyctl:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   export PATH="$HOME/.fly/bin:$PATH"
   ```

2. **Login:**
   ```bash
   flyctl auth login
   ```

3. **Deploy:**
   ```bash
   cd /home/ubuntu/.openclaw/workspace/currents-full-local
   flyctl launch --name currents-demo --region iad --yes
   flyctl deploy
   ```

4. **Your app will be live at:** `https://currents-demo.fly.dev`

---

## Option 3: Via Railway (Alternative)

1. Go to https://railway.app
2. Sign up/Login
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Railway auto-detects Python and deploys
6. Get your URL from the deployment

---

## Testing Locally First

Before deploying, test locally:

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
./start.sh
```

Open: http://localhost:5000

---

## Files Included

- ✅ `app.py` - Flask application (production-ready)
- ✅ `requirements.txt` - Python dependencies (Flask + gunicorn)
- ✅ `build.sh` - Build script for deployment
- ✅ `Dockerfile` - Docker configuration
- ✅ `fly.toml` - Fly.io configuration
- ✅ `render.yaml` - Render.com configuration
- ✅ `brain.db` - Pre-seeded database
- ✅ `templates/` - HTML templates

Everything is ready to deploy!

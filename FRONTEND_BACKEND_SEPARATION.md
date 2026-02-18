# Frontend/Backend Separation Guide

**Separate architecture: Database on your server, Frontend elsewhere**

---

## Architecture Overview

### Current (All-in-One):
```
┌─────────────────────────────┐
│   Single Server             │
│  ┌─────────────────────┐   │
│  │   Flask Backend     │   │
│  │   (app.py)          │   │
│  └──────────┬──────────┘   │
│             │               │
│  ┌──────────▼──────────┐   │
│  │   SQLite Database   │   │
│  │   (brain.db)        │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

### New (Separated):
```
┌────────────────────┐         ┌──────────────────────┐
│  Frontend Server   │         │   Database Server    │
│                    │         │                      │
│  ┌──────────────┐ │         │  ┌────────────────┐ │
│  │ Flask Backend│ │ ◄─────► │  │   PostgreSQL   │ │
│  │  (app.py)    │ │  API    │  │   or MySQL     │ │
│  └──────────────┘ │         │  └────────────────┘ │
│                    │         │                      │
│  ┌──────────────┐ │         │   353 markets        │
│  │  Templates   │ │         │   All user data      │
│  │  Static      │ │         │   Interactions       │
│  └──────────────┘ │         │                      │
└────────────────────┘         └──────────────────────┘
```

---

## Step 1: Choose Database System

### Option A: PostgreSQL (Recommended for Production) ⭐

**Why PostgreSQL?**
- Most robust for production
- Better concurrency handling
- JSON support for complex queries
- Best for personalization algorithms

**Install on Database Server:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Option B: MySQL/MariaDB

**Install on Database Server:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y mysql-server

# Secure installation
sudo mysql_secure_installation
```

---

## Step 2: Create Database & User

### For PostgreSQL:

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL console:
CREATE DATABASE currents;
CREATE USER currents_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE currents TO currents_user;
\q
```

**Allow Remote Connections:**
```bash
# Edit postgresql.conf
sudo nano /etc/postgresql/*/main/postgresql.conf
# Change: listen_addresses = '*'

# Edit pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Add: host  currents  currents_user  0.0.0.0/0  md5

# Restart
sudo systemctl restart postgresql
```

### For MySQL:

```bash
# Login to MySQL
sudo mysql

# In MySQL console:
CREATE DATABASE currents CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'currents_user'@'%' IDENTIFIED BY 'YOUR_SECURE_PASSWORD';
GRANT ALL PRIVILEGES ON currents.* TO 'currents_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

**Allow Remote Connections:**
```bash
# Edit mysqld.cnf
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Change: bind-address = 0.0.0.0

# Restart
sudo systemctl restart mysql
```

---

## Step 3: Convert SQLite Dump to PostgreSQL/MySQL

I've created the SQLite dump. Now you need to convert it:

### For PostgreSQL:

**Install converter:**
```bash
pip install sqlite3-to-postgres
```

**Convert:**
```bash
sqlite3-to-postgres \
    --sqlite-file brain.db \
    --postgres-dsn "postgresql://currents_user:YOUR_PASSWORD@YOUR_DB_SERVER:5432/currents"
```

### For MySQL:

**Manual conversion needed** (SQLite dump won't work directly):

1. Use the schema conversion below
2. Import data using CSV exports

---

## Step 4: Database Schema (PostgreSQL)

Save this as `create_schema_postgres.sql`:

```sql
-- Currents Database Schema for PostgreSQL

CREATE TABLE markets (
    market_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category VARCHAR(100),
    language VARCHAR(10) DEFAULT 'en',
    probability DECIMAL(5,4) NOT NULL,
    volume_24h DECIMAL(15,2) DEFAULT 0,
    volume_total DECIMAL(15,2) DEFAULT 0,
    participant_count INTEGER DEFAULT 0,
    image_url TEXT,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_date TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    outcome TEXT,
    market_type VARCHAR(50) DEFAULT 'binary',
    editorial_description TEXT,
    article_text TEXT,
    article_source TEXT,
    article_fetched_at TIMESTAMP
);

CREATE INDEX idx_markets_status ON markets(status);
CREATE INDEX idx_markets_category ON markets(category);
CREATE INDEX idx_markets_volume ON markets(volume_24h DESC);
CREATE INDEX idx_markets_type ON markets(market_type);

CREATE TABLE market_tags (
    market_id VARCHAR(255),
    tag VARCHAR(100),
    PRIMARY KEY (market_id, tag),
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

CREATE INDEX idx_market_tags_tag ON market_tags(tag);

CREATE TABLE market_taxonomy (
    market_id VARCHAR(255),
    taxonomy_path TEXT,
    PRIMARY KEY (market_id, taxonomy_path),
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

CREATE TABLE probability_history (
    id SERIAL PRIMARY KEY,
    market_id VARCHAR(255) NOT NULL,
    probability DECIMAL(5,4) NOT NULL,
    volume DECIMAL(15,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

CREATE INDEX idx_probability_history_market ON probability_history(market_id);

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    anon_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    market_id VARCHAR(255),
    event_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

CREATE INDEX idx_interactions_user ON interactions(user_id);
CREATE INDEX idx_interactions_market ON interactions(market_id);
CREATE INDEX idx_interactions_timestamp ON interactions(timestamp);

CREATE TABLE user_taste (
    user_id VARCHAR(255),
    dimension_type VARCHAR(50),
    dimension_value TEXT,
    weight DECIMAL(5,4) DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, dimension_type, dimension_value),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE trending_cache (
    market_id VARCHAR(255),
    scope VARCHAR(100),
    score DECIMAL(10,6),
    rank INTEGER,
    window VARCHAR(10) DEFAULT '24h',
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (market_id, scope, window)
);

CREATE INDEX idx_trending_scope ON trending_cache(scope, rank);

CREATE TABLE user_seen (
    user_id VARCHAR(255),
    market_id VARCHAR(255),
    last_seen_at TIMESTAMP,
    last_probability DECIMAL(5,4),
    last_volume DECIMAL(15,2),
    view_count INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, market_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

CREATE TABLE market_options (
    option_id VARCHAR(255) PRIMARY KEY,
    market_id VARCHAR(255) NOT NULL,
    option_text TEXT NOT NULL,
    probability DECIMAL(5,4) NOT NULL DEFAULT 0,
    position INTEGER DEFAULT 0,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

CREATE INDEX idx_options_market ON market_options(market_id);
CREATE INDEX idx_options_market_prob ON market_options(market_id, probability DESC);

-- BRain v1 Tables
CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_key VARCHAR(255) NOT NULL,
    market_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255),
    metadata JSONB
);

CREATE INDEX idx_user_interactions_user ON user_interactions(user_key);
CREATE INDEX idx_user_interactions_market ON user_interactions(market_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp);

CREATE TABLE user_market_impressions (
    id SERIAL PRIMARY KEY,
    user_key VARCHAR(255) NOT NULL,
    market_id VARCHAR(255) NOT NULL,
    feed_position INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_impressions_user ON user_market_impressions(user_key);
CREATE INDEX idx_impressions_market ON user_market_impressions(market_id);

CREATE TABLE user_topic_scores (
    user_key VARCHAR(255),
    topic_type VARCHAR(50),
    topic_value TEXT,
    score DECIMAL(10,6) DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_key, topic_type, topic_value)
);

CREATE TABLE user_session_state (
    user_key VARCHAR(255) PRIMARY KEY,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_vector JSONB
);

CREATE TABLE market_velocity_rollups (
    market_id VARCHAR(255),
    window VARCHAR(10),
    views INTEGER DEFAULT 0,
    trades INTEGER DEFAULT 0,
    odds_change DECIMAL(5,4) DEFAULT 0,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (market_id, window)
);

CREATE TABLE waitlist_submissions (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    month_belief VARCHAR(20) NOT NULL,
    ip_address VARCHAR(50),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    position INTEGER,
    is_test_submission BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_waitlist_email ON waitlist_submissions(email);
CREATE INDEX idx_waitlist_ip ON waitlist_submissions(ip_address);
```

**Load Schema:**
```bash
psql -U currents_user -d currents -h YOUR_DB_SERVER < create_schema_postgres.sql
```

---

## Step 5: Import Data

### Export from SQLite (on dev server):

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Export each table to CSV
sqlite3 brain.db ".headers on" ".mode csv" ".output markets.csv" "SELECT * FROM markets;"
sqlite3 brain.db ".headers on" ".mode csv" ".output market_tags.csv" "SELECT * FROM market_tags;"
sqlite3 brain.db ".headers on" ".mode csv" ".output probability_history.csv" "SELECT * FROM probability_history;"
# ... etc for all tables
```

### Import to PostgreSQL:

```bash
# Copy CSV files to database server, then:
psql -U currents_user -d currents -h YOUR_DB_SERVER

# In psql:
\copy markets FROM 'markets.csv' WITH (FORMAT csv, HEADER true);
\copy market_tags FROM 'market_tags.csv' WITH (FORMAT csv, HEADER true);
\copy probability_history FROM 'probability_history.csv' WITH (FORMAT csv, HEADER true);
# ... etc
```

---

## Step 6: Configure Flask to Use Remote Database

### Install PostgreSQL Driver:

```bash
pip install psycopg2-binary
```

### Update Connection String:

**Create `.env` file on frontend server:**
```bash
DATABASE_URL=postgresql://currents_user:YOUR_PASSWORD@YOUR_DB_SERVER:5432/currents
```

### Update `app.py`:

Replace SQLite connection with:

```python
import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://currents_user:password@localhost:5432/currents')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# Replace all sqlite3.connect('brain.db') with:
conn = get_db_connection()
```

---

## Step 7: Firewall Configuration

### On Database Server:

```bash
# Allow PostgreSQL port from frontend server
sudo ufw allow from FRONTEND_SERVER_IP to any port 5432

# Or for MySQL:
sudo ufw allow from FRONTEND_SERVER_IP to any port 3306
```

---

## Step 8: Test Connection

**On Frontend Server:**

```bash
# Test PostgreSQL connection
psql -U currents_user -h YOUR_DB_SERVER -d currents

# Or test from Python:
python3 -c "import psycopg2; conn = psycopg2.connect('postgresql://currents_user:PASSWORD@DB_SERVER:5432/currents'); print('Connected!')"
```

---

## Files You Need

### From Dev Server:

1. **Database Dump (Full):**
   - `currents_database_dump.sql` (42MB) - Complete SQLite dump
   
2. **Schema Only:**
   - `database_schema.sql` - Just the structure
   
3. **Application Code:**
   - Already on GitHub: https://github.com/currentsfeed/currents

### I Can Provide:

- ✅ SQLite dump (42MB) - **Already created**
- ✅ PostgreSQL schema - **Provided above**
- ✅ MySQL schema - Can create if needed
- ✅ CSV exports of all tables - Can generate
- ✅ Migration script - Can create automated version

---

## Summary: What You Need

### For Database Server:
1. Install PostgreSQL or MySQL
2. Create database and user
3. Load schema (`create_schema_postgres.sql`)
4. Import data (use converter or CSV import)
5. Configure firewall

### For Frontend Server:
1. Clone from GitHub
2. Install `psycopg2-binary`
3. Set `DATABASE_URL` environment variable
4. Update `app.py` connection code
5. Deploy normally

---

## Next Steps

**Tell me:**
1. PostgreSQL or MySQL?
2. Do you want me to create CSV exports?
3. Do you want automated migration script?
4. What's your database server IP? (for connection string example)

**I'll provide:**
- Complete data export in your chosen format
- Updated `app.py` with database connection
- Step-by-step deployment guide

Ready to proceed? 🚀

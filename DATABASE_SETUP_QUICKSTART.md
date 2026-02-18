# Database Setup - Quick Start

**Get your database running in 15 minutes**

---

## What You Have

✅ **currents_database_dump.sql** (42MB) - Complete database with 353 markets  
✅ **database_schema.sql** - Structure only  
✅ **FRONTEND_BACKEND_SEPARATION.md** - Detailed guide  

---

## Option 1: PostgreSQL (Recommended) ⭐

### Step 1: Install PostgreSQL (on your database server)

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Create Database

```bash
sudo -u postgres psql

# In PostgreSQL:
CREATE DATABASE currents;
CREATE USER currents_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE currents TO currents_user;
\q
```

### Step 3: Import Data

**Option A: Convert SQLite dump directly**
```bash
# Install converter
pip install sqlite3-to-postgres

# Convert (on server with brain.db file)
sqlite3-to-postgres \
    --sqlite-file brain.db \
    --postgres-dsn "postgresql://currents_user:PASSWORD@DB_SERVER:5432/currents"
```

**Option B: Use SQL dump (may need adjustments)**
```bash
# Load dump (will need some syntax fixes)
psql -U currents_user -d currents -h DB_SERVER -f currents_database_dump.sql
```

### Step 4: Allow Remote Connections

```bash
# Edit config
sudo nano /etc/postgresql/*/main/postgresql.conf
# Change: listen_addresses = '*'

# Edit access
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Add: host  currents  currents_user  0.0.0.0/0  md5

# Restart
sudo systemctl restart postgresql

# Open firewall
sudo ufw allow 5432/tcp
```

---

## Option 2: Keep SQLite (Simplest)

If you want to keep using SQLite (fine for MVP):

### Step 1: Copy Database File

```bash
# On database server
mkdir -p /var/db/currents
cd /var/db/currents

# Copy brain.db here (from GitHub repo or dev server)
```

### Step 2: Share via NFS or Mount

**If frontend is on different server:**
```bash
# On database server - Install NFS
sudo apt install nfs-kernel-server
echo "/var/db/currents *(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports
sudo exportfs -a

# On frontend server - Mount NFS
sudo apt install nfs-common
sudo mkdir -p /mnt/database
sudo mount DB_SERVER:/var/db/currents /mnt/database
```

### Step 3: Update Flask Config

```python
# In app.py or config.py
DATABASE_PATH = '/mnt/database/brain.db'  # Or wherever you mounted it
```

---

## Option 3: MySQL/MariaDB

### Step 1: Install MySQL

```bash
sudo apt update
sudo apt install -y mysql-server
sudo mysql_secure_installation
```

### Step 2: Create Database

```bash
sudo mysql

# In MySQL:
CREATE DATABASE currents CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'currents_user'@'%' IDENTIFIED BY 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON currents.* TO 'currents_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Allow Remote Access

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Change: bind-address = 0.0.0.0

sudo systemctl restart mysql
sudo ufw allow 3306/tcp
```

### Step 4: Import Data

MySQL requires schema conversion (SQLite syntax differs). See FRONTEND_BACKEND_SEPARATION.md for full schema.

---

## Configure Frontend to Connect

### For PostgreSQL:

**Install driver:**
```bash
pip install psycopg2-binary
```

**Create `.env` file:**
```bash
DATABASE_URL=postgresql://currents_user:PASSWORD@DB_SERVER_IP:5432/currents
```

**Update app.py:** (I can provide modified version)

### For MySQL:

**Install driver:**
```bash
pip install mysql-connector-python
```

**Create `.env` file:**
```bash
DATABASE_URL=mysql://currents_user:PASSWORD@DB_SERVER_IP:3306/currents
```

### For SQLite (NFS mounted):

No changes needed, just update path:
```python
DATABASE_PATH = '/mnt/database/brain.db'
```

---

## Test Connection

### PostgreSQL:
```bash
psql -U currents_user -h DB_SERVER_IP -d currents
```

### MySQL:
```bash
mysql -u currents_user -h DB_SERVER_IP -p currents
```

### SQLite:
```bash
sqlite3 /path/to/brain.db "SELECT COUNT(*) FROM markets;"
# Should return: 353
```

---

## What's In The Database?

**353 Markets:**
- 134 Sports (20 upcoming games Feb 19-24)
- 48 Technology
- 42 Politics
- 34 Economics
- 32 World
- 23 Crypto
- 16 Entertainment
- 14 Culture
- 9 Crime
- 1 Business (Yaniv)

**Key Tables:**
- `markets` - All market data
- `market_tags` - Tags for personalization
- `probability_history` - Historical data
- `user_interactions` - Click/trade/view tracking
- `user_market_impressions` - Feed impressions
- `trending_cache` - Pre-computed trending scores
- `waitlist_submissions` - 54 email signups

---

## Recommendation

**For MVP (easiest):** Keep SQLite with NFS mount  
**For Production (best):** PostgreSQL with remote connection  
**For Scale (later):** Add read replicas, connection pooling  

---

## Need Help?

**Questions:**
1. Which database system? (PostgreSQL/MySQL/SQLite)
2. Is database on same server as frontend?
3. Do you need connection string examples?

**I can provide:**
- Modified `app.py` with your database connection
- Complete PostgreSQL/MySQL schemas
- Import scripts for your chosen system
- Connection troubleshooting

Ready to set it up? Tell me which option you prefer! 🚀

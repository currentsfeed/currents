# BRain v1 Rollback Guide

**Purpose**: Safe rollback to pre-BRain v1 system if issues occur

---

## Quick Rollback (1 command)

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
bash rollback_to_v159.sh
```

This will:
1. Disable BRain v1 in config
2. Restart Flask app
3. Remove BRain v1 cron jobs
4. Switch back to old personalization

**Site continues running** - zero downtime.

---

## What Gets Rolled Back

### ✅ Reverted
- Personalization algorithm (back to old system)
- Homepage feed generation (old `/api/homepage` endpoint)
- Tracking integration (removes BRain v1 calls)
- Cron jobs (removes velocity computation)

### ✅ Preserved
- All markets and market data
- User interaction history (for future use)
- BRain v1 tables (kept for data retention)
- Database viewer
- All other functionality

### ❌ Not Affected
- Wallet connection
- Mobile feed
- Desktop grid layout
- Trading UI
- Image system
- Category system

---

## Rollback Steps (Manual)

### Step 1: Disable BRain v1
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Edit config
python3 << 'EOF'
import json
with open('config.py', 'r') as f:
    content = f.read()

# Add BRAIN_V1_ENABLED flag
if 'BRAIN_V1_ENABLED' not in content:
    lines = content.split('\n')
    # Insert after USE_RAIN_API line
    for i, line in enumerate(lines):
        if 'USE_RAIN_API' in line:
            lines.insert(i + 1, 'BRAIN_V1_ENABLED = False  # Toggle BRain v1 on/off')
            break
    content = '\n'.join(lines)
    with open('config.py', 'w') as f:
        f.write(content)
    print("✅ Added BRAIN_V1_ENABLED flag")
else:
    # Set to False
    content = content.replace('BRAIN_V1_ENABLED = True', 'BRAIN_V1_ENABLED = False')
    with open('config.py', 'w') as f:
        f.write(content)
    print("✅ Set BRAIN_V1_ENABLED = False")
EOF
```

### Step 2: Restart Flask
```bash
sudo systemctl restart currents.service
sleep 3
sudo systemctl status currents.service --no-pager | head -10
```

### Step 3: Remove BRain v1 Cron Jobs
```bash
# Backup current crontab
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt

# Remove BRain v1 jobs
(crontab -l 2>/dev/null | grep -v "compute_velocity.sh" | grep -v "impression_tracker" | grep -v "session_manager") | crontab -

echo "✅ BRain v1 cron jobs removed"
echo "Note: Trending refresh and score decay cron jobs preserved"
```

### Step 4: Verify Rollback
```bash
# Test old homepage endpoint
curl -s http://localhost:5555/api/homepage | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Old homepage working: {len(data)} markets')"

# Check config
grep "BRAIN_V1_ENABLED" config.py
```

---

## Re-enabling BRain v1

If you want to switch back to BRain v1:

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
bash enable_brain_v1.sh
```

This will:
1. Set BRAIN_V1_ENABLED = True
2. Restart Flask
3. Re-add cron jobs
4. Verify APIs working

---

## Testing After Rollback

### 1. Check homepage loads
```bash
curl -s http://localhost:5555/ | grep "<title>Currents</title>"
```

### 2. Check old API works
```bash
curl -s http://localhost:5555/api/homepage | head -20
```

### 3. Check tracking works
```bash
curl -X POST http://localhost:5555/api/track \
  -H "Content-Type: application/json" \
  -d '{"user_key": "test", "market_id": "test-market", "event_type": "click"}'
```

### 4. Check personalization
```bash
# Old personalizer should be active
curl -s http://localhost:5555/api/admin/users | python3 -m json.tool
```

---

## Data Preservation

### BRain v1 Tables Kept (for future use)
- user_market_impressions
- market_velocity_rollups
- user_session_state
- market_probability_history

**Why keep them?**
- Historical data valuable for analysis
- Can re-enable BRain v1 later without data loss
- No performance impact (not queried when disabled)
- Can drop manually if needed:

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
python3 << 'EOF'
import sqlite3
conn = sqlite3.connect('brain.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS user_market_impressions")
cursor.execute("DROP TABLE IF EXISTS market_velocity_rollups")
cursor.execute("DROP TABLE IF EXISTS user_session_state")
cursor.execute("DROP TABLE IF EXISTS market_probability_history")
conn.commit()
conn.close()
print("✅ BRain v1 tables dropped")
EOF
```

---

## Comparison: Old vs BRain v1

### Old System (v159)
- **Algorithm**: Simple personalization.py (category-level)
- **Scoring**: Volume + contestedness + time decay
- **Learning**: Basic topic scores
- **Trending**: 30-min refresh cache
- **Penalties**: Time decay only
- **Diversity**: Category limits (max 3 per category in top 9)

### BRain v1 (v160)
- **Algorithm**: feed_composer.py (5-channel quotas)
- **Scoring**: LT/ST/Trend/Fresh components with penalties
- **Learning**: Tag-level (90%) + category (10%)
- **Trending**: Real-time velocity rollups (5m/1h/24h)
- **Penalties**: Cooldown + frequency + hide suppression
- **Diversity**: Consecutive limits + category share + tag cluster limits

---

## Troubleshooting

### Issue: Flask won't start after rollback
```bash
# Check logs
sudo journalctl -u currents.service -n 50 --no-pager

# Check syntax errors
cd /home/ubuntu/.openclaw/workspace/currents-full-local
python3 -c "import app; print('✅ No syntax errors')"
```

### Issue: Homepage empty after rollback
```bash
# Check if personalizer is working
python3 << 'EOF'
from personalization import personalizer
feed = personalizer.get_personalized_feed('test_user', limit=10)
print(f"Personalizer returned {len(feed)} items")
EOF
```

### Issue: Old tracking not working
```bash
# Verify tracking_engine.py not requiring BRain v1 modules
python3 << 'EOF'
from tracking_engine import tracker
# Should work without errors
print("✅ Tracker loaded")
EOF
```

---

## Rollback Decision Tree

```
Issue with BRain v1?
├─ YES → Run rollback_to_v159.sh
│   ├─ Site works? → Stay on v159, investigate BRain v1 issue
│   └─ Site broken? → Check TROUBLESHOOTING section
└─ NO → Keep BRain v1 enabled
```

---

## Contact

Questions about rollback? See:
- DEPLOYMENT_v160_BRAIN_V1.md (what changed)
- BRAIN_V1_COMPLETE.md (full implementation)
- This file (rollback procedure)

**Rollback tested**: Feb 15, 2026  
**Zero downtime**: Site stays up during rollback  
**Reversible**: Can re-enable BRain v1 anytime

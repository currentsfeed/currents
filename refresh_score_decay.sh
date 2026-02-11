#!/bin/bash
# Apply score decay daily (5% every 7 days)
# Added: Feb 11, 2026 for Milestone 1

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Calculate decay factor: 5% per 7 days = 0.9928 per day
# Formula: (0.95)^(1/7) = 0.992754
DECAY_FACTOR=0.992754

/home/linuxbrew/.linuxbrew/bin/python3 << EOF
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = 'brain.db'
DECAY_FACTOR = $DECAY_FACTOR

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Apply decay to user_topic_scores
    cursor.execute("""
        UPDATE user_topic_scores
        SET score = score * ?
        WHERE score > 0
    """, (DECAY_FACTOR,))
    
    rows_updated = cursor.rowcount
    conn.commit()
    
    logger.info(f"Score decay applied: {rows_updated} scores updated with factor {DECAY_FACTOR}")
    print(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} - Score decay: {rows_updated} scores updated")
    
except Exception as e:
    logger.error(f"Score decay failed: {e}")
    print(f"ERROR: {e}")
finally:
    conn.close()
EOF

echo "$(date -u '+%Y-%m-%d %H:%M UTC') - Score decay completed" >> /tmp/score_decay.log

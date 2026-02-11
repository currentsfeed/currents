#!/bin/bash
# Refresh trending scores every 30 minutes
# Added: Feb 11, 2026 for Milestone 1

cd /home/ubuntu/.openclaw/workspace/currents-full-local
/home/linuxbrew/.linuxbrew/bin/python3 compute_trending.py >> /tmp/trending_refresh.log 2>&1

echo "$(date -u '+%Y-%m-%d %H:%M UTC') - Trending refresh completed" >> /tmp/trending_refresh.log

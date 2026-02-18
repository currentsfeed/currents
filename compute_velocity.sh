#!/bin/bash
# BRain v1 - Velocity Rollup Computation
# Run every 5 minutes via cron

cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Compute velocity rollups
python3 << 'EOF'
from velocity_computer import velocity_computer
import json

print("[Velocity] Computing rollups...")

# Record current probabilities first
prob_result = velocity_computer.record_current_probabilities()
print(f"[Velocity] Recorded {prob_result['recorded']} probabilities")

# Compute all rollups
result = velocity_computer.compute_all_rollups()

print(f"[Velocity] Updated {result['updated_count']} rollups across {result['geo_buckets']} geo buckets")
print(f"[Velocity] Duration: {result['duration_ms']:.0f}ms")
EOF

echo "[$(date)] Velocity computation complete" >> /tmp/velocity_compute.log

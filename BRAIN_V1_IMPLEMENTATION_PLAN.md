# BRain Personalization v1 - Implementation Plan

**Spec Received**: Feb 15, 2026 05:05 UTC  
**From**: Roy Shaham  
**Status**: Ready to implement

## Overview

Implementing complete personalization overhaul per Roy's spec:
- Impression tracking (not just interactions)
- Session vs long-term separation
- Quota-based feed composition
- Cooldown/frequency penalties
- "Changed" re-show logic

## Implementation Order (Per Spec)

### Phase 1: Schema & Impression Tracking (2-3 hours)
1. ✅ Create user_market_impressions table
2. ✅ Create market_velocity_rollups table  
3. ✅ Create user_session_state table
4. ✅ Update /api/brain/feed to log impressions server-side
5. ✅ Test impression logging

### Phase 2: Session State (1-2 hours)
1. ✅ Implement session rotation (60min timeout)
2. ✅ Add decay logic (0.90 multiplier)
3. ✅ Update track events to update session state
4. ✅ Test session vs long-term separation

### Phase 3: Velocity Rollups (1-2 hours)
1. ✅ Create cron job to compute rollups
2. ✅ Start with 1h + 24h windows
3. ✅ Add 5m window later
4. ✅ Test velocity computations

### Phase 4: New Scoring System (3-4 hours)
1. ✅ Implement NEW vs KNOWN user detection
2. ✅ Add LT, ST, Trend, Fresh components
3. ✅ Add cooldown/frequency penalties
4. ✅ Add "changed" bonus logic
5. ✅ Test scoring on sample markets

### Phase 5: Quota-Based Feed (2-3 hours)
1. ✅ Implement quota allocation
2. ✅ Generate candidates per channel
3. ✅ Merge with quota enforcement
4. ✅ Test quota distribution

### Phase 6: Diversity & Polish (1-2 hours)
1. ✅ Add diversity post-processing
2. ✅ Add debug mode
3. ✅ Move config to file
4. ✅ Test full pipeline

**Total Estimate**: 10-16 hours

## Starting Implementation Now

I'll implement in stages and update this document as I progress.

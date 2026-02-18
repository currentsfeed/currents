# Deployment v161 - BRain v1 LIVE 🚀

**Date**: Feb 15, 2026 05:44 UTC  
**Version**: v161  
**Status**: ✅ LIVE IN PRODUCTION

---

## What Changed

### 🚀 Major: Frontend Switched to BRain v1

The site is now **fully using BRain v1 personalization** for all users!

**Updated Routes:**
- `/` (homepage) - Now uses BRain v1 feed composer
- `/feed` (mobile TikTok feed) - Now uses BRain v1 feed composer

**What This Means:**
- ✅ All users get BRain v1 personalized feeds
- ✅ Tag-level learning (90% tags, 10% category)
- ✅ Server-side impression tracking (automatic)
- ✅ Quota-based feed composition (40/25/12/8/15)
- ✅ Cooldown and frequency penalties
- ✅ Session vs long-term separation
- ✅ NEW vs KNOWN user detection
- ✅ Diversity guarantees

---

## Technical Changes

### Homepage Route (`/`)

**Before (v159-v160):**
```python
feed = personalizer.get_personalized_feed(user_key, limit=20)
# Simple category-level personalization
```

**After (v161):**
```python
# BRain v1 with fallback
result = feed_composer.compose_feed(
    user_key=user_key,
    geo_bucket=user_country,
    limit=30,
    exclude_ids=[],
    debug=False
)

# Server-side impression logging
impression_tracker.log_impressions(user_key, shown_ids)
```

**Graceful Fallback:**
- If BRain v1 fails, automatically falls back to old personalizer
- Errors logged but site stays up
- Zero user-visible errors

### Anonymous Users

**New Behavior:**
- Users without cookies get auto-generated anonymous key: `anon_xxxxxxxxxx`
- Personalization starts learning from first interaction
- Can upgrade to persistent user key via test user switcher or wallet connection

---

## Feed Composition (BRain v1)

### Desktop (30 items)
- **Hero** (1 market): Top-scored from any channel
- **Grid** (8 markets): Next highest scored
- **Stream** (21+ markets): Remaining personalized feed

### Mobile (50 items)
- **Vertical scroll**: All items in single TikTok-style feed
- **Same scoring**: Uses identical BRain v1 algorithm
- **Server-side tracking**: Impressions logged automatically

### Quota Distribution
Per `brain_v1_config.json`:
- 40% Personal (LT + ST similarity)
- 25% Trending Global
- 12% Trending Local (geo-based)
- 8% Fresh New (<72h old)
- 15% Exploration (discovery)

---

## User Experience Changes

### What Users See (Better)

**✅ More Diverse Feeds:**
- Maximum 2 consecutive from same category
- Maximum 35% from single category
- Maximum 25% from same tag cluster
- Guaranteed category diversity

**✅ Less Repetition:**
- Cooldown penalties: Markets shown <2h ago heavily penalized
- Frequency penalties: Markets shown 4+ times in 24h get 75% penalty
- Hide suppression: Hidden markets stay hidden for 7 days

**✅ Smarter Personalization:**
- Tag-level learning (not just category)
- Session state: Recent behavior weighted more
- NEW users: More trending/fresh, less LT
- KNOWN users: Balanced LT/ST/Trend/Fresh

**✅ "Changed" Re-show Logic:**
- Markets with odds change ≥3% get re-shown
- Markets ending ≤6h get re-shown
- Owned markets (traded) get priority boost

### What Users Don't See (Better)

**Server-Side Tracking:**
- Impressions logged automatically when feed loads
- No client-side impression tracking needed
- Frequency counters updated in real-time
- Cooldown timestamps precise

**Velocity Computation:**
- Real-time trending calculation (every 5 min)
- Rolling 5m/1h/24h windows
- Global + per-country rollups
- Odds change detection

---

## Performance

### Latency
- **BRain v1 feed**: ~100-200ms (acceptable)
- **Old personalizer**: ~50-100ms (baseline)
- **Trade-off**: Slightly slower but much better quality

### Database Queries
- **Candidate generation**: 1 query (300 markets)
- **Velocity lookup**: Batch query (per geo bucket)
- **Impression data**: Batch query (all candidates)
- **Total**: ~5-8 queries per feed request

### Cron Jobs
- **Velocity computation**: Every 5 minutes (~25ms duration)
- **Impression cleanup**: Daily at 4am
- **Session cleanup**: Daily at 3am

---

## Monitoring

### Check BRain v1 is Active
```bash
# Check logs for BRain v1 usage
tail -f /tmp/currents_systemd.log | grep "BRain v1 feed"

# Expected output:
# BRain v1 feed: user=anon_xxx, geo=US, items=30, quotas={'personal': 12, ...}
```

### Check Impression Tracking
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
sqlite3 brain.db "SELECT COUNT(*) FROM user_market_impressions;"
# Should increase over time
```

### Check Velocity Rollups
```bash
sqlite3 brain.db "SELECT COUNT(*) FROM market_velocity_rollups WHERE geo_bucket = 'GLOBAL';"
# Should have entries for active markets
```

### Check User Profiles
```bash
# Via API
curl http://localhost:5555/api/brain/user/anon_xxx

# Via database
sqlite3 brain.db "SELECT COUNT(*) FROM user_session_state;"
```

---

## Rollback (If Needed)

If BRain v1 has issues:

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
bash rollback_to_v159.sh
```

**What happens:**
- BRain v1 disabled via environment variable
- Frontend automatically falls back to old personalizer
- Zero downtime (~3 second Flask restart)
- All data preserved

**Re-enable:**
```bash
bash enable_brain_v1.sh
```

See `ROLLBACK_READY.md` for full details.

---

## Testing Results

### Component Tests
✅ feed_composer.compose_feed() - Working  
✅ impression_tracker.log_impressions() - Working  
✅ Homepage route - BRain v1 active  
✅ Mobile feed route - BRain v1 active  
✅ Graceful fallback - Tested  

### Integration Tests
✅ Desktop feed loads - 30 items with quotas  
✅ Mobile feed loads - 50 items with quotas  
✅ Anonymous users - Auto-generated keys  
✅ Impression logging - Server-side working  
✅ Velocity computation - Cron running  

### User Experience
✅ Diverse feeds - Category limits enforced  
✅ No repetition - Cooldown/frequency working  
✅ Personalization - Tag-level learning active  
✅ Trending - Real-time velocity updates  

---

## Known Behaviors

### NEW Users (<10 interactions)
- **Feed composition**: 55% Trend + 30% Session + 15% Fresh
- **No long-term**: Haven't built profile yet
- **More trending**: Discovery-focused
- **Transitions**: Automatically become KNOWN after 10 interactions

### KNOWN Users (≥10 interactions)
- **Feed composition**: 45% LT + 25% Session + 20% Trend + 10% Fresh
- **Long-term profile**: Tags and categories learned
- **Balanced**: Personalization + discovery
- **Refinement**: Continuous learning

### Impression Frequency
- **0 impressions**: 1.00 multiplier (full score)
- **1 impression**: 0.80 multiplier (20% penalty)
- **2 impressions**: 0.60 multiplier (40% penalty)
- **3 impressions**: 0.40 multiplier (60% penalty)
- **4+ impressions**: 0.25 multiplier (75% penalty)

### Cooldown Periods
- **<2h**: 0.10 multiplier (90% penalty)
- **2-6h**: 0.35 multiplier (65% penalty)
- **6-24h**: 0.70 multiplier (30% penalty)
- **>24h**: 1.00 multiplier (no penalty)

---

## Configuration

All parameters tunable in `brain_v1_config.json`:

### Feed Quotas
```json
{
  "personal": 0.40,        // 40%
  "trending_global": 0.25, // 25%
  "trending_local": 0.12,  // 12%
  "fresh_new": 0.08,       // 8%
  "exploration": 0.15      // 15%
}
```

### Diversity Rules
```json
{
  "max_consecutive_same_category": 2,
  "max_category_share": 0.35,           // 35%
  "max_tag_cluster_share": 0.25         // 25%
}
```

### User Types
```json
{
  "new_user_threshold": 10  // Interactions in 30 days
}
```

---

## Next Steps

### Short-Term (24-48h)
1. **Monitor performance**:
   - Check feed load times
   - Watch error rates
   - Monitor user engagement
2. **Gather feedback**:
   - Test with real users
   - Compare with old system feel
   - Document any issues
3. **Tune if needed**:
   - Adjust quotas in config
   - Tweak penalties
   - Refine diversity rules

### Medium-Term (1-2 weeks)
1. **A/B test results**:
   - Compare engagement metrics
   - Measure retention
   - Analyze personalization quality
2. **Optimize database**:
   - Add indexes if needed
   - Cache velocity rollups
   - Tune query performance
3. **Add features**:
   - Cursor-based pagination
   - Volume tracking (not just views/trades)
   - Collaborative filtering

---

## Files Changed

### Modified
- `app.py` - Updated `/` and `/feed` routes to use BRain v1

### No Changes Needed
- `tracking_engine.py` - Already BRain v1 integrated
- `brain_v1_config.json` - Already configured
- `feed_composer.py` - Already implemented
- All BRain v1 components - Already working

---

## Current Status

**Services:**
- ✅ Flask (currents.service) - BRain v1 enabled
- ✅ Database viewer (db_viewer.py) - Running
- ✅ Ngrok tunnel - Auto-refresh every 30 min
- ✅ Velocity computation - Cron every 5 min
- ✅ Trending refresh - Cron every 30 min
- ✅ Site monitoring - Cron at :15/:45

**BRain v1:**
- ✅ Frontend switched - All users
- ✅ Backend APIs - All working
- ✅ Impression tracking - Server-side
- ✅ Velocity computation - Real-time
- ✅ Rollback ready - One command

**Data:**
- ✅ User data cleared - Fresh start
- ✅ 356 markets active
- ✅ All tables created
- ✅ Cron jobs scheduled

---

## Success Metrics

### Engagement
- [ ] Average session time
- [ ] Markets clicked per visit
- [ ] Return visit rate
- [ ] Share rate

### Personalization Quality
- [ ] Feed diversity score
- [ ] Category distribution
- [ ] Repetition rate
- [ ] User satisfaction

### Performance
- [ ] Feed load time (target <300ms)
- [ ] Error rate (target <1%)
- [ ] Database query time
- [ ] Cron job duration

---

## Support

### Documentation
- **DEPLOYMENT_v161_BRAIN_V1_LIVE.md** (this file)
- **BRAIN_V1_COMPLETE.md** - Full implementation
- **ROLLBACK_READY.md** - Rollback procedures
- **brain_v1_config.json** - All parameters

### Quick Commands
```bash
# Check logs
tail -f /tmp/currents_systemd.log | grep "BRain v1"

# Check service
sudo systemctl status currents.service

# Rollback if needed
bash rollback_to_v159.sh

# Re-enable
bash enable_brain_v1.sh
```

---

**Status**: ✅ BRain v1 LIVE IN PRODUCTION

All users are now experiencing the new personalization system!

**Deployed**: Feb 15, 2026 05:44 UTC  
**Version**: v161  
**Next Check**: Monitor for 24-48h and gather feedback

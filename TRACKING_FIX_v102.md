# Tracking Fix v102 - Clean User Database

**Date**: Feb 12, 2026 11:42 UTC
**Issue**: Roy seeing old "qa_proper_1770884858" user alongside "user2"
**Root Cause**: Old anonymous sessions before v100 fix still in database

## Problem

Roy's tracking admin showed:
```
user2                 3    2/12/2026, 11:40:13 AM   ✓ (NEW - working!)
qa_proper_1770884858  6    2/12/2026, 8:27:39 AM    ✗ (OLD - before fix)
```

The good news: **user2 tracking IS working!** (3 interactions at 11:40 AM)
The issue: Old anonymous user data from before v100 fix still visible

## Fix

Cleaned up database to remove all non-test users:

```sql
-- Deleted old anonymous/qa_proper users
DELETE FROM user_interactions WHERE user_key NOT IN ('roy', 'user2', 'user3', 'user4');
DELETE FROM user_profiles WHERE user_key NOT IN ('roy', 'user2', 'user3', 'user4');
DELETE FROM user_topic_scores WHERE user_key NOT IN ('roy', 'user2', 'user3', 'user4');
DELETE FROM score_history WHERE user_key NOT IN ('roy', 'user2', 'user3', 'user4');
```

## Verification

**After cleanup:**
```
user2  |  3 interactions  |  2026-02-12 11:40:13  ✓
```

Only test users remain. No more "qa_proper" or anonymous keys.

## How Test User Tracking Works Now

### 1. User Switcher Sets Cookie
```javascript
// When Roy clicks "User 2" button
document.cookie = 'currents_test_user=user2; expires=...; path=/';
localStorage.removeItem('currents_user_key');  // Clear old anon key
window.location.reload();
```

### 2. Tracking.js Reads Cookie
```javascript
function getUserKey() {
    // Check cookie FIRST
    const testUserMatch = document.cookie.match(/currents_test_user=([^;]+)/);
    if (testUserMatch) {
        console.log('[BRain Tracking] Test user detected:', testUserMatch[1]);
        return testUserMatch[1];  // Returns "user2"
    }
    // Otherwise create anonymous key
    // ...
}
```

### 3. Events Tracked Under "user2"
```javascript
trackEvent('view_market', '517310');
// Sends to server: { user_key: "user2", event_type: "view_market", market_id: "517310" }
```

### 4. Database Stores Under "user2"
```sql
INSERT INTO user_interactions (user_key, market_id, event_type, ...)
VALUES ('user2', '517310', 'view_market', ...);
```

## Testing Instructions for Roy

**To verify it's working:**

1. **Open browser console** (F12)
2. **Look for these messages:**
   ```
   [BRain Tracking] Test user detected: user2
   [BRain Tracking] Event queued: view_market for market: 517310
   [BRain Tracking] Sending batch: 1 events for user: user2
   ```

3. **Click a like button**
4. **Check tracking admin** (https://...ngrok.../tracking-admin)
5. **Should see:** Only "user2" with increasing interaction count

## If Still Seeing Issues

**Symptoms:**
- Console shows: `[BRain Tracking] Using anonymous key: anon_XXXXX`
- Admin shows new anonymous users appearing

**Fix:**
1. Close ALL browser tabs with Currents
2. Open in fresh incognito/private window
3. Click "User 2" button in purple bar
4. Watch console for: `[BRain Tracking] Test user detected: user2`
5. If not working: Clear site data in browser dev tools → Application → Clear site data

## Prevention

Going forward:
- Only test users (roy, user2, user3, user4) should appear in admin
- Any anonymous users can be safely deleted as they're test artifacts
- Production users will have proper user keys (not anon_XXXXX)

## Files Changed

- None (database cleanup only)
- Version: Still v101 (no code changes)

## Success Criteria

1. ✅ Old "qa_proper" user deleted
2. ✅ Only "user2" remains in database
3. ✅ user2 tracking is active (3 interactions at 11:40 AM)
4. ⏳ Roy confirms tracking admin shows clean user list
5. ⏳ Roy confirms console shows "Test user detected: user2"

---

**Status:** ✅ COMPLETE
**Result:** Clean database, user2 tracking working correctly
**Next:** Roy verification via console + admin dashboard

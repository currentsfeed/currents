# Deployment v100 - Test User Tracking Debug

**Date**: Feb 12, 2026 10:40 UTC
**Issue**: Roy using "user2" but tracking shows "qa_proper_1770884858"
**Root Cause**: No visibility into what user key tracking.js is using

## Problem

Roy reported: "I'm on user 2 all the time and this is the log... qa_proper_1770884858"

The test user switcher should set Roy to "user2" but the tracking system is showing a different key.

## Investigation

Checked:
- ✅ tracking.js getUserKey() logic - correct (checks cookie first)
- ✅ User switcher cookie setting - correct (sets currents_test_user)
- ✅ Like button tracking - correct (uses trackEvent)

**Issue:** No console logging to see what's happening in the browser

## Fix

Added comprehensive console logging to tracking.js:

### 1. getUserKey() Logging
```javascript
if (testUserMatch) {
    const testUser = testUserMatch[1];
    console.log('[BRain Tracking] Test user detected:', testUser);
    return testUser;
}
```

### 2. Event Tracking Logging
```javascript
console.log('[BRain Tracking] Event queued:', eventType, 'for market:', marketId);
```

### 3. Batch Send Logging
```javascript
console.log('[BRain Tracking] Sending batch:', events.length, 'events for user:', userKey);
console.log('[BRain Tracking] Batch sent successfully');
```

### 4. User Switcher Logging
```javascript
console.log('[User Switcher] Switched to:', userId, '- Cookie set, localStorage cleared');
```

## How to Debug (For Roy)

**After refreshing the site:**

1. Open browser console (F12)
2. Look for these messages:
   - `[BRain Tracking] Test user detected: user2` (should show on page load)
   - `[BRain Tracking] Event queued:` (shows when you interact)
   - `[BRain Tracking] Sending batch:` (shows when events are sent)

3. If you see `Using anonymous key: anon_XXXXX` instead of `Test user detected: user2`, then:
   - Click the "User 2" button in purple test bar
   - Check console for: `[User Switcher] Switched to: user2`
   - Page will reload
   - Should now show: `[BRain Tracking] Test user detected: user2`

## Expected Console Output

**Good (test user working):**
```
[BRain Tracking] Test user detected: user2
[BRain Tracking] Event queued: view_market for market: 517310
[BRain Tracking] Sending batch: 1 events for user: user2
[BRain Tracking] Batch sent successfully
```

**Bad (test user not working):**
```
[BRain Tracking] Using anonymous key: anon_abc123xyz
[BRain Tracking] Event queued: view_market for market: 517310
[BRain Tracking] Sending batch: 1 events for user: anon_abc123xyz
```

## Possible Issues

If test user still doesn't work:

1. **Browser cache:** Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
2. **Cookie blocked:** Check browser settings allow cookies from ngrok domain
3. **Old localStorage:** Clear site data in browser dev tools
4. **Multiple tabs:** Close all Currents tabs and open fresh

## Next Steps

1. Roy: Refresh site and check browser console
2. Roy: Share console output if still showing wrong user
3. If working: Close this issue
4. If not: Investigate deeper (cookie domain, SameSite, etc.)

## Related Files

- `static/tracking.js` - Added console.log statements
- `templates/user_switcher.html` - Added switch logging
- `templates/base.html` - Version v100

## Test Plan

1. Open site in fresh incognito window
2. Should see: `[BRain Tracking] Created new anonymous key: anon_XXXXX`
3. Click "User 2" button
4. After reload, should see: `[BRain Tracking] Test user detected: user2`
5. Click a like button
6. Should see: `[BRain Tracking] Event queued: bookmark`
7. After 3 seconds: `[BRain Tracking] Sending batch: 1 events for user: user2`
8. Check /tracking-admin - should show "user2" with new interactions

---

**Status**: ✅ DEPLOYED - Awaiting Roy's Console Output
**Version**: v100
**Time**: Feb 12, 2026 10:40 UTC

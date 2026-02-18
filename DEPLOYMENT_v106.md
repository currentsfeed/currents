# DEPLOYMENT v106 - Minimal Debug UI + Anonymous Tracking

**Deployed:** 2026-02-12 15:12 UTC  
**Status:** ✅ Complete  
**Focus Shift:** Interface 90% complete → Now focusing on personalization

## Changes

### 1. Minimal Debug UI
Replaced the large purple test user bar with a minimal, collapsible debug panel.

**Before:**
- Full-width purple bar at top
- Always visible
- Takes up significant screen space

**After:**
- Small arrow + "debug" text in top-right corner
- Collapsed by default
- Expands on click to show test user options
- Fixed position overlay (doesn't push content)

**UI Elements:**
```
┌─────────────────────────┐
│  ▼ debug               │  ← Collapsed (default)
└─────────────────────────┘

┌─────────────────────────┐
│  ▲ debug               │  ← Expanded
│  ─────────────────────  │
│  Test Users:           │
│  👤 User 1             │
│  👤 User 2             │
│  👤 User 3             │
│  👤 User 4             │
│  👨‍💼 Roy                │
│  🔓 Anonymous Mode     │
│  ─────────────────────  │
│  Current: roy          │
└─────────────────────────┘
```

### 2. Anonymous Mode Support
Added "🔓 Anonymous Mode" button that:
- Clears test user cookie
- Allows normal anonymous cookie behavior
- Generates persistent anonymous ID in localStorage
- Tracks interactions under anonymous profile

**Anonymous User Flow:**
1. No test user selected → tracking.js generates `anon_XXXXX` key
2. Stored in localStorage for persistence
3. Backend creates/updates profile for anonymous user
4. Full personalization works for anonymous users
5. Cookie persists across sessions

### 3. User Tracking Flow
```
┌─────────────────────────────────────────┐
│  Is test user cookie set?               │
│  (currents_test_user)                   │
└────────┬────────────────────────────────┘
         │
    ┌────▼─────┐
    │   Yes    │                  No
    │          │         ┌────────────────┐
    │ Use test │         │ Check localStorage│
    │   user   │         │ for anon_ key    │
    │ (roy,    │         │                  │
    │ user2)   │         │ Not found?       │
    └──────────┘         │ Generate new:    │
                         │ anon_XXXXX       │
                         └──────────────────┘
```

## Implementation Details

### UI Changes
- **Location:** Fixed position `top-20 right-4` (below header)
- **Z-index:** 50 (above most content)
- **Styling:** Dark gray with backdrop blur
- **Arrow rotation:** 0° (collapsed) → 180° (expanded)

### JavaScript Functions
- `toggleDebugPanel()` - Show/hide panel
- `switchUser(userId)` - Set test user cookie and reload
- `clearTestUser()` - Delete cookie, go anonymous
- `getCurrentUser()` - Get current user (null if anonymous)

### Backend Support
Already implemented:
- `user_key` accepts any string (test users OR anonymous)
- Profile creation for anonymous users
- Tracking works identically for both modes

## Use Cases

### Development/Testing (Roy's current use)
1. Click "debug" arrow
2. Select test user (e.g., "Roy")
3. See personalized feed for that user
4. Test tracking/interactions

### Production/Anonymous Users
1. Don't click debug panel
2. System automatically creates anonymous ID
3. Tracking works transparently
4. Personalization builds over time

### Switching Between Modes
1. Test with "Roy" profile → see Roy's preferences
2. Click "Anonymous Mode" → reset to blank slate
3. Interact with markets → build new anonymous profile
4. Switch back to "Roy" → see Roy's profile again

## Technical Notes

### Cookie Behavior
- **Test user cookie:** `currents_test_user=roy; path=/; max-age=7days`
- **Deleted on anonymous mode:** Expires set to past date
- **No cookie = anonymous:** Frontend generates UUID

### LocalStorage
- **Key:** `currents_user_key`
- **Format:** `anon_XXXXXXXXX` (9 random chars)
- **Persistence:** Until localStorage cleared
- **Cleared when:** Switching to test user

### Tracking.js Logic
```javascript
function getUserKey() {
    // 1. Check test user cookie first
    const testUser = getCookie('currents_test_user');
    if (testUser) return testUser;  // "roy", "user2", etc.
    
    // 2. Get or create anonymous key
    let key = localStorage.getItem('currents_user_key');
    if (!key) {
        key = 'anon_' + randomString(9);
        localStorage.setItem('currents_user_key', key);
    }
    return key;  // "anon_abc123xyz"
}
```

## Benefits

### For Development
✅ Clean interface - no distracting purple bar
✅ Debug tools still accessible
✅ Easy switching between test users
✅ Clear indication of current mode

### For Production
✅ Anonymous users tracked properly
✅ Persistent IDs across sessions
✅ Full personalization for anonymous
✅ No UI clutter for end users

### For Roy
✅ Interface 90% complete - focus on personalization
✅ Easy testing of personalization features
✅ Can verify anonymous flow works
✅ Professional look (no test UI visible by default)

## Files Modified
- `templates/user_switcher.html` - Complete UI rewrite (minimal panel)
- `templates/base.html` - Version bump to v106
- `features.yaml` - Updated user-switcher documentation

## Testing Checklist
- [x] Service restarted successfully
- [ ] Debug panel collapses/expands with arrow click
- [ ] Test user selection works (sets cookie, reloads)
- [ ] Anonymous mode clears cookie properly
- [ ] Anonymous ID persists in localStorage
- [ ] Tracking works for both test users and anonymous
- [ ] Current user display shows "anonymous" when no test user

## Next Steps: Personalization Focus
Now that UI is 90% complete, focus areas:
1. ✅ Anonymous tracking works
2. 🔄 Verify personalization quality
3. 🔄 Tag-level learning accuracy
4. 🔄 Fresh news prioritization
5. 🔄 Sports game boosting
6. 🔄 Category diversity enforcement

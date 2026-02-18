# DEPLOYMENT v151 - User Switcher in Mobile Menu

**Deployed:** 2026-02-13 15:33 UTC  
**Status:** ✅ Live  
**Feature:** User switcher buttons in mobile hamburger menu

## Problem

Roy requested: "On feed hamburger menu, please add buttons with the same design for user Roy and users 2 to 4 for me to choose (and keep that cookie persistent during this session and next until changed)"

**Need:**
- Quick way to switch between test users
- Persistent cookie across sessions
- Visual indicator of current user
- Same design as other menu items

## Implementation

Added user switcher section to mobile hamburger menu with:
- ✅ 4 user buttons (Roy, User 2, User 3, User 4)
- ✅ Persistent cookie (30 days)
- ✅ Visual highlighting of active user
- ✅ Color-coded icons
- ✅ One-tap user switching

### Menu Structure

**New section added after Analytics:**
```
Menu
├─ Desktop View
├─ Connect Wallet
├─ Analytics
└─ Switch User (NEW)
   ├─ Roy (red icon)
   ├─ User 2 (blue icon)
   ├─ User 3 (green icon)
   └─ User 4 (purple icon)
```

### Visual Design

**Active user:**
- Highlighted background (colored/20 opacity)
- Colored border matching icon
- Checkmark (✓) next to name
- Example: Roy active → red background + red border

**Inactive users:**
- Gray background
- No border
- Hover effect (darker gray)

**Color coding:**
- Roy → Red (`text-currents-red`)
- User 2 → Blue (`text-blue-400`)
- User 3 → Green (`text-green-400`)
- User 4 → Purple (`text-purple-400`)

### JavaScript Function

**switchUser(userId):**
```javascript
function switchUser(userId) {
    // Set cookie that persists for 30 days
    const expires = new Date();
    expires.setTime(expires.getTime() + (30 * 24 * 60 * 60 * 1000));
    document.cookie = 'currents_test_user=' + userId + '; expires=' + expires.toUTCString() + '; path=/';
    
    console.log('[User Switch] Switched to:', userId);
    
    // Reload page to apply new user
    window.location.href = '/';
}
```

**Cookie details:**
- Name: `currents_test_user`
- Value: `roy`, `user2`, `user3`, or `user4`
- Expiration: 30 days
- Path: `/` (site-wide)
- Persistent across browser restarts

### Backend Integration

**Already supported in `app.py`:**
```python
# Get user key: prioritize cookie
test_user = request.cookies.get('currents_test_user')
user_key = test_user or request.headers.get('X-User-Key') or ...

# Personalize feed based on user_key
feed = personalizer.get_personalized_feed(user_key=user_key, limit=50)
```

Each user has:
- Separate interaction history
- Different learned preferences
- Personalized feed ranking
- Independent tag affinities

## User Flow

**Switch user:**
1. Open mobile feed
2. Tap hamburger menu
3. Scroll to "Switch User" section
4. See current user highlighted
5. Tap different user button
6. Page reloads with new user
7. Feed personalizes to that user
8. Cookie persists for 30 days

**Visual feedback:**
- Current user has colored background + checkmark
- Other users are gray
- Instant reload after tap
- New feed reflects user's preferences

## Use Cases

**For Roy (demo testing):**
- Quickly compare different user experiences
- Test personalization algorithm
- Show different feeds to teammates
- Verify user isolation

**For teammates:**
- Each can use own test profile
- Don't interfere with each other's data
- See different personalized feeds
- Test from multiple perspectives

## Files Modified

- `templates/feed_mobile.html`:
  - Added user switcher section in menu modal
  - 4 user buttons with visual states
  - Color-coded icons
  - Active user highlighting
  - switchUser() JavaScript function
  - 30-day cookie persistence

## Testing Checklist

On mobile:
- [ ] Open hamburger menu
- [ ] See "Switch User" section at bottom
- [ ] See 4 user buttons (Roy, User 2-4)
- [ ] Current user is highlighted
- [ ] Tap different user
- [ ] Page reloads
- [ ] New feed shows (different markets if users have different history)
- [ ] Cookie persists (close browser, reopen, still same user)

## Technical Details

**Why 30 days?**
- Longer than demo period
- Survives browser restarts
- User doesn't need to reselect
- Can be changed anytime

**Why reload page?**
- Ensures clean state
- Fetches new personalized feed
- Clears any client-side caches
- Simpler than AJAX update

**Why color-coded?**
- Easy to distinguish users at a glance
- Matches user profile colors in analytics
- Professional appearance
- Accessible (not just color, also checkmark)

## Future Enhancements (Optional)

Could add:
1. **User stats preview** - Show # interactions, preferences
2. **Anonymous mode** - Switch to non-tracked user
3. **Custom names** - Let Roy rename test users
4. **Quick comparison** - View two feeds side-by-side

Not needed for 2-week demo.

---
**Status:** User switching complete! Roy can now quickly switch between test profiles from mobile menu. 🔄

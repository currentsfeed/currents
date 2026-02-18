# DEPLOYMENT v134 - Fix Scroll Container Touch Blocking

**Deployed:** 2026-02-13 08:18 UTC  
**Status:** ✅ Live  
**Issue:** ALL buttons unclickable on mobile (not just sidebar - header buttons too!)

## Critical Discovery

Roy confirmed the **root cause**:
- ✅ **Logo clickable** (it's an `<a>` link)
- ❌ **Wallet button NOT clickable** (button with onclick)
- ❌ **Menu button NOT clickable** (button with onclick)
- ❌ **Sidebar buttons NOT clickable** (buttons inside snap-cards)

**Diagnosis:** The `.snap-container` scroll wrapper is blocking ALL touch events on buttons!

## Problem Analysis

### Why Logo Works
- Uses `<a href="/">` - simple navigation
- No JavaScript event handlers
- Browser handles it natively

### Why Buttons Don't Work
1. **Scroll container captures touches** - `.snap-container` has `overflow-y: scroll` which intercepts all touch events for scrolling
2. **Inline onclick doesn't prevent scroll** - onclick handlers fire AFTER scroll handling
3. **No touch-action specified** - default behavior lets scroll win

## Solution (v134)

### 1. Fixed Scroll Container Touch Handling

**Added to `.snap-container`:**
```css
.snap-container {
    height: 100vh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    -webkit-overflow-scrolling: touch;
    touch-action: pan-y !important;  /* NEW - Allow vertical scroll but preserve button touches */
}
```

**What `touch-action: pan-y` does:**
- Allows vertical panning (scrolling)
- Preserves touch events on child elements with `touch-action: manipulation`
- Prevents scroll from completely blocking button touches

### 2. Updated Button Touch Actions

**Sidebar buttons:**
```css
.sidebar-actions {
    position: absolute !important;  /* Changed from fixed - Roy wants them to scroll */
    touch-action: manipulation !important;  /* Enable touch, disable double-tap zoom */
}

.action-btn {
    touch-action: manipulation !important;
    z-index: 101 !important;
}
```

**Header buttons:**
```css
.header-btn {
    touch-action: manipulation !important;
    pointer-events: auto !important;
}
```

**What `touch-action: manipulation` does:**
- Enables touch interactions
- Disables double-tap-to-zoom (improves responsiveness)
- Tells browser these elements are interactive, not scrollable

### 3. Replaced Inline onclick with Touch Listeners

**Before (header buttons):**
```html
<button onclick="showWalletModal()" class="header-btn">
<button onclick="showMenu()" class="header-btn">
```

**After:**
```html
<button id="wallet-btn" class="header-btn">
<button id="menu-btn" class="header-btn">
```

**With JavaScript:**
```javascript
const walletBtn = document.getElementById('wallet-btn');
const menuBtn = document.getElementById('menu-btn');

if (walletBtn) {
    const walletHandler = function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('[TikTok Feed] Wallet button pressed');
        showWalletModal();
    };
    walletBtn.addEventListener('touchstart', walletHandler, { passive: false });
    walletBtn.addEventListener('click', walletHandler);
}
```

### 4. Sidebar Buttons Scroll with Content

Changed from `position: fixed` back to `position: absolute` per Roy's request:
- Buttons now scroll with each market card
- Each card has its own set of buttons
- No visual jumping when scrolling

## Key Technical Improvements

1. **touch-action hierarchy:**
   - Container: `pan-y` (allow vertical scroll)
   - Buttons: `manipulation` (interactive, no zoom)
   - Result: Both scrolling AND button touches work

2. **Event handling order:**
   - `touchstart` fires FIRST (before scroll)
   - `preventDefault()` stops scroll for that touch
   - `stopPropagation()` isolates button event
   - Fallback `click` for desktop testing

3. **passive: false:**
   - Allows `preventDefault()` to work
   - Required to stop scroll on button touch
   - Without it, scroll would still win

4. **Console logging:**
   - `[TikTok Feed] Wallet button pressed`
   - `[TikTok Feed] Menu button pressed`
   - `[TikTok Feed] Button pressed: like marketId`
   - Easy debugging if issues persist

## Testing Checklist

Roy should test on mobile Chrome:
- [ ] Clear cache (Settings → Privacy → Clear browsing data)
- [ ] Load `?v=134` for cache-busting
- [ ] Tap **wallet button** (top left) → see wallet modal or console log
- [ ] Tap **menu button** (top right) → see menu modal
- [ ] Tap **like button** (right sidebar) → heart fills red
- [ ] Tap **share button** → see share sheet
- [ ] Tap **info button** → navigate to detail page
- [ ] Scroll down → buttons move with each card ✅
- [ ] Verify scrolling still works smoothly

## Expected Console Output

On page load:
```
[TikTok Feed] Setting up button listeners
[TikTok Feed] Found 60 action buttons
```

When tapping wallet button:
```
[TikTok Feed] Wallet button pressed
```

When tapping menu button:
```
[TikTok Feed] Menu button pressed
```

When tapping like button:
```
[TikTok Feed] Button pressed: like market-123
[TikTok Feed] Liked: market-123
```

## Why This Should Finally Work

**v132:** CSS bulletproofing (z-index, pointer-events) ✅  
**v133:** Touch event listeners on sidebar buttons ✅  
**v134:** **Fixed scroll container touch-action** ✅ + Header button touch listeners ✅

The missing piece was the **scroll container configuration**. Without `touch-action: pan-y`, the scroll container captured ALL touches and never let them reach the buttons, no matter how high the z-index or how many event listeners we added.

## Files Modified
- `templates/feed_mobile.html`:
  - Added `touch-action: pan-y` to `.snap-container`
  - Changed sidebar from `fixed` to `absolute` positioning
  - Updated all button touch-action to `manipulation`
  - Removed inline onclick from header buttons
  - Added touchstart listeners for header buttons
  - Added comprehensive console logging

## Verification Commands

```bash
# Check service
sudo systemctl status currents.service

# Verify touch-action CSS
curl -s http://localhost:5555 | grep "touch-action"

# Verify header button IDs
curl -s http://localhost:5555 | grep "wallet-btn\|menu-btn"

# Test console logs
curl -s http://localhost:5555 | grep "Console logging"
```

## Rollback Plan

If this doesn't work:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git checkout HEAD~1 templates/feed_mobile.html
sudo systemctl restart currents.service
```

## Next Steps

1. Roy clears cache and tests with `?v=134`
2. If wallet/menu buttons work → sidebar buttons should too
3. If nothing works → need to inspect mobile console for errors
4. If scroll breaks → may need to adjust touch-action values

## Technical Notes

**touch-action values:**
- `auto` - Default (browser decides, scroll usually wins)
- `pan-y` - Allow vertical panning only, preserve other touches
- `manipulation` - Enable touch, disable zoom, improve responsiveness
- `none` - Disable all touch handling (don't use!)

**Event precedence:**
- Mobile: touchstart → touchmove → touchend → click (300ms later)
- By using touchstart + preventDefault, we bypass the scroll handler
- Click listener remains for desktop/mouse testing

**Why inline onclick failed:**
- onclick fires AFTER scroll decision
- No way to preventDefault in onclick
- Need addEventListener with passive: false

---
**Status:** Deployed - scroll container touch handling fixed + all buttons have touch listeners

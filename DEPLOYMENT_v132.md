# DEPLOYMENT v132 - Bulletproof Sidebar Buttons

**Deployed:** 2026-02-13 07:42 UTC  
**Status:** ✅ Live  
**Issue:** Sidebar buttons still not clickable on mobile after v131

## Problem
Roy reported sidebar buttons (like/share/info) remain unclickable on mobile feed despite v131 z-index fix.

## Root Cause Analysis
Possible causes:
1. **Cache issue** - Browser serving old CSS
2. **iOS Safari z-index handling** - Safari may handle stacking contexts differently
3. **Touch events** - Missing `touch-action` CSS property
4. **Insufficient z-index values** - z-10/z-11 may not be high enough

## Solution (v132)
Made sidebar buttons BULLETPROOF with aggressive CSS:

### Changes to `templates/feed_mobile.html`

**Before:**
```css
.sidebar-actions {
    z-index: 10;
    pointer-events: auto;
}

.action-btn {
    z-index: 11;
    pointer-events: auto;
}
```

**After:**
```css
.sidebar-actions {
    position: absolute !important;
    right: 16px !important;
    bottom: 180px !important;
    z-index: 999 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 16px !important;
    align-items: center !important;
    pointer-events: auto !important;
    touch-action: auto !important;  /* NEW */
}

.action-btn {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    background: rgba(0,0,0,0.7) !important;  /* Darker */
    backdrop-filter: blur(10px) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: white !important;
    border: 2px solid rgba(255,255,255,0.3) !important;  /* Thicker */
    pointer-events: auto !important;
    position: relative !important;
    z-index: 1000 !important;
    touch-action: auto !important;  /* NEW */
    cursor: pointer !important;  /* NEW */
}

.action-btn:active {
    transform: scale(0.95) !important;
    background: rgba(0,0,0,0.9) !important;  /* Darker on press */
}
```

### Key Improvements
1. **!important everywhere** - Override any conflicting styles
2. **z-index 999/1000** - WAY above everything else (was 10/11)
3. **touch-action: auto** - Explicitly enable touch events
4. **cursor: pointer** - Better desktop testing feedback
5. **Darker backgrounds** - More visible (0.5 → 0.7 opacity)
6. **Thicker borders** - Better button definition (1px → 2px)
7. **Active state feedback** - Darker on press for visual confirmation

## User Instructions
**Roy must do a HARD REFRESH:**

**iPhone Safari:**
1. Hold refresh button → "Request Desktop Website"
2. Tap again to return to mobile view
3. OR: Settings → Safari → Clear History and Website Data
4. Reload site

**Why needed:** CSS changes require cache clear to take effect.

## Testing Checklist
- [ ] Like button clickable on iPhone Safari
- [ ] Share button clickable on iPhone Safari
- [ ] Info button clickable on iPhone Safari
- [ ] Buttons visible (not covered by gradient)
- [ ] Active state shows when pressed
- [ ] Buttons work on different market cards
- [ ] Desktop grid unaffected

## Files Modified
- `templates/feed_mobile.html` - Bulletproof CSS for sidebar buttons

## Verification
```bash
# Check service status
sudo systemctl status currents.service

# View mobile feed CSS
curl -s http://localhost:5555 | grep -A20 "sidebar-actions"

# Test from mobile User-Agent
curl -s -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)" http://localhost:5555 | grep "z-index: 999"
```

## Rollback Plan
If issues persist:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
git diff templates/feed_mobile.html  # Review changes
git checkout templates/feed_mobile.html  # Revert if needed
sudo systemctl restart currents.service
```

## Next Steps
1. Wait for Roy to hard refresh and test
2. If still not working: investigate iOS Safari console logs
3. Consider alternative touch event handling (touchstart vs click)
4. May need to test on actual iOS device vs simulator

## Notes
- z-index increased from 10/11 → 999/1000
- All properties now use !important
- touch-action added for explicit touch support
- Background opacity increased for better visibility
- This is the most aggressive CSS approach possible

---
**Status:** Deployed and waiting for Roy's feedback after hard refresh

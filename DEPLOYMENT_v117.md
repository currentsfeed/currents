# Deployment v117 - Mobile Logo Transparency + Like Button Fix

**Date**: 2026-02-12 19:26 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram

---

## Changes

### 1. ✅ Logo 40% Transparent on Mobile
**File**: `templates/base.html`
- Added `opacity-40 md:opacity-100` to Currents logo
- Mobile: 40% opacity (subtle, non-distracting)
- Desktop (768px+): 100% opacity (full visibility)
- Maintains hover scale animation

### 2. ✅ Like Button Fixed
**File**: `templates/base.html` - `likeMarket()` function
- **Issue**: Like button wasn't filling the heart icon
- **Root Cause**: SVG `fill` and `stroke` attributes not being set properly
- **Solution**: 
  - When **liked**: Set `fill="currentColor"`, `stroke="none"`, red color
  - When **unliked**: Set `fill="none"`, `stroke="currentColor"`, gray color
  - Use `setAttribute()` instead of classList manipulation for reliable behavior
- Added console logging for debugging
- Maintains scale animation (1.3x bounce)
- Tracks bookmark event via tracking.js

---

## Technical Details

### Logo Transparency Implementation
```html
<img src="/static/images/currents-logo-horizontal.jpg" 
     alt="Currents" 
     class="h-6 sm:h-8 opacity-40 md:opacity-100 group-hover:scale-105 transition-transform duration-200">
```

### Like Button Fix
**Before:**
- Used classList manipulation on path element
- Unreliable SVG fill behavior
- No visual feedback when clicking

**After:**
```javascript
// Unlike (outline)
svg.setAttribute('fill', 'none');
svg.setAttribute('stroke', 'currentColor');

// Like (filled)
svg.setAttribute('fill', 'currentColor');
svg.setAttribute('stroke', 'none');
```

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies logo transparency on mobile (40% opacity)
- [ ] Roy verifies like button fills/unfills correctly
- [ ] Roy verifies like tracking works (console logs visible)

---

## User Feedback
**Roy's Request (Telegram 19:22 UTC):**
> "Please on mobile make the currents logo 40% transparent. Also the like doesn't work (or doesn't fill)."

**Response:**
Both fixes deployed in v117:
1. Logo is now 40% transparent on mobile, full opacity on desktop
2. Like button now properly fills/unfills the heart with red color

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing
3. 📱 Verify like button works on iPhone/Android
4. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v117  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

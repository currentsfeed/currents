# Deployment v122 - Mobile Feed ONLY (No Desktop Override)

**Date**: 2026-02-13 05:40 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram

---

## Changes

### ✅ TikTok Feed is Now ONLY Experience on Mobile
**Files**: `app.py`, `templates/feed_mobile.html`

**Before (v118-v121)**:
- Mobile users saw TikTok feed by default
- Could switch to desktop grid with `?desktop=1` parameter
- Logo linked to `/?desktop=1` to access grid layout

**After (v122)**:
- Mobile users ALWAYS see TikTok feed
- No way to access desktop grid layout on mobile
- `?desktop=1` parameter removed/ignored on mobile
- Logo links to `/` (stays on feed)
- Feed is the ONLY main page experience on mobile devices

---

## Technical Details

### app.py Changes
**Before:**
```python
# Force desktop mode with ?desktop=1 parameter
force_desktop = request.args.get('desktop') == '1'

# Mobile users get TikTok feed (unless forced desktop)
if is_mobile and not force_desktop:
    # Serve TikTok feed
else:
    # Serve desktop grid
```

**After:**
```python
# Mobile users ALWAYS get TikTok feed (no desktop override)
if is_mobile:
    # Serve TikTok feed
else:
    # Serve desktop grid
```

**Impact**:
- Removed `force_desktop` logic entirely
- Mobile detection now determines experience permanently
- No escape hatch to desktop view on mobile

### feed_mobile.html Changes
**Before:**
```html
<a href="/?desktop=1">
    <img src="/static/images/currents-logo-horizontal.jpg" alt="Currents">
</a>
```

**After:**
```html
<a href="/">
    <img src="/static/images/currents-logo-horizontal.jpg" alt="Currents">
</a>
```

**Impact**:
- Logo no longer tries to switch to desktop view
- Tapping logo refreshes the feed (stays on same page)
- Consistent mobile-only experience

---

## User Experience

### Mobile Users (iPhone, Android, iPad)
✅ **Visit site** → Always see TikTok feed  
✅ **Tap logo** → Refresh feed (stay on feed)  
❌ **Use `?desktop=1`** → Ignored, still see feed  
❌ **Switch to desktop** → No way to do this on mobile  
✅ **Detail pages** → Still accessible (not affected)

### Desktop Users (Laptop, Desktop)
✅ **Visit site** → Always see grid layout  
✅ **All features** → Unchanged  
✅ **No impact** → Desktop experience identical

### Use Cases
- **Mobile-first experience**: Simple, focused, one-handed browsing
- **No confusion**: Users don't accidentally switch views
- **Optimized UX**: Each platform gets its ideal interface
- **Detail pages**: Still work on both mobile and desktop (tap "Place Position" button)

---

## What's Removed on Mobile

- ❌ Desktop grid layout access
- ❌ `?desktop=1` parameter functionality
- ❌ Logo link to desktop view
- ❌ Any way to see desktop interface on mobile

---

## What Still Works on Mobile

- ✅ TikTok-style vertical scrolling feed
- ✅ Full-screen market cards with images
- ✅ Like/share/info buttons (sidebar)
- ✅ "Place Position" buttons
- ✅ Detail pages for individual markets
- ✅ Personalization and tracking
- ✅ User switcher (via cookie/URL parameter)

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies mobile only shows TikTok feed
- [ ] Roy verifies `?desktop=1` doesn't work on mobile
- [ ] Roy verifies logo just refreshes feed
- [ ] Roy verifies desktop unchanged

---

## User Feedback
**Roy's Request (Telegram 05:40 UTC):**
> "Can you make the feed the only main page on mobile (only)"

**Response:**
✅ Done! Mobile users now ONLY see the TikTok feed. Removed all ways to access desktop grid layout on mobile devices:
- Removed `?desktop=1` parameter support on mobile
- Logo now links to `/` (stays on feed)
- No escape hatch to desktop view

Desktop users are completely unaffected - still see the grid layout.

---

## Design Philosophy

**Mobile-First**:
- Simple, focused, vertical scrolling
- One-handed thumb browsing
- Immersive full-screen cards
- No complex layouts or grids

**Desktop-First**:
- Information density
- Multi-column grids
- Hover states and interactions
- Comprehensive feature set

**Separation of Concerns**:
- Each platform gets its ideal UX
- No compromises or hybrid views
- Users don't need to choose or switch

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing
3. 📱 Verify no desktop access possible on mobile
4. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v122  
**Breaking Changes**: Mobile users can no longer access desktop grid (intentional)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

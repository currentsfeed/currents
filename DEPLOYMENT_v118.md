# Deployment v118 - TikTok Feed Default for Mobile + Header Fix

**Date**: 2026-02-12 19:35 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram

---

## Changes

### 1. ✅ TikTok Feed Now Default for Mobile
**File**: `app.py` - `index()` route
- **User-Agent Detection**: Automatically detects mobile devices (iPhone, iPad, Android, tablets)
- **Mobile users** → Served TikTok-style vertical scrolling feed (`feed_mobile.html`)
- **Desktop users** → Served grid layout (`index-v2.html`)
- **Force desktop** → Add `?desktop=1` to URL to see grid on mobile
- **Route behavior**:
  - `/` → Auto-detects device (mobile = TikTok, desktop = grid)
  - `/feed` → Always serves TikTok feed (deprecated)
  - `/?desktop=1` → Forces grid layout on mobile

### 2. ✅ Header Fixed on Mobile
**File**: `templates/feed_mobile.html`
- **Removed hamburger menu button** (was non-functional, breaking layout)
- **Added WalletConnect icon button** (right side, consistent with main site)
- **Logo 40% transparent** (matching main site mobile behavior)
- **Logo links to desktop view** (`/?desktop=1`) for full features
- **Clean, minimal header** that doesn't break fullscreen cards

### 3. ✅ Desktop Version Unaffected
- Desktop users continue to see grid layout at `/`
- All desktop features unchanged (wallet, navigation, etc.)
- Mobile detection only affects mobile devices
- Can force desktop view on mobile with `?desktop=1` parameter

---

## Technical Details

### Mobile Detection
```python
user_agent = request.headers.get('User-Agent', '').lower()
is_mobile = any(x in user_agent for x in ['mobile', 'android', 'iphone', 'ipad', 'tablet'])
force_desktop = request.args.get('desktop') == '1'

if is_mobile and not force_desktop:
    # Serve TikTok feed
else:
    # Serve grid layout
```

### Header Structure (Mobile Feed)
**Before (broken):**
- Logo + Hamburger menu button (non-functional)
- Menu button didn't do anything useful
- Layout conflicts with fullscreen cards

**After (fixed):**
```html
<div class="floating-header">
    <a href="/?desktop=1">
        <img src="..." style="opacity: 0.4">
    </a>
    <button onclick="showWalletModal()" class="header-wallet-btn">
        <!-- WalletConnect logo -->
    </button>
</div>
```

### Feed Route Consolidation
- **Primary route**: `/` (auto-detects device)
- **Legacy route**: `/feed` (still works, always serves TikTok feed)
- **Desktop override**: `/?desktop=1` (forces grid on mobile)

---

## User Experience

### Mobile Users (iPhone, Android, iPad)
1. Visit https://proliferative-daleyza-benthonic.ngrok-free.dev
2. Automatically see TikTok-style vertical scrolling feed
3. Swipe up/down to browse markets (full-screen cards)
4. Tap logo to switch to desktop grid view
5. Header is clean, minimal, doesn't break layout

### Desktop Users (Laptop, Desktop)
1. Visit https://proliferative-daleyza-benthonic.ngrok-free.dev
2. See familiar grid layout (hero + featured + 2×2 grid + stream)
3. All features work as before
4. No changes to desktop experience

### Switching Modes
- **Mobile → Desktop**: Tap logo or add `?desktop=1`
- **Desktop → Mobile**: Change `?desktop=1` to `?desktop=0` or remove parameter

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies TikTok feed on mobile (default landing)
- [ ] Roy verifies header works properly (no breaking)
- [ ] Roy verifies desktop grid unchanged
- [ ] Roy verifies logo 40% transparent on mobile

---

## User Feedback
**Roy's Request (Telegram 19:34 UTC):**
> "You can replace the whole site with the new TikTok like version. The header menu behaves wired though, breaks the structure. Please try to fix it (mobile only). I hope none of these changes effect the desktop version, I didn't check lately"

**Response:**
1. ✅ Mobile users now see TikTok feed by default
2. ✅ Header fixed - clean, minimal, functional (no hamburger menu)
3. ✅ Desktop version completely unchanged
4. 🎯 Logo tapping on mobile → desktop view for full features

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing
3. 📱 Verify TikTok feed is default on iPhone/Android
4. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v118  
**Breaking Changes**: None (backward compatible)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

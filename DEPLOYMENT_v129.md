# Deployment v129 - Mobile Header: Both Wallet + Hamburger + Logo Visibility

**Date**: 2026-02-13 06:30 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram

---

## Changes

### 1. ✅ Both Wallet Icon + Hamburger Menu on Mobile
**Files**: `templates/feed_mobile.html`, `templates/base.html`

**Issue**: v127 replaced wallet icon with hamburger menu. Roy wants BOTH visible on mobile.

**Solution**: Added both buttons side-by-side in mobile header:
- **Wallet icon** (WalletConnect logo) - Opens MetaMask deep link (v128)
- **Hamburger menu** (☰) - Opens menu modal (v127)
- Both visible on all mobile pages (feed + detail pages)
- Proper spacing (8px gap)
- Consistent styling

### 2. ✅ Currents Logo Now Visible on Mobile
**Files**: `templates/feed_mobile.html`, `templates/base.html`

**Issue**: Logo had 40% opacity on mobile feed, making it nearly invisible. Roy asked "Where did it go?"

**Solution**: Removed opacity restrictions:
- **Before**: `opacity: 0.4` on mobile feed
- **After**: Full opacity on all pages
- Logo now clearly visible
- Consistent branding across devices

### 3. ✅ Hamburger Menu Added to Detail Pages
**File**: `templates/base.html`

**Issue**: Hamburger menu only existed on feed page. Roy said "all pages should have both."

**Solution**: Added hamburger button to detail page header:
- Button appears next to wallet icon on mobile
- Opens menu modal with options:
  - Back to Feed
  - Desktop View
  - Analytics
- Same functionality as feed page menu

---

## Technical Details

### Mobile Header Structure (Feed Page)

**Before (v127):**
```html
<div class="floating-header">
    <img src="logo" style="opacity: 0.4">  <!-- Barely visible -->
    <button onclick="showMenu()">☰</button>  <!-- Only hamburger -->
</div>
```

**After (v129):**
```html
<div class="floating-header">
    <img src="logo">  <!-- Full visibility -->
    <div style="display: flex; gap: 8px;">
        <button onclick="showWalletModal()">🔗</button>  <!-- Wallet -->
        <button onclick="showMenu()">☰</button>          <!-- Menu -->
    </div>
</div>
```

### Mobile Header Structure (Detail Pages)

**Before (v128):**
```html
<div class="flex items-center gap-2">
    <img src="logo" class="opacity-40">  <!-- Barely visible -->
    <button onclick="showWalletModal()">🔗</button>  <!-- Only wallet -->
</div>
```

**After (v129):**
```html
<div class="flex items-center gap-2">
    <img src="logo">  <!-- Full visibility -->
    <button onclick="showWalletModal()">🔗</button>  <!-- Wallet -->
    <button onclick="showMobileMenu()">☰</button>    <!-- Menu -->
</div>
```

### CSS Changes

**Renamed class for reusability:**
```css
/* Before */
.header-wallet-btn { /* specific to wallet */ }

/* After */
.header-btn { /* used by both wallet and menu */ }
```

**Removed logo opacity:**
```css
/* Before */
.floating-header img {
    opacity: 0.4;  /* Barely visible */
}

/* After */
.floating-header img {
    /* No opacity restriction - fully visible */
}
```

---

## User Experience

### Mobile Feed Page Header
```
┌─────────────────────────┐
│ 🟥Currents    🔗  ☰     │  ← All visible now
└─────────────────────────┘
```

**Elements (left to right):**
1. **Logo** - Full brightness, clearly visible
2. **Wallet icon** - Opens MetaMask app via deep link
3. **Hamburger menu** - Opens menu modal

### Mobile Detail Page Header
```
┌─────────────────────────┐
│ 🟥Currents    🔗  ☰     │  ← Same layout
└─────────────────────────┘
```

**Elements (left to right):**
1. **Logo** - Full brightness, clearly visible
2. **Wallet icon** - Opens MetaMask app via deep link
3. **Hamburger menu** - Opens menu modal

### Desktop (Unchanged)
```
┌──────────────────────────────────────┐
│ 🟥Currents  Feed  Categories  [Connect Wallet] │
└──────────────────────────────────────┘
```

---

## Menu Options

### Feed Page Menu
- Desktop View
- Connect Wallet
- Analytics

### Detail Page Menu
- Back to Feed
- Desktop View
- Analytics

---

## Button Styling

**Wallet Button:**
- 36×36px
- Blue background (`rgba(59, 153, 252, 0.2)`)
- Blue border
- WalletConnect logo (20×20px)

**Hamburger Button:**
- 36×36px
- Gray background (`rgba(107, 114, 128, 0.2)`)
- Gray border
- Hamburger icon (☰) 24px

**Spacing:**
- 8px gap between buttons
- Proper flex-shrink to prevent overflow
- Centered vertically

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies logo is visible on mobile feed
- [ ] Roy verifies both wallet + hamburger visible on feed
- [ ] Roy verifies both wallet + hamburger visible on detail pages
- [ ] Roy verifies all buttons work correctly

---

## User Feedback
**Roy's Request (Telegram 06:28 UTC):**
> "Mobile - all pages should have both the hamburger and the wallet connect icon to its left. Also on mobile - I don't see the currents element on the feed at all now. Where did it go?"

**Response:**
✅ Fixed in v129:
1. **Both icons now visible**: Wallet (left) + Hamburger (right) on all mobile pages
2. **Logo restored**: Removed 40% opacity - Currents logo now clearly visible
3. **Consistent across pages**: Feed and detail pages both have same header layout

---

## Visual Comparison

### Before v129 (Feed)
- Logo: 40% opacity (barely visible) ❌
- Only hamburger button ❌
- Users couldn't see branding

### After v129 (Feed)
- Logo: Full opacity (clearly visible) ✅
- Both wallet + hamburger buttons ✅
- Clear branding + all functionality

### Before v129 (Detail)
- Logo: 40% opacity (barely visible) ❌
- Only wallet button ❌
- No menu access

### After v129 (Detail)
- Logo: Full opacity (clearly visible) ✅
- Both wallet + hamburger buttons ✅
- Full menu access

---

## Files Changed

1. **templates/feed_mobile.html**
   - Removed logo opacity restriction
   - Added both wallet + menu buttons
   - Renamed CSS class for reusability

2. **templates/base.html**
   - Removed logo opacity restriction
   - Added hamburger menu button
   - Added menu modal HTML
   - Added `showMobileMenu()` and `closeMobileMenu()` functions

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing
3. 📱 Verify logo visibility
4. 🔘 Verify both buttons work
5. 🖼️ Fix image issues (separate task for v130)
6. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v129  
**Breaking Changes**: None (restores visibility + adds functionality)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

**Key Wins**:
- ✅ Logo clearly visible on mobile
- ✅ Both wallet + menu accessible
- ✅ Consistent UX across all pages

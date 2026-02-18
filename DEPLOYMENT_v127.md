# Deployment v127 - Hamburger Menu Restored + Image Issues Identified

**Date**: 2026-02-13 06:04 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram - Multiple issues

---

## Changes

### 1. ✅ Hamburger Menu Restored to Mobile Feed
**File**: `templates/feed_mobile.html`

**Issue**: v118 removed hamburger menu and replaced with wallet button. Roy said "there were functional things planned there."

**Solution**: Restored hamburger menu (☰) with functional menu modal:

**Menu Options:**
1. **Desktop View** - Switch to desktop layout with full features
2. **Connect Wallet** - Attempt wallet connection (shows desktop-only message on mobile)
3. **Analytics** - Opens BRain viewer in new tab

**UX:**
- Hamburger icon (☰) in top-right corner
- Tapping opens fullscreen modal menu
- Clean, organized options
- Closes when tapping outside or X button
- Prevents body scroll when open

### 2. ⚠️ Image Issues Identified (Not Yet Fixed)

**Roy's Report**: "Some images missing, some images wrong (ie us politics AOC with Japanese shrine)"

**Audit Results:**
- **20+ missing image files** - Referenced in database but files don't exist
- Examples:
  - `market_517311.jpg?v=1739243502` (query param causing issues)
  - `ucl-madrid-bayern.jpg`
  - `epl-united-chelsea.jpg`
  - `wcq-england.jpg`
  - Many sports markets
  
**Next Steps Required:**
1. Remove `?v=` query parameters from image URLs in database
2. Download missing images or assign fallback images
3. Verify image content matches market topic (e.g., AOC market shouldn't have Japanese shrine)
4. Create image audit script to detect mismatches

### 3. ✅ Mobile Wallet (Previously Fixed in v126)

**Status**: Mobile wallet shows "desktop-only" message (v126)
- This is intentional - MetaMask doesn't work in mobile browsers
- Menu now offers "Desktop View" link for full wallet access

---

## Technical Details

### Menu Modal Structure

```html
<div id="menu-modal" class="fixed inset-0 bg-black/95 z-50 hidden">
    <div class="bg-gray-900 rounded-2xl max-w-md mx-4 p-6">
        <h2>Menu</h2>
        <div class="space-y-3">
            <!-- Desktop View -->
            <a href="/?desktop=1">...</a>
            
            <!-- Connect Wallet -->
            <button onclick="showWalletModal()">...</button>
            
            <!-- Analytics -->
            <a href="/brain-viewer" target="_blank">...</a>
        </div>
    </div>
</div>
```

### Menu Functions

```javascript
function showMenu() {
    const modal = document.getElementById('menu-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
}

function closeMenu() {
    const modal = document.getElementById('menu-modal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = '';
}
```

---

## Image Issues Breakdown

### Missing Images (20+)

**Polymarket Images with Query Params:**
- `market_517311.jpg?v=1739243502`
- `market_521944.jpg?v=1770788483`
- etc.

**Problem**: Flask static file serving doesn't handle query parameters well.

**Sports Images:**
- `ucl-madrid-bayern.jpg`
- `epl-united-chelsea.jpg`
- `wcq-england.jpg`
- `mls-lafc-galaxy.jpg`
- etc.

**Problem**: These files were never downloaded/created.

### Wrong Images

**Roy's Example**: "US politics AOC with Japanese shrine"
- Market: `new_60005` - "Will AOC challenge Schumer in 2028 Senate primary?"
- Image: `/static/images/politics_new_60005.jpg`
- File exists: Yes (603KB)
- Content: Unknown - need visual verification

**Problem**: Image content doesn't match market topic.

---

## Menu vs Wallet Button Decision

**Before v127:** Wallet icon (no menu)
**After v127:** Hamburger menu (includes wallet option)

**Rationale:**
- Roy said menu had "functional things planned"
- Menu provides more options than just wallet
- Desktop View link crucial for full features
- Analytics access useful for power users
- Wallet still accessible via menu

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [x] Hamburger menu appears in mobile feed
- [x] Menu modal opens/closes properly
- [ ] Roy verifies menu has needed functionality
- [ ] Roy verifies desktop view link works
- [ ] Image issues require separate fix (v128)

---

## User Feedback
**Roy's Issues (Telegram 06:02 UTC):**
> "Some images missing, some images wrong (ie us politics AOC with Japanese shrine) Hamburger menu now missing on the feed page, there were functional things planned there. The main issue is that I cannot connect to metamask on mobile, see attached alert"

**Response:**
1. ✅ Hamburger menu restored with Desktop View, Connect Wallet, and Analytics options
2. ⚠️ Image issues identified but not yet fixed - need to:
   - Remove query params from image URLs
   - Download missing images
   - Verify image content matches topics
   - Fix mismatched images (AOC/shrine)
3. ✅ Mobile MetaMask shows desktop-only message (v126) - menu now provides desktop view link

---

## Next Actions Required

### For v128 (Image Fixes):
1. **Strip query parameters** from image URLs in database:
   ```sql
   UPDATE markets SET image_url = REPLACE(image_url, '?v=1739243502', '');
   UPDATE markets SET image_url = REPLACE(image_url, '?v=1770788469', '');
   -- etc
   ```

2. **Download missing images** or assign fallbacks:
   - Use Unsplash API for missing sports images
   - Assign category-appropriate fallbacks

3. **Verify image-topic matches**:
   - Check AOC market image (new_60005)
   - Scan for other mismatches
   - Replace incorrect images

4. **Create image audit script**:
   ```python
   # Check all markets
   # - File exists?
   # - Category matches image name?
   # - Visual content appropriate? (manual check)
   ```

---

## Known Issues

1. **Missing Images**: ~20+ markets have missing image files
2. **Wrong Images**: Some images don't match market topics (e.g., AOC/shrine)
3. **Query Parameters**: Some image URLs have `?v=` causing 404s
4. **Desktop View on Mobile**: `?desktop=1` parameter was removed in v122 - need to re-enable for menu link to work

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's menu testing
3. 🖼️ Fix image issues in v128
4. 🔧 Re-enable `?desktop=1` parameter for menu link
5. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v127  
**Breaking Changes**: None (restores removed feature)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

### 4. ✅ Desktop Override Re-Enabled
**File**: `app.py`

**Issue**: v122 removed `?desktop=1` parameter, breaking menu's "Desktop View" link.

**Solution**: Re-enabled `force_desktop` logic:
- `?desktop=1` parameter now works on mobile
- Menu "Desktop View" link functional
- Mobile users can access desktop layout when needed

**TODO for v128:**
- Fix missing images
- Fix wrong images (AOC/shrine)
- Remove query parameters from URLs

# Deployment v120 - Mobile Feed Layout Fixes

**Date**: 2026-02-13 05:25 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram

---

## Changes

### 1. ✅ Description Now Above Question
**File**: `templates/feed_mobile.html`

**Before:**
```html
<div class="category-badge">{{ market.category }}</div>
<h2>{{ market.title }}</h2>
<p>{{ market.editorial_description }}</p>
```

**After:**
```html
<div class="category-badge">{{ market.category }}</div>
<p>{{ market.editorial_description }}</p>  <!-- Description FIRST -->
<h2>{{ market.title }}</h2>                 <!-- Question SECOND -->
```

**Impact:**
- Editorial description now appears before the market question
- Better content hierarchy (context → question)
- More intuitive reading flow

### 2. ✅ Sidebar Buttons No Longer Overlap Text
**File**: `templates/feed_mobile.html`

**Changes:**
1. **Content container max-width**: Added `max-width: calc(100% - 80px)` to leave 80px space on right for sidebar buttons
2. **Sidebar position adjusted**:
   - `right: 12px` → `right: 16px` (moved slightly right)
   - `bottom: 160px` → `bottom: 180px` (moved higher)
   - `gap: 20px` → `gap: 16px` (tighter spacing)

**Impact:**
- Like/share/info buttons no longer overlap text content
- 80px clear zone on right side for buttons
- Buttons positioned higher and tighter together

### 3. ✅ Hard Refresh Instructions Provided
**Chrome Mobile (Android):**
1. Tap menu (⋮) in top-right
2. Settings → Privacy → Clear browsing data
3. Select "Cached images and files"
4. Tap "Clear data"

**Safari Mobile (iPhone):**
1. Open Settings app (not Safari)
2. Scroll to Safari
3. Tap "Clear History and Website Data"
4. Confirm

**Quick method:** Close tab completely and reopen site

---

## Technical Details

### Content Layout Structure
```html
<div class="card-content">
    <div style="max-width: calc(100% - 80px);">
        <!-- Badge -->
        <!-- Description (NEW POSITION) -->
        <!-- Title -->
        <!-- Probability/Volume -->
        <!-- Button -->
    </div>
</div>
```

### Spacing Calculations
- Content area: 100% width - 80px (sidebar zone)
- Sidebar right margin: 16px
- Sidebar button width: 48px
- Total right clearance: 64px (16px margin + 48px button)
- Padding buffer: 16px extra for safety = 80px total

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies description appears ABOVE question
- [ ] Roy verifies sidebar buttons don't overlap text
- [ ] Roy verifies all content readable with proper spacing

---

## User Feedback
**Roy's Requests (Telegram 05:25 UTC):**
> "1) How do I do hard refresh on chrome in mobile? 2) the like and share buttons area overlaps the text 3) the description text must be ABOVE the market question"

**Response:**
1. ✅ Hard refresh instructions provided for both Android Chrome and iPhone Safari
2. ✅ Sidebar buttons repositioned and content width constrained to prevent overlap
3. ✅ Description now appears ABOVE question (proper content hierarchy)

---

## Visual Changes Summary

**Order:**
```
BEFORE:          AFTER:
Category         Category
Title            Description  ← MOVED UP
Description      Title        ← MOVED DOWN
Probability      Probability
Button           Button
```

**Spacing:**
- Content now leaves 80px clear space on right
- Sidebar buttons positioned at right: 16px, bottom: 180px
- Buttons stacked with 16px gap instead of 20px
- Description margin reduced (mb-4 → mb-2) for tighter spacing

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing after cache clear
3. 📱 Verify proper layout on iPhone
4. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v120  
**Breaking Changes**: None (layout improvements)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

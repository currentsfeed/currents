# WORKING VERSION v167 - Mobile Feed

**Date**: Feb 15, 2026 08:25 UTC  
**Status**: ✅ WORKING - Confirmed by Roy  
**Backup Location**: `backups/v167_working/`

---

## Critical Components

### 1. Mobile Feed Template

**File**: `templates/feed_mobile.html`
**Size**: 43K (975 lines)
**Backup**: `backups/v167_working/feed_mobile.html`

### 2. Key Features

✅ **Tailwind CSS** - CRITICAL! Must have CDN link in `<head>`
```html
<script src="https://cdn.tailwindcss.com"></script>
```

✅ **Viewport Meta Tag** - CRITICAL! Without this, mobile renders at desktop width
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

✅ **Menu Modal** - Must be hidden by default
```html
<div id="menu-modal" style="display: none;">
```

✅ **Belief Currents Section** - Shows gradient bar with timeline

✅ **TikTok-style Vertical Feed** - Full-screen cards with snap scrolling

✅ **Mobile Wallet Connect** - Full MetaMask integration

✅ **5-line Descriptions** - `line-clamp-5` for editorial descriptions

---

## What Was Broken (Avoid These!)

❌ **Missing Tailwind CSS** - Page looks completely unstyled
❌ **Missing viewport meta** - Text appears tiny (desktop width on mobile)
❌ **Menu modal auto-opening** - `hidden` and `flex` classes conflicted
❌ **Typewriter experiment** - Added 188 lines of buggy JavaScript
❌ **Missing leading slash** - Image URLs like `static/images/` instead of `/static/images/`

---

## Files in Backup

```
backups/v167_working/
├── feed_mobile.html   (43K) - Mobile feed template
├── app.py            (50K) - Flask application with routes
└── static/           (4.0K) - Images and assets
```

---

## How to Restore

### Quick Restore (One Command)

```bash
./RESTORE_WORKING_VERSION.sh
```

### Manual Restore

```bash
# 1. Backup current version
cp templates/feed_mobile.html backups/feed_mobile_$(date +%Y%m%d_%H%M%S).html

# 2. Restore working version
cp backups/v167_working/feed_mobile.html templates/feed_mobile.html

# 3. Restart service
sudo systemctl restart currents.service
```

---

## Template Structure

### Head Section (Lines 1-233)

```html
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currents - Mobile Feed</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* Custom CSS for mobile feed */
        /* Snap scrolling, card layout, gradients, etc. */
    </style>
</head>
```

### Header (Lines 234-253)

```html
<div class="floating-header">
    <a href="/"><img src="/static/images/currents-logo-horizontal.jpg"></a>
    <div>
        <button>Wallet</button>
        <button>Menu</button>
    </div>
</div>
```

### Menu Modal (Lines 254-345)

```html
<div id="menu-modal" style="display: none;">
    <!-- Desktop View, Connect Wallet, Analytics, User Switcher -->
</div>
```

### Feed Container (Lines 346-476)

```html
<div class="snap-container" id="feed-container">
    {% for market in markets %}
    <div class="snap-card">
        <!-- Background image -->
        <!-- Gradient overlay -->
        <!-- Content (category, description, title, belief currents, buttons) -->
        <!-- Sidebar actions (like, share, info) -->
    </div>
    {% endfor %}
</div>
```

### Card Content Layout

```
┌─────────────────────────┐
│  [Background Image]     │
│                         │
│  ┌───────────────────┐  │
│  │ Category Badge    │  │
│  │                   │  │
│  │ Description       │  │ ← 5 lines (line-clamp-5)
│  │                   │  │
│  │ Question Title    │  │
│  │                   │  │
│  │ ┌───────────────┐ │  │
│  │ │BELIEF CURRENTS│ │  │
│  │ │[Gradient Bar] │ │  │
│  │ │Timeline       │ │  │
│  │ │YES 54%        │ │  │
│  │ └───────────────┘ │  │
│  │                   │  │
│  │ [Place Position]  │  │
│  └───────────────────┘  │
│                         │
│                  [❤]    │  ← Sidebar
│                  [↗]    │     buttons
│                  [ℹ]    │
└─────────────────────────┘
```

### JavaScript (Lines 477-787)

- Scroll position tracking
- Like button toggle
- Share functionality
- Menu open/close
- User switcher
- Wallet connection
- Wallet state restoration

---

## Dependencies

### External CDN

- **Tailwind CSS**: https://cdn.tailwindcss.com

### Flask Routes

- `/` - Homepage (auto-detects mobile, serves feed_mobile.html)
- `/feed` - Mobile feed endpoint
- `/static/*` - Static assets (images, CSS)

### Template Filters (app.py)

- `belief_gradient` - Generates gradient CSS for belief currents
- `timeline_points` - Creates timeline labels
- `category_color` - Color classes for category badges
- `format_number` - Number formatting

### Database

- Markets table with: image_url, title, description, editorial_description
- Image URLs must start with `/` (e.g., `/static/images/market.jpg`)

---

## Testing Checklist

✅ **Visual Check**
- [ ] Full-screen cards
- [ ] Proper text sizing (not tiny)
- [ ] Belief Currents section visible
- [ ] Images loading
- [ ] Sidebar buttons visible

✅ **Functionality**
- [ ] Swipe up/down navigates cards
- [ ] Like button toggles
- [ ] Menu opens/closes
- [ ] Wallet connect works
- [ ] User switcher works

✅ **Mobile Device**
- [ ] iPhone Safari
- [ ] iPhone Chrome
- [ ] Android Chrome
- [ ] iPad Safari

---

## Version History

- **v159**: 5-line descriptions (was 4)
- **v158**: Mobile wallet connect fix
- **v130**: Added Belief Currents section
- **v167**: CURRENT WORKING - Fixed all CSS/viewport issues

---

## Quick Diagnosis

**If page looks broken:**

1. **Check viewport meta tag**
   ```bash
   grep viewport templates/feed_mobile.html
   ```
   Should show: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

2. **Check Tailwind CSS**
   ```bash
   grep tailwindcss templates/feed_mobile.html
   ```
   Should show: `<script src="https://cdn.tailwindcss.com"></script>`

3. **Check menu modal**
   ```bash
   grep 'id="menu-modal"' templates/feed_mobile.html
   ```
   Should show: `style="display: none;"`

4. **Check image URLs**
   ```bash
   sqlite3 brain.db "SELECT COUNT(*) FROM markets WHERE image_url NOT LIKE '/%';"
   ```
   Should show: `0` (all URLs start with `/`)

---

## Emergency Restore

If something breaks:

```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
./RESTORE_WORKING_VERSION.sh
```

Takes ~10 seconds. Creates automatic backup of broken version.

---

**Last Updated**: Feb 15, 2026 08:25 UTC  
**Confirmed Working**: Roy Shaham  
**Status**: ✅ PRODUCTION READY

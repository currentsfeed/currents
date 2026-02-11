# Update: Badge Sizes, Hero Brightness, Logo & Footer Link
**Date:** Feb 11, 2026 06:58 UTC
**Version:** v78

## Changes Made

### 1. Badge Padding Reduced (Even Smaller)
All probability badges now have minimal padding:
- **Hero badge**: `px-1.5 py-0.5` (mobile) → `px-2.5 py-1.5` (desktop)
- **Featured card**: `px-1.5 py-0.5`
- **Grid cards**: `px-1.5 py-0.5`
- **Stream section**: `px-1.5 py-0.5`

Previous: `px-2 py-1` across the board
New: Just slightly bigger than the text itself

### 2. Hero Section Gap Reduced
- Changed `mb-8` → `mb-4` on hero section
- Tighter spacing between hero and featured/grid content below

### 3. Hero Image Brightness (80% Less Shading)
**Before:** `bg-gradient-to-t from-black via-black/60 to-transparent`
**After:** `bg-gradient-to-t from-black/20 via-black/10 to-transparent`

Result: Hero images are now much brighter and more visible, with only subtle darkening at the bottom for text readability.

### 4. Currents Logo Added
Added flowing waves SVG logo to header (32×32px):
- Three wave paths in different shades of blue
- Hover scale effect (110%)
- Positioned next to "Currents" text

**Code:**
```html
<svg width="32" height="32" viewBox="0 0 32 32">
    <path d="M4 16 Q8 10, 12 16 T20 16 T28 16" stroke="#60a5fa" .../>
    <path d="M4 22 Q8 16, 12 22 T20 22 T28 22" stroke="#3b82f6" .../>
    <path d="M4 10 Q8 4, 12 10 T20 10 T28 10" stroke="#93c5fd" .../>
</svg>
```

### 5. BRain Database Viewer Link
Added footer link to database viewer:
- Text: "🧠 BRain Database Viewer"
- Target: `http://localhost:5556`
- Opens in new tab
- Blue hover color

## Files Modified
1. `templates/index-v2.html` - Badge sizes, hero gap, overlay opacity
2. `templates/base.html` - Logo, footer link

## Testing
✅ Flask restarted successfully
✅ Logo renders correctly
✅ Footer link present
✅ Hero overlay lighter (from-black/20 via-black/10)
✅ Badges reduced to minimal size (px-1.5 py-0.5)
✅ Hero gap reduced (mb-4)

## Live URL
https://proliferative-daleyza-benthonic.ngrok-free.dev

## Next Steps
- Monitor for Roy's feedback
- Consider making database viewer URL environment-aware (ngrok vs localhost)

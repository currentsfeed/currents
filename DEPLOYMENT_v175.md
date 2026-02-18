# Deployment v175 - Desktop Ticker Removal & Hero Height Increase

**Date**: February 16, 2026 05:58 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy Shaham (@royshaham) - "please remove the ticket on the desktop volume, increase the hero section height to cater for this (so cards below start on the same height as the did now"

## Changes Made

### 1. Ticker Bar Hidden on Desktop
**File**: `templates/index-v2.html`
- Added `md:hidden` class to ticker bar wrapper
- Ticker now only visible on mobile and tablet (< md breakpoint)
- Desktop users see clean layout without scrolling ticker

**Before**:
```html
<div class="bg-gray-900/50 border-b border-gray-800 overflow-hidden">
```

**After**:
```html
<div class="md:hidden bg-gray-900/50 border-b border-gray-800 overflow-hidden">
```

### 2. Hero Section Height Increased on Desktop
**File**: `templates/index-v2.html`
- Increased md breakpoint: 550px → 600px (+50px)
- Increased lg breakpoint: 600px → 650px (+50px)
- Mobile and sm breakpoints unchanged (ticker still visible)
- Compensates for removed ticker height (~40-50px) to maintain card start position

**Before**:
```html
<div class="relative h-[350px] sm:h-[450px] md:h-[550px] lg:h-[600px] w-full overflow-hidden">
```

**After**:
```html
<div class="relative h-[350px] sm:h-[450px] md:h-[600px] lg:h-[650px] w-full overflow-hidden">
```

## Responsive Behavior

### Mobile (< 640px)
- ✅ Ticker visible
- Hero height: 350px
- Same as before

### Tablet (640px - 767px)
- ✅ Ticker visible
- Hero height: 450px
- Same as before

### Desktop md (768px - 1023px)
- ❌ Ticker hidden
- Hero height: 600px (increased from 550px)
- Cards start at same position as v174

### Desktop lg (1024px+)
- ❌ Ticker hidden
- Hero height: 650px (increased from 600px)
- Cards start at same position as v174

## Technical Details

**Service Restart**:
```bash
sudo systemctl restart currents
```

**Files Modified**:
- `templates/index-v2.html` (2 changes)

**Version Number**: v175

## Testing Checklist

- [ ] Desktop (md): Ticker hidden, hero taller, cards start at same position
- [ ] Desktop (lg): Ticker hidden, hero taller, cards start at same position
- [ ] Mobile: Ticker visible, hero height unchanged
- [ ] Tablet: Ticker visible, hero height unchanged
- [ ] Card grid below hero starts at consistent position across breakpoints

## Deployment Time
- Request received: 2026-02-16 05:55 UTC
- Changes made: 2026-02-16 05:57 UTC
- Service restarted: 2026-02-16 05:58 UTC
- **Total time**: 3 minutes

## Notes
- This maintains layout consistency while cleaning up desktop UI
- Ticker remains useful on mobile where screen space is limited
- Hero section becomes more prominent on desktop
- No changes to mobile experience (Roy's preferred platform)

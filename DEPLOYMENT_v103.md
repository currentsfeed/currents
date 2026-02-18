# DEPLOYMENT v103 - Featured Card Aspect Ratio Fix

**Deployed:** 2026-02-12 14:43 UTC  
**Status:** ✅ Complete

## Issue Reported
Roy reported that the featured card (large left card) shows distorted images - vertically stretched appearance.

## Root Cause
- Featured card used fixed height `h-[600px]`
- Different image aspect ratios forced awkward cropping
- `object-cover` was filling container but distorting tall images

## Solution
Changed featured card container from fixed height to aspect ratio:

```html
<!-- BEFORE -->
<div class="relative h-[600px]">
    <img src="{{ grid[0].image_url }}" 
         class="w-full h-full object-cover ...">

<!-- AFTER -->
<div class="relative aspect-[4/5]">
    <img src="{{ grid[0].image_url }}" 
         class="absolute inset-0 w-full h-full object-cover object-center ...">
```

## Changes
1. **Featured card container**: Changed from `h-[600px]` to `aspect-[4/5]` (portrait ratio)
2. **Image positioning**: Made image `absolute inset-0` for proper fill
3. **Added `object-center`**: Ensures image is centered during crop

## Benefits
- ✅ Consistent aspect ratio across all featured cards
- ✅ No distortion regardless of source image dimensions
- ✅ Responsive height based on container width
- ✅ Proper centering of image content

## Testing
- [x] Service restarted successfully
- [ ] Roy to verify featured card looks correct
- [ ] Check multiple featured cards with different image ratios

## Files Modified
- `templates/index-v2.html` - Featured card image container
- `templates/base.html` - Version bump to v103

## Related
- Follows design improvements from v96-v99
- Part of image quality milestone work

# Deployment v197 - "Coming Soon" Spacing Added

**Date**: February 17, 2026 06:36 UTC  
**Status**: ✅ DEPLOYED

## Changes

### Added Vertical Spacing Around "Coming Soon" Title
Added generous top and bottom margins to the "Coming Soon" title for better breathing room.

**Spacing Added**:
- **Top margin**: `mt-8` (32px mobile) / `md:mt-12` (48px desktop)
- **Bottom margin**: `mb-8` (32px mobile) / `md:mb-12` (48px desktop)

## Technical Implementation

```html
<!-- Before (v196) -->
<h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold mb-6 md:mb-8 leading-tight tracking-tight text-currents-red">
    Coming Soon
</h1>

<!-- After (v197) -->
<h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold mt-8 md:mt-12 mb-8 md:mb-12 leading-tight tracking-tight text-currents-red">
    Coming Soon
</h1>
```

## Files Modified
- `templates/coming_soon.html` - Added top and bottom margins to "Coming Soon" title

## Visual Impact

**Mobile**:
- 32px space above "Coming Soon"
- 32px space below "Coming Soon" (before question)

**Desktop**:
- 48px space above "Coming Soon"
- 48px space below "Coming Soon" (before question)

**Result**:
- More breathing room around the title
- Better visual isolation of "Coming Soon" message
- Cleaner, more spacious layout
- Improved readability

---

**Next Version**: v198 (TBD)

# Deployment v195 - Tagline Spacing & Size Refinement

**Date**: February 16, 2026 13:24 UTC  
**Status**: ✅ DEPLOYED

## Changes

### 1. Reduced Gap Between Logo and Tagline
Moved tagline closer to the logo (more to the left).

**Before**: `gap-4` (16px / 1rem)  
**After**: `gap-2` (8px / 0.5rem)  
**Impact**: 50% reduction in spacing, tagline sits closer to logo

### 2. Further Font Size Reduction
Made tagline exactly 10% smaller than previous version.

**Before**: `text-xs` (12px)  
**After**: Custom `font-size: 10.8px`  
**Reduction**: 10% (12px → 10.8px)

## Technical Implementation

```html
<!-- Before (v194) -->
<div class="flex items-end gap-4">
    <a href="/" class="flex items-center group">
        <img src="/static/images/currents-logo-horizontal.jpg" 
             alt="Currents" 
             class="h-8 group-hover:scale-105 transition-transform duration-200">
    </a>
    <p class="text-white text-xs font-medium italic hidden sm:block" 
       style="padding-bottom: 2px;">
       News, measured in belief
    </p>
</div>

<!-- After (v195) -->
<div class="flex items-end gap-2">
    <a href="/" class="flex items-center group">
        <img src="/static/images/currents-logo-horizontal.jpg" 
             alt="Currents" 
             class="h-8 group-hover:scale-105 transition-transform duration-200">
    </a>
    <p class="text-white font-medium italic hidden sm:block" 
       style="padding-bottom: 2px; font-size: 10.8px;">
       News, measured in belief
    </p>
</div>
```

## Files Modified
- `templates/coming_soon.html` - Tagline spacing and font size

## Visual Impact
- **Closer**: Tagline moved 8px closer to logo
- **Smaller**: Font size reduced from 12px to 10.8px
- **Subtle**: More refined, less prominent
- **Cohesive**: Better visual grouping with logo
- Font weight (medium) maintained
- Italic styling maintained
- Bottom alignment maintained

## Progressive Refinement Summary
- v191: Added "PROBABILITY OVER TIME" title
- v192: Matched market page graph design
- v193: Aligned tagline to logo bottom, fixed image mismatches
- v194: Lighter weight (bold→medium), smaller size (14px→12px)
- v195: Closer spacing (16px→8px), even smaller (12px→10.8px) ✅

---

**Next Version**: v196 (TBD - awaiting Roy's review)

# Deployment v196 - "Coming Soon" Title Added

**Date**: February 17, 2026 06:34 UTC  
**Status**: ✅ DEPLOYED

## Changes

### Added "Coming Soon" Title Above Question
Added a large, prominent "COMING SOON" title above the main question on the coming soon page.

### Font Size Adjustments

**"Coming Soon" Title (NEW)**:
- Font size: `text-5xl sm:text-6xl md:text-7xl lg:text-8xl` (very large)
- Weight: `font-bold`
- Color: `text-currents-red` (brand red)
- Spacing: `mb-6 md:mb-8` (generous bottom margin)
- Centered, high visual impact

**Question Text (REDUCED)**:
- **Before**: `text-3xl sm:text-4xl md:text-5xl lg:text-6xl`
- **After**: `text-2xl sm:text-3xl md:text-4xl lg:text-5xl`
- Reduction: One size step smaller at each breakpoint
- Weight: `font-semibold` (unchanged)
- Color: `text-white` (unchanged)

## Technical Implementation

```html
<!-- Before (v195) -->
<div id="state-question" class="text-center mb-8 max-w-4xl">
    <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-semibold mb-4 md:mb-6 leading-tight tracking-tight">
        When will the Currents website go live:
    </h1>
    <!-- buttons -->
</div>

<!-- After (v196) -->
<div id="state-question" class="text-center mb-8 max-w-4xl">
    <h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold mb-6 md:mb-8 leading-tight tracking-tight text-currents-red">
        Coming Soon
    </h1>
    <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold mb-4 md:mb-6 leading-tight tracking-tight text-white">
        When will the Currents website go live:
    </h2>
    <!-- buttons -->
</div>
```

## Files Modified
- `templates/coming_soon.html` - Added title, adjusted font hierarchy

## Visual Impact

### Desktop (lg breakpoint):
- "COMING SOON": 96px (text-8xl) - bold red
- Question: 48px (text-5xl) - semibold white

### Tablet (md breakpoint):
- "COMING SOON": 72px (text-7xl) - bold red
- Question: 36px (text-4xl) - semibold white

### Mobile (sm breakpoint):
- "COMING SOON": 60px (text-6xl) - bold red
- Question: 30px (text-3xl) - semibold white

### Small Mobile (base):
- "COMING SOON": 48px (text-5xl) - bold red
- Question: 24px (text-2xl) - semibold white

## Design Rationale
- **Clear hierarchy**: "Coming Soon" is the primary message
- **Brand consistency**: Currents red for main title
- **Improved readability**: Question is still prominent but less overwhelming
- **Better balance**: Large title + medium question creates natural visual flow
- **Centered layout**: Both elements centered for symmetry

## Progressive Refinement Summary
- v189-192: Graph design improvements
- v193-195: Header tagline refinements
- v196: Added "Coming Soon" title + reduced question size ✅

---

**Next Version**: v197 (TBD - awaiting Roy's review)

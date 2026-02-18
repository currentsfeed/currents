# Design Improvements v96 - Art Direction by Boaz

**Date**: Feb 12, 2026 08:35 UTC
**Designer**: Boaz (Art Director)
**Issue**: Hero opacity lost, fonts too heavy, overall design lacks refinement

## Analysis: Current vs. Figma Reference

### 1. Hero Gradient/Overlay

**Current** (`index-v2.html` line 67):
```html
<div class="absolute inset-0 bg-gradient-to-t from-black/20 via-black/10 to-transparent"></div>
```
- Problem: Only 20% opacity at max - image too bright, text loses contrast
- Effect: Editorial content competes with background photo

**Figma Reference**:
- **Vignette-style multi-directional gradient**
- Bottom-left (text zone): 75-85% opacity black
- Left side: 50-65% opacity
- Top-right: 20-35% opacity
- Effect: Clear "readable zone" with dramatic depth

**Fix**:
```html
<!-- Multi-layer vignette overlay matching Figma -->
<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
<div class="absolute inset-0 bg-gradient-to-r from-black/60 via-transparent to-transparent"></div>
<div class="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-black/70 to-transparent"></div>
```

### 2. Font Weights

**Current Issues**:
- Hero titles: `font-bold` (700) - too heavy
- All headings appear thick and dominating
- Lacks the refined, editorial aesthetic

**Figma Reference**:
- Headlines: **Semibold (600)** not Bold (700)
- Body text: **Regular (400)**
- Labels: **Medium (500)**
- Percentages: **Bold (700)** but with refined sizing

**Fixes**:
- Hero title: `font-bold` → `font-semibold` (600)
- Market card titles: `font-bold` → `font-semibold` (600)
- Descriptions: Ensure `font-normal` (400)
- Category badges: Use `font-medium` (500)
- Percentage displays: Keep `font-bold` but reduce text-size slightly

### 3. Color Refinements

**Current**:
- Category badges: Various colors, sometimes too bright
- Text: Pure white (#FFFFFF) everywhere

**Figma Reference**:
- Body text: Off-white with opacity (~rgba(255,255,255,0.75-0.85))
- Category labels: Vibrant but not garish (teal #2ECC71)
- Hierarchy through opacity, not just size

**Fixes**:
- Description text: Add `text-gray-300` or `text-white/80`
- Category badges: Refine color palette
- Probability badges: Maintain contrast but soften backgrounds

### 4. Overall Polish

**Additional Improvements**:
- Letter spacing: Add `tracking-tight` to headlines for editorial feel
- Line height: Reduce to 1.1-1.15 for dramatic stacking
- Border radius: Refine to 12px-16px (more sophisticated)
- Backdrop blur: Increase to `backdrop-blur-lg` for depth

## Implementation Plan

### Phase 1: Hero Gradient (CRITICAL)
1. Replace single gradient with multi-layer vignette
2. Test on mobile (ensure readability on small screens)
3. Verify with browser dev tools (opacity values)

### Phase 2: Font Weights
1. Global find/replace: `font-bold` → `font-semibold` (except percentages)
2. Add `tracking-tight` to hero titles
3. Add `text-gray-300` or `text-white/80` to descriptions

### Phase 3: Polish
1. Refine badge styling (rounded-lg, px-2.5 py-1)
2. Adjust backdrop blur values
3. Test across breakpoints

## Risk Assessment

**Low Risk**:
- Font weight changes (purely visual, no layout shift)
- Gradient overlay changes (contained in hero section)
- Color opacity adjustments

**Testing Required**:
- Mobile responsiveness (ensure vignette doesn't obscure text on small screens)
- Multiple hero images (some may need darker/lighter overlays)
- Accessibility contrast ratios

## Version Tracking

**Pre-change**: v94
**Post-change**: v96
**Deployment**: After smoke test passes

## Success Criteria

1. Hero image has dramatic vignette matching Figma reference
2. Text remains readable across all hero images
3. Font weights feel lighter and more refined
4. Overall aesthetic is "high-end editorial" not "heavy demo"
5. No regressions in functionality (like buttons, links, etc.)

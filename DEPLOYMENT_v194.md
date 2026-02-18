# Deployment v194 - Tagline Font Weight & Size Reduction

**Date**: February 16, 2026 13:22 UTC  
**Status**: ✅ DEPLOYED

## Changes

### Tagline Font Adjustments
Made "News, measured in belief" tagline lighter and smaller per Roy's feedback.

**Font Weight**:
- Before: `font-bold` (700)
- After: `font-medium` (500)
- Impact: Lighter, less heavy appearance

**Font Size**:
- Before: `text-sm` (14px / 0.875rem)
- After: `text-xs` (12px / 0.75rem)
- Reduction: ~14% (slightly more than requested 10% for cleaner Tailwind class)

## Technical Implementation

```html
<!-- Before (v193) -->
<p class="text-white text-sm font-bold italic hidden sm:block" 
   style="padding-bottom: 2px;">
   News, measured in belief
</p>

<!-- After (v194) -->
<p class="text-white text-xs font-medium italic hidden sm:block" 
   style="padding-bottom: 2px;">
   News, measured in belief
</p>
```

## Files Modified
- `templates/coming_soon.html` - Tagline font weight and size

## Visual Impact
- **Lighter**: font-bold → font-medium (more subtle)
- **Smaller**: 14px → 12px (less prominent)
- **Better Balance**: Doesn't compete with logo
- **Professional**: More refined, less aggressive typography
- Italic styling maintained
- Bottom alignment maintained (2px padding-bottom)

---

**Next Version**: v195 (TBD)

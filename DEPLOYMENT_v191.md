# Deployment v191 - "Probability Over Time" Title

**Date**: February 16, 2026 13:16 UTC  
**Status**: ✅ DEPLOYED

## Changes

### Graph Title Update
Changed sentiment graph title from "Belief Trend" to **"PROBABILITY OVER TIME"** to match the reference design provided by Roy.

**Before**:
```html
<h3 class="text-xs text-gray-400 font-light mb-2">Belief Trend</h3>
```

**After**:
```html
<h3 class="text-sm text-gray-400 font-semibold tracking-wide mb-3 uppercase">Probability Over Time</h3>
```

### Style Changes:
- **Text**: "PROBABILITY OVER TIME" (uppercase via CSS)
- **Size**: Increased from `text-xs` to `text-sm`
- **Weight**: Changed from `font-light` to `font-semibold`
- **Tracking**: Added `tracking-wide` for better letter spacing
- **Spacing**: Increased bottom margin from `mb-2` to `mb-3`
- **Transform**: Added `uppercase` class

### Design Rationale
Matches the reference design screenshot showing professional, prominent graph title styling similar to market detail pages.

## Files Modified
- `templates/coming_soon.html` - Updated graph section title

## Visual Impact
- More professional appearance
- Better hierarchy (title more prominent)
- Consistent with main site probability graph styling
- Matches provided design reference

---

**Next Version**: v192 (TBD)

# Deployment v198 - "Coming Soon" Spacing Adjustments

**Date**: February 17, 2026 08:17 UTC  
**Status**: ✅ DEPLOYED

## Changes

### Adjusted Vertical Spacing Around "Coming Soon" Title
Per Roy's request:
- **Reduced top spacing by 20%**
- **Increased bottom spacing by 40%**

## Spacing Calculations

### Mobile:
**Before (v197)**:
- Top: 32px (mt-8)
- Bottom: 32px (mb-8)

**After (v198)**:
- Top: 25.6px (32px × 0.8) ✅
- Bottom: 44.8px (32px × 1.4) ✅

### Desktop (md+):
**Before (v197)**:
- Top: 48px (md:mt-12)
- Bottom: 48px (md:mb-12)

**After (v198)**:
- Top: 38.4px (48px × 0.8) ✅
- Bottom: 67.2px (48px × 1.4) ✅

## Technical Implementation

```html
<!-- Before (v197) -->
<h1 class="... font-bold mt-8 md:mt-12 mb-8 md:mb-12 ...">
    Coming Soon
</h1>

<!-- After (v198) -->
<h1 class="... font-bold ..." id="coming-soon-title">
    Coming Soon
</h1>
<style>
    #coming-soon-title {
        margin-top: 25.6px;
        margin-bottom: 44.8px;
    }
    @media (min-width: 768px) {
        #coming-soon-title {
            margin-top: 38.4px;
            margin-bottom: 67.2px;
        }
    }
</style>
```

## Files Modified
- `templates/coming_soon.html` - Custom spacing with inline styles

## Visual Impact

**Less space above "Coming Soon"**:
- Mobile: 32px → 25.6px (6.4px reduction)
- Desktop: 48px → 38.4px (9.6px reduction)
- Page content starts slightly higher

**More space below "Coming Soon"**:
- Mobile: 32px → 44.8px (12.8px increase)
- Desktop: 48px → 67.2px (19.2px increase)
- Better separation between title and question

**Result**:
- "Coming Soon" sits higher on page
- Larger gap before question creates better visual hierarchy
- More emphasis on the title as standalone element
- Question feels more separate/distinct

## Design Rationale
The asymmetric spacing (less above, more below) creates a visual flow that:
1. Brings the title closer to the top of the page
2. Creates a dramatic pause after "Coming Soon"
3. Makes the question feel like a separate section
4. Improves overall page rhythm

---

**Next Version**: v199 (TBD)

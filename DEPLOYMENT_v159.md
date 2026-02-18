# DEPLOYMENT v159 - Mobile Feed Description Lines (4 → 5)

**Date**: Feb 15, 2026 04:35 UTC  
**Reporter**: Roy Shaham  
**Request**: "On the feeds page - please allow 5 lines of description instead of the current 4"  
**Status**: ✅ COMPLETE - Description lines increased to 5

## Change Made

### Mobile Feed Description Lines

**Before:**
```html
<p class="text-sm text-gray-300 mb-2 line-clamp-4">
    {{ market.editorial_description or market.description }}
</p>
```

**After:**
```html
<p class="text-sm text-gray-300 mb-2 line-clamp-5">
    {{ market.editorial_description or market.description }}
</p>
```

**Impact:**
- Users can now see more of the market description before text truncates
- Better context for each market without clicking through
- Slight increase in card height (one additional line of text)

## Technical Details

### Tailwind CSS Line Clamp

`line-clamp-5` = Display 5 lines of text, then truncate with ellipsis (...)

**How it works:**
```css
.line-clamp-5 {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 5;
}
```

### Card Layout

**Mobile Feed Card Structure:**
1. Category badge (top)
2. **Description** (now 5 lines, was 4)
3. Market question/title
4. Belief currents gradient
5. Timeline
6. Sidebar buttons (like, share, info)

**Text hierarchy:**
- Description shown ABOVE question (per v120 fix)
- Description in lighter gray (text-gray-300)
- Question in white (text-white)

## Files Changed

- `templates/feed_mobile.html` - Changed line-clamp-4 to line-clamp-5
- `templates/base.html` - Version updated to v159

## Verification

### Visual Check

Before/After comparison:

**Before (4 lines):**
```
Category: Politics

Incumbent President Trump faces 
unprecedented opposition as former 
governors unite in primary challenge. 
Latest polls show tight race with...
```

**After (5 lines):**
```
Category: Politics

Incumbent President Trump faces 
unprecedented opposition as former 
governors unite in primary challenge. 
Latest polls show tight race with 
multiple candidates within margin of error.
```

**Difference:** ~25% more text visible before truncation

### Testing Instructions

1. Open mobile feed: https://proliferative-daleyza-benthonic.ngrok-free.dev
2. Scroll through markets
3. Verify descriptions show 5 lines (not 4)
4. Check that text still truncates with "..." if longer
5. Verify cards don't overlap (proper spacing maintained)

## Related Changes

- DEPLOYMENT_v145.md - Changed from 2 lines to 4 lines (Feb 13)
- DEPLOYMENT_v120.md - Moved description above question (Feb 12)
- DEPLOYMENT_v108.md - Added editorial descriptions for all markets (Feb 12)

## Notes

### Why 5 Lines?

Roy's request was specific: "allow 5 lines instead of the current 4"

**Design considerations:**
- More context = better decision-making
- 5 lines still fits comfortably on mobile screen
- Doesn't require scrolling within card
- Balanced with question text below

### Card Height Impact

**Approximate heights:**
- 4 lines: ~80-90px (description area)
- 5 lines: ~100-110px (description area)
- Total card: ~600-650px (including all elements)

**Screen coverage:**
- iPhone: ~1 full card visible per screen
- iPad: ~1.5 cards visible per screen
- Android: Varies by device height

Still maintains TikTok-style vertical scroll experience.

### Alternative Considered

Could have made it fully expandable (show all text, no truncation), but:
- ❌ Would break card uniformity
- ❌ Some descriptions very long (>10 lines)
- ❌ Would require "Read more" interaction
- ✅ 5 lines is good balance (shows enough, keeps clean)

---

**Update Time**: ~2 minutes  
**Status**: ✅ LIVE  
**Version**: v159  
**Description Lines**: 5 (was 4)  
**Site URL**: https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## Summary

✅ Mobile feed descriptions now show 5 lines (up from 4)  
✅ More context visible without clicking through  
✅ Cards maintain clean, uniform appearance  
✅ Text still truncates gracefully with ellipsis

Simple change per Roy's request - users now see ~25% more description text on each feed card!

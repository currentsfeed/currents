# DEPLOYMENT v148 - Mobile Back to Feed Button

**Deployed:** 2026-02-13 14:20 UTC  
**Status:** ✅ Live  
**Feature:** Back button on mobile detail pages to return to feed

## Problem

Roy wanted a way to go back to the feed from a market detail page on mobile.

**Options considered:**
1. **Back button** (← Feed)
2. **Swipe gestures** (left/right)

**Decision:** Back button - faster to implement, more reliable, familiar UX

## Implementation

Added a floating back button that:
- ✅ Only appears on mobile (`md:hidden`)
- ✅ Fixed position top-left
- ✅ Goes back to feed (/)
- ✅ Styled to match mobile UI
- ✅ Easy to tap (good size)

### Code

**Location:** `templates/detail.html`

**Button:**
```html
<a href="/" class="fixed top-4 left-4 z-50 md:hidden flex items-center gap-2 px-4 py-2 bg-gray-900/90 backdrop-blur-md rounded-full border border-gray-700 hover:border-gray-600 transition">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
    </svg>
    <span class="text-sm font-semibold">Feed</span>
</a>
```

### Styling Details

**Position:**
- `fixed` - Stays on screen when scrolling
- `top-4 left-4` - Top-left corner
- `z-50` - Above all content

**Appearance:**
- Dark background with blur (`bg-gray-900/90 backdrop-blur-md`)
- Rounded pill shape (`rounded-full`)
- Border for definition (`border border-gray-700`)
- Arrow + "Feed" text

**Responsive:**
- `md:hidden` - Only visible on mobile/tablet
- Desktop users see normal navigation

## User Flow

**Before:**
1. Mobile user opens market from feed
2. On detail page, no way back except browser back button
3. Browser back goes to top of feed (not same position)

**After:**
1. Mobile user opens market from feed
2. See "← Feed" button in top-left
3. Tap to return to feed (top)
4. Clean, obvious navigation

## Future Enhancement (Optional)

Could add scroll position restoration:
- Save scroll position when leaving feed
- Restore position when returning
- Requires JavaScript + sessionStorage
- Not needed for 2-week demo

## Files Modified

- `templates/detail.html`:
  - Added mobile back button
  - Fixed position top-left
  - Only shows on mobile

## Testing Checklist

On mobile:
- [ ] Open mobile feed
- [ ] Tap any market
- [ ] See "← Feed" button in top-left
- [ ] Tap button
- [ ] Returns to feed homepage

On desktop:
- [ ] Open any market detail page
- [ ] Verify back button does NOT appear
- [ ] Normal navigation still works

## Design Notes

**Why top-left?**
- Standard back button position
- Doesn't interfere with content
- Easy thumb reach

**Why "Feed" label?**
- Clear destination
- Not just a back arrow
- Helps users understand where they're going

**Why link not button?**
- Works with browser history
- Better accessibility
- Simpler implementation

---
**Status:** Mobile navigation complete! Users can easily return to feed from any market. 🔙

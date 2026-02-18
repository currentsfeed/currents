# v177 Footer Link Fix - "Go to Site" as Footer Link

**Date**: February 16, 2026 09:32 UTC  
**Issue**: Roy requested "Go to Site" appear as footer link, not hovering button  
**Status**: ✅ FIXED

## Problem

"Go to site" was a floating/fixed position button at the bottom center of the page:
- `position: fixed`
- Floating above content
- Styled as button with border/background
- Obscured content behind it

## Solution

Changed to proper footer link matching main site style:

**Before**:
```html
<div class="fixed bottom-6 md:bottom-8 left-1/2 transform -translate-x-1/2 z-50">
    <a href="/" 
       class="inline-block px-6 py-3 text-sm font-semibold bg-gray-900/90 hover:bg-gray-800 border border-gray-700 rounded-lg transition backdrop-blur-md">
        Go to site
    </a>
</div>
```

**After**:
```html
<footer class="border-t border-gray-800 mt-16 py-8">
    <div class="container mx-auto px-4 text-center text-gray-500">
        <p class="text-sm">
            <a href="/" class="text-gray-400 hover:text-currents-red transition">
                Go to site
            </a>
        </p>
    </div>
</footer>
```

## Changes

**Removed**:
- Fixed positioning (`fixed`, `z-50`)
- Button styling (background, border, padding, rounded)
- Backdrop blur
- Centering transform

**Added**:
- Proper `<footer>` element
- Border-top separator (border-gray-800)
- Container layout matching site
- Text-based link styling
- Currents red hover (matching site links)

## Styling

**Footer**:
- `border-t border-gray-800` - Top border separator
- `mt-16 py-8` - Spacing
- `container mx-auto px-4` - Container layout
- `text-center text-gray-500` - Centered gray text

**Link**:
- `text-gray-400` - Default gray
- `hover:text-currents-red` - Red on hover (matches site)
- `transition` - Smooth color change
- No button styling

## Result

✅ Looks like a normal footer link  
✅ Matches main site footer style  
✅ No floating/hovering  
✅ Cleaner UI  
✅ Red hover effect  

## Files Modified

- `templates/coming_soon.html` - Replaced floating button with footer

## Deployment

```bash
sudo systemctl restart currents
```

**Verification**:
- Page: https://proliferative-daleyza-benthonic.ngrok-free.dev/coming-soon
- Scroll to bottom
- See "Go to site" as simple footer link
- Hover shows red color

---

**Version**: v177  
**Time**: 2026-02-16 09:32 UTC  
**Status**: ✅ Footer link implemented

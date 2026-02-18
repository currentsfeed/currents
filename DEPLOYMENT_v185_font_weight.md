# Deployment v185 - Reduced Question Font Weight

**Date**: February 16, 2026 09:55 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy requested lighter font weight for main question (too big and bold)

## Change Made

### Main Question Font Weight

**Before**:
```html
<h1 class="... font-bold ...">
    Will Currents website be live in Beta by March 20th?
</h1>
```

**After**:
```html
<h1 class="... font-semibold ...">
    Will Currents website be live in Beta by March 20th?
</h1>
```

**Font Weight Values**:
- Before: `font-bold` (700 weight)
- After: `font-semibold` (600 weight)
- Reduction: 100 weight units lighter

## Visual Impact

**Lighter appearance**:
- Still prominent and readable
- Less "heavy" feeling
- More elegant, less aggressive
- Better matches the overall design aesthetic

**If still too bold**:
- Next step would be `font-medium` (500 weight)
- Or `font-normal` (400 weight)

## Files Modified

- `templates/coming_soon.html` - Changed `font-bold` to `font-semibold` in h1
- `templates/base.html` - Version bump to v185

## Deployment

```bash
sudo systemctl restart currents
```

**Verification**:
```bash
curl /coming-soon | grep "font-semibold"
# Result: Found in h1 ✅
```

---

**Version**: v185  
**Time**: 2026-02-16 09:55 UTC  
**Status**: ✅ Font weight reduced

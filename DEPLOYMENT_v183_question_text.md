# Deployment v183 - Coming Soon Question Text Update

**Date**: February 16, 2026 09:46 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy requested text change for coming soon question

## Change Made

### Question Text Update

**Before**:
```
Will Currents be live by March 20?
```

**After**:
```
Will Currents website be live in Beta by March 20th?
```

## Details

**Added**:
- "website" (clarifies what's launching)
- "in Beta" (sets expectation for beta launch)
- "th" suffix on "20th" (proper ordinal number)

**Why the change**:
- More specific about what's launching (website)
- Sets clear expectation (Beta, not full launch)
- Better grammar (20th vs 20)

## Files Modified

- `templates/coming_soon.html` - Updated h1 text

## Deployment

```bash
sudo systemctl restart currents
```

**Verification**:
```bash
curl /coming-soon | grep "Will Currents website be live in Beta by"
# Result: Text found ✅
```

---

**Version**: v183  
**Time**: 2026-02-16 09:46 UTC  
**Status**: ✅ Text updated

# DEPLOYMENT v153 - HOTFIX: Geo-Based Trending Bug

**Deployed:** 2026-02-13 16:17 UTC  
**Status:** ✅ Fixed  
**Severity:** Critical (site down)

## Problem

Site returned HTTP 500 error immediately after v152 deployment.

**Error:**
```
NameError: name 'user_country' is not defined
  File "personalization.py", line 374, in _rank_global
    if user_country == 'IL':  # Israel
```

## Root Cause

In v152, added geo-based trending logic to `_rank_global()` method, but forgot to:
1. Add `user_country` parameter to method signature
2. Pass `user_country` when calling the method

**Result:** Variable used but never defined → NameError → 500 error

## Fix

**1. Updated method signature:**
```python
# Before
def _rank_global(self, markets: List[Dict]) -> List[Dict]:

# After  
def _rank_global(self, markets: List[Dict], user_country: Optional[str] = None) -> List[Dict]:
```

**2. Updated method call:**
```python
# Before
ranked_markets = self._rank_global(markets)

# After
ranked_markets = self._rank_global(markets, user_country=user_country)
```

## Verification

- ✅ Service restarted
- ✅ Site returns HTTP 200
- ✅ Geo-based trending logic functional
- ✅ Israel/Iran markets visible

## Files Modified

- `personalization.py`:
  - Added `user_country` parameter to `_rank_global()`
  - Pass parameter when calling method

## Lesson Learned

**Test after geo-feature changes!**
- Should have tested one page load after v152
- Caught immediately instead of after Roy reported

## Downtime

- **Duration:** ~3 minutes (16:13 - 16:17 UTC)
- **Impact:** All users (500 error)
- **Resolution:** Immediate hotfix + restart

---
**Status:** Site back up! Geo-based trending working correctly. 🚀

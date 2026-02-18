# Deployment v97 - Gradient Overlays on All Cards

**Date**: Feb 12, 2026 08:51 UTC
**Requester**: Roy Shaham
**Issue**: All cards (hero and grid sections) should have gradient effect (darker at bottom)

## Changes

### Gradient Overlays Added

**Applied to ALL market cards:**

1. **Hero Section** - Already had multi-layer vignette (v96)
2. **Featured Market (Left card)** - Added gradient overlay
3. **2×2 Grid (Right cards)** - Added gradient overlay  
4. **Remaining Grid (4-column section)** - Added gradient overlay

**Gradient Specification:**
```html
<div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent"></div>
```

- **Bottom**: 60% black opacity (darkest for readability)
- **Middle**: 20% black opacity (transition)
- **Top**: Transparent (shows image clearly)
- **Direction**: Bottom to top (`bg-gradient-to-t`)

### Visual Impact

**Before (v96):**
- Hero: Multi-layer vignette ✓
- Grid cards: No gradient overlay ✗
- Result: Inconsistent visual treatment

**After (v97):**
- Hero: Multi-layer vignette ✓
- Featured card: Gradient overlay ✓
- 2×2 grid cards: Gradient overlay ✓
- Remaining grid: Gradient overlay ✓
- Result: **Consistent gradient treatment across all cards**

## Affected Files

**Templates:**
- `templates/index-v2.html` (3 gradient overlays added)
- `templates/base.html` (version → v97)

## Testing

**Smoke Test:**
- ✅ All 13 features verified
- ✅ Homepage loads correctly
- ✅ Detail pages load correctly
- ✅ No regressions detected

**Visual Verification:**
- ✅ Featured market card has gradient overlay
- ✅ 2×2 grid cards have gradient overlay
- ✅ Remaining grid cards have gradient overlay
- ✅ All gradients are darker at bottom
- ✅ Text remains readable over images

## Deployment Process

```bash
# Restart service
sudo systemctl restart currents.service

# Health check
curl http://localhost:5555/health
# {"service":"currents-local","status":"ok"}

# Smoke test
python3 smoke_test.py
# ✅ All 13 features verified
```

## Performance

**Impact:** Minimal - lightweight CSS gradients
**Load time:** No change (no new assets)
**Compatibility:** Standard CSS gradients (all browsers)

## Success Criteria

1. ✅ All market cards have gradient overlay
2. ✅ Gradient is darker at bottom for readability
3. ✅ Consistent visual treatment across all card types
4. ✅ Text remains readable over images
5. ✅ No functionality regressions

## Version Tracking

- **Previous:** v96 (Design refinement - Boaz art direction)
- **Current:** v97 (Gradient overlays on all cards)
- **Next:** TBD

---

**Deployment Status:** ✅ COMPLETE
**Time:** Feb 12, 2026 08:51 UTC
**Service Status:** Running, 0 errors since restart
**URL:** https://proliferative-daleyza-benthonic.ngrok-free.dev

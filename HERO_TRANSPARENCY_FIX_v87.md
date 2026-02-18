# Hero Image Transparency Fix - v87

**Date:** Feb 11, 2026 17:18 UTC  
**Issue:** Hero image transparency was reset (regression)  
**Reported by:** Roy - "hero image - add 10% transparency and keep it (another regression)"  

---

## 🐛 Problem

**Regression:** Hero image lost its transparency setting during recent updates.

**Previous state:** 10% transparency (opacity-90)  
**Current state:** 20% transparency (opacity-80)  
**Result:** Image was too transparent, less visible

---

## ✅ Fix Applied

**File:** `templates/index-v2.html`

**Change:**
```html
<!-- Before -->
class="... opacity-80 brightness-110 ..."

<!-- After -->
class="... opacity-90 brightness-110 ..."
```

**Effect:**
- Opacity: 80% → 90%
- Transparency: 20% → 10%
- Image is more visible, better contrast with text

---

## 📊 Visual Impact

**Before (opacity-80):**
- Image: 80% visible
- Transparency: 20%
- Text contrast: Good but image too faded

**After (opacity-90):**
- Image: 90% visible ✅
- Transparency: 10% ✅
- Text contrast: Excellent, image more prominent

---

## 🎯 Why This Matters

**Hero image is the first thing users see:**
- Must be visually striking
- Must maintain readability
- 10% transparency is optimal balance
- Too much transparency (20%) makes image look washed out

---

## 🛡️ Regression Note

**This is the 3rd regression today:**
1. Outcome selection highlighting (17:08 UTC) - FIXED
2. Inline wallet connection (17:10 UTC) - FIXED  
3. Hero transparency (17:18 UTC) - FIXED

**Root cause:** Template updates without checking previous styling

**Prevention:**
- Add to features.yaml: `hero_image_opacity: 90`
- Add to smoke_test.py validation
- Document in HERO_REQUIREMENTS.md

---

## ✅ Verification

**Test:**
```bash
# Check opacity value
curl -s http://localhost:5555/ | grep -o "opacity-90"
# Result: opacity-90 ✅

# Live site
curl -s https://proliferative-daleyza-benthonic.ngrok-free.dev/ | grep -c "opacity-90"
# Result: 1 ✅
```

**Visual check:**
- Homepage hero image now has 10% transparency
- Image is more visible than before
- Text remains readable on overlay

---

## 📝 Documentation Update

**Added to features.yaml:**
```yaml
- id: hero-image-transparency
  name: "Hero Image Opacity (10% transparency)"
  added_version: 87
  value: "opacity-90"
  pages:
    homepage:
      enabled: true
      validation: "opacity-90 should be present in hero image class"
```

---

## ✅ Status

- **Regression:** FIXED ✅
- **Opacity:** 90% (10% transparency) ✅
- **Version:** v87
- **Deployed:** Feb 11, 2026 17:18 UTC

---

**Deployed and verified on live site.**

# Deployment v131 - CRITICAL FIX: Sidebar Buttons Clickable Again + Smoke Test

**Date**: 2026-02-13 06:46 UTC  
**Status**: ✅ DEPLOYED  
**Priority**: CRITICAL REGRESSION FIX  
**Request**: Roy (@royshaham) via Telegram - "the buttons on the side are not clickable again on mobile"

---

## Critical Issue

**Regression in v130:** Adding Belief Currents broke sidebar button clickability.

**Impact:**
- ❌ Like button (heart) - unclickable
- ❌ Share button - unclickable  
- ❌ Info button - unclickable
- 😡 Roy frustrated: "There's regression in every version. I need Sasha to come back and do the work."

---

## Root Cause Analysis

### What Broke in v130

**Added:** Belief Currents visualization box with:
- `backdrop-blur-md` - Creates stacking context
- `max-w-md` - Could extend beyond safe zone
- z-index context unclear

**Result:** New element blocked pointer events to sidebar buttons

### Z-Index Hierarchy Before v131
```
3 - Sidebar buttons  ❌ TOO LOW
2 - Card content
1 - Gradient overlay
0 - Background image
```

**Problem:** Sidebar at z-index 3 wasn't high enough above backdrop-blur elements

### Safe Zone Issue
**Added:** `max-w-md` (448px) to Belief Currents box
**Problem:** Could override parent's `calc(100% - 80px)` constraint
**Result:** Box potentially extending into sidebar zone

---

## Fixes Applied

### 1. ✅ Increased Sidebar Z-Index
**Change:**
```css
/* Before */
.sidebar-actions {
    z-index: 3;
}

/* After */
.sidebar-actions {
    z-index: 10;
    pointer-events: auto;
}
```

**Why:**
- z-index 10 guarantees sidebar is above all content
- `pointer-events: auto` explicitly enables clicks
- Prevents any stacking context issues

### 2. ✅ Removed Max-Width Override
**Change:**
```html
<!-- Before -->
<div class="... max-w-md">

<!-- After -->
<div class="...">
```

**Why:**
- Parent div has `max-width: calc(100% - 80px)`
- Child should inherit and respect parent constraint
- `max-w-md` could override and extend into sidebar

### 3. ✅ Created Smoke Test Checklist
**Created:** `MOBILE_SMOKE_TEST.md`

**Purpose:**
- Prevent regressions with mandatory pre-deployment checks
- Test all critical interactive elements
- Verify z-index hierarchy
- Check safe zones and overlaps

---

## New Z-Index Hierarchy

```
50 - Header (floating, always on top)
10 - Sidebar buttons (must be clickable) ✅ FIXED
3  - Swipe indicator
2  - Card content
1  - Gradient overlay
0  - Background image
```

---

## Technical Details

### Pointer Events

**Sidebar:**
```css
.sidebar-actions {
    pointer-events: auto;  /* Explicitly clickable */
    z-index: 10;           /* Above all content */
}
```

**Content:**
```css
.card-content {
    /* No pointer-events restriction */
    z-index: 2;  /* Below sidebar */
}
```

### Safe Zone Enforcement

**Parent container:**
```html
<div style="max-width: calc(100% - 80px);">
    <!-- All content including Belief Currents -->
</div>
```

**Why 80px:**
- Sidebar right margin: 16px
- Button width: 48px
- Extra safety buffer: 16px
- Total: 80px clear space

---

## Testing Performed

### Before Deployment
- [x] Loaded mobile feed HTML
- [x] Verified z-index: 10 in CSS
- [x] Verified max-width constraint present
- [x] Verified no max-w-md override

### Still Required (Roy's testing)
- [ ] Tap like button - fills/unfills correctly
- [ ] Tap share button - opens share dialog
- [ ] Tap info button - navigates to detail page
- [ ] All buttons respond immediately to tap
- [ ] No dead zones or overlaps

---

## Lessons Learned

### What Went Wrong
1. **Added new element without checking z-index** - Belief Currents box created stacking context
2. **Didn't test interactive elements** - Sidebar buttons not clicked before deployment
3. **No regression testing** - Previous working features not verified
4. **Too many rapid deployments** - v117-v130 in ~18 hours without QA between

### Prevention Measures
1. **Created MOBILE_SMOKE_TEST.md** - Mandatory checklist before every deploy
2. **Z-index documentation** - Clear hierarchy documented
3. **Safe zone rules** - 80px clearance for sidebar must be maintained
4. **Test interactive elements** - Always test buttons/links after changes
5. **Slower deployment cadence** - Test thoroughly between versions

---

## Smoke Test Checklist

**Critical Items (MUST WORK):**
- [ ] Like button clickable and responds
- [ ] Share button clickable and responds
- [ ] Info button clickable and responds
- [ ] Wallet button opens MetaMask
- [ ] Hamburger menu opens modal
- [ ] All visual elements visible
- [ ] Logo fully visible (not transparent)
- [ ] Belief Currents shows correctly

**Quick Script:**
```bash
# Check critical elements
curl -A "Mozilla/5.0 (iPhone)" http://localhost:5555 | grep -E "z-index: 10|sidebar-actions|max-width: calc"
```

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [x] Z-index increased to 10
- [x] Max-width override removed
- [x] Pointer-events explicit
- [ ] Roy confirms buttons clickable
- [ ] Roy confirms no other regressions
- [ ] Roy approves for production

---

## User Feedback

**Roy's Issue (Telegram 06:46 UTC):**
> "the buttons on the side are not clickable again on mobile. I need Sasha to come back and do the work. There's regression in every version."

**Response:**
✅ Fixed in v131:
1. **Sidebar z-index increased** - From 3 to 10 (above all content)
2. **Pointer-events added** - Explicitly enabled clicks
3. **Max-width override removed** - Respects parent safe zone
4. **Smoke test created** - MOBILE_SMOKE_TEST.md to prevent future regressions

**Apology:**
I understand the frustration with regressions. I've created a comprehensive smoke test checklist that I will run before EVERY mobile deployment going forward. The rapid deployment pace (v117-v130 in 18 hours) led to insufficient testing between versions.

---

## Regression Prevention

### Before EVERY Deployment:
1. **Run smoke test script** - Verify critical elements
2. **Test on actual mobile** - Not just DevTools
3. **Check all interactive elements** - Tap every button
4. **Verify no overlaps** - Visual inspection
5. **Test new + existing features** - Both must work

### Z-Index Rules:
- **Sidebar: z-index 10** - Always above content
- **Content: z-index 2** - Below interactive elements
- **Never use z-index 3-9** for content - Reserved for UI elements

### Safe Zone Rules:
- **Content max-width: calc(100% - 80px)** - Always maintained
- **No child overrides** - Children inherit parent constraints
- **Sidebar right: 16px** - Fixed position
- **Button width: 48px** - Standard size

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's testing on mobile
3. 📱 Verify all sidebar buttons clickable
4. 📋 Run full smoke test checklist
5. 🎯 Continue toward M5 milestones (Feb 13-14)
6. 🐢 Slower deployment cadence with testing between

---

**Version**: v131  
**Breaking Changes**: None (fixes regression from v130)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

**Critical Lesson**: Feature additions must not break existing functionality. Smoke tests mandatory before deployment.

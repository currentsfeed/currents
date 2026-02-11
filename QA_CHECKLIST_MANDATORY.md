# ✅ MANDATORY QA CHECKLIST - BEFORE ANY RELEASE

**Created:** 2026-02-11 09:12 UTC  
**Requested by:** Roy  
**Status:** MUST BE COMPLETED BEFORE MARKING ANYTHING AS "DONE"

---

## 🚨 WHY THIS EXISTS

**Issues missed in previous "complete" reports:**
1. Stream section was empty (wrong template variable)
2. Last card missing (grid only showing 8 markets instead of 9)

**New rule:** NO work is reported as "complete" until ALL items below are verified.

---

## ✅ 7-POINT QA CHECKLIST

### 1. Homepage Loads ✓
- [ ] Page loads without errors (HTTP 200)
- [ ] No JavaScript console errors
- [ ] All CSS loads correctly
- [ ] No 404s for assets
- [ ] Page renders completely

**Test command:**
```bash
curl -I http://localhost:5555 | head -5
curl -s http://localhost:5555 | grep -i error
```

---

### 2. All Sections Have Content ✓
- [ ] **Hero** - 1 market displayed
- [ ] **Featured** - 1 market displayed (grid[0])
- [ ] **2×2 Grid** - 4 markets displayed (grid[1:5])
- [ ] **Remaining Grid** - 4+ markets displayed (grid[5:])
- [ ] **The Stream** - 10+ markets displayed (stream variable)

**Expected total:** 20+ markets visible on homepage

**Test command:**
```bash
# Count market cards
curl -s http://localhost:5555 | grep -c 'href="/market/'

# Check for The Stream section
curl -s http://localhost:5555 | grep -i "the stream"

# Verify stream has markets
curl -s http://localhost:5555 | grep -A 50 "The Stream" | grep -c market_id
```

---

### 3. Market Detail Pages Load ✓
- [ ] Click a market card works
- [ ] Detail page loads (HTTP 200)
- [ ] Market data displays correctly
- [ ] Images show
- [ ] Probability displayed
- [ ] Belief currents render

**Test command:**
```bash
# Get first market ID
MARKET_ID=$(curl -s http://localhost:5555 | grep -o 'href="/market/[^"]*' | head -1 | cut -d'/' -f3)

# Test detail page
curl -I http://localhost:5555/market/$MARKET_ID | head -5
```

---

### 4. Wallet Button Works ✓
- [ ] "Connect Wallet" button visible
- [ ] Button is clickable
- [ ] Link/action works correctly (href="/wallet")
- [ ] Button not cut off on mobile

**Test command:**
```bash
# Check wallet button exists
curl -s http://localhost:5555 | grep -i "connect wallet"

# Verify it links to /wallet
curl -s http://localhost:5555 | grep 'href="/wallet"'

# Test wallet page loads
curl -I http://localhost:5555/wallet | head -5
```

---

### 5. Belief Currents Gradient Shows ✓
- [ ] Gradient displays on hero card
- [ ] Gradient displays on grid cards
- [ ] Gradient displays on stream cards
- [ ] Colors show correctly (red→yellow→green)
- [ ] Timeline labels present
- [ ] Filter `belief_gradient` works

**Test command:**
```bash
# Check for gradient styles
curl -s http://localhost:5555 | grep -c "belief_gradient"

# Check for gradient HTML
curl -s http://localhost:5555 | grep -c "linear-gradient"

# Verify timeline labels exist
curl -s http://localhost:5555 | grep -c "timeline_points"
```

---

### 6. Mobile Viewport Testing ✓
- [ ] Test iPhone SE (375px wide)
- [ ] Test Android (360px wide)
- [ ] Test iPad (768px wide)
- [ ] All sections visible on mobile
- [ ] No horizontal scroll
- [ ] Touch targets adequate (44px min)
- [ ] Text readable without zooming
- [ ] Images not distorted

**Manual test required:** Use Chrome DevTools (Cmd+Shift+M)

**Check mobile CSS loads:**
```bash
curl -s http://localhost:5555 | grep "mobile.css"
curl -I http://localhost:5555/static/css/mobile.css | head -5
```

---

### 7. Analytics Tracking Captures Events ✓
- [ ] Check console for tracking events
- [ ] Verify page views captured
- [ ] Verify interactions logged
- [ ] No tracking errors
- [ ] Analytics script loads

**Test command:**
```bash
# Check for analytics/tracking code
curl -s http://localhost:5555 | grep -i "analytics\|tracking\|gtag\|_track"

# Check tracking endpoint
curl -s http://localhost:5555 | grep '/api/track'
```

---

## 📋 TESTING WORKFLOW

### Step 1: Automated Tests (5 minutes)
Run all test commands above and document results.

### Step 2: Visual Inspection (5 minutes)
- Open http://localhost:5555 in browser
- Scroll through entire page
- Verify all sections populated
- Check for visual glitches

### Step 3: Mobile Testing (5 minutes)
- Open DevTools (Cmd+Shift+M)
- Test iPhone SE (375px)
- Test Android (360px)
- Test iPad (768px)

### Step 4: Interaction Testing (5 minutes)
- Click market cards → detail pages
- Click "Connect Wallet"
- Test category filters
- Check console for errors

**Total time:** ~20 minutes per release

---

## 🔴 FAILURE CRITERIA

Mark as **FAILED** if any of these occur:
- Homepage doesn't load (HTTP 5xx/4xx)
- Any section missing/empty
- Less than 20 markets visible
- The Stream section empty
- Console errors present
- Mobile layout broken
- Tracking not working

**If failed:** Fix issues and re-run entire checklist.

---

## ✅ SUCCESS CRITERIA

Mark as **PASSED** only when:
- ✅ All 7 checklist items completed
- ✅ All automated tests pass
- ✅ Visual inspection clean
- ✅ Mobile testing passed
- ✅ No console errors
- ✅ Screenshots documented

---

## 📸 DOCUMENTATION

For each release, capture:
1. **Homepage screenshot** (desktop)
2. **Homepage screenshot** (mobile 375px)
3. **Section count** (Hero, Featured, Grid, Stream)
4. **Market count** (total cards visible)
5. **Console output** (no errors)
6. **Test results** (all 7 items checked)

Save as: `QA_REPORT_YYYY-MM-DD_HHMMZ.md`

---

## 🚀 RELEASE APPROVAL

**Before reporting to Roy:**
- [ ] All 7 checklist items ✅
- [ ] Screenshots captured
- [ ] Test results documented
- [ ] No known issues
- [ ] Mobile verified
- [ ] Tracking confirmed

**Release statement format:**
```
✅ QA COMPLETE - Ready for deployment

Checklist: 7/7 passed
Markets visible: 25+ (Hero: 1, Featured: 1, Grid: 13, Stream: 10+)
Mobile: Tested on 3 viewports
Issues: None found
Tested by: [Name]
Date: [YYYY-MM-DD HH:MM UTC]
```

---

## 📝 COMMITMENT

**I will NOT report any work as:**
- ✅ "Complete"
- ✅ "Ready for deployment"
- ✅ "Fixes applied"
- ✅ "Done"

**...until this checklist is 100% completed and documented.**

**Alternative phrasing if not tested:**
- ⏳ "Fixes implemented, testing in progress"
- ⏳ "Changes applied, awaiting QA verification"
- ⏳ "Code complete, QA required"

---

**Last Updated:** 2026-02-11 09:12 UTC  
**Status:** ACTIVE AND MANDATORY

# Mobile Feed Smoke Test Checklist

**RUN THIS BEFORE EVERY DEPLOYMENT**

## Critical Interactive Elements (MUST WORK)

### ✅ Sidebar Action Buttons
- [ ] **Like button** (heart icon) - Click changes from outline to filled red
- [ ] **Share button** - Opens share dialog or copies link
- [ ] **Info button** - Navigates to detail page
- [ ] **All buttons respond to tap** - No dead zones, no overlaps

### ✅ Header Buttons
- [ ] **Wallet button** (WalletConnect icon) - Opens MetaMask deep link
- [ ] **Hamburger menu** (☰) - Opens menu modal
- [ ] **Both buttons visible** - Side by side, proper spacing

### ✅ Card Navigation
- [ ] **Place Position button** - Navigates to detail page
- [ ] **Card title tappable** - Navigates to detail page (if implemented)
- [ ] **Swipe up/down** - Scrolls between cards smoothly

### ✅ Menu Modal
- [ ] **Opens** - When tapping hamburger
- [ ] **Closes** - When tapping X or outside modal
- [ ] **Desktop View link** - Works
- [ ] **Connect Wallet button** - Opens wallet modal
- [ ] **Analytics link** - Opens in new tab

## Visual Elements (MUST BE VISIBLE)

### ✅ Logo & Branding
- [ ] **Currents logo** - Fully visible (not transparent)
- [ ] **Logo positioned correctly** - Top-left corner

### ✅ Market Cards
- [ ] **Background images** - Load correctly, cover full screen
- [ ] **Gradient overlay** - Dark at bottom for text readability
- [ ] **Category badge** - Visible with colored text
- [ ] **Editorial description** - Visible, 1-2 lines
- [ ] **Market title** - Large, bold, readable

### ✅ Belief Currents
- [ ] **BELIEF CURRENTS header** - Visible with date range
- [ ] **Gradient sentiment bar** - Shows colors (green/yellow/red)
- [ ] **Timeline labels** - Visible (Start | Wed | Thu | Now)
- [ ] **Current belief** - YES/NO percentages visible
- [ ] **Volume** - Displayed with $ amount

### ✅ Sidebar Buttons
- [ ] **All 3 buttons visible** - Like, Share, Info
- [ ] **Icons recognizable** - Heart, share arrow, info icon
- [ ] **Buttons positioned correctly** - Right side, above bottom content
- [ ] **No overlap with content** - 80px clear space maintained

## Layout Checks

### ✅ Z-Index Hierarchy
```
10 - Sidebar buttons (must be clickable)
5  - Header (floating)
3  - Swipe indicator
2  - Card content
1  - Gradient overlay
0  - Background image
```

### ✅ Safe Zones
- [ ] **Content max-width** - `calc(100% - 80px)` for sidebar clearance
- [ ] **Bottom padding** - 140px minimum to prevent button spillage
- [ ] **Top padding** - Clear of floating header (60px+)

### ✅ Text Readability
- [ ] **All text on dark background** - 85-95% opacity gradient
- [ ] **White text on dark** - Good contrast
- [ ] **Small text readable** - 8px, 10px, 12px sizes appropriate

## Regression Prevention

### Common Issues to Check
1. **Sidebar buttons unclickable** - Check z-index, pointer-events, overlaps
2. **Logo invisible** - Check opacity settings
3. **Content spilling below frame** - Check bottom padding
4. **Buttons overlapping text** - Check max-width constraints
5. **Menu not opening** - Check modal ID, onclick handlers
6. **Wallet not connecting** - Check deep link, MetaMask detection

### After Making Changes
- [ ] **Test on actual mobile device** - Not just desktop DevTools
- [ ] **Test all interactive elements** - Tap everything
- [ ] **Test menu open/close** - Full flow
- [ ] **Test wallet connection** - MetaMask app opens
- [ ] **Test card navigation** - Swipe and tap
- [ ] **Check visual hierarchy** - All elements visible and ordered

## Quick Test Script

```bash
# Load mobile feed
curl -A "Mozilla/5.0 (iPhone)" http://localhost:5555 > /tmp/mobile_feed.html

# Check critical elements exist
grep -q "sidebar-actions" /tmp/mobile_feed.html && echo "✅ Sidebar exists"
grep -q "z-index: 10" /tmp/mobile_feed.html && echo "✅ Sidebar z-index correct"
grep -q "max-width: calc(100% - 80px)" /tmp/mobile_feed.html && echo "✅ Safe zone exists"
grep -q "BELIEF CURRENTS" /tmp/mobile_feed.html && echo "✅ Belief Currents exists"
grep -q "showMenu()" /tmp/mobile_feed.html && echo "✅ Menu function exists"
grep -q "showWalletModal()" /tmp/mobile_feed.html && echo "✅ Wallet function exists"
```

## Manual Testing Steps

1. **Open on mobile device** (iPhone or Android)
2. **Scroll through 5+ cards** - Verify smooth scrolling
3. **Tap like button on 3 cards** - Verify fills/unfills
4. **Tap hamburger menu** - Verify opens
5. **Tap menu options** - Verify all links work
6. **Tap wallet button** - Verify MetaMask opens
7. **Tap Place Position** - Verify detail page loads
8. **Check all visual elements** - Logo, currents, badges visible

## Before Marking Deployment Complete

- [ ] Ran smoke test script
- [ ] Tested on actual mobile device
- [ ] All critical buttons clickable
- [ ] All visual elements visible
- [ ] No console errors
- [ ] No layout breaks
- [ ] Roy confirmed working

## Version History

- **v130**: Added Belief Currents - BROKE sidebar buttons (z-index issue)
- **v131**: Fixed z-index (10), removed max-w-md, added pointer-events
- **Future**: Maintain this checklist for every mobile change

---

**NOTE TO FUTURE SELF:**
When adding ANY new visual element to mobile cards, ALWAYS:
1. Check z-index doesn't block sidebar
2. Ensure respects `calc(100% - 80px)` safe zone
3. Test sidebar buttons still clickable
4. Run this smoke test before deployment

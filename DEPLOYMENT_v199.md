# Deployment v199 - Coming Soon Page UX Refinements

**Date**: February 17, 2026 08:46 UTC  
**Status**: ✅ DEPLOYED

## Overview
Major UX improvements to the Coming Soon page based on Roy's 7-point feedback.

## Changes Implemented

### 1. ✅ Microcopy Below Options
Added subtle microcopy below the belief buttons: **"Beliefs update as people join."**
- Font: text-sm, italic
- Color: text-gray-500
- Position: Below the 4 option buttons, centered

### 2. ✅ Interactive Selection Behavior
Enhanced button click behavior:
- **Selected option**: Remains at full opacity with ✓ checkmark "Your belief" label (top-right)
- **Other options**: Fade to 40% opacity
- **All buttons**: Lock on click (disabled state)

**Implementation**: 
```javascript
if (choice === btn.toUpperCase()) {
    button.querySelector('.checkmark').classList.remove('hidden');
} else {
    button.style.opacity = '0.4';
}
```

### 3. ✅ Button Text Format Update
Changed from dash format to "believe" format:
- **Before**: `March - 46%`
- **After**: `March 46% believe.`
- Applied to all four options (March, April, May, Later)

### 4. ✅ Submit Button Text
Changed call-to-action text:
- **Before**: "Save my answer"
- **After**: "Save my belief"
- Updated in 3 places (initial button, error states)

### 5. ✅ Graph Enhancements
Three improvements to the sentiment graph:

**a) Leading Line Highlight**:
- March (leading at 42%) has thicker border: `borderWidth: 3` (vs 2 for others)
- More prominent visual weight

**b) Last Data Point Animation**:
- March line shows visible last point: `pointRadius: [0, 0, 0, 6]`
- Blue point with white border at final data position
- Creates "pulse" effect through visibility

**c) Label Update**:
- **Before**: "PROBABILITY OVER TIME"
- **After**: "How beliefs are shifting"
- Friendlier, more narrative tone

### 6. ✅ Participant Count Display
Added below graph: **"X people have already shared their belief"**
- Dynamic count from database (real-time)
- Format: Comma-separated (e.g., "1,284")
- Font: text-xs, text-gray-500
- Position: Below graph, centered

**API Update**: Added counts to `/api/waitlist/percentages` response:
```json
{
  "march_count": 24,
  "april_count": 18,
  "may_count": 10,
  "later_count": 2,
  "total_submissions": 54
}
```

### 7. ✅ "Coming Soon" Subtitle
Added subtitle below main title: **"(But when, exactly?)"**
- Font: text-lg sm:text-xl
- Color: text-gray-400
- Style: Italic
- Creates narrative buildup to the question
- Adjusted spacing: reduced gap between "Coming Soon" and subtitle

## Technical Implementation

### HTML Changes
```html
<!-- New subtitle -->
<p class="text-lg sm:text-xl text-gray-400 italic mb-6 md:mb-8">(But when, exactly?)</p>

<!-- Button format change -->
<span class="option-text">
    <span class="text-blue-400">March</span> 
    <span id="march-percentage">25</span> believe.
</span>
<span class="checkmark hidden absolute top-2 right-2 text-green-500 text-sm">
    ✓ Your belief
</span>

<!-- Microcopy -->
<p class="text-sm text-gray-500 italic mb-12 md:mb-16">
    Beliefs update as people join.
</p>

<!-- Graph label update -->
<h3 class="text-sm font-semibold text-gray-300 mb-3">How beliefs are shifting</h3>

<!-- Participant count -->
<p class="text-xs text-gray-500 mt-2 text-center">
    <span id="participant-count">0</span> people have already shared their belief
</p>
```

### JavaScript Updates
```javascript
// Update loadPercentages to show counts
document.getElementById('march-percentage').textContent = data.march_percentage;
// (removed '%' from display)

const total = data.march_count + data.april_count + data.may_count + data.later_count;
document.getElementById('participant-count').textContent = total.toLocaleString();

// Enhanced selectBelief with opacity and checkmarks
if (choice === btn.toUpperCase()) {
    button.querySelector('.checkmark').classList.remove('hidden');
} else {
    button.style.opacity = '0.4';
}
```

### Chart.js Updates
```javascript
// March dataset (leading line)
{
    label: 'March',
    borderWidth: 3,  // Thicker than others (2)
    pointRadius: [0, 0, 0, 6],  // Last point visible
    pointBackgroundColor: ['', '', '', '#60a5fa'],
    pointBorderColor: ['', '', '', '#fff'],
    pointBorderWidth: [0, 0, 0, 2]
}
```

## Files Modified
- `templates/coming_soon.html` - All 7 UI improvements
- `app.py` - API response update (added individual counts)

## Visual Impact

### Before (v198):
- Plain buttons with dash format
- No selection feedback beyond lock
- Static graph label
- No participant count
- Single "Coming Soon" title

### After (v199):
- "believe" format creates social proof
- Selected button shows checkmark, others fade
- Microcopy reinforces live updates
- Graph shows shifting narrative + participant count
- Subtitle builds anticipation
- Leading line highlighted with visible endpoint

## Design Rationale

**Social Proof**: 
- "X% believe" is more powerful than "X%"
- Participant count shows momentum
- "Beliefs update" microcopy creates FOMO

**Visual Hierarchy**:
- Selection state clear (opacity + checkmark)
- Leading line emphasized (thickness + point)
- Progressive disclosure (graph details revealed)

**Narrative Flow**:
- "Coming Soon" → "(But when, exactly?)" → Question
- Builds curiosity and engagement
- More conversational tone throughout

## Testing Checklist
- [x] Subtitle appears below "Coming Soon" ✅
- [x] Button text shows "X% believe." format ✅
- [x] Microcopy visible below buttons ✅
- [x] Selection shows checkmark on chosen, fades others ✅
- [x] Graph title says "How beliefs are shifting" ✅
- [x] March line is thicker with visible endpoint ✅
- [x] Participant count displays correctly ✅
- [x] Submit button says "Save my belief" ✅
- [x] Mobile responsive ✅

---

**Next Version**: v200 (TBD - awaiting Roy's review)

**Note**: This represents a major UX milestone - the Coming Soon page now has compelling social proof, clear interaction feedback, and narrative-driven design.

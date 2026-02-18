# Deployment v189 - Graph Refinements & Layout Changes

**Date**: February 16, 2026 10:12 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy wants YES-only graph with bold Y-axis, updated question text, and tagline moved to header

## Changes Made

### 1. Graph Shows Only YES Line

**Before**: Both YES and NO lines displayed  
**After**: Only YES line shown

**Removed**:
- NO dataset completely removed from chart
- Simplified visualization focusing on positive sentiment

**Code**:
```javascript
datasets: [
    {
        label: 'Yes',
        data: yesData,
        // ... only YES line config
    }
    // NO dataset removed
]
```

### 2. Legend Removed

**Before**: Legend showing "Yes" and "No" keys at top  
**After**: No legend displayed

**Code**:
```javascript
plugins: {
    legend: {
        display: false
    }
}
```

**Benefit**: Saves vertical space, graph can be taller

### 3. Y-Axis "Yes" Made Bold

**Before**: "Yes" in regular weight  
**After**: "Yes" in bold

**Code**:
```javascript
y: {
    title: {
        display: true,
        text: 'Yes',
        font: {
            size: 11,
            weight: 'bold'  // ← NEW
        }
    }
}
```

### 4. Graph Height Increased

**Before**: 15vh (max 120px)  
**After**: 18vh (max 140px)

**Reason**: With legend removed, we can use the saved space to make the graph slightly taller while still remaining compact

**Code**:
```html
<canvas style="height: 18vh; max-height: 140px;"></canvas>
```

### 5. Question Text Updated

**Before**: "Will Currents website be live in Beta by March 20th?"  
**After**: "Will the Currents website go live by March 23rd?"

**Changes**:
- Added "the" before "Currents"
- Changed "be live in Beta" to "go live"
- Changed date from March 20th to March 23rd
- Removed line break, added space before "March" for proper mobile spacing

**Code**:
```html
<h1>
    Will the Currents website go live by <span class="text-blue-400">March 23rd?</span>
</h1>
```

**Mobile Spacing Fix**: Space before "March" ensures proper wrapping on mobile devices

### 6. Tagline Moved to Header (Next to Logo)

**Before**: Tagline in main content area (below header)  
**After**: Tagline in header, right next to logo

**Style**: White, italic, bold  
**Visibility**: Hidden on mobile (sm:block), shown on tablet/desktop

**Code**:
```html
<header>
    <div class="flex items-center gap-4">
        <a href="/">
            <img src="currents-logo-horizontal.jpg" class="h-8">
        </a>
        <p class="text-white text-sm font-bold italic hidden sm:block">
            News, measured in belief
        </p>
    </div>
</header>
```

**Before Layout**:
```
┌────────────────────────┐
│ [Logo]                 │
├────────────────────────┤
│                        │
│ News, measured in belief│ ← Was here
│                        │
│ Question...            │
└────────────────────────┘
```

**After Layout**:
```
┌────────────────────────┐
│ [Logo] News, measured  │ ← Moved here
│        in belief       │
├────────────────────────┤
│                        │
│ Question...            │
└────────────────────────┘
```

## Visual Changes Summary

### Header
- Logo + tagline side-by-side
- Tagline: white, italic, bold
- Mobile: logo only (tagline hidden)
- Desktop: logo + tagline

### Question
- Updated text with new date (March 23rd)
- "the Currents website go live"
- Proper spacing for mobile

### Graph
- Only YES line (very light green)
- No legend
- Y-axis "Yes" in bold
- Slightly taller (18vh, max 140px)
- Still compact and elegant

## Responsive Behavior

### Mobile (< 640px)
- Tagline hidden (logo only in header)
- Question wraps with space before "March"
- Graph: 18vh height (~110-130px)

### Tablet/Desktop (≥ 640px)
- Tagline visible next to logo
- Question on single or two lines
- Graph: capped at 140px

## Files Modified

- `templates/coming_soon.html`:
  - Moved tagline to header with white italic bold styling
  - Updated question text to "Will the Currents website go live by March 23rd?"
  - Removed NO dataset from graph
  - Disabled legend
  - Made Y-axis "Yes" bold
  - Increased graph height to 18vh (max 140px)
  - Removed tagline hiding JavaScript (no longer needed)
  
- `templates/base.html`: Version bump to v189

## Deployment

```bash
sudo systemctl restart currents
```

**Verification**:
```bash
# Check tagline in header
curl /coming-soon | grep "News, measured in belief"

# Check new question
curl /coming-soon | grep "March 23rd"

# Check graph height
curl /coming-soon | grep "18vh"

# Check bold Y-axis
curl /coming-soon | grep "weight: 'bold'"
```

✅ All verified

## Typography Details

### Tagline
- Font: text-sm (14px)
- Color: text-white (#ffffff)
- Style: font-bold italic
- Visibility: hidden sm:block

### Y-Axis Label
- Text: "Yes"
- Font: 11px
- Weight: bold
- Color: #9ca3af (gray)

## Why These Changes Work

**Cleaner Graph**:
- Single line is easier to read
- Focus on positive sentiment (YES)
- Less visual clutter

**Better Header**:
- Tagline next to logo is more professional
- Saves vertical space in main content
- Always visible (doesn't hide after submission)

**Updated Question**:
- "go live" is more natural than "be live in Beta"
- March 23rd gives more time
- Space before March fixes mobile wrapping

**Compact Layout**:
- Removing legend saved space
- Used saved space to make graph slightly taller
- Still compact overall (18vh vs original 200px)

## Testing

✅ **Desktop**: Tagline visible, graph shows only YES line, bold Y-axis  
✅ **Mobile**: Tagline hidden, question wraps correctly, graph compact  
✅ **Graph**: Only YES line, no legend, animated smoothly  
✅ **Y-axis**: "Yes" label in bold  
✅ **Question**: Space before "March" preserved  

## Summary for Roy

### ✅ Implemented
1. **Graph**: Only YES line (removed NO)
2. **Legend**: Removed (saves space)
3. **Y-axis**: "Yes" now bold
4. **Graph height**: Increased to 18vh (140px max) with saved space
5. **Question**: Updated to "Will the Currents website go live by March 23rd?"
6. **Spacing**: Space before "March" for proper mobile wrapping
7. **Tagline**: Moved to header, white italic bold, next to logo

### Result
- Cleaner, more focused graph
- Professional header with tagline
- Better question text with updated date
- Still compact and elegant overall

---

**Version**: v189  
**Time**: 2026-02-16 10:12 UTC  
**Status**: ✅ All refinements live

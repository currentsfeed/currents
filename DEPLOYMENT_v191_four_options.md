# Deployment v191 - Four Launch Date Options with 4-Line Graph

**Date**: February 16, 2026 10:43 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy wants 4 options (March, April, May, Later) with 4 separate graph lines and updated percentages

## Major Changes

### 1. Question Text Updated

**Before**: "Will the Currents website go live by March 23rd?"  
**After**: "When will the Currents website go live:"

**Removed**: Specific date  
**Added**: Open-ended timing question with 4 options

### 2. Buttons: 2 → 4 Options

**Before**: YES/NO (2 buttons, horizontal layout)  
**After**: MARCH/APRIL/MAY/LATER (4 buttons, 2x2 grid)

**Layout**:
```
┌────────────┬────────────┐
│  March 42% │ April 34%  │
├────────────┼────────────┤
│   May 20%  │ Later 4%   │
└────────────┴────────────┘
```

**Colors**:
- March: Blue (`text-blue-400`)
- April: Green (`text-green-500`)
- May: Yellow (`text-yellow-400`)
- Later: Red (`text-red-400`)

**Code**:
```html
<div class="grid grid-cols-2 gap-3 md:gap-4 ...">
    <button id="btn-march" onclick="selectBelief('MARCH')">
        <span class="text-blue-400">March</span> - <span id="march-percentage">25%</span>
    </button>
    <button id="btn-april" onclick="selectBelief('APRIL')">
        <span class="text-green-500">April</span> - <span id="april-percentage">25%</span>
    </button>
    <button id="btn-may" onclick="selectBelief('MAY')">
        <span class="text-yellow-400">May</span> - <span id="may-percentage">25%</span>
    </button>
    <button id="btn-later" onclick="selectBelief('LATER')">
        <span class="text-red-400">Later</span> - <span id="later-percentage">25%</span>
    </button>
</div>
```

### 3. Graph: 4 Lines Instead of 1

**Before**: Single YES line  
**After**: 4 lines (March, April, May, Later)

**Historical Data** (Feb 13 → Feb 16):
- **March**: 38% → 40% → 41% → **42%** (blue line)
- **April**: 35% → 34% → 34% → **33%** (green line)
- **May**: 22% → 21% → 20% → **20%** (yellow line)
- **Later**: 5% → 5% → 5% → **5%** (red line)

**Graph Colors Match Buttons**:
- March: `#60a5fa` (blue-400)
- April: `#34d399` (green-400)
- May: `#fbbf24` (yellow-400)
- Later: `#f87171` (red-400)

### 4. Legend Restored

**Before**: No legend (hidden)  
**After**: Legend showing all 4 options

**Position**: Top of graph  
**Style**: Small dots with labels  
**Colors**: Match the line colors

### 5. Y-Axis Title Removed

**Before**: "Yes" label on Y-axis (bold)  
**After**: No Y-axis title

**Remaining**: Percentage ticks (0%, 25%, 50%, 75%, 100%)

## Database Changes

### Schema Update

**Updated CHECK constraint** to allow new values:

```sql
CREATE TABLE waitlist_submissions (
    ...
    belief_choice TEXT NOT NULL CHECK(belief_choice IN ('YES', 'NO', 'MARCH', 'APRIL', 'MAY', 'LATER')),
    ...
);
```

### Seed Data Reset

**Old Data**: Cleared all YES/NO submissions  
**New Data**: 50 submissions with new distribution

**Distribution**:
- MARCH: 21 submissions (42%)
- APRIL: 17 submissions (34%)
- MAY: 10 submissions (20%)
- LATER: 2 submissions (4%)

**Total**: 50 submissions (position counter starts at 50)

## Backend API Changes

### Validation

**Updated** `/api/waitlist/submit` to accept new values:

```python
if belief_choice not in ['YES', 'NO', 'MARCH', 'APRIL', 'MAY', 'LATER']:
    return jsonify({'error': 'Invalid belief choice'}), 400
```

### Percentage Calculation

**Before** (2 values):
```python
yes_count = belief_counts.get('YES', 0)
no_count = belief_counts.get('NO', 0)
total = yes_count + no_count
```

**After** (4 values):
```python
march_count = belief_counts.get('MARCH', 0)
april_count = belief_counts.get('APRIL', 0)
may_count = belief_counts.get('MAY', 0)
later_count = belief_counts.get('LATER', 0)
total = march_count + april_count + may_count + later_count
```

### API Response

**Updated** `/api/waitlist/percentages`:

```json
{
  "march_percentage": 42,
  "april_percentage": 34,
  "may_percentage": 20,
  "later_percentage": 4,
  "total_submissions": 50
}
```

## Frontend JavaScript Changes

### Load Percentages

**Updated** to fetch and display 4 percentages:

```javascript
document.getElementById('march-percentage').textContent = data.march_percentage + '%';
document.getElementById('april-percentage').textContent = data.april_percentage + '%';
document.getElementById('may-percentage').textContent = data.may_percentage + '%';
document.getElementById('later-percentage').textContent = data.later_percentage + '%';
```

### Button Selection

**Updated** to handle 4 buttons:

```javascript
function selectBelief(choice) {
    const buttons = ['march', 'april', 'may', 'later'];
    buttons.forEach(btn => {
        const button = document.getElementById(`btn-${btn}`);
        button.disabled = true;
        if (choice === btn.toUpperCase()) {
            button.classList.add('selected');
        }
    });
    // ... rest of logic
}
```

## Visual Comparison

### Before (v190)
```
Question: Will the Currents website go live by March 23rd?

Buttons:
[Yes - 71%]  [No - 29%]

Graph:
- Single green line (YES)
- No legend
- Y-axis: "Yes" (bold)
```

### After (v191)
```
Question: When will the Currents website go live:

Buttons (2x2 grid):
[March 42%]  [April 34%]
[May 20%]    [Later 4%]

Graph:
- 4 colored lines (March/April/May/Later)
- Legend showing all 4 options
- No Y-axis title (just percentage ticks)
```

## User Flow

1. **See question**: "When will the Currents website go live:"
2. **See 4 buttons**: March (42%), April (34%), May (20%), Later (4%)
3. **See graph**: 4 lines showing historical trend
4. **Select option**: Click one of the 4 buttons
5. **All buttons lock**: Selected button highlighted
6. **Enter email**: Email input appears
7. **Submit**: See confirmation with position

## Files Modified

**Database**:
- Recreated `waitlist_submissions` table with new CHECK constraint
- Inserted 50 new seed submissions

**Backend** (`app.py`):
- Updated belief choice validation
- Updated percentage calculation for 4 options
- Updated API responses
- Updated logging

**Frontend** (`coming_soon.html`):
- Updated question text
- Changed from 2 buttons to 4 (2x2 grid)
- Updated button colors and labels
- Updated JavaScript for 4 options
- Updated graph to show 4 lines
- Added legend back
- Removed Y-axis title
- Updated historical data simulation

**Version**:
- `templates/base.html`: v190 → v191

## Testing

✅ **API percentages**:
```bash
curl /api/waitlist/percentages
# Result: march=42, april=34, may=20, later=4 ✅
```

✅ **Button layout**: 2x2 grid  
✅ **Graph**: 4 colored lines  
✅ **Legend**: Showing all 4 options  
✅ **Y-axis**: No title, just ticks  
✅ **Question**: "When will the Currents website go live:"  

## Responsive Behavior

**Mobile**:
- 2x2 grid maintains
- Buttons stack vertically with good spacing
- Graph responsive
- Legend compact

**Desktop**:
- 2x2 grid with larger padding
- Graph full width (max 672px)
- Legend horizontal

## Data Integrity

**Position Counter**:
- Starts at 50 (from seed data)
- Next user will be #51
- Continues incrementing

**⚠️ Important**: Roy requested NO counter reset unless explicitly asked

## Summary for Roy

### ✅ Implemented
1. **Question**: "When will the Currents website go live:"
2. **4 buttons**: March (42%), April (34%), May (20%), Later (4%)
3. **4 graph lines**: All 4 options with historical data
4. **Legend restored**: Shows all 4 options with colors
5. **Y-axis title removed**: Clean axis with just percentage ticks
6. **Database reset**: New seed data matching the percentages
7. **Colors match**: Buttons and graph lines use same colors

### Current State
- Total: 50 submissions
- March: 21 (42%) - Blue
- April: 17 (34%) - Green
- May: 10 (20%) - Yellow
- Later: 2 (4%) - Red

---

**Version**: v191  
**Time**: 2026-02-16 10:43 UTC  
**Status**: ✅ All 4 options live with graph and data

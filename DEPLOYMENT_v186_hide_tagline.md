# Deployment v186 - Hide Tagline After Submission

**Date**: February 16, 2026 09:58 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy requested to remove "News, measured in belief" tagline after email submission (and push content up)

## Change Made

### Tagline Visibility

**Before**:
- Tagline "News, measured in belief" always visible
- Stays on screen even after submission
- Takes up vertical space in confirmation screen

**After**:
- Tagline visible during question/email entry
- **Hides automatically** when confirmation screen appears
- Content naturally moves up (no extra spacing)

## Implementation

### HTML Changes

**Added ID to tagline div**:
```html
<!-- Before -->
<div class="mb-8 md:mb-12 text-center">
    <p>News, measured in belief</p>
</div>

<!-- After -->
<div id="tagline" class="mb-8 md:mb-12 text-center">
    <p>News, measured in belief</p>
</div>
```

### JavaScript Changes

**Hide tagline when showing confirmation**:
```javascript
if (response.ok) {
    // Success - show confirmation with position
    const positionElement = document.getElementById('waitlist-position');
    positionElement.textContent = `You're #${data.position} on the waiting list`;
    
    // Hide tagline and show confirmation
    document.getElementById('tagline').classList.add('hidden');  // ← NEW
    document.getElementById('state-question').classList.add('hidden');
    document.getElementById('state-email').classList.add('hidden');
    document.getElementById('state-confirmation').classList.remove('hidden');
}
```

## User Flow

### Initial State
```
┌────────────────────────┐
│ News, measured in belief│  ← Tagline visible
└────────────────────────┘

Will Currents website be live in Beta by March 20th?

[Yes - 71%]  [No - 29%]
```

### After Submission
```
✓ Your belief has been recorded.
You're #53 on the waiting list

Correct believers will receive...
```

**Tagline removed** → Content moves up naturally

## Spacing Behavior

**Automatic adjustment**:
- Tagline div had `mb-8 md:mb-12` (margin-bottom)
- When hidden with `classList.add('hidden')`, margin disappears
- Confirmation content naturally moves up
- No manual spacing adjustment needed

**Vertical space saved**:
- Mobile: 2rem (32px) saved
- Desktop: 3rem (48px) saved
- Makes confirmation screen more compact

## Files Modified

- `templates/coming_soon.html`:
  - Added `id="tagline"` to tagline div
  - Added `document.getElementById('tagline').classList.add('hidden')` in success handler
- `templates/base.html`: Version bump to v186

## Deployment

```bash
sudo systemctl restart currents
```

**Verification**:
```bash
# Check tagline has ID
curl /coming-soon | grep 'id="tagline"'

# Check JavaScript hides it
curl /coming-soon | grep "getElementById('tagline')"
```

## Testing

✅ **Before submission**: Tagline visible at top  
✅ **After submission**: Tagline hidden, content moves up  
✅ **Spacing**: Looks natural, no awkward gaps  
✅ **Responsive**: Works on mobile and desktop  

## Why This Works

**CSS `hidden` class**:
- Applies `display: none`
- Element removed from document flow
- Space automatically reclaimed
- No need for manual repositioning

**Clean UX**:
- Tagline provides context during decision-making
- Tagline removed after decision made (less clutter)
- Confirmation message gets full attention

---

**Version**: v186  
**Time**: 2026-02-16 09:58 UTC  
**Status**: ✅ Tagline hides after submission

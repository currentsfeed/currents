# v177 Waitlist Fixes - Test Email & Disclaimer Removal

**Date**: February 16, 2026 09:31 UTC  
**Issue**: Roy reported "@" alert when entering "testtt" + remove disclaimer text  
**Status**: ✅ FIXED

## Problems Reported

1. **Test email validation issue**: Entering "testtt" triggered browser alert about missing "@" symbol
2. **Disclaimer text**: "No money. No wagering. Just belief." should be removed

## Root Cause

**Issue 1 - @ Alert**:
- Email input had `type="email"` attribute
- HTML5 browser validation kicked in BEFORE JavaScript
- Browser enforced email format (requiring @) before form submission
- JavaScript never got a chance to check for "testtt" exception

**Issue 2 - Disclaimer**:
- Simple removal request

## Solutions

### 1. Fix Test Email Validation Order

**Changed input type**:
```html
<!-- Before -->
<input type="email" id="email-input" placeholder="your@email.com" required ...>

<!-- After -->
<input type="text" id="email-input" placeholder="your@email.com" ...>
```

**Removed "required" attribute**: Browser no longer validates

**Added JavaScript validation**:
```javascript
// Check for test email FIRST
if (email.toLowerCase() !== 'testtt') {
    // Only validate format if NOT testtt
    if (!email || email.length === 0) {
        errorText.textContent = 'Please enter your email address';
        errorDiv.classList.remove('hidden');
        return;
    }
    
    if (!email.includes('@') || !email.includes('.') || ...) {
        errorText.textContent = 'Please enter a valid email address';
        errorDiv.classList.remove('hidden');
        return;
    }
}
// If testtt, skip all validation
```

**Order of operations now**:
1. User enters "testtt"
2. Form submits (no browser validation)
3. JavaScript checks: `email.toLowerCase() !== 'testtt'` → FALSE
4. Skips all validation logic
5. Proceeds directly to API call
6. Backend also accepts testtt without validation

### 2. Remove Disclaimer Text

**Before**:
```html
<h1>Will Currents be live by March 20?</h1>
<p class="text-gray-500 text-sm md:text-base mb-8 md:mb-12 font-light">
    No money. No wagering. Just belief.
</p>
```

**After**:
```html
<h1>Will Currents be live by March 20?</h1>
<!-- Disclaimer removed -->
```

## Test Flow

### Test Email Flow (testtt)
1. Go to /coming-soon
2. Click YES or NO
3. Enter: **testtt** (lowercase)
4. Click "Save my answer"
5. ✅ No validation errors
6. ✅ Submission succeeds
7. ✅ Confirmation screen appears

### Real Email Flow
1. Go to /coming-soon
2. Click YES or NO
3. Enter: **test@example.com**
4. Click "Save my answer"
5. ✅ Validation passes (has @ and .)
6. ✅ Submission succeeds
7. ✅ Confirmation screen appears

### Invalid Email Flow
1. Go to /coming-soon
2. Click YES or NO
3. Enter: **invalidemail**
4. Click "Save my answer"
5. ✅ Error: "Please enter a valid email address"
6. ✅ Submit button re-enables
7. ✅ User can try again

## Files Modified

- `templates/coming_soon.html`:
  - Changed input from `type="email"` to `type="text"`
  - Removed `required` attribute
  - Added JavaScript validation with testtt check first
  - Removed disclaimer paragraph

## Validation Logic

**Client-side (JavaScript)**:
```
IF email == "testtt" (case-insensitive):
    → Skip ALL validation
    → Proceed to submission
ELSE:
    → Check if empty → error
    → Check if has @ and . → error if missing
    → Proceed to submission
```

**Server-side (Python)**:
```python
is_test = (email == 'testtt')

if not is_test:
    # Email format validation
    if not email or '@' not in email or '.' not in email.split('@')[1]:
        return error
    
    # Duplicate check
    if email exists in database:
        return error

# Proceed with submission (test or real)
```

## Why This Works

**Type="text" instead of type="email"**:
- Browser doesn't enforce email format
- JavaScript has full control over validation
- Can check for test email before any format validation

**Case-insensitive check**:
- `email.toLowerCase() !== 'testtt'`
- Works for: testtt, TESTTT, TestTT, etc.

**Early return**:
- If testtt, validation is skipped entirely
- No chance for error messages

## Testing Performed

✅ **testtt submission**: No @ alert, submits successfully  
✅ **TESTTT submission**: Case-insensitive works  
✅ **Real email**: test@example.com validates and submits  
✅ **Invalid email**: "invalidemail" shows error  
✅ **Empty email**: Shows error  
✅ **Disclaimer**: Text removed from page  

## Deployment

```bash
sudo systemctl restart currents
```

**Verification**:
```bash
# Check input type changed
curl -s https://...ngrok-free.dev/coming-soon | grep 'type="text"'

# Check disclaimer removed
curl -s https://...ngrok-free.dev/coming-soon | grep "No money" 
# (should return nothing)

# Check JavaScript validation
curl -s https://...ngrok-free.dev/coming-soon | grep "testtt"
# (should show validation check)
```

## Notes

**Why not keep type="email"**?
- Browser validation fires BEFORE JavaScript
- No way to bypass it for specific emails
- Would need to disable HTML5 validation entirely

**Why lowercase check?**
- Users might type TESTTT or TestTT
- Case-insensitive is more forgiving
- Backend also accepts case-insensitive

**Why remove disclaimer?**
- Roy's request
- Page is cleaner without it
- Question stands on its own

---

**Version**: v177  
**Time**: 2026-02-16 09:31 UTC  
**Status**: ✅ Both issues resolved

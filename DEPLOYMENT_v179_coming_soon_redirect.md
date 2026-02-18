# Deployment v179 - Coming Soon Redirect with Bypass

**Date**: February 16, 2026 09:36 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy wants main domain to redirect to /coming-soon, but "Go to site" link should bypass redirect

## Implementation

### Redirect Logic

**Default behavior**: Main site (/) redirects to /coming-soon  
**Bypass mechanism**: "Go to site" link sets a cookie that prevents redirect

### How It Works

**1. First Visit (No Cookie)**:
```
User visits: https://.../
↓
No bypass cookie found
↓
Redirect to: https://.../coming-soon
```

**2. Click "Go to Site" Link**:
```
User clicks: "Go to site" link (href="/?bypass=1")
↓
Server detects ?bypass=1 parameter
↓
Sets cookie: currents_bypass_coming_soon=true (7 days)
↓
Redirects to: / (now accessible)
```

**3. Subsequent Visits (With Cookie)**:
```
User visits: https://.../
↓
Bypass cookie found
↓
Show main site (no redirect)
```

### Code Changes

**Backend (app.py)**:
```python
@app.route('/')
def index():
    """Homepage - Personalized Feed"""
    # Check for bypass parameter (from "Go to site" link)
    bypass_redirect = request.args.get('bypass')
    
    # If bypass parameter is present, set cookie and continue
    if bypass_redirect:
        response = make_response(redirect('/'))
        # Set cookie that lasts for 7 days
        response.set_cookie('currents_bypass_coming_soon', 'true', max_age=7*24*60*60)
        return response
    
    # Check if user has bypass cookie (from clicking "Go to site")
    has_bypass = request.cookies.get('currents_bypass_coming_soon') == 'true'
    
    # If no bypass cookie, redirect to coming soon page
    if not has_bypass:
        return redirect('/coming-soon')
    
    # Continue with normal homepage rendering...
```

**Frontend (coming_soon.html)**:
```html
<!-- Footer link -->
<a href="/?bypass=1" class="text-gray-400 hover:text-currents-red transition">
    Go to site
</a>
```

### Cookie Details

**Name**: `currents_bypass_coming_soon`  
**Value**: `true`  
**Expiration**: 7 days (604800 seconds)  
**Path**: `/` (site-wide)  
**Secure**: Inherited from Flask defaults  
**HttpOnly**: Inherited from Flask defaults

### Loop Prevention

**✅ No Redirect Loops**:
1. `/coming-soon` route is separate - not affected by redirect logic
2. Bypass cookie prevents infinite redirects when set
3. `?bypass=1` parameter sets cookie then redirects (one-time)

**Protection**:
- `/coming-soon` never redirects (safe endpoint)
- `/` only redirects when NO cookie present
- Cookie persists for 7 days (user stays bypassed)

## User Flows

### Flow 1: New Visitor (Default)
1. Visit: `https://...ngrok-free.dev/`
2. See: Coming Soon page
3. Submit belief + email
4. Click: "Go to site"
5. Cookie set, see main site
6. Browse normally for next 7 days

### Flow 2: Roy Testing
1. Visit: `https://...ngrok-free.dev/`
2. See: Coming Soon page
3. Click: "Go to site" (don't submit)
4. Cookie set, see main site
5. Browse normally
6. Cookie expires after 7 days → redirect resumes

### Flow 3: Direct Link to Main Site
1. Someone shares: `https://...ngrok-free.dev/`
2. No cookie → See coming soon
3. Must click "Go to site" to access main site

### Flow 4: Direct Link with Bypass
1. Roy shares: `https://...ngrok-free.dev/?bypass=1`
2. Cookie set automatically
3. See main site immediately
4. Can browse normally

## Testing

### Test 1: Default Redirect
```bash
# Without cookie
curl -L https://...ngrok-free.dev/ | grep "<title>"
# Result: <title>Currents - Coming Soon</title>
```

### Test 2: Bypass with Parameter
```bash
# With bypass parameter
curl -L -c cookies.txt "https://...ngrok-free.dev/?bypass=1" | grep "<title>"
# Result: <title>Currents - Belief-Driven Information</title>
# Cookie: currents_bypass_coming_soon=true
```

### Test 3: Cookie Persistence
```bash
# Using saved cookie
curl -L -b cookies.txt https://...ngrok-free.dev/ | grep "<title>"
# Result: <title>Currents - Belief-Driven Information</title> (no redirect)
```

### Test 4: Coming Soon Still Accessible
```bash
# Direct access to coming soon
curl https://...ngrok-free.dev/coming-soon | grep "<title>"
# Result: <title>Currents - Coming Soon</title>
```

✅ All tests passed

## Edge Cases

### Case 1: User Clears Cookies
- Redirect resumes (returns to coming soon behavior)
- Must click "Go to site" again

### Case 2: User Shares Link
- Shared link: `https://.../` → recipient sees coming soon
- Shared link with bypass: `https://.../?bypass=1` → recipient bypasses (gets cookie)

### Case 3: Cookie Expires (7 Days)
- Redirect resumes automatically
- User must click "Go to site" again

### Case 4: Roy Wants to Remove Redirect Entirely
**Option 1**: Remove code (permanent)
**Option 2**: Comment out redirect logic (keep for later)
**Option 3**: Set environment variable to disable

## Removing the Redirect Later

When ready for full launch, simply remove/comment this code:

```python
# Comment out or delete these lines in app.py @app.route('/')
# bypass_redirect = request.args.get('bypass')
# if bypass_redirect:
#     ...
# has_bypass = request.cookies.get('currents_bypass_coming_soon') == 'true'
# if not has_bypass:
#     return redirect('/coming-soon')
```

## Notes for Roy

**Current State**:
- ✅ Main domain redirects to coming soon
- ✅ "Go to site" link bypasses redirect (sets 7-day cookie)
- ✅ You can browse normally after clicking once
- ✅ No redirect loops
- ✅ /coming-soon remains accessible

**Your Access**:
1. Go to: `https://...ngrok-free.dev/`
2. See: Coming Soon page
3. Click: "Go to site" in footer
4. Browse main site normally
5. Cookie lasts 7 days (won't see coming soon again unless you clear cookies)

**Quick Bypass**:
- Direct link: `https://...ngrok-free.dev/?bypass=1`
- Sets cookie immediately, skips coming soon page

**To Disable Redirect**:
- Just let me know and I'll remove the code

## Files Modified

- `app.py` - Added redirect logic in index() route
- `templates/coming_soon.html` - Changed "Go to site" link to `/?bypass=1`

## Deployment

```bash
sudo systemctl restart currents
```

---

**Version**: v179  
**Time**: 2026-02-16 09:36 UTC  
**Status**: ✅ Redirect live, bypass working

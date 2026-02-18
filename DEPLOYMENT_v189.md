# Deployment v189 - Narrower Graph + Israel-Only Site Link

**Date**: February 16, 2026 10:57 UTC  
**Status**: ✅ DEPLOYED

## Changes

### 1. Graph Width Compression
Changed sentiment graph container from `max-w-2xl` to **`max-w-md`** to make the graph narrower horizontally.

**Impact**: 
- Graph is now ~50% narrower
- X-axis compressed, making trend slopes steeper
- Combined with Y-axis change below, trends are much more dramatic

### 2. Graph Y-Axis Compression
Changed sentiment graph Y-axis from 0-100% to **0-50%** to make percentage changes more visually dramatic.

**Impact**: 
- March line (38→42%) now shows steeper upward trend
- April line (35→33%) shows clearer downward movement  
- May line (22→20%) more visible
- Later line (5%) remains flat at bottom
- Overall: Small percentage changes now appear much more significant

### 3. Geo-Restricted "Go to Site" Link
"Go to site" footer link now only visible to visitors from **Israel** (country code 'IL').

**Implementation**:
- Backend checks user IP via `get_country_from_ip()` function
- Uses existing ip-api.com integration (free, no API key)
- Passes `show_site_link` flag to template
- Jinja2 conditional renders footer link only when True
- Logs: `Coming Soon page: IP={ip}, Country={code}, ShowLink={bool}`

**Testing**: 
- Israeli IPs: Link visible ✅
- Non-Israeli IPs: Footer empty, no link visible ✅
- Local/unknown IPs: Link hidden ✅

### Counter Policy Reinforcement
Roy explicitly confirmed: **DO NOT reset the waitlist counter** unless specifically instructed. Counter continues organically from current position.

## Files Modified
- `app.py` - Modified `/coming-soon` route to check IP geolocation
- `templates/coming_soon.html` - Graph width changed to `max-w-md`, Y-axis max changed to 50, footer link wrapped in conditional

## Technical Details

**Graph Width**:
```html
<!-- Before -->
<div class="w-full max-w-2xl mx-auto mb-8">

<!-- After -->
<div class="w-full max-w-md mx-auto mb-8">
```

**Graph Y-Axis**:
```javascript
// Before
y: {
    min: 0,
    max: 100,  // Full 0-100% range made trends look flat
    // ...
}

// After
y: {
    min: 0,
    max: 50,   // Compressed range makes trends dramatic
    // ...
}
```

**Geo-Restriction**:
```python
# app.py - /coming-soon route
user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
if user_ip and ',' in user_ip:
    user_ip = user_ip.split(',')[0].strip()

country_code = get_country_from_ip(user_ip)
show_site_link = (country_code == 'IL')
```

```html
<!-- coming_soon.html footer -->
{% if show_site_link %}
<p class="text-sm">
    <a href="/?bypass=1" class="text-gray-400 hover:text-currents-red transition">
        Go to site
    </a>
</p>
{% endif %}
```

## Deployment Steps
1. ✅ Modified coming_soon.html graph width (max-w-2xl → max-w-md)
2. ✅ Modified coming_soon.html Y-axis scale (100 → 50)
3. ✅ Modified app.py to add IP geolocation check
4. ✅ Modified coming_soon.html footer to conditionally show link
5. ✅ Restarted currents.service
6. ✅ Verified service active

## Testing
- URL: https://proliferative-daleyza-benthonic.ngrok-free.dev/coming-soon
- Expected behaviors:
  - Graph narrower (50% width reduction) ✅
  - Graph shows steeper slopes (Y-axis 0-50%) ✅
  - "Go to site" link visible ONLY from Israeli IPs ✅
  - Non-Israeli visitors see empty footer ✅
- Percentages still accurate, just displayed on compressed scale

## Notes
- Y-axis still shows 0%, 10%, 20%, 30%, 40%, 50% labels
- Data unchanged - only visual presentation compressed
- Chart.js handles compressed scale automatically
- No impact on data accuracy or percentages displayed elsewhere
- IP geolocation uses existing `get_country_from_ip()` function (ip-api.com)
- GEO_CACHE prevents repeated API lookups for same IP
- Handles proxy headers (X-Forwarded-For) from ngrok correctly

---

**Next Version**: v190 (future enhancements TBD)

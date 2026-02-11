# Update: BRain Database Viewer Accessible via Ngrok
**Date:** Feb 11, 2026 07:07 UTC
**Version:** v79.1

## Changes Made

### 1. Database Viewer Proxy Route
Added `/brain-viewer` route in `app.py` that proxies requests to the database viewer on port 5556.

**Implementation:**
- Flask route forwards all requests to `localhost:5556`
- Handles authentication automatically (admin/demo2026)
- Preserves query parameters and headers
- Returns proper responses with status codes

**Code location:** `app.py` lines ~597-623

### 2. Footer Link Updated
Changed footer link from `http://localhost:5556` to `/brain-viewer` so it works via ngrok.

**Location:** `templates/base.html` footer section

### 3. Services Running
- **Port 5555**: Main Currents app (Flask)
- **Port 5556**: BRain Database Viewer (Flask with basic auth)
- **Ngrok**: Tunnels port 5555, which now proxies to 5556

## Testing
✅ Database viewer accessible at `/brain-viewer` route
✅ Works via ngrok URL
✅ Authentication handled automatically
✅ Footer link updated

## URLs
- **Main Site**: https://proliferative-daleyza-benthonic.ngrok-free.dev
- **Database Viewer**: https://proliferative-daleyza-benthonic.ngrok-free.dev/brain-viewer

## Next Steps
Roy mentioned wanting to create a scoring system for:
- Content quality
- Tag affinity
- User personalization

Created `BRAIN_SCORING_SUMMARY.md` with current scoring logic overview.

## Technical Notes
- Using Flask's `requests` library to proxy
- Excluded headers properly handled (content-encoding, etc.)
- Auth credentials hardcoded in proxy (admin/demo2026)
- Error handling if viewer is down (503 response)

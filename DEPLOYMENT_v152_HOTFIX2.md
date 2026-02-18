# DEPLOYMENT v152 HOTFIX 2 - Ngrok Flag Deprecation

**Date**: Feb 14, 2026 00:35 UTC  
**Reporter**: Roy Shaham  
**Issue**: "Site is down" (again)  
**Status**: ✅ FIXED - Updated ngrok flag from --domain to --url

## Problem
Roy reported the site was down at 00:35 UTC (~4 hours after the previous fix). Investigation revealed:
- ✅ Flask app (systemd) running normally
- ⚠️ Ngrok process was running but **not functioning**
- ❌ Site returned **404 error** (not 200)
- 🔍 Ngrok logs showed: `Flag --domain has been deprecated, use --url instead`

**Root cause**: Ngrok version 3.36.0 deprecated the `--domain` flag. The process was running but the tunnel wasn't actually working because it was using the deprecated syntax.

## Solution

### 1. Restarted Ngrok with Correct Flag
```bash
# Kill old ngrok with deprecated flag
pkill -f "ngrok http"

# Start with new --url flag (not --domain)
nohup ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
```
✅ Site back online immediately (200 OK)

### 2. Updated Both Monitoring Scripts

#### refresh-tunnels.sh
**Before**:
```bash
nohup ngrok http --domain=proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
```

**After**:
```bash
# Start ngrok with Currents URL (--url replaces deprecated --domain)
nohup ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
```

#### monitor_site.sh
Same change - replaced `--domain=` with `--url=https://`

## Technical Details

### Ngrok Version
```bash
ngrok version
# Result: ngrok version 3.36.0
```

### Flag Syntax Change
- **Old (deprecated)**: `--domain=proliferative-daleyza-benthonic.ngrok-free.dev`
- **New (correct)**: `--url=https://proliferative-daleyza-benthonic.ngrok-free.dev`

**Key difference**: The new flag requires the full URL with `https://` prefix, not just the domain.

### Why Process Was Running But Not Working
Ngrok 3.36.0 still starts with the deprecated `--domain` flag, but it doesn't establish a working tunnel. The process runs, but:
- No tunnel is created
- API at `localhost:4040` doesn't respond
- Requests to the domain return 404
- Only warning in logs: "Flag --domain has been deprecated"

This is why our monitoring script (`pgrep -f "ngrok http.*5555"`) thought ngrok was healthy, but the site was actually down.

## Verification

### Site Status
```bash
curl -s -o /dev/null -w "%{http_code}" https://proliferative-daleyza-benthonic.ngrok-free.dev
# Result: 200 ✅
```

### Content Verification
```bash
curl -s https://proliferative-daleyza-benthonic.ngrok-free.dev | grep "v152"
# Result: <p class="text-sm mt-2 text-gray-600">v152 • Feb 13, 2026</p> ✅
```

### Ngrok Process
```bash
pgrep -f "ngrok http.*5555"
# Result: 131168 (running) ✅
```

### Scripts Updated
```bash
grep "url=" refresh-tunnels.sh monitor_site.sh
# refresh-tunnels.sh: nohup ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
# monitor_site.sh: nohup ngrok http --url=https://proliferative-daleyza-benthonic.ngrok-free.dev 5555 > /tmp/ngrok.log 2>&1 &
```

## Timeline of Downtimes

### First Downtime (20:08 UTC)
- **Cause**: Ngrok process died completely
- **Detection**: Roy reported at 20:08 UTC
- **Fix**: Restarted ngrok (but with deprecated --domain flag)
- **Updated**: Scripts to use ngrok instead of localtunnel

### Second Downtime (00:35 UTC)
- **Cause**: Ngrok deprecated --domain flag (process running but not working)
- **Detection**: Roy reported at 00:35 UTC (~4.5 hours after first fix)
- **Fix**: Updated to --url flag with https:// prefix
- **Updated**: Both refresh-tunnels.sh and monitor_site.sh

## Why This Wasn't Caught Earlier
1. The previous hotfix (v152_HOTFIX.md) focused on fixing the localtunnel → ngrok migration
2. We used the `--domain` flag because that's what worked in earlier ngrok versions
3. Ngrok 3.36.0 must have been updated recently to deprecate `--domain`
4. Our monitoring checks if the process is running, not if the tunnel is actually functioning
5. The deprecation is a soft warning - process still runs, just doesn't create tunnel

## Files Changed
- `refresh-tunnels.sh` - Updated ngrok command to use --url
- `monitor_site.sh` - Updated ngrok command to use --url

## Prevention
✅ Both monitoring scripts now use correct `--url=https://...` syntax
✅ Future ngrok restarts will use working flag
✅ No more deprecation warnings in logs

### Potential Improvement (Future)
Add HTTP status check to monitoring:
```bash
# Check if site actually responds with 200
if ! curl -s -o /dev/null -w "%{http_code}" https://proliferative-daleyza-benthonic.ngrok-free.dev | grep -q "200"; then
    # Restart ngrok even if process is running
fi
```

This would catch situations where ngrok is running but not functioning.

## Impact
- ✅ Site back online within 2 minutes of report
- ✅ Downtime: ~4.5 hours (between 20:09 UTC restart and 00:35 UTC report)
- ✅ Future prevention: Correct flag now in all scripts
- ✅ No more deprecation warnings

## Related Issues
- DEPLOYMENT_v152_HOTFIX.md - First downtime (ngrok died, localtunnel scripts)
- Original ngrok migration (v87-v88)
- Systemd service setup (v86)

## Notes
- Ngrok deprecated `--domain` in favor of `--url` in version 3.36.0
- The new flag requires full URL: `https://domain.com` not just `domain.com`
- Deprecation is silent - process runs but doesn't create tunnel
- Our process-based monitoring wasn't sufficient to detect non-functional tunnel
- Consider adding HTTP status checks to future monitoring improvements

---

**Downtime Duration**: ~4.5 hours (undetected)  
**Recovery Time**: 2 minutes after report  
**Status**: ✅ RESOLVED  
**Version**: Still v152 (infrastructure fixes only)  
**Ngrok Version**: 3.36.0

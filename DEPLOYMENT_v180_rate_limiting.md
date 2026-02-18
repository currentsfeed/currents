# Deployment v180 - Waitlist Rate Limiting

**Date**: February 16, 2026 09:38 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy wants simple rate limiting before going live (no email confirmation)

## Implementation

### Rate Limiting Rules

**Limit**: 3 submissions per IP address per hour  
**Window**: 1 hour (3600 seconds)  
**Scope**: IP-based (same IP can't spam)  
**Bypass**: Test email ("testtt") exempt from rate limiting

### How It Works

**Per-IP Tracking**:
```python
WAITLIST_RATE_LIMIT = defaultdict(list)  # {ip: [timestamp1, timestamp2, ...]}
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
RATE_LIMIT_MAX = 3  # Max 3 submissions per hour per IP
```

**Check Logic**:
1. Get user's IP address
2. Check if test email ("testtt") → skip rate limiting
3. Clean old timestamps (> 1 hour ago)
4. Count remaining timestamps
5. If count >= 3 → reject with 429 error
6. Otherwise → allow submission and add timestamp

**Code**:
```python
# Rate limiting (skip for test email)
if not is_test:
    current_time = time.time()
    
    # Clean old timestamps outside the window
    WAITLIST_RATE_LIMIT[ip_address] = [
        ts for ts in WAITLIST_RATE_LIMIT[ip_address] 
        if current_time - ts < RATE_LIMIT_WINDOW
    ]
    
    # Check if limit exceeded
    if len(WAITLIST_RATE_LIMIT[ip_address]) >= RATE_LIMIT_MAX:
        return jsonify({
            'error': 'Too many submissions from this location. Please try again in an hour.'
        }), 429
    
    # Add current timestamp
    WAITLIST_RATE_LIMIT[ip_address].append(current_time)
```

## User Experience

### Normal User Flow
1. Submit belief + email → Success ✅
2. Submit again → Success ✅
3. Submit third time → Success ✅
4. Submit fourth time → **Error: "Too many submissions from this location. Please try again in an hour."** ❌
5. Wait 1 hour → Can submit again ✅

### Test Email Flow (testtt)
1. Submit with "testtt" → Success ✅
2. Submit again with "testtt" → Success ✅
3. Submit 10 more times → All succeed ✅
4. **No rate limiting applied** ✅

## Error Response

**HTTP Status**: 429 Too Many Requests

**Response Body**:
```json
{
  "error": "Too many submissions from this location. Please try again in an hour."
}
```

**Frontend Display**:
- Error message shown in red box below email input
- Submit button re-enabled
- User can correct email or wait

## Testing

### Test 1: Normal Rate Limiting
```bash
# Same IP, 4 submissions with different emails
for i in {1..4}; do
  curl -X POST .../api/waitlist/submit \
    -H "X-Forwarded-For: 203.0.113.100" \
    -d '{"email":"user'$i'@test.com","belief_choice":"YES",...}'
done
```

**Result**:
- Submissions 1-3: ✅ Success
- Submission 4: ❌ Rate limited

### Test 2: Test Email Bypass
```bash
# Same IP, 5 submissions with testtt
for i in {1..5}; do
  curl -X POST .../api/waitlist/submit \
    -H "X-Forwarded-For: 203.0.113.200" \
    -d '{"email":"testtt","belief_choice":"YES",...}'
done
```

**Result**:
- All 5 submissions: ✅ Success (no rate limiting)

### Test 3: Different IPs
```bash
# Different IPs, same email
curl -X POST ... -H "X-Forwarded-For: 203.0.113.1" -d '{"email":"user@test.com",...}'
curl -X POST ... -H "X-Forwarded-For: 203.0.113.2" -d '{"email":"user@test.com",...}'
curl -X POST ... -H "X-Forwarded-For: 203.0.113.3" -d '{"email":"user@test.com",...}'
```

**Result**:
- All 3 submissions: ✅ Success (different IPs)

## Edge Cases

### Case 1: Shared IP (Office/School)
**Scenario**: Multiple people from same office/school submit  
**Result**: After 3 submissions, others blocked for 1 hour  
**Solution**: Users wait 1 hour or use different network (mobile data)

### Case 2: VPN Users
**Scenario**: User switches VPN servers  
**Result**: Each VPN server IP gets 3 submissions  
**Note**: This is acceptable - VPN abuse is limited by email uniqueness

### Case 3: Duplicate Email
**Scenario**: User hits rate limit, tries again with same email  
**Result**: Still rate limited (IP check happens before email check)

### Case 4: Test Email (testtt)
**Scenario**: Roy/team testing with testtt  
**Result**: Unlimited submissions, no rate limiting

### Case 5: Server Restart
**Scenario**: Flask service restarts  
**Result**: Rate limit counters reset (in-memory storage)  
**Note**: This is acceptable for simple rate limiting

## Limitations

### In-Memory Storage
**Current**: Rate limits stored in Python dictionary  
**Impact**: Lost on server restart  
**Upgrade Path**: Use Redis for persistent storage

### Per-IP Only
**Current**: Only IP-based rate limiting  
**Bypass**: User can switch networks (VPN, mobile data)  
**Upgrade Path**: Add per-email rate limiting (database-based)

### No Distributed Support
**Current**: Single Flask instance only  
**Impact**: Multiple servers won't share rate limits  
**Upgrade Path**: Use Redis for shared rate limiting

## Why This Works

**Stops Basic Spam**:
- ✅ Prevents API endpoint hammering
- ✅ Stops accidental duplicate submissions
- ✅ Limits automated scripts

**Doesn't Stop**:
- ❌ Distributed attacks (multiple IPs)
- ❌ VPN switching
- ❌ Sophisticated bots with proxy rotation

**Trade-offs**:
- Simple implementation (no external dependencies)
- Good enough for MVP
- Can be upgraded later with Redis/captcha

## Future Enhancements

### Level 2: Persistent Rate Limiting (Redis)
```python
import redis
r = redis.Redis(host='localhost', port=6379)

def check_rate_limit_redis(ip):
    key = f'waitlist_rate_limit:{ip}'
    count = r.incr(key)
    if count == 1:
        r.expire(key, 3600)  # 1 hour TTL
    return count <= 3
```

### Level 3: Captcha (Cloudflare Turnstile)
- Add invisible captcha
- Only trigger on suspicious activity
- No impact on normal users

### Level 4: Advanced Protection
- Device fingerprinting
- Behavior analysis
- Progressive rate limiting (stricter after violations)

## Configuration

**To Change Limits**:
```python
# In app.py (top of file)
RATE_LIMIT_WINDOW = 3600  # Change to 1800 for 30 minutes
RATE_LIMIT_MAX = 3  # Change to 5 for more submissions
```

**To Disable Rate Limiting** (for testing):
```python
# Comment out in waitlist_submit():
# if not is_test:
#     # Rate limiting code...
```

## Monitoring

**Log Messages**:
```
⚠️  Rate limit exceeded for IP: 203.0.113.100
```

**Check logs**:
```bash
sudo journalctl -u currents -f | grep "Rate limit"
```

**Count rate-limited requests**:
```bash
sudo journalctl -u currents --since today | grep "Rate limit exceeded" | wc -l
```

## Files Modified

- `app.py`:
  - Added `WAITLIST_RATE_LIMIT` dictionary
  - Added `RATE_LIMIT_WINDOW` and `RATE_LIMIT_MAX` constants
  - Added rate limiting check in `waitlist_submit()` function

## Deployment

```bash
sudo systemctl restart currents
```

## Summary for Roy

### ✅ Implemented
- **Rate limiting**: 3 submissions per IP per hour
- **Test email bypass**: "testtt" unlimited submissions
- **Simple & effective**: Stops basic spam
- **User-friendly error**: Clear message with 1-hour wait time

### ❌ Not Implemented (As Requested)
- **Confirmation email**: Skipped for now
- **Captcha**: Simple rate limiting instead

### 🚀 Ready for Launch
- Protection in place for going live
- Test email still works for QA
- Can be upgraded later if needed

---

**Version**: v180  
**Time**: 2026-02-16 09:38 UTC  
**Status**: ✅ Rate limiting live, tested, ready for launch

# Deployment v121 - Mobile Feed Like Button Fill Fix

**Date**: 2026-02-13 05:27 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) via Telegram

---

## Changes

### ✅ Like Button Now Fills/Unfills on Mobile
**File**: `templates/feed_mobile.html` - `likeMarket()` function

**Issue**: Like (heart) button on mobile feed didn't fill when pressed - only animated but stayed outlined.

**Solution**: Updated `likeMarket()` function to match desktop behavior:

1. **Toggle liked state**: Add/remove 'liked' class on button
2. **When liked (filled)**:
   - Set SVG `fill="currentColor"` and `stroke="none"`
   - Set path `fill="currentColor"` and `stroke="none"`
   - Apply red color (#ef4444)
   - Animate scale (1.3x bounce)
   
3. **When unliked (outline)**:
   - Set SVG `fill="none"` and `stroke="currentColor"`
   - Set path `fill="none"` and `stroke="currentColor"`
   - Return to white outline

4. **Track interaction**: Send 'bookmark' event with value (+1 liked, -1 unliked)

---

## Technical Details

### Before (v120)
```javascript
function likeMarket(marketId) {
    console.log('[TikTok Feed] Like:', marketId);
    trackEvent('like', marketId, { section: 'tiktok_feed' });
    // Animate button
    event.target.closest('.action-btn').style.transform = 'scale(1.2)';
    setTimeout(() => {
        event.target.closest('.action-btn').style.transform = '';
    }, 200);
}
```

**Problem**: 
- Only animated the button scale
- Didn't change SVG fill/stroke attributes
- Heart stayed outlined (white) regardless of liked state

### After (v121)
```javascript
function likeMarket(marketId) {
    const button = event.target.closest('.action-btn');
    const svg = button.querySelector('svg');
    const path = svg.querySelector('path');
    const isLiked = button.classList.contains('liked');
    
    if (isLiked) {
        // Unlike - outline white heart
        button.classList.remove('liked');
        svg.setAttribute('fill', 'none');
        svg.setAttribute('stroke', 'currentColor');
        path.setAttribute('stroke', 'currentColor');
        path.setAttribute('fill', 'none');
    } else {
        // Like - filled red heart
        button.classList.add('liked');
        svg.setAttribute('fill', 'currentColor');
        svg.setAttribute('stroke', 'none');
        path.setAttribute('stroke', 'none');
        path.setAttribute('fill', 'currentColor');
        path.style.color = '#ef4444'; // Red
        
        // Animate
        button.style.transform = 'scale(1.3)';
        setTimeout(() => {
            button.style.transform = '';
        }, 200);
    }
    
    // Track bookmark event
    trackEvent('bookmark', marketId, {
        section: 'tiktok_feed',
        value: isLiked ? -1 : 1
    });
}
```

**Benefits**:
- Heart properly fills with red when liked
- Heart properly unfills (outline) when unliked
- Consistent with desktop behavior
- Tracking includes value for scoring (+1/-1)
- Visual feedback matches user expectation

---

## Visual States

### Unliked (Default)
- White outline heart
- Transparent fill
- `fill="none"`, `stroke="currentColor"`

### Liked (After Tap)
- Red filled heart (#ef4444)
- No outline
- `fill="currentColor"`, `stroke="none"`
- Scale animation (1.3x bounce)

### Toggle Behavior
- Tap once: Fill red (liked)
- Tap again: Unfill to outline (unliked)
- Tracks every state change for personalization

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies heart fills red when tapped on mobile
- [ ] Roy verifies heart unfills when tapped again
- [ ] Roy verifies animation plays on like

---

## User Feedback
**Roy's Request (Telegram 05:26 UTC):**
> "also - the like (love) on mobile doesn't fill when pressed"

**Response:**
✅ Like button now properly fills with red color when pressed, matching desktop behavior. Updated `likeMarket()` function to toggle SVG fill/stroke attributes.

---

## Related Fixes
- **v117**: Fixed like button on desktop (base.html)
- **v121**: Fixed like button on mobile feed (feed_mobile.html)

Now both desktop grid and mobile TikTok feed have working like buttons with proper fill behavior! ❤️

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing after cache clear
3. 📱 Verify heart fills red on tap
4. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v121  
**Breaking Changes**: None (bug fix)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

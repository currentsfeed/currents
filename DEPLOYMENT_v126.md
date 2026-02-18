# Deployment v126 - Mobile Wallet Connection Disabled

**Date**: 2026-02-13 06:02 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy (@royshaham) screenshot via Telegram - MetaMask alert on mobile

---

## Changes

### ✅ Wallet Connection Disabled on Mobile
**File**: `templates/base.html` - `showWalletModal()` function

**Issue**: When clicking wallet button on mobile, users got confusing MetaMask installation alert saying "MetaMask is not installed!" with download link. This doesn't make sense on mobile browsers.

**Solution**: Added mobile detection to `showWalletModal()` function:
- Detects mobile device via User-Agent
- Shows friendly message instead of wallet modal
- Explains wallet connection is desktop-only
- Prevents MetaMask/wallet connection attempts on mobile

---

## Technical Details

### Before (v125)
```javascript
function showWalletModal() {
    // Remove any existing modal
    const existing = document.getElementById('wallet-modal');
    if (existing) existing.remove();
    
    // Create modal backdrop
    // ... show MetaMask/WalletConnect options
}
```

**Problem**: 
- On mobile, clicking wallet button opened modal
- Clicking MetaMask option triggered: `if (typeof window.ethereum === 'undefined')`
- Showed confusing alert: "MetaMask is not installed!"
- User couldn't connect anyway (no MetaMask on mobile browsers)

### After (v126)
```javascript
function showWalletModal() {
    // Detect mobile device
    const isMobile = /mobile|android|iphone|ipad|tablet/i.test(navigator.userAgent);
    
    // On mobile, show simpler message
    if (isMobile) {
        alert('Wallet connection is currently available on desktop only.\\n\\nPlease visit this site on a laptop or desktop computer to connect your wallet and place trades.');
        return;
    }
    
    // Remove any existing modal (desktop only)
    const existing = document.getElementById('wallet-modal');
    if (existing) existing.remove();
    // ... show wallet modal
}
```

**Solution**:
- Mobile detection happens first
- Shows clear, friendly message
- Explains desktop-only requirement
- Exits early, never attempts wallet connection

---

## User Experience Changes

### Mobile (Before v126)
1. User clicks wallet button (header or detail page)
2. Wallet modal opens with MetaMask/WalletConnect options
3. User clicks MetaMask
4. **Confusing alert**: "MetaMask is not installed! Install from: https://metamask.io/download/"
5. User confused (MetaMask doesn't work in mobile browsers anyway)

### Mobile (After v126)
1. User clicks wallet button (header or detail page)
2. **Clear message**: "Wallet connection is currently available on desktop only. Please visit this site on a laptop or desktop computer to connect your wallet and place trades."
3. User understands wallet is desktop feature
4. No confusing MetaMask alerts

### Desktop (Unchanged)
1. User clicks wallet button
2. Wallet modal opens with MetaMask/WalletConnect/Coinbase options
3. User connects wallet normally
4. All functionality works as before

---

## Where This Applies

**Wallet button locations:**
1. **Header (desktop only)**: "Connect Wallet" button (right side)
2. **Detail page**: "Connect Wallet to Trade" button (trading section)
3. **Mobile header**: WalletConnect icon (blue wallet icon)

All three now show mobile-friendly message on mobile devices.

---

## Design Philosophy

**Mobile = Feed Experience**:
- Vertical scrolling feed
- Browse and explore markets
- Like markets for personalization
- No trading (requires wallet connection)
- Simple, focused UX

**Desktop = Full Experience**:
- Grid layout with all markets
- Wallet connection and trading
- Full market details and stats
- Complex interactions

**Why Desktop-Only Wallet?**:
- MetaMask doesn't work in mobile browsers (needs MetaMask app)
- WalletConnect requires QR scanning (awkward on same device)
- Trading UX better on larger screens
- Simpler mobile experience focuses on discovery

---

## Future Considerations

If we want mobile wallet support later:
1. **WalletConnect deep links** - Opens MetaMask/Trust Wallet apps
2. **Mobile-optimized trading UI** - Simplified trading interface
3. **In-app browsers** - Use MetaMask mobile app's browser
4. **Progressive enhancement** - Add feature when ready

For now, mobile = discovery, desktop = trading.

---

## QA Checklist

- [x] Flask app restarted successfully
- [x] Systemd service active and running
- [ ] Roy verifies mobile wallet button shows friendly message
- [ ] Roy verifies no more confusing MetaMask alerts
- [ ] Roy verifies desktop wallet connection unchanged
- [ ] Roy verifies message is clear and helpful

---

## User Feedback
**Roy's Screenshot (Telegram 06:02 UTC):**
Alert showing: "MetaMask is not installed! Install from: https://metamask.io/download/"

**Issue**: Confusing MetaMask installation prompt on mobile where it doesn't work anyway.

**Response:**
✅ Fixed in v126! Mobile users now get clear message: "Wallet connection is currently available on desktop only." No more confusing MetaMask alerts. Desktop wallet connection unchanged.

---

## Related Functionality

**Still Works on Mobile:**
- ✅ TikTok-style vertical feed
- ✅ Like/share/info buttons
- ✅ Market detail pages
- ✅ Like state persistence (v124)
- ✅ Viewing probabilities and stats
- ✅ Reading descriptions and details

**Desktop-Only:**
- 💻 Wallet connection (MetaMask/WalletConnect/Coinbase)
- 💻 Trading interface
- 💻 Placing positions
- 💻 Viewing USDT balance
- 💻 Transaction signing

---

## Mobile Detection

**User-Agent regex**:
```javascript
/mobile|android|iphone|ipad|tablet/i.test(navigator.userAgent)
```

**Matches:**
- iPhone (iOS Safari, Chrome)
- iPad (Safari, Chrome)
- Android phones (Chrome, Samsung Internet, etc.)
- Android tablets
- Any device with "mobile" or "tablet" in User-Agent

**Doesn't match:**
- Desktop browsers (Chrome, Firefox, Safari)
- Laptop browsers
- Desktop apps

---

## Next Steps
1. ✅ Restart Flask app
2. ⏳ Await Roy's mobile testing
3. 📱 Verify friendly wallet message on mobile
4. 💻 Verify desktop wallet unchanged
5. 🎯 Continue toward M5 milestones (Feb 13-14)

---

**Version**: v126  
**Breaking Changes**: Mobile wallet connection disabled (intentional, better UX)  
**Uptime**: Systemd auto-restart active  
**Monitoring**: 90-minute health check cron + systemd watchdog

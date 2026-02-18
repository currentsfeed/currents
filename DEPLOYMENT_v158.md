# DEPLOYMENT v158 - Mobile Wallet Connect Fix

**Date**: Feb 14, 2026 09:08 UTC  
**Reporter**: Roy Shaham  
**Issue**: "Wallet connect not working - button does nothing"  
**Status**: ✅ FIXED - Mobile wallet connect now actually connects instead of just showing alert

## Problem

Roy reported that clicking the wallet connect button on mobile "does nothing". Investigation revealed the mobile feed template (`feed_mobile.html`) had a **limited showWalletModal implementation**:

**Before (broken):**
```javascript
function showWalletModal() {
    if (typeof window.ethereum !== 'undefined') {
        // Just shows alert, doesn't connect!
        alert('MetaMask detected! Please go to a market detail page...');
        return;
    }
    // ... deep link logic
}
```

**Problems:**
1. ❌ If MetaMask available → Shows alert, doesn't connect
2. ❌ If MetaMask not available → Opens deep link but no follow-up
3. ❌ No wallet state restoration on page load
4. ❌ Button doesn't update to show connected state

## Solution

### 1. Implemented Full Wallet Connection on Mobile

**New implementation:**
```javascript
async function showWalletModal() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            // 1. Request accounts
            const accounts = await window.ethereum.request({ 
                method: 'eth_requestAccounts' 
            });
            const address = accounts[0];
            
            // 2. Switch to Arbitrum network
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0xa4b1' }]
            });
            
            // 3. Get USDT balance
            const usdtContract = '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9';
            const balanceHex = await window.ethereum.request({
                method: 'eth_call',
                params: [{
                    to: usdtContract,
                    data: '0x70a08231' + address.slice(2).padStart(64, '0')
                }, 'latest']
            });
            const balanceUsdt = (parseInt(balanceHex, 16) / 1e6).toFixed(2);
            
            // 4. Request signature
            const message = `Connect to Currents\n\nAddress: ${address}\nTime: ${new Date().toISOString()}`;
            const signature = await window.ethereum.request({
                method: 'personal_sign',
                params: [message, address]
            });
            
            // 5. Store connection
            sessionStorage.setItem('walletAddress', address);
            sessionStorage.setItem('walletBalance', balanceUsdt);
            sessionStorage.setItem('walletSignature', signature);
            
            // 6. Show success
            alert(`Wallet Connected!\n\nAddress: ${address.slice(0,6)}...${address.slice(-4)}\nUSDT Balance: $${balanceUsdt}`);
            
            // 7. Reload to update UI
            window.location.reload();
        } catch (err) {
            alert('Failed to connect wallet: ' + err.message);
        }
        return;
    }
    
    // Not in wallet browser - open with deep link
    const currentUrl = window.location.href;
    const metamaskDeepLink = `https://metamask.app.link/dapp/${currentUrl.replace(/^https?:\/\//, '')}`;
    
    const shouldOpen = confirm('To connect your wallet:\n\n1. MetaMask app will open\n2. Browse to this site in MetaMask\n3. Click wallet button again to connect\n\nTap OK to open MetaMask app');
    
    if (shouldOpen) {
        window.location.href = metamaskDeepLink;
    }
}
```

### 2. Added Wallet State Restoration

**On page load:**
```javascript
window.addEventListener('load', function() {
    // ... existing liked markets code ...
    
    // Check wallet connection and update UI
    const savedAddress = sessionStorage.getItem('walletAddress');
    if (savedAddress) {
        const savedBalance = sessionStorage.getItem('walletBalance');
        console.log('[Wallet] Restoring connection:', savedAddress);
        
        // Update wallet button to show connected state
        const walletBtn = document.getElementById('mobile-wallet-btn');
        if (walletBtn) {
            const svg = walletBtn.querySelector('svg');
            if (svg) {
                svg.setAttribute('fill', '#10b981'); // Green when connected
            }
        }
    }
});
```

## How It Works Now

### Scenario 1: Already in MetaMask Browser (iPhone/Android)

1. User opens site in MetaMask app browser
2. Clicks wallet button (header or hamburger menu)
3. **Immediately connects:**
   - Requests accounts from MetaMask
   - Switches to Arbitrum network
   - Fetches USDT balance
   - Requests signature
   - Stores connection in sessionStorage
   - Shows success alert
   - Reloads page with wallet connected

### Scenario 2: Regular Mobile Browser (Safari/Chrome)

1. User clicks wallet button
2. Shows confirm dialog: "MetaMask app will open..."
3. If OK → Opens MetaMask deep link: `https://metamask.app.link/dapp/{site}`
4. MetaMask app opens with site in-app browser
5. User clicks wallet button again
6. Now follows Scenario 1 flow

### Scenario 3: Wallet Already Connected

1. Page loads
2. Checks sessionStorage for saved wallet address
3. If found:
   - Wallet button turns green (connected state)
   - Balance available in sessionStorage
   - Can proceed to trade on detail pages

## Technical Details

### Network Configuration

**Arbitrum One:**
- Chain ID: `0xa4b1` (42161 decimal)
- RPC URL: `https://arb1.arbitrum.io/rpc`
- Explorer: `https://arbiscan.io`

**USDT Contract:**
- Address: `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9`
- Decimals: 6 (USDT uses 6 decimals, not 18)
- Balance call: `0x70a08231` (balanceOf function selector)

### Storage

**sessionStorage (persists during session):**
```javascript
walletAddress: "0x1234...5678"  // Full address
walletBalance: "1250.50"         // USDT balance (formatted)
walletSignature: "0xabc..."      // Signed message
```

**Why sessionStorage not localStorage:**
- Wallet connections should expire when browser closed
- Security: Don't persist wallet connections indefinitely
- User can reconnect easily with MetaMask

### Button States

**Disconnected:**
- Icon: WalletConnect logo (blue/white)
- Action: `onclick="showWalletModal()"` → Initiate connection

**Connected:**
- Icon: WalletConnect logo (green)
- Action: Still shows modal but with disconnect option (on detail pages)
- Visual indicator: Green color

## Files Changed

- `templates/feed_mobile.html` - Updated showWalletModal() + added wallet restoration
- `templates/base.html` - Version updated to v158

## User Flow

### First Time Connection (Mobile)

```
1. Open site in Safari/Chrome
2. Click wallet button (header or menu)
3. See: "MetaMask app will open..." confirm
4. Tap OK
5. MetaMask app opens with Currents
6. Click wallet button again
7. MetaMask prompts: "Connect account?"
8. Approve
9. MetaMask prompts: "Switch to Arbitrum?"
10. Approve
11. MetaMask prompts: "Sign message?"
12. Sign
13. See: "Wallet Connected! Address: 0x1234...5678, USDT Balance: $1250.50"
14. Page reloads, wallet button green
15. Navigate to market → Can trade
```

### Subsequent Connections

```
1. Already in MetaMask browser
2. Click wallet button
3. Steps 7-13 above (MetaMask prompts)
4. Connected immediately
```

### After Connected (Same Session)

```
1. Browse feed → Wallet button green
2. Go to market detail → Trade section visible
3. Select YES/NO outcome → Amount input visible
4. Enter amount → Place Trade button enabled
5. Click Place Trade → Transaction sent to blockchain
```

## Testing Instructions

### For Roy (iPhone)

**Test 1: Fresh Connection**
1. Open https://proliferative-daleyza-benthonic.ngrok-free.dev in Safari
2. Click wallet icon (top right)
3. Confirm "MetaMask app will open"
4. In MetaMask app, click wallet icon again
5. Approve all MetaMask prompts
6. Verify: "Wallet Connected" alert shows
7. Verify: Wallet icon turns green

**Test 2: Navigate After Connected**
1. After Test 1, scroll feed
2. Click any market
3. Verify: "Connect Wallet to Trade" button NOT shown
4. Verify: Trade section visible with YES/NO options
5. Select YES → Verify amount input appears
6. Enter "10" → Verify "Place Trade" button enabled

**Test 3: Already in MetaMask Browser**
1. Open MetaMask app
2. Browse to https://proliferative-daleyza-benthonic.ngrok-free.dev
3. Click wallet icon
4. Approve prompts
5. Verify: Connects immediately (no deep link needed)

### Expected Behavior

**✅ Wallet button should:**
- Show modal/connect (not just alert)
- Request MetaMask permissions
- Switch to Arbitrum
- Fetch USDT balance
- Store connection
- Turn green when connected

**❌ Wallet button should NOT:**
- Just show alert and do nothing
- Fail silently
- Stay same color after connection
- Require going to detail page first

## Related Issues

- DEPLOYMENT_v87.md - Original wallet integration
- DEPLOYMENT_v88.md - Wallet disconnect functionality
- DEPLOYMENT_v128.md - MetaMask mobile deep linking added

## Notes

### Why Reload After Connect?

After connecting wallet:
- Need to update all UI elements (buttons, states)
- Easier than manually updating every wallet-aware component
- sessionStorage persists across reload
- Clean slate ensures consistency

Could be optimized in future to avoid reload, but reload is safest for MVP.

### Why sessionStorage not Cookies?

**sessionStorage advantages:**
- Tab-scoped (each tab can have different wallet)
- Expires when browser closes (security)
- Not sent to server (privacy)
- Easy to read/write from JavaScript

**Cookies disadvantages:**
- Sent with every request (overhead)
- Shared across tabs (confusing for multiple wallets)
- Require server-side parsing
- More complex to manage

### Deep Link Behavior

**MetaMask deep link format:**
```
https://metamask.app.link/dapp/{url_without_protocol}
```

**Example:**
```
Current URL: https://proliferative-daleyza-benthonic.ngrok-free.dev
Deep link: https://metamask.app.link/dapp/proliferative-daleyza-benthonic.ngrok-free.dev
```

**What happens:**
1. Opens MetaMask app (if installed)
2. MetaMask's in-app browser loads the URL
3. Site detects `window.ethereum` is available
4. Can connect directly

**Fallback:**
If MetaMask not installed → Shows "Install MetaMask" prompt (handled by MetaMask's link)

---

**Update Time**: ~15 minutes  
**Status**: ✅ LIVE  
**Version**: v158  
**Wallet Connection**: Now works on mobile feed  
**Site URL**: https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## Summary

✅ Mobile wallet button now actually connects (not just alert)  
✅ Full MetaMask integration on mobile feed  
✅ Wallet state restores on page load  
✅ Button shows connected state (green)  
✅ Deep link works for non-MetaMask browsers  
✅ Ready for mobile trading

Roy can now connect his wallet directly from the mobile feed and proceed to trade on market detail pages!

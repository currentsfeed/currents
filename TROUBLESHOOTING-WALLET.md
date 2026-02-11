# 🔧 Wallet Connection Troubleshooting

**Issue**: "Failed to connect wallet"

---

## 📋 **Quick Fixes (Try These First)**

### 1. **Check Browser Console**
**Most important step!**

1. Open browser Developer Tools:
   - Chrome/Edge: Press `F12` or `Ctrl+Shift+I`
   - Mac: `Cmd+Option+I`
2. Click **Console** tab
3. Refresh the page
4. Look for **red errors**
5. **Take a screenshot** of any errors and send to me

### 2. **Clear Browser Cache**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Or try **Incognito/Private window**

### 3. **Check MetaMask**
- Is MetaMask installed?
- Is MetaMask unlocked?
- Is MetaMask on Polygon network?
- Try disconnecting all sites in MetaMask → Settings → Connected Sites

### 4. **Check URL**
Are you on the correct URL?
- ✅ https://poor-hands-slide.loca.lt/wallet-demo
- ❌ NOT http://localhost:8080/wallet_v2.html

---

## 🔍 **Common Errors & Fixes**

### **Error: "WalletConnectProvider is not defined"**
**Cause**: CDN libraries not loading

**Fix**: Check if blocked by ad blocker or firewall
- Disable ad blocker
- Try different browser
- Check if `cdn.jsdelivr.net` is accessible

### **Error: "User rejected the request"**
**Cause**: You clicked "Cancel" in MetaMask

**Fix**: Click "Connect Wallet" again and approve

### **Error: "Unsupported chain id"**
**Cause**: MetaMask is on wrong network

**Fix**:
1. Open MetaMask
2. Click network dropdown (top left)
3. Select "Polygon Mainnet"
4. If not in list, add it:
   - Network Name: Polygon Mainnet
   - RPC: https://polygon-rpc.com
   - Chain ID: 137
   - Symbol: MATIC
   - Explorer: https://polygonscan.com

### **Error: "No injected provider found"**
**Cause**: MetaMask not installed or not enabled

**Fix**:
1. Install MetaMask: https://metamask.io/download/
2. Create wallet or import existing
3. Refresh page

---

## 🧪 **Step-by-Step Debug**

### **Test 1: Check Page Loads**
1. Visit: https://poor-hands-slide.loca.lt/wallet-demo
2. Enter password: `35.172.150.243`
3. Page should show "Connection Status" with red dot
4. Button should say "Connect Wallet"

**If page doesn't load**: Send me screenshot

### **Test 2: Check Browser Console**
1. Press F12
2. Click Console tab
3. Look for errors (red text)
4. Take screenshot
5. Send to me

### **Test 3: Check Network Tab**
1. In Developer Tools, click **Network** tab
2. Refresh page
3. Look for failed requests (red)
4. Check if these load:
   - `@walletconnect/web3-provider@1.8.0`
   - `ethers@5.7.2`

### **Test 4: Test MetaMask Directly**
1. Open MetaMask
2. Click three dots (top right)
3. Click "Connected sites"
4. If poor-hands-slide.loca.lt is there, disconnect it
5. Try connecting again

---

## 💻 **Try Different Browser**

Sometimes one browser works better:
- ✅ Chrome (best support)
- ✅ Brave (works well)
- ✅ Firefox (works)
- ⚠️ Safari (sometimes issues)

---

## 📱 **Try Mobile Instead**

If desktop isn't working, try mobile:

1. **Open MetaMask app** on phone
2. **Use in-app browser** (don't use Chrome/Safari)
3. Visit: https://poor-hands-slide.loca.lt/wallet-demo
4. Enter password
5. Click "Connect Wallet"
6. Should auto-connect (no need for QR)

---

## 🔬 **What I Need From You**

Send me screenshots of:
1. **Browser console errors** (F12 → Console tab)
2. **The exact error message** you see
3. **Which page** you're on (copy full URL)
4. **Which browser** you're using
5. **MetaMask version** (MetaMask → Settings → About)

---

## 🚀 **Quick Test URLs**

Try each of these and tell me which works:

1. **Wallet Demo**: https://poor-hands-slide.loca.lt/wallet-demo
2. **Transaction Demo**: https://poor-hands-slide.loca.lt/wallet-transactions
3. **Main Site**: https://poor-hands-slide.loca.lt/

Password for all: `35.172.150.243`

---

## 🔧 **Manual Console Test**

If nothing works, try this in browser console (F12 → Console):

```javascript
// Test 1: Check if libraries loaded
console.log('WalletConnectProvider:', typeof WalletConnectProvider);
console.log('ethers:', typeof ethers);

// Test 2: Check if MetaMask exists
console.log('MetaMask:', typeof window.ethereum);

// Test 3: Try manual connection
if (window.ethereum) {
    window.ethereum.request({ method: 'eth_requestAccounts' })
        .then(accounts => console.log('Connected:', accounts[0]))
        .catch(err => console.error('Error:', err));
}
```

Send me the output!

---

## ⚡ **Emergency Fallback**

If wallet demo pages don't work at all, we can:

1. Integrate wallet directly into main Currents site
2. Use different library (Ethers.js + Metamask SDK)
3. Build custom connector
4. Try RainbowKit or Web3Modal alternative

**But first**, send me those console errors so I know what's actually failing!

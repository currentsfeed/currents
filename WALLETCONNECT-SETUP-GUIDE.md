# 🔑 WalletConnect Setup Guide for Roy

**You have a WalletConnect account. Here's what to do next:**

---

## Step 1: Get Your Project ID

1. Go to https://cloud.walletconnect.com/
2. Sign in with your account
3. You should see your project (or create a new one)
4. Click on the project
5. Copy the **Project ID** (looks like: `a1b2c3d4e5f6g7h8...`)

**Screenshot areas to look for:**
- Dashboard → Your Project → Project ID
- Settings → Project ID

---

## Step 2: Configure Project Settings

While in the WalletConnect Cloud dashboard:

### **Basic Info:**
- **Name**: Currents
- **Description**: Belief-Driven Prediction Markets
- **Homepage**: https://poor-hands-slide.loca.lt (or your production domain)

### **Allowed Domains** (add these):
```
poor-hands-slide.loca.lt
localhost
127.0.0.1
```

### **Verified Domains** (optional, for production):
- Add your production domain when ready

### **Platform:**
- Select: **Web**

---

## Step 3: Send Me the Project ID

Once you have the Project ID, send it to me in the format:

```
Project ID: a1b2c3d4e5f6g7h8...
```

I'll configure it immediately.

---

## Step 4: What Happens Next

### I will:
1. ✅ Update config files with your Project ID
2. ✅ Fix the current wallet implementation (based on Shraga's review)
3. ✅ Test wallet connection
4. ✅ Restart services

### Parallel Agent will:
1. ✅ Build a NEW working wallet implementation from scratch
2. ✅ Use proven WalletConnect v2 patterns
3. ✅ Create demo transaction page
4. ✅ Provide integration guide

---

## What You Can Test (After Setup)

### Test 1: Connect Wallet
```
1. Visit: https://poor-hands-slide.loca.lt
2. Click "Connect Wallet" (header)
3. Choose wallet (MetaMask or WalletConnect mobile)
4. Approve connection
5. Should show: "0x1234...5678" (your address)
```

### Test 2: Network Validation
```
1. Connect wallet on wrong network (e.g., Ethereum)
2. System should prompt to switch to Polygon
3. Approve network switch
4. Should continue normally
```

### Test 3: Position Placement
```
1. Connect wallet (Polygon network)
2. Go to market detail page
3. Select an option
4. Click "Place Position"
5. Modal opens with amount input
6. Enter amount (e.g., 100 USDC)
7. See fee calculation (5%)
8. Click "Confirm Position"
9. Approve transaction in wallet
10. Wait for confirmation
```

---

## Troubleshooting

### "Failed to connect wallet"
**Possible causes:**
- Wrong Project ID
- Wallet extension not installed
- Network issues
- Project ID not approved yet (takes a few minutes)

**Try:**
1. Refresh page
2. Clear browser cache
3. Try incognito window
4. Check browser console (F12) for errors

### "Wrong network" message
**Fix:**
1. Open MetaMask
2. Click network dropdown
3. Select "Polygon Mainnet"
4. If not in list, add it:
   - Network Name: Polygon Mainnet
   - RPC URL: https://polygon-rpc.com
   - Chain ID: 137
   - Currency Symbol: MATIC
   - Block Explorer: https://polygonscan.com

### "Transaction failed"
**Possible causes:**
- Insufficient MATIC for gas
- Insufficient USDC balance
- Network congestion
- Contract not approved

**Check:**
1. MATIC balance (need ~0.01 for gas)
2. USDC balance
3. PolygonScan transaction details

---

## Optional: Advanced Settings

### Rate Limiting
- Default is fine for now
- Can adjust later if needed

### Analytics
- Enable to track wallet connection rates
- See which wallets users prefer
- Monitor connection success rate

### Notifications
- Set up email alerts for:
  - High error rates
  - Unusual activity
  - Rate limit hits

---

## What's Next After Setup

### Phase 1: Testing (This Week)
- ✅ Wallet connects successfully
- ✅ Network validation works
- ✅ Position modal displays

### Phase 2: Rain Integration (Week 2)
- 🔜 Install Rain Protocol SDK
- 🔜 Integrate smart contracts
- 🔜 Real USDC transactions
- 🔜 Position recording on-chain

### Phase 3: Production (Week 3-4)
- 🔜 Security audit
- 🔜 Load testing
- 🔜 Monitoring setup
- 🔜 Production deployment

---

## Support

If you hit any issues:
1. Check browser console (F12 → Console tab)
2. Check WalletConnect dashboard for errors
3. Send me screenshots
4. Send me error messages

---

**Ready to proceed? Send me that Project ID!** 🚀

# 🔗 WalletConnect Integration - Currents

**Status**: Implemented (Demo Mode)  
**Version**: v26  
**Protocol**: WalletConnect v2 + Web3Modal  
**Chain**: Polygon (137)

---

## 📋 Implementation Overview

WalletConnect has been integrated into Currents to enable:
- Wallet connection (MetaMask, WalletConnect, Coinbase Wallet, etc.)
- Position placement on prediction markets
- Transaction signing
- Balance checking
- Multi-wallet support

---

## 🎯 Key Features

### 1. **Connect Wallet Button**
- Located in header (top-right)
- Orange button: "Connect Wallet"
- Green when connected: "0x1234...5678"
- Click to show wallet menu (copy address, disconnect)

### 2. **Wallet State Management**
- Persists connection across page reloads (localStorage)
- Listens for account changes
- Listens for network changes
- Handles disconnection events

### 3. **Position Placement Flow**
1. User selects market option
2. User clicks "Place Position"
3. If not connected → Prompt to connect wallet
4. If connected → Show position modal
5. User enters amount (USDC)
6. Show fees and potential return
7. User confirms → Sign transaction
8. Position placed on Rain protocol

### 4. **Supported Networks**
- **Primary**: Polygon (137)
- **RPC**: https://polygon-rpc.com
- **Currency**: MATIC
- **Explorer**: PolygonScan

---

## 🛠️ Technical Stack

### Libraries Used
```html
<!-- Web3Modal v3 -->
<script src="https://cdn.jsdelivr.net/npm/@web3modal/wagmi@latest/dist/index.umd.js"></script>

<!-- Wagmi Core -->
<script src="https://cdn.jsdelivr.net/npm/@wagmi/core@latest/dist/index.umd.js"></script>

<!-- Viem (Ethereum library) -->
<script src="https://cdn.jsdelivr.net/npm/viem@latest/dist/index.umd.js"></script>
```

### Configuration
```javascript
const projectId = 'YOUR_WALLETCONNECT_PROJECT_ID';
const chains = [{
    id: 137,
    name: 'Polygon',
    network: 'polygon',
    nativeCurrency: {
        decimals: 18,
        name: 'MATIC',
        symbol: 'MATIC',
    },
    rpcUrls: {
        default: 'https://polygon-rpc.com',
    },
    blockExplorers: {
        default: { name: 'PolygonScan', url: 'https://polygonscan.com' },
    },
}];
```

---

## 📁 Files Modified

### 1. `templates/wallet_connect.html` (NEW)
- WalletConnect initialization
- Wallet state management
- UI update functions
- Event listeners
- **8KB** of wallet logic

### 2. `templates/base.html` (UPDATED)
- Added `id="connect-wallet-btn"` to header button
- Added `onclick="walletConnect.connect()"`
- Included `wallet_connect.html` at bottom
- Made button dynamic (changes to address when connected)

### 3. `templates/detail.html` (UPDATED)
- Modified "Place Position" button click handler
- Checks wallet connection before showing modal
- Added position placement modal UI
- Integrated with wallet state
- Shows fees and potential returns
- **120 lines** of new JavaScript

---

## 🔐 Security Features

### 1. **Client-Side Only**
- No private keys stored on server
- User controls wallet via browser extension
- Transactions signed locally

### 2. **State Persistence**
- Only stores public address in localStorage
- No sensitive data cached
- User can disconnect anytime

### 3. **Network Validation**
- Checks user is on Polygon network
- Prompts to switch if wrong network
- Reloads page on network change

### 4. **Transaction Safety**
- Shows full transaction details before signing
- Displays fee breakdown (5%)
- User must approve each transaction

---

## 💰 Fee Structure Display

When placing a position, users see:

```
Amount: 100 USDC
Trading fee (5%): 5 USDC
Net amount: 95 USDC
Potential return: [calculated based on probability]
```

Breakdown matches Rain protocol fees:
- Protocol: 2.50%
- LP: 1.10%
- Market Creator: 1.00%
- Resolver: 0.20%
- Resolution Proposer: 0.10%
- **Total**: 5.00%

---

## 🎨 UI/UX Flow

### Initial State (Not Connected)
```
Header: [Connect Wallet] (orange button)
Detail Page: [Select an option to continue] (disabled)
```

### After Selecting Option (Not Connected)
```
Header: [Connect Wallet] (orange button)
Detail Page: [Connect Wallet to Continue] (disabled, gray)
```

### After Connecting Wallet
```
Header: [0x1234...5678] (green button)
Detail Page: [Place Position] (enabled, orange)
```

### After Selecting Option (Connected)
```
Header: [0x1234...5678] (green button)
Detail Page: [Place Position] (enabled, orange)
Click → Position Modal Opens
```

### Position Modal
```
┌─────────────────────────────────┐
│ Place Position                  │
├─────────────────────────────────┤
│ Selected Option:                │
│ ┌─────────────────────────────┐ │
│ │ Immigration/Border action   │ │
│ │ Current probability: 45%    │ │
│ └─────────────────────────────┘ │
│                                 │
│ Amount (USDC):                  │
│ ┌─────────────────────────────┐ │
│ │ 100.00                      │ │
│ └─────────────────────────────┘ │
│                                 │
│ You'll receive if correct:      │
│ 211.11 USDC                     │
│ Trading fee (5%): 5.00 USDC     │
│                                 │
│ Connected: 0x1234...5678        │
│                                 │
│ [Cancel]  [Confirm Position]    │
└─────────────────────────────────┘
```

---

## 🚀 Setup Instructions

### 1. Get WalletConnect Project ID
```
1. Visit: https://cloud.walletconnect.com/
2. Create account
3. Create new project
4. Copy Project ID
```

### 2. Update Configuration
Edit `templates/wallet_connect.html`:
```javascript
const projectId = 'YOUR_WALLETCONNECT_PROJECT_ID';
```

Replace with your actual project ID.

### 3. Test Locally
```bash
# Restart Flask app
cd /home/ubuntu/.openclaw/workspace/currents-full-local
pkill -f "python3 app.py"
python3 app.py > /tmp/currents-app.log 2>&1 &

# Visit: http://localhost:5555
# Click "Connect Wallet"
```

### 4. Deploy
Already deployed at: https://poor-hands-slide.loca.lt

---

## 🧪 Testing Workflow

### Test 1: Connect Wallet
```
1. Visit Currents homepage
2. Click "Connect Wallet" (header)
3. Choose wallet (MetaMask, WalletConnect, etc.)
4. Approve connection
5. Verify: Button shows "0x1234...5678"
6. Click address → See wallet menu
7. Try "Copy Address"
8. Try "Disconnect"
```

### Test 2: Place Position (Not Connected)
```
1. Visit market detail page
2. Select an option
3. Click "Place Position"
4. Should prompt: "Please connect your wallet..."
5. Click "OK"
6. Wallet connection modal opens
```

### Test 3: Place Position (Connected)
```
1. Connect wallet (see Test 1)
2. Visit market detail page
3. Select an option
4. Click "Place Position"
5. Position modal opens
6. Enter amount: 100
7. Verify fees shown: 5 USDC
8. Verify potential return calculated
9. Click "Confirm Position"
10. Transaction processing... (demo mode)
11. Success message
```

### Test 4: Account Switching
```
1. Connect wallet
2. In MetaMask/wallet, switch accounts
3. Verify: Currents updates address automatically
4. Header button shows new address
```

### Test 5: Network Switching
```
1. Connect wallet on Polygon
2. In wallet, switch to Ethereum mainnet
3. Verify: Page reloads
4. Reconnect to Polygon
```

---

## ⚠️ Known Limitations (Demo Mode)

### 1. **No Actual Transactions**
- Currently simulates transaction with 2-second delay
- Does not interact with Rain protocol smart contracts
- Position is not recorded on-chain

### 2. **Missing Smart Contract Integration**
- Need Rain protocol contract addresses
- Need ABI (Application Binary Interface)
- Need USDC token contract

### 3. **No Balance Checking**
- Doesn't verify user has sufficient USDC
- Doesn't check allowance
- Needs token approval flow

### 4. **No Transaction History**
- Positions not saved to database
- No transaction receipts
- No confirmation emails/notifications

---

## 🔮 Production Roadmap

### Phase 1: Smart Contract Integration (Week 1-2)
```javascript
// Add Rain protocol contract
const RAIN_MARKET_CONTRACT = '0x...';
const RAIN_MARKET_ABI = [...];

// Add USDC contract
const USDC_CONTRACT = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'; // Polygon USDC
const USDC_ABI = [...];

// Check balance
const usdcBalance = await usdcContract.balanceOf(userAddress);

// Check allowance
const allowance = await usdcContract.allowance(userAddress, RAIN_MARKET_CONTRACT);

// Approve if needed
if (allowance < amount) {
    await usdcContract.approve(RAIN_MARKET_CONTRACT, amount);
}

// Place position
const tx = await rainContract.placePosition(marketId, optionId, amount);
await tx.wait();
```

### Phase 2: Position History (Week 3)
- Save positions to database
- Link user_id to wallet address
- Show "My Positions" page
- Display pending/settled positions

### Phase 3: Notifications (Week 4)
- Transaction confirmations
- Position updates
- Market resolution alerts
- Email/push notifications

### Phase 4: Advanced Features (Week 5+)
- Limit orders
- Position sharing
- Portfolio tracking
- P&L charts

---

## 🐛 Troubleshooting

### Issue: "Connect Wallet" button doesn't work
**Solution:**
1. Check browser console for errors
2. Verify WalletConnect libraries loaded
3. Check Project ID is set correctly
4. Try incognito/private window

### Issue: Wrong network error
**Solution:**
1. Open wallet (MetaMask)
2. Switch to Polygon network
3. Refresh page
4. Reconnect wallet

### Issue: Transaction fails
**Solution:**
1. Check wallet has MATIC for gas
2. Check wallet has sufficient USDC
3. Verify allowance is set
4. Try smaller amount

### Issue: Position modal doesn't open
**Solution:**
1. Verify wallet is connected (header shows address)
2. Check option is selected (border should be orange)
3. Open browser console for errors
4. Hard refresh page (Ctrl+Shift+R)

---

## 📊 Metrics to Track

### User Engagement
- Wallet connection rate
- Positions attempted
- Positions completed
- Average position size

### Technical
- Connection success rate
- Transaction success rate
- Average gas cost
- Time to confirmation

### Financial
- Total volume (USDC)
- Total fees collected
- Active wallets (24h/7d/30d)
- Repeat users

---

## 🔗 Resources

- **WalletConnect Docs**: https://docs.walletconnect.com/
- **Web3Modal Docs**: https://docs.walletconnect.com/web3modal/about
- **Polygon Docs**: https://docs.polygon.technology/
- **Rain Protocol**: (coming soon)
- **USDC Contract**: https://polygonscan.com/token/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174

---

## ✅ Review Checklist (for Shraga)

- [ ] WalletConnect integration properly initialized
- [ ] Wallet state management secure
- [ ] UI updates correctly on connect/disconnect
- [ ] Position modal shows correct calculations
- [ ] Fee structure matches Rain protocol (5%)
- [ ] Error handling for failed connections
- [ ] Network validation (Polygon only)
- [ ] Transaction flow is clear to users
- [ ] No private keys or sensitive data exposed
- [ ] Ready for smart contract integration

---

**Implemented**: 2026-02-10  
**Status**: Demo mode (no real transactions)  
**Next**: Get Rain protocol contracts and integrate

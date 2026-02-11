# 🌧️ Rain Protocol SDK Integration

**Package**: `@rainprotocolsdk/sdk`  
**Version**: 1.1.1  
**NPM**: https://www.npmjs.com/package/@rainprotocolsdk/sdk  
**Status**: Installing...

---

## 📦 Installation

```bash
npm install @rainprotocolsdk/sdk
```

---

## 🔗 Integration with WalletConnect

The Rain SDK will be integrated with our existing WalletConnect implementation to enable:
- Market creation
- Position placement
- Order management
- Settlement handling
- Balance queries

---

## 📋 Integration Plan

### Phase 1: SDK Setup (Current)
```javascript
// Import Rain SDK
import { RainSDK } from '@rainprotocolsdk/sdk';

// Initialize with provider from WalletConnect
const rainSDK = new RainSDK({
    provider: window.walletConnect.getProvider(),
    network: 'polygon'  // Chain ID 137
});
```

### Phase 2: Market Queries
```javascript
// Get market details
async function getMarketDetails(marketId) {
    const market = await rainSDK.markets.getMarket(marketId);
    return market;
}

// Get market options
async function getMarketOptions(marketId) {
    const options = await rainSDK.markets.getOptions(marketId);
    return options;
}

// Get market orders
async function getMarketOrders(marketId) {
    const orders = await rainSDK.markets.getOrders(marketId);
    return orders;
}
```

### Phase 3: Position Placement
```javascript
// Place a position on a market
async function placePosition(marketId, optionId, amount) {
    try {
        // Check USDC balance
        const balance = await rainSDK.tokens.balanceOf(
            userAddress,
            USDC_ADDRESS
        );
        
        if (balance < amount) {
            throw new Error('Insufficient USDC balance');
        }
        
        // Check allowance
        const allowance = await rainSDK.tokens.allowance(
            userAddress,
            rainSDK.contracts.marketContract
        );
        
        // Approve if needed
        if (allowance < amount) {
            const approveTx = await rainSDK.tokens.approve(
                rainSDK.contracts.marketContract,
                amount
            );
            await approveTx.wait();
        }
        
        // Place position
        const tx = await rainSDK.markets.placePosition({
            marketId,
            optionId,
            amount,
            userAddress
        });
        
        // Wait for confirmation
        const receipt = await tx.wait();
        
        return receipt;
        
    } catch (error) {
        console.error('Failed to place position:', error);
        throw error;
    }
}
```

### Phase 4: Order Management
```javascript
// Cancel an order
async function cancelOrder(orderId) {
    const tx = await rainSDK.markets.cancelOrder(orderId);
    return await tx.wait();
}

// Get user positions
async function getUserPositions(userAddress) {
    const positions = await rainSDK.markets.getUserPositions(userAddress);
    return positions;
}

// Get user order history
async function getUserOrderHistory(userAddress) {
    const orders = await rainSDK.markets.getUserOrders(userAddress);
    return orders;
}
```

---

## 🔄 Updated WalletConnect Integration

### Modified `wallet_connect.html`

```javascript
// Add Rain SDK import (after WalletConnect libraries)
<script type="module">
import { RainSDK } from '/node_modules/@rainprotocolsdk/sdk/dist/index.js';

// Global Rain SDK instance
let rainSDK;

// Initialize Rain SDK after wallet connection
async function initRainSDK(provider) {
    try {
        rainSDK = new RainSDK({
            provider,
            network: 'polygon'
        });
        
        console.log('Rain SDK initialized');
        window.rainSDK = rainSDK;
        
    } catch (error) {
        console.error('Failed to initialize Rain SDK:', error);
    }
}

// Update connectWallet function
async function connectWallet() {
    try {
        // ... existing wallet connection code ...
        
        // Initialize Rain SDK
        await initRainSDK(provider);
        
        // Update UI
        updateWalletUI(userAddress, true);
        
    } catch (error) {
        console.error('Failed to connect wallet:', error);
    }
}

// Export Rain SDK for use in other scripts
window.rainSDK = {
    getInstance: () => rainSDK,
    placePosition: async (marketId, optionId, amount) => {
        if (!rainSDK) throw new Error('Rain SDK not initialized');
        return await rainSDK.markets.placePosition({
            marketId,
            optionId,
            amount,
            userAddress
        });
    }
};
</script>
```

---

## 🎯 Updated Position Placement Flow

### Modified `detail.html`

```javascript
// Place position using Rain SDK
async function placePosition() {
    const amountInput = document.getElementById('position-amount');
    const amount = parseFloat(amountInput.value);
    
    if (!amount || amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }
    
    try {
        // Show loading state
        const confirmBtn = event.target;
        confirmBtn.textContent = 'Processing...';
        confirmBtn.disabled = true;
        
        // Get market and option IDs
        const marketId = '{{ market.market_id }}';
        const optionId = selectedOption.optionId;
        
        // Convert to Wei (USDC has 6 decimals)
        const amountWei = Math.floor(amount * 1e6);
        
        // Call Rain SDK
        const receipt = await window.rainSDK.placePosition(
            marketId,
            optionId,
            amountWei
        );
        
        console.log('Position placed:', receipt);
        
        // Show success message
        alert('Position placed successfully!');
        
        // Close modal
        confirmBtn.parentElement.parentElement.parentElement.remove();
        
        // Refresh market data
        window.location.reload();
        
    } catch (error) {
        console.error('Failed to place position:', error);
        
        let errorMsg = 'Failed to place position. ';
        if (error.message.includes('insufficient')) {
            errorMsg += 'Insufficient balance.';
        } else if (error.message.includes('allowance')) {
            errorMsg += 'Token approval required.';
        } else {
            errorMsg += error.message;
        }
        
        alert(errorMsg);
        
        // Reset button
        const confirmBtn = event.target;
        confirmBtn.textContent = 'Confirm Position';
        confirmBtn.disabled = false;
    }
}
```

---

## 📊 Market Data Sync

### Fetch market data from Rain Protocol

```javascript
// Update BRain database with Rain protocol data
async function syncMarketData(marketId) {
    try {
        // Fetch from Rain SDK
        const market = await rainSDK.markets.getMarket(marketId);
        const options = await rainSDK.markets.getOptions(marketId);
        
        // Update local database via API
        await fetch('/api/markets/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                market_id: marketId,
                data: market,
                options: options
            })
        });
        
    } catch (error) {
        console.error('Failed to sync market data:', error);
    }
}

// Sync on page load
document.addEventListener('DOMContentLoaded', async () => {
    if (window.rainSDK) {
        const marketId = '{{ market.market_id }}';
        await syncMarketData(marketId);
    }
});
```

---

## 🔐 Security Considerations

### 1. **Transaction Signing**
- All transactions signed by user's wallet
- No private keys stored
- User approves each action

### 2. **Amount Validation**
- Check user balance before transaction
- Verify allowance
- Validate amounts client-side and contract-side

### 3. **Error Handling**
- Graceful failure for network issues
- Clear error messages for users
- Retry logic for transient failures

### 4. **Gas Estimation**
- Estimate gas before transaction
- Warn user about high gas costs
- Allow gas price customization

---

## 🧪 Testing Plan

### Test 1: SDK Initialization
```javascript
// Should initialize without errors
console.log(window.rainSDK);  // Should not be undefined
```

### Test 2: Market Query
```javascript
// Should fetch market details
const market = await rainSDK.markets.getMarket('multi_001');
console.log(market);
```

### Test 3: Balance Check
```javascript
// Should return USDC balance
const balance = await rainSDK.tokens.balanceOf(userAddress, USDC_ADDRESS);
console.log('Balance:', balance / 1e6, 'USDC');
```

### Test 4: Position Placement
```javascript
// Should place position and return receipt
const receipt = await rainSDK.markets.placePosition({
    marketId: 'multi_001',
    optionId: 'option_1',
    amount: 100e6  // 100 USDC (6 decimals)
});
console.log('Transaction:', receipt.transactionHash);
```

---

## 📚 Documentation Needs

Once SDK is installed, document:
1. Available methods
2. Contract addresses
3. Event listening
4. Error codes
5. Gas optimization tips

---

## 🚀 Deployment Checklist

- [ ] Install Rain SDK (`npm install @rainprotocolsdk/sdk`)
- [ ] Configure SDK with Polygon network
- [ ] Update WalletConnect integration
- [ ] Implement position placement
- [ ] Add balance checking
- [ ] Add token approval flow
- [ ] Test on testnet first
- [ ] Add error handling
- [ ] Add loading states
- [ ] Add transaction confirmations
- [ ] Document API usage
- [ ] Add monitoring/analytics

---

**Status**: Installing SDK now  
**Next**: Explore SDK API and integrate with WalletConnect  
**Timeline**: 1-2 days for full integration

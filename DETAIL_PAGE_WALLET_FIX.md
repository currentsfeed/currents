# Detail Page Wallet Fix - v88

**Issues reported by Roy:**
1. Wallet connection loop - doesn't recognize already connected
2. Shows ETH instead of USDT
3. Need trading UI with simulated trades

**Root cause:** detail.html has duplicate wallet code not synced with base.html

**Fix plan:**
1. Remove duplicate wallet functions from detail.html
2. Use global wallet functions from base.html
3. Add wallet connection check on page load
4. Add trading UI that appears when wallet connected
5. Implement simulated trading (no real transactions)

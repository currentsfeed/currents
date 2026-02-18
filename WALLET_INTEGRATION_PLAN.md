# Wallet Integration Plan

**Status:** Future Implementation  
**Priority:** Post-MVP  
**Documented:** 2026-02-12 15:23 UTC

## Requirements from Roy

### 1. Test User Mode ✅ (Implemented v109)
**Current behavior:**
- Test user selected (user1, user2, roy, etc.) → All interactions track to that user
- Badge shows current tracking user in debug panel
- Console logs show which user is being tracked

**Status:** ✅ Working

---

### 2. Anonymous Cookie Mode ✅ (Implemented v109)
**Current behavior:**
- No test user selected → System generates `anon_XXXXX` key
- Key stored in localStorage for persistence
- Full personalization tracking works for anonymous users
- Badge shows "anon" in debug panel

**Status:** ✅ Working

---

### 3. Wallet Connection → Inherit Cookie Data 🔄 (Future)
**Requirement:**
When user connects wallet, all existing cookie/localStorage data should transfer to wallet address.

**Implementation Plan:**

```javascript
// When wallet connects successfully
async function onWalletConnected(walletAddress) {
    // 1. Get current user key (from cookie or localStorage)
    const currentUserKey = getUserKey();  // e.g., "anon_abc123xyz"
    
    // 2. Check if this wallet has existing data
    const walletProfile = await fetch(`/api/user/profile/${walletAddress}`);
    
    if (!walletProfile.exists && currentUserKey.startsWith('anon_')) {
        // 3. Transfer anonymous data to wallet
        await fetch('/api/user/transfer-to-wallet', {
            method: 'POST',
            body: JSON.stringify({
                from_key: currentUserKey,
                to_wallet: walletAddress
            })
        });
        
        console.log('[Wallet] Transferred data from', currentUserKey, 'to', walletAddress);
    }
    
    // 4. Set wallet as current user key
    sessionStorage.setItem('currents_wallet', walletAddress);
    
    // 5. Update tracking to use wallet address
    // All future interactions now track to wallet
}
```

**Backend Requirements:**
```python
@app.route('/api/user/transfer-to-wallet', methods=['POST'])
def transfer_to_wallet():
    """
    Transfer user data from cookie/anon key to wallet address
    """
    data = request.get_json()
    from_key = data['from_key']
    to_wallet = data['to_wallet']
    
    # Transfer interactions
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Update all interactions
    cursor.execute("""
        UPDATE interactions 
        SET user_key = ? 
        WHERE user_key = ?
    """, (to_wallet, from_key))
    
    # Update or merge profile scores
    cursor.execute("""
        UPDATE user_profiles 
        SET user_key = ? 
        WHERE user_key = ?
    """, (to_wallet, from_key))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})
```

**getUserKey() Update:**
```javascript
function getUserKey() {
    // 1. Check if wallet is connected (highest priority)
    const wallet = sessionStorage.getItem('currents_wallet');
    if (wallet) {
        console.log('[Tracking] Using wallet:', wallet);
        return wallet;
    }
    
    // 2. Check for test user cookie
    const testUser = getCookie('currents_test_user');
    if (testUser) {
        console.log('[Tracking] Using test user:', testUser);
        return testUser;
    }
    
    // 3. Get or create anonymous key
    let anonKey = localStorage.getItem('currents_user_key');
    if (!anonKey) {
        anonKey = 'anon_' + randomString(9);
        localStorage.setItem('currents_user_key', anonKey);
    }
    console.log('[Tracking] Using anonymous:', anonKey);
    return anonKey;
}
```

---

### 4. Wallet Disconnect → Transfer Back to Cookie 🔄 (Future)
**Requirement:**
When user disconnects wallet, transfer all wallet data back to cookie so flow is seamless.

**Implementation Plan:**

```javascript
async function onWalletDisconnected(walletAddress) {
    // 1. Generate new anonymous key (or reuse existing)
    let anonKey = localStorage.getItem('currents_user_key');
    if (!anonKey) {
        anonKey = 'anon_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('currents_user_key', anonKey);
    }
    
    // 2. Transfer wallet data to anonymous key
    await fetch('/api/user/transfer-from-wallet', {
        method: 'POST',
        body: JSON.stringify({
            from_wallet: walletAddress,
            to_key: anonKey
        })
    });
    
    console.log('[Wallet] Transferred data from', walletAddress, 'to', anonKey);
    
    // 3. Clear wallet from session
    sessionStorage.removeItem('currents_wallet');
    
    // 4. Update UI
    updateUserBadge(anonKey);
}
```

**Backend Requirements:**
```python
@app.route('/api/user/transfer-from-wallet', methods=['POST'])
def transfer_from_wallet():
    """
    Transfer user data from wallet back to cookie key
    """
    data = request.get_json()
    from_wallet = data['from_wallet']
    to_key = data['to_key']
    
    # Transfer interactions
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Update all interactions
    cursor.execute("""
        UPDATE interactions 
        SET user_key = ? 
        WHERE user_key = ?
    """, (to_key, from_wallet))
    
    # Update profile
    cursor.execute("""
        UPDATE user_profiles 
        SET user_key = ? 
        WHERE user_key = ?
    """, (to_key, from_wallet))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})
```

---

## User Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│  User Journey with Wallet Integration                  │
└─────────────────────────────────────────────────────────┘

1. Initial Visit (No Wallet, No Cookie)
   → Generate anon_abc123xyz
   → Store in localStorage
   → Track interactions
   → Build personalization profile

2. Connect Wallet (0x742d35Cc...)
   → Check wallet has no existing data
   → Transfer anon_abc123xyz data → 0x742d35Cc...
   → Set wallet as user_key
   → Clear/archive anonymous key
   → Continue tracking to wallet

3. Browse with Wallet Connected
   → All interactions track to 0x742d35Cc...
   → Personalization continues building
   → Can see wallet address in debug badge

4. Disconnect Wallet
   → Transfer 0x742d35Cc... data → new anon_xyz789def
   → Set anonymous key as user_key
   → Clear wallet from session
   → Seamless transition, no data loss

5. Reconnect Same Wallet Later
   → Recognize 0x742d35Cc...
   → Restore full profile
   → Merge any new anonymous data if exists
   → Continue where user left off
```

---

## Database Schema

### Current Implementation ✅
```sql
CREATE TABLE user_profiles (
    user_key TEXT PRIMARY KEY,  -- Can be: anon_xxx, user1, roy, or 0x742d35Cc...
    total_interactions INTEGER,
    last_active TEXT,
    created_at TEXT
);

CREATE TABLE interactions (
    id INTEGER PRIMARY KEY,
    user_key TEXT,  -- Can be: anon_xxx, user1, roy, or 0x742d35Cc...
    market_id TEXT,
    event_type TEXT,
    timestamp TEXT,
    geo_country TEXT
);
```

**No schema changes needed!** The `user_key` field is already flexible enough to store:
- Anonymous keys: `anon_abc123xyz`
- Test users: `user1`, `user2`, `roy`
- Wallet addresses: `0x742d35Cc6e4C5C07b9c76961fAb1feF91f06B4B6`

---

## Priority Ranking

### v109 (Current) ✅
- [x] Test user tracking
- [x] Anonymous cookie tracking
- [x] Visual user badge
- [x] Console debugging logs
- [x] Seamless switching between modes

### Post-MVP (Future)
- [ ] Wallet connection inherits cookie data
- [ ] Wallet disconnect transfers back to cookie
- [ ] Profile merge conflict resolution
- [ ] Multi-device sync via wallet
- [ ] Wallet-based personalization across dApps

---

## Testing Plan (Future)

### Test Case 1: Anonymous → Wallet → Anonymous
1. Visit site (no wallet)
2. Interact with 5 markets → Profile builds
3. Connect wallet → Data transfers
4. Interact with 5 more markets → Continues tracking
5. Disconnect wallet → Data transfers back
6. Check: All 10 interactions preserved

### Test Case 2: Wallet → Disconnect → Reconnect
1. Connect wallet (no prior data)
2. Interact with 10 markets
3. Disconnect wallet
4. Clear browser (simulate new device)
5. Connect same wallet
6. Check: All 10 interactions restored

### Test Case 3: Multiple Wallets Same Browser
1. Anonymous user interacts (Profile A)
2. Connect Wallet 1 → Transfers Profile A
3. Disconnect Wallet 1
4. Connect Wallet 2 → Starts fresh Profile B
5. Disconnect Wallet 2
6. Connect Wallet 1 again
7. Check: Profile A restored, Profile B separate

---

## Security Considerations

### 1. Wallet Verification
- Always verify wallet signature before data transfer
- Don't trust client-side wallet claims
- Use on-chain proof of ownership

### 2. Data Privacy
- Never expose full wallet address in public APIs
- Show abbreviated addresses: `0x742d...B4B6`
- GDPR: Allow wallet-based data deletion

### 3. Anti-Gaming
- Detect suspicious profile transfers (gaming the system)
- Rate-limit transfer operations
- Flag wallet addresses with unusual activity

---

## Implementation Timeline

**Phase 1 (Current - v109):** ✅ Complete
- Test user tracking
- Anonymous cookie tracking
- Debug tools

**Phase 2 (Post-MVP):**
- Wallet connection API
- Data transfer endpoints
- Profile merge logic

**Phase 3 (Polish):**
- Multi-device sync
- Conflict resolution
- Advanced analytics

---

## Roy's Requirements Summary

✅ **Requirement 1:** Test user selected → future interactions on that user  
✅ **Requirement 2:** No user selected → anonymous cookie  
🔄 **Requirement 3:** Wallet connection → inherit cookie data (future)  
🔄 **Requirement 4:** Wallet disconnect → transfer back to cookie (future)

**Current Status:** Requirements 1 & 2 implemented in v109. Requirements 3 & 4 documented for post-MVP implementation.

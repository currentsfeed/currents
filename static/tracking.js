/**
 * BRain Tracking Client
 * Tracks user interactions and sends to /api/track
 */

(function() {
    // Track page view time
    let pageStartTime = Date.now();
    let currentMarketId = null;
    let eventQueue = [];
    
    // Get or create user key
    function getUserKey() {
        // Check for test user cookie first (from user switcher)
        const testUserMatch = document.cookie.match(/currents_test_user=([^;]+)/);
        if (testUserMatch) {
            const testUser = testUserMatch[1];
            console.log('[BRain Tracking] Test user detected:', testUser);
            return testUser;  // Use test user key (e.g., 'roy', 'user2')
        }
        
        // Otherwise, get or create anonymous key
        let key = localStorage.getItem('currents_user_key');
        if (!key) {
            key = 'anon_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('currents_user_key', key);
            console.log('[BRain Tracking] Created new anonymous key:', key);
        } else {
            console.log('[BRain Tracking] Using anonymous key:', key);
        }
        return key;
    }
    
    // Track event
    function trackEvent(eventType, marketId, extraData = {}) {
        const event = {
            market_id: marketId || currentMarketId,
            event_type: eventType,
            ...extraData
        };
        
        console.log('[BRain Tracking] Event queued:', eventType, 'for market:', marketId || currentMarketId);
        eventQueue.push(event);
        
        // Send batch if queue is large enough or after delay
        if (eventQueue.length >= 5) {
            console.log('[BRain Tracking] Queue full, sending batch now');
            sendBatch();
        } else {
            // Debounced send
            clearTimeout(window.batchTimeout);
            window.batchTimeout = setTimeout(sendBatch, 3000);
        }
    }
    
    // Send batched events
    function sendBatch() {
        if (eventQueue.length === 0) return;
        
        const userKey = getUserKey();
        const events = [...eventQueue];
        eventQueue = [];
        
        const displayKey = userKey.startsWith('anon_') ? 'anonymous' : userKey;
        console.log('[BRain Tracking] Sending batch:', events.length, 'events for user:', displayKey);
        
        fetch('/api/track/batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Key': userKey
            },
            body: JSON.stringify({
                user_key: userKey,
                events: events
            })
        })
        .then(response => {
            if (response.ok) {
                console.log('[BRain Tracking] Batch sent successfully');
            } else {
                console.error('[BRain Tracking] Batch failed:', response.status);
            }
        })
        .catch(err => console.error('[BRain Tracking] Network error:', err));
    }
    
    // Track page view on load
    window.addEventListener('load', function() {
        const userKey = getUserKey();
        const displayKey = userKey.startsWith('anon_') ? 'anonymous' : userKey;
        console.log('[BRain Tracking] ===== SESSION START =====');
        console.log('[BRain Tracking] Tracking as user:', displayKey);
        console.log('[BRain Tracking] Test user cookie:', document.cookie.match(/currents_test_user=([^;]+)/) ? 'SET' : 'NOT SET');
        console.log('[BRain Tracking] Mode:', userKey.startsWith('anon_') ? 'Anonymous' : 'Test User');
        console.log('[BRain Tracking] ===========================');
        
        // Check if we're on a market detail page
        const urlMatch = window.location.pathname.match(/\/market\/([^\/]+)/);
        if (urlMatch) {
            currentMarketId = urlMatch[1];
            trackEvent('view_market', currentMarketId);
        }
    });
    
    // Track dwell time on page unload
    window.addEventListener('beforeunload', function() {
        if (currentMarketId) {
            const dwellMs = Date.now() - pageStartTime;
            
            // Classify dwell
            let eventType = 'view_market';
            if (dwellMs >= 30000) {
                eventType = 'dwell_30+';
            } else if (dwellMs >= 5000) {
                eventType = 'dwell_5+';
            }
            
            // Send immediately (synchronous)
            const userKey = getUserKey();
            navigator.sendBeacon('/api/track', JSON.stringify({
                user_key: userKey,
                market_id: currentMarketId,
                event_type: eventType,
                dwell_ms: dwellMs
            }));
        }
        
        // Send remaining queued events
        if (eventQueue.length > 0) {
            sendBatch();
        }
    });
    
    // Track clicks on market cards
    document.addEventListener('click', function(e) {
        const marketCard = e.target.closest('[data-market-id]');
        if (marketCard) {
            const marketId = marketCard.getAttribute('data-market-id');
            const section = marketCard.getAttribute('data-section') || 'unknown';
            const position = parseInt(marketCard.getAttribute('data-position') || '0');
            
            trackEvent('click', marketId, {
                section: section,
                position: position
            });
        }
    });
    
    // Expose global tracking function for manual events
    window.trackCurrents = trackEvent;
    window.trackEvent = trackEvent;  // Also expose as trackEvent for backward compatibility
    
    // Log tracking initialization with user key
    const userKey = getUserKey();
    const isTestUser = document.cookie.match(/currents_test_user=([^;]+)/) ? true : false;
    console.log(`📊 BRain tracking initialized | User: ${userKey}${isTestUser ? ' (test mode)' : ' (anonymous)'}`);
})();

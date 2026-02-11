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
        let key = localStorage.getItem('currents_user_key');
        if (!key) {
            key = 'anon_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('currents_user_key', key);
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
        
        eventQueue.push(event);
        
        // Send batch if queue is large enough or after delay
        if (eventQueue.length >= 5) {
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
        }).catch(err => console.error('Track error:', err));
    }
    
    // Track page view on load
    window.addEventListener('load', function() {
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
    
    console.log('📊 BRain tracking initialized');
})();

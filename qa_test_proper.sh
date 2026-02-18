#!/bin/bash
# QA Test Script - Using Real Market IDs

BASE_URL="http://localhost:5555"
USER_KEY="qa_proper_$(date +%s)"

echo "🧪 QA Testing Personalization System (PROPER)"
echo "=============================================="
echo "User Key: $USER_KEY"
echo ""

# First, get real NBA market IDs from the database
echo "📊 Fetching real NBA market IDs from database..."
NBA_MARKETS=$(sqlite3 /home/ubuntu/.openclaw/workspace/currents-full-local/brain.db << 'EOF'
SELECT market_id FROM markets WHERE market_id LIKE 'nba%' LIMIT 5;
EOF
)

echo "NBA Markets to test:"
echo "$NBA_MARKETS"
echo ""

# Convert to array
IFS=$'\n' read -r -d '' -a MARKETS_ARRAY <<< "$NBA_MARKETS"

# Test 1: Track Clicks
echo "📊 Test 1: Tracking 5 Click Interactions"
for market in "${MARKETS_ARRAY[@]}"; do
    echo "Tracking click on: $market"
    curl -s -X POST "$BASE_URL/api/track" \
        -H "Content-Type: application/json" \
        -d "{\"user_key\":\"$USER_KEY\",\"market_id\":\"$market\",\"event_type\":\"click\"}" \
        | grep -q "success" && echo "  ✅ Tracked" || echo "  ❌ Failed"
    sleep 0.3
done
echo ""

# Test 2: Track Bookmark
echo "📊 Test 2: Tracking Bookmark/Like"
FIRST_MARKET="${MARKETS_ARRAY[0]}"
curl -s -X POST "$BASE_URL/api/track" \
    -H "Content-Type: application/json" \
    -d "{\"user_key\":\"$USER_KEY\",\"market_id\":\"$FIRST_MARKET\",\"event_type\":\"bookmark\"}" \
    | grep -q "success" && echo "✅ Bookmark tracked" || echo "❌ Bookmark failed"
echo ""

# Wait for profile computation
echo "⏳ Waiting 1 second for profile computation..."
sleep 1

# Test 3: Check Database State
echo "📊 Test 3: Database Verification"
echo ""

sqlite3 /home/ubuntu/.openclaw/workspace/currents-full-local/brain.db << EOF
.mode column
.headers on
.width 40 20

SELECT '=== User Interactions ===' as section;
SELECT COUNT(*) as total_interactions FROM user_interactions WHERE user_key = '$USER_KEY';

SELECT '' as blank;
SELECT '=== User Profile ===' as section;
SELECT user_key, total_interactions, last_active FROM user_profiles WHERE user_key = '$USER_KEY';

SELECT '' as blank;
SELECT '=== Topic Scores ===' as section;
SELECT topic_type, topic_value, ROUND(score, 2) as score 
FROM user_topic_scores 
WHERE user_key = '$USER_KEY' 
ORDER BY score DESC 
LIMIT 10;

SELECT '' as blank;
SELECT '=== Interactions by Type ===' as section;
SELECT event_type, COUNT(*) as count 
FROM user_interactions 
WHERE user_key = '$USER_KEY' 
GROUP BY event_type;
EOF

echo ""

# Test 4: Personalized Feed
echo "📊 Test 4: Personalized Feed Test"
curl -s "$BASE_URL/?user=$USER_KEY" -o /tmp/qa_feed.html

if grep -q "🎯 Personalized feed" /tmp/qa_feed.html; then
    echo "✅ PASS: Personalization banner appears"
else
    echo "⚠️  WARNING: Personalization banner not found"
fi

# Count NBA markets in top 9
NBA_IN_TOP_9=$(grep -o 'data-market-id="[^"]*"' /tmp/qa_feed.html | head -9 | grep -c "nba" || echo "0")
echo "NBA markets in top 9: $NBA_IN_TOP_9"

if [ "$NBA_IN_TOP_9" -ge 2 ]; then
    echo "✅ PASS: NBA markets are ranking higher (personalization working)"
else
    echo "⚠️  INFO: NBA markets in top 9: $NBA_IN_TOP_9"
fi

echo ""
echo "✅ QA Test Complete!"
echo "User Key: $USER_KEY"

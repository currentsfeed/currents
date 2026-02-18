#!/bin/bash
# QA Test Script - Simulate User Interactions

BASE_URL="http://localhost:5555"
USER_KEY="qa_test_user_$(date +%s)"

echo "🧪 QA Testing Personalization System"
echo "====================================="
echo "User Key: $USER_KEY"
echo ""

# Test 1: Homepage Load (No Personalization Yet)
echo "📊 Test 1: Homepage Load (New User - No Personalization)"
curl -s "$BASE_URL/?user=$USER_KEY" -o /tmp/qa_homepage_initial.html
if grep -q "🎯 Personalized feed" /tmp/qa_homepage_initial.html; then
    echo "❌ ERROR: Personalization banner should NOT appear for new user"
else
    echo "✅ PASS: No personalization banner (expected for new user)"
fi
echo ""

# Test 2: Track Click Interactions
echo "📊 Test 2: Tracking Click Interactions (5 clicks)"
NBA_MARKETS=("nba-lakers-celtics-feb14" "nba-warriors-bulls-feb14" "nba-nets-heat-feb14" "nba-mvp-2025-2026" "nba-76ers-nuggets-feb14")

for market in "${NBA_MARKETS[@]}"; do
    echo "Tracking click on: $market"
    curl -s -X POST "$BASE_URL/api/track" \
        -H "Content-Type: application/json" \
        -d "{\"user_key\":\"$USER_KEY\",\"market_id\":\"$market\",\"event_type\":\"click\",\"metadata\":{}}" \
        | grep -q "success" && echo "  ✅ Tracked" || echo "  ❌ Failed"
    sleep 0.5
done
echo ""

# Test 3: Track Like (Bookmark)
echo "📊 Test 3: Tracking Like/Bookmark"
curl -s -X POST "$BASE_URL/api/track" \
    -H "Content-Type: application/json" \
    -d "{\"user_key\":\"$USER_KEY\",\"market_id\":\"nba-lakers-celtics-feb14\",\"event_type\":\"bookmark\",\"metadata\":{}}" \
    | grep -q "success" && echo "✅ PASS: Bookmark tracked" || echo "❌ FAIL: Bookmark not tracked"
echo ""

# Wait for profile computation
echo "⏳ Waiting 2 seconds for profile computation..."
sleep 2

# Test 4: Check Database State
echo "📊 Test 4: Database Verification"
echo ""

sqlite3 /home/ubuntu/.openclaw/workspace/currents-full-local/brain.db << EOF
.mode column
.headers on

SELECT '=== User Interactions ===' as section;
SELECT COUNT(*) as total_interactions FROM user_interactions WHERE user_key = '$USER_KEY';

SELECT '' as blank;
SELECT '=== User Profile ===' as section;
SELECT user_key, total_interactions, created_at FROM user_profiles WHERE user_key = '$USER_KEY';

SELECT '' as blank;
SELECT '=== Top Topic Scores ===' as section;
SELECT topic_type, topic_value, ROUND(score, 3) as score 
FROM user_topic_scores 
WHERE user_key = '$USER_KEY' 
ORDER BY score DESC 
LIMIT 10;

SELECT '' as blank;
SELECT '=== Event Type Breakdown ===' as section;
SELECT event_type, COUNT(*) as count 
FROM user_interactions 
WHERE user_key = '$USER_KEY' 
GROUP BY event_type;
EOF

echo ""

# Test 5: Personalized Feed
echo "📊 Test 5: Personalized Feed (After 5+ Interactions)"
curl -s "$BASE_URL/?user=$USER_KEY" -o /tmp/qa_homepage_personalized.html
if grep -q "🎯 Personalized feed" /tmp/qa_homepage_personalized.html; then
    echo "✅ PASS: Personalization banner appears"
else
    echo "⚠️  WARNING: Personalization banner not found (might need more interactions)"
fi

# Check if NBA markets rank higher
echo ""
echo "Checking market rankings..."
grep -o 'data-market-id="[^"]*"' /tmp/qa_homepage_personalized.html | head -9 | grep -c "nba" > /tmp/qa_nba_count.txt
NBA_COUNT=$(cat /tmp/qa_nba_count.txt)
echo "NBA markets in top 9: $NBA_COUNT"
if [ "$NBA_COUNT" -ge 2 ]; then
    echo "✅ PASS: NBA markets are ranking higher (personalization working)"
else
    echo "⚠️  INFO: NBA markets: $NBA_COUNT in top 9"
fi

echo ""
echo "✅ QA Test Complete!"
echo "User Key: $USER_KEY"

#!/bin/bash
# Quick waitlist checker for Roy

echo "🌊 Currents Waitlist Status"
echo "=========================="
echo ""

# Stats from API
echo "📊 Live Stats (excluding test emails):"
curl -s https://proliferative-daleyza-benthonic.ngrok-free.dev/api/waitlist/stats -H "ngrok-skip-browser-warning: true" | jq .
echo ""

# Recent submissions
echo "📝 Recent Submissions (last 10):"
cd /home/ubuntu/.openclaw/workspace/currents-full-local
sqlite3 brain.db "SELECT 
    id, 
    email, 
    belief_choice, 
    device_type,
    CASE WHEN is_test_submission = 1 THEN '🧪 TEST' ELSE '✅ REAL' END as type,
    datetime(timestamp_submitted) as submitted
FROM waitlist_submissions 
ORDER BY id DESC 
LIMIT 10;" | column -t -s'|'
echo ""

# Total breakdown
echo "📈 Total Breakdown:"
sqlite3 brain.db "SELECT 
    CASE WHEN is_test_submission = 1 THEN '🧪 Test Submissions' ELSE '✅ Real Submissions' END as type,
    COUNT(*) as count,
    SUM(CASE WHEN belief_choice = 'YES' THEN 1 ELSE 0 END) as yes,
    SUM(CASE WHEN belief_choice = 'NO' THEN 1 ELSE 0 END) as no
FROM waitlist_submissions
GROUP BY is_test_submission;" | column -t -s'|'
echo ""

echo "💡 Tip: Use 'testtt' as email for unlimited test submissions"
echo "🔗 Page: https://proliferative-daleyza-benthonic.ngrok-free.dev/coming-soon"

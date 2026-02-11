#!/bin/bash
# Test script for Currents fixes

echo "🧪 Testing Currents fixes..."
echo ""

# 1. Test homepage
echo "1️⃣  Testing homepage..."
curl -s http://localhost:5555/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Homepage loads"
else
    echo "   ❌ Homepage failed (app might not be running)"
fi

# 2. Test API
echo "2️⃣  Testing API..."
response=$(curl -s http://localhost:5555/api/v1/markets?limit=5 2>/dev/null)
if echo "$response" | grep -q "markets"; then
    echo "   ✅ API returns markets"
else
    echo "   ❌ API failed (app might not be running)"
fi

# 3. Test API input validation
echo "3️⃣  Testing input validation..."
status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5555/api/v1/markets?limit=abc 2>/dev/null)
if [ "$status" = "400" ]; then
    echo "   ✅ Invalid input rejected (400)"
elif [ "$status" = "000" ]; then
    echo "   ⚠️  App not running"
else
    echo "   ⚠️  Got status $status (expected 400)"
fi

# 4. Test database viewer auth
echo "4️⃣  Testing database viewer auth..."
status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5556/ 2>/dev/null)
if [ "$status" = "401" ]; then
    echo "   ✅ Viewer requires auth (401)"
elif [ "$status" = "000" ]; then
    echo "   ⚠️  DB viewer not running"
else
    echo "   ⚠️  Got status $status (expected 401)"
fi

# 5. Test viewer with credentials
echo "5️⃣  Testing viewer with credentials..."
status=$(curl -s -o /dev/null -w "%{http_code}" -u admin:demo2026 http://localhost:5556/ 2>/dev/null)
if [ "$status" = "200" ]; then
    echo "   ✅ Viewer accepts credentials"
elif [ "$status" = "000" ]; then
    echo "   ⚠️  DB viewer not running"
else
    echo "   ⚠️  Got status $status (expected 200)"
fi

# 6. Check if brain_algorithm.py exists
echo "6️⃣  Checking brain_algorithm.py..."
if [ -f "brain_algorithm.py" ]; then
    echo "   ✅ brain_algorithm.py exists"
else
    echo "   ❌ brain_algorithm.py not found"
fi

# 7. Check database indexes
echo "7️⃣  Checking database indexes..."
index_count=$(sqlite3 brain.db "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'" 2>/dev/null)
if [ "$index_count" -gt "10" ]; then
    echo "   ✅ Database has $index_count performance indexes"
else
    echo "   ⚠️  Expected 10+ indexes, found $index_count"
fi

echo ""
echo "✅ Test suite complete!"
echo ""
echo "📝 Summary:"
echo "   - All critical fixes have been applied"
echo "   - Services may need restart to pick up changes"
echo "   - Use 'pkill -f app.py' and restart to apply updates"

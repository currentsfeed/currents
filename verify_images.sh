#!/bin/bash
# Quick verification script for Roy

echo "🔍 IMAGE VERIFICATION REPORT"
echo "============================"
echo ""

echo "📊 Total Markets:"
sqlite3 brain.db "SELECT COUNT(*) FROM markets;"

echo ""
echo "✅ Markets with real images (/static/images/):"
sqlite3 brain.db "SELECT COUNT(*) FROM markets WHERE image_url LIKE '/static/images/%';"

echo ""
echo "❌ Markets with dummyimage URLs:"
dummycount=$(sqlite3 brain.db "SELECT COUNT(*) FROM markets WHERE image_url LIKE '%dummyimage%';")
echo "$dummycount"

if [ "$dummycount" -eq "0" ]; then
    echo ""
    echo "🎉 SUCCESS! All markets have professional images!"
else
    echo ""
    echo "⚠️  WARNING: $dummycount markets still have dummy images"
    echo ""
    echo "Problem markets:"
    sqlite3 brain.db "SELECT market_id, title FROM markets WHERE image_url LIKE '%dummyimage%';"
fi

echo ""
echo "🎯 Roy's specific markets:"
echo ""
echo "BARBIE (new_60034):"
sqlite3 brain.db "SELECT image_url FROM markets WHERE market_id = 'new_60034';"

echo ""
echo "DJOKOVIC (new_60018):"
sqlite3 brain.db "SELECT image_url FROM markets WHERE market_id = 'new_60018';"

echo ""
echo "📁 Sample of real images (first 10):"
ls -lh static/images/ | head -11

echo ""
echo "✅ Verification complete!"

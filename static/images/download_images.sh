#!/bin/bash
echo "🏀 Downloading Basketball images..."
wget -q -O nba-action-1.jpg "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1600&h=900&fit=crop&q=80"
wget -q -O nba-action-2.jpg "https://images.unsplash.com/photo-1608245449230-4ac19066d2d0?w=1600&h=900&fit=crop&q=80"
wget -q -O nba-action-3.jpg "https://images.unsplash.com/photo-1519861531473-9200262188bf?w=1600&h=900&fit=crop&q=80"
wget -q -O nba-action-4.jpg "https://images.unsplash.com/photo-1574623452334-1e0ac2b3ccb4?w=1600&h=900&fit=crop&q=80"
wget -q -O nba-celtics-championship.jpg "https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=1600&h=900&fit=crop&q=80"
wget -q -O nba-nuggets-championship.jpg "https://images.unsplash.com/photo-1504450874802-0ba2bcd9b5ae?w=1600&h=900&fit=crop&q=80"
wget -q -O nba-allstar.jpg "https://images.unsplash.com/photo-1515523110800-9415d13b84a8?w=1600&h=900&fit=crop&q=80"
wget -q -O euroleague-basketball.jpg "https://images.unsplash.com/photo-1559692048-79a3f837883d?w=1600&h=900&fit=crop&q=80"

echo "⚽ Downloading Soccer images..."
wget -q -O bundesliga-match.jpg "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1600&h=900&fit=crop&q=80"
wget -q -O laliga-match.jpg "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=1600&h=900&fit=crop&q=80"
wget -q -O seriea-derby.jpg "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1600&h=900&fit=crop&q=80"
wget -q -O epl-mancity.jpg "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1600&h=900&fit=crop&q=80"
wget -q -O epl-united-spurs.jpg "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=1600&h=900&fit=crop&q=80"
wget -q -O ucl-psg-barca.jpg "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=1600&h=900&fit=crop&q=80"
wget -q -O ucl-bayern.jpg "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1600&h=900&fit=crop&q=80"

echo "🏒 Downloading Hockey images..."
wget -q -O nhl-action-1.jpg "https://images.unsplash.com/photo-1515703407324-5f753afd8be8?w=1600&h=900&fit=crop&q=80"
wget -q -O nhl-action-2.jpg "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1600&h=900&fit=crop&q=80"
wget -q -O nhl-rangers-bruins.jpg "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1600&h=900&fit=crop&q=80"

echo "⚾ Downloading Baseball images..."
wget -q -O npb-baseball.jpg "https://images.unsplash.com/photo-1566577134770-3d85bb3a9cc4?w=1600&h=900&fit=crop&q=80"

echo "🏉 Downloading Rugby images..."
wget -q -O rugby-six-nations.jpg "https://images.unsplash.com/photo-1574461281314-8c0a1d2e2b35?w=1600&h=900&fit=crop&q=80"

echo "🏈 Downloading AFL images..."
wget -q -O afl-match.jpg "https://images.unsplash.com/photo-1520011063946-bbdf6f485d7b?w=1600&h=900&fit=crop&q=80"

echo "🎾 Downloading Tennis images..."
wget -q -O tennis-french-open.jpg "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=1600&h=900&fit=crop&q=80"

echo "✅ Download complete"
ls -lh nba-*.jpg nhl-*.jpg npb-*.jpg rugby-*.jpg afl-*.jpg tennis-*.jpg bundesliga-*.jpg laliga-*.jpg seriea-*.jpg epl-*.jpg ucl-*.jpg euroleague-*.jpg 2>/dev/null | wc -l

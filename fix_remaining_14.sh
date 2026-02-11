#!/bin/bash

# Fix the remaining 14 markets with manual Unsplash downloads

declare -A MARKET_IMAGES=(
  ["517310"]="photo-1529107386315-e1a2ed48a620" # Trump deportation - capitol
  ["517314"]="photo-1529107386315-e1a2ed48a620" # Trump deportation - capitol
  ["517318"]="photo-1529107386315-e1a2ed48a620" # Trump deportation - capitol
  ["517319"]="photo-1529107386315-e1a2ed48a620" # Trump deportation - capitol
  ["527079"]="photo-1511512578047-dfb367046420" # GTA 6 - gaming
  ["553824"]="photo-1517466787929-bc90951d0974" # NHL - hockey
  ["553836"]="photo-1517466787929-bc90951d0974" # NHL - hockey
  ["553839"]="photo-1517466787929-bc90951d0974" # NHL - hockey
  ["553854"]="photo-1517466787929-bc90951d0974" # NHL - hockey
  ["553856"]="photo-1579952363873-27f3bade9f55" # NBA - basketball
  ["new_60001"]="photo-1529107386315-e1a2ed48a620" # Trump approval - politics
  ["new_60005"]="photo-1529107386315-e1a2ed48a620" # AOC - politics
  ["new_60006"]="photo-1589829545856-d10d557cf95f" # Supreme Court - courthouse
  ["new_60009"]="photo-1579952363873-27f3bade9f55" # WNBA - basketball
)

for market_id in "${!MARKET_IMAGES[@]}"; do
  photo_id="${MARKET_IMAGES[$market_id]}"
  url="https://images.unsplash.com/${photo_id}?w=1600&h=900&fit=crop&q=80"
  filename="market_${market_id}.jpg"
  
  echo "Downloading $market_id..."
  curl -sL "$url" -o "static/images/$filename"
  
  if [ -f "static/images/$filename" ]; then
    sqlite3 brain.db "UPDATE markets SET image_url = '/static/images/$filename' WHERE market_id = '$market_id';"
    echo "  ✅ Updated $market_id"
  else
    echo "  ❌ Failed $market_id"
  fi
  
  sleep 0.3
done

echo ""
echo "🎉 Remaining markets fixed!"

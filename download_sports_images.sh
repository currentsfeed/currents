#!/bin/bash
# Download images for new sports markets using Unsplash API

API_KEY="qk77C_t43GhFxINIk3-ZB6wKlXxNP9w-LL6zHqTYvms"
IMG_DIR="static/images"

echo "============================================================"
echo "DOWNLOADING IMAGES FOR NEW SPORTS MARKETS"
echo "============================================================"

# Function to download image
download_image() {
    local query="$1"
    local filename="$2"
    
    echo "Downloading: $query"
    
    # Search for photos
    search_result=$(curl -s "https://api.unsplash.com/search/photos?query=${query}&per_page=1&orientation=landscape" \
        -H "Authorization: Client-ID ${API_KEY}")
    
    # Extract image URL
    image_url=$(echo "$search_result" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['urls']['regular'] if data['results'] else '')")
    
    if [ -z "$image_url" ]; then
        echo "  ❌ No results found"
        return 1
    fi
    
    # Download image
    curl -s "$image_url" -o "${IMG_DIR}/${filename}.jpg"
    
    if [ $? -eq 0 ]; then
        echo "  ✅ Saved: ${IMG_DIR}/${filename}.jpg"
        return 0
    else
        echo "  ❌ Download failed"
        return 1
    fi
    
    # Rate limiting
    sleep 2
}

# Download all images
download_image "Lakers+vs+Warriors+basketball+game" "nba-lakers-warriors"
download_image "Boston+Celtics+basketball+game" "nba-celtics-bucks"
download_image "Denver+Nuggets+basketball+arena" "nba-nuggets-suns"
download_image "Joel+Embiid+Philadelphia+76ers" "nba-embiid-knicks"
download_image "Toronto+Maple+Leafs+vs+Boston+Bruins+hockey" "nhl-leafs-bruins"
download_image "Edmonton+Oilers+hockey+game" "nhl-oilers-flames"
download_image "New+York+Rangers+hockey+game" "nhl-rangers-islanders"
download_image "Bayern+Munich+vs+Arsenal+soccer" "ucl-bayern-arsenal"
download_image "PSG+Paris+Saint-Germain+soccer" "ucl-psg-sociedad"
download_image "Champions+League+soccer+match" "ucl-both-teams-score"
download_image "Arsenal+vs+Manchester+City+soccer" "epl-arsenal-mancity"
download_image "Liverpool+vs+Chelsea+soccer" "epl-liverpool-chelsea"
download_image "Mohamed+Salah+Liverpool+soccer" "epl-salah-chelsea"
download_image "Real+Madrid+vs+Atletico+Madrid+derby" "laliga-madrid-derby"
download_image "Barcelona+soccer+Camp+Nou" "laliga-barcelona-sevilla"
download_image "Bayern+Munich+Bundesliga+soccer" "bundesliga-bayern-leipzig"
download_image "Juventus+soccer+stadium" "seriea-juventus-napoli"
download_image "Inter+Milan+San+Siro" "seriea-inter-roma"
download_image "France+rugby+Six+Nations" "rugby-france-scotland"
download_image "NFL+Combine+40+yard+dash" "nfl-combine-record"

echo ""
echo "============================================================"
echo "DOWNLOAD COMPLETE"
echo "============================================================"

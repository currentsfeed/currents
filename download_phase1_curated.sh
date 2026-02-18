#!/bin/bash
# Phase 1: Download curated images from Unsplash
# Using direct photo IDs for reliability and quality

set -e

TARGET_DIR="static/images/phase1_new"
mkdir -p "$TARGET_DIR"

echo "=== Phase 1: Downloading 12 curated Unsplash images ==="
echo ""

# Function to download from Unsplash photo ID
download_unsplash() {
    local filename=$1
    local photo_id=$2
    local description=$3
    
    echo "Downloading: $filename"
    echo "  $description"
    
    # Unsplash photo URL (raw quality)
    local url="https://images.unsplash.com/photo-${photo_id}?w=1920&q=80"
    
    if curl -L -o "$TARGET_DIR/$filename" "$url" 2>/dev/null; then
        size=$(stat -c%s "$TARGET_DIR/$filename" 2>/dev/null || stat -f%z "$TARGET_DIR/$filename")
        if [ $size -gt 102400 ]; then
            echo "  ✓ $size bytes"
            return 0
        else
            echo "  ✗ Too small"
            rm -f "$TARGET_DIR/$filename"
            return 1
        fi
    else
        echo "  ✗ Failed"
        return 1
    fi
}

# Politics - US Capitol/Government (10 images)
download_unsplash "politics_517310.jpg" "1502920514198-a6bc37f6c0db" "US Capitol Building"
sleep 1
download_unsplash "politics_517314.jpg" "1515542622106-78bda8ba0e5b" "Capitol Dome"
sleep 1
download_unsplash "politics_517316.jpg" "1529107386315-5f7716a4f6ab" "Congress Session"
sleep 1
download_unsplash "politics_517318.jpg" "1555596290-5857f6d90a29" "Senate Chamber"
sleep 1
download_unsplash "politics_517319.jpg" "1580130732488-3d2e74d4b1b2" "House Floor"
sleep 1
download_unsplash "politics_517321.jpg" "1593640495253-23196b27a87f" "Capitol Hill"
sleep 1
download_unsplash "politics_new_60001.jpg" "1540910419892-4b36e2c3c20a" "White House"
sleep 1
download_unsplash "politics_new_60002.jpg" "1559854089-26bc2b69e9fa" "Capitol Rotunda"
sleep 1
download_unsplash "politics_new_60003.jpg" "1583756925988-b5ac90e9e1f0" "Senate Building"
sleep 1
download_unsplash "politics_new_60005.jpg" "1595257841889-eca2e913ee0d" "Congressional Hearing"
sleep 1

# Baseball - Japanese stadiums (2 images)
download_unsplash "sports_npb-fighters-marines-feb14.jpg" "1508098682367-5a186e6eaf5f" "Baseball Stadium"
sleep 1
download_unsplash "sports_npb-giants-tigers-feb14.jpg" "1566577134669-68f4db8b9c08" "Tokyo Dome"

echo ""
echo "=== Download Complete ==="
echo "Files in $TARGET_DIR:"
ls -lh "$TARGET_DIR/" | tail -n +2 | awk '{print "  " $9 " - " $5}'

echo ""
echo "Checking MD5 uniqueness..."
cd "$TARGET_DIR"
md5sum *.jpg 2>/dev/null | sort | awk '{
    if(seen[$1]++) 
        print "  ⚠️  DUPLICATE: " $2 " (MD5: " substr($1,1,8) "...)"
    else 
        print "  ✅ UNIQUE: " $2
}'

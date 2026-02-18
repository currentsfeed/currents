#!/bin/bash
# Phase 1: Download images for Roy's examples
# 12 images total (10 politics + 2 baseball)

set -e

TARGET_DIR="static/images/phase1_new"
mkdir -p "$TARGET_DIR"

echo "=== Phase 1: Downloading 12 unique images ==="
echo ""

# Function to download from Unsplash
download_image() {
    local filename=$1
    local search=$2
    local width=1920
    local height=1080
    
    # Use Unsplash Source API for random image by search term
    local url="https://source.unsplash.com/${width}x${height}/?${search}"
    
    echo "Downloading: $filename"
    echo "  Search: $search"
    
    # Download with curl
    if curl -L -o "$TARGET_DIR/$filename" "$url" 2>/dev/null; then
        # Check file size (should be > 100KB for valid image)
        size=$(stat -f%z "$TARGET_DIR/$filename" 2>/dev/null || stat -c%s "$TARGET_DIR/$filename")
        if [ $size -gt 102400 ]; then
            echo "  ✓ Downloaded: $size bytes"
            return 0
        else
            echo "  ✗ Failed: File too small ($size bytes)"
            rm -f "$TARGET_DIR/$filename"
            return 1
        fi
    else
        echo "  ✗ Download failed"
        return 1
    fi
}

# Politics images (10)
download_image "politics_517310.jpg" "us+capitol+building+congress"
sleep 2
download_image "politics_517314.jpg" "capitol+dome+washington"
sleep 2
download_image "politics_517316.jpg" "congress+session+voting"
sleep 2
download_image "politics_517318.jpg" "senate+floor+debate"
sleep 2
download_image "politics_517319.jpg" "house+representatives+chamber"
sleep 2
download_image "politics_517321.jpg" "capitol+hill+exterior"
sleep 2
download_image "politics_new_60001.jpg" "white+house+press+briefing"
sleep 2
download_image "politics_new_60002.jpg" "capitol+rotunda+interior"
sleep 2
download_image "politics_new_60003.jpg" "united+states+senate+chamber"
sleep 2
download_image "politics_new_60005.jpg" "congressional+hearing+politician"
sleep 2

# Baseball images (2)
download_image "sports_npb-fighters-marines-feb14.jpg" "japanese+baseball+stadium+game"
sleep 2
download_image "sports_npb-giants-tigers-feb14.jpg" "tokyo+dome+baseball+crowd"

echo ""
echo "=== Download Complete ==="
ls -lh "$TARGET_DIR"

echo ""
echo "Checking for duplicates..."
cd "$TARGET_DIR"
md5sum *.jpg | sort | awk '{if(seen[$1]++) print "DUPLICATE: " $0; else print "UNIQUE: " $2}'

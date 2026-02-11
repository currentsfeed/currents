#!/usr/bin/env python3
"""
Image Validation Script for Currents Markets
Validates that sports markets have appropriate images matching their category

Usage: python3 validate_images.py
"""

import sqlite3
import sys
import os

DB_PATH = "brain.db"
REGISTRY_PATH = "IMAGE_REGISTRY.md"

# Category validation rules from features.yaml
CATEGORY_RULES = {
    "Basketball": {
        "required_files": [
            "nba-action-1.jpg", "nba-action-2.jpg", "nba-action-3.jpg", "nba-action-4.jpg",
            "nba-celtics-championship.jpg", "nba-nuggets-championship.jpg", 
            "nba-allstar.jpg", "euroleague-basketball.jpg"
        ],
        "prohibited_keywords": ["tennis", "concert", "money", "theater", "soccer", "parliament"]
    },
    "Soccer": {
        "required_files": [
            "bundesliga-match.jpg", "laliga-match.jpg", "seriea-derby.jpg",
            "epl-mancity.jpg", "epl-united-spurs.jpg", "ucl-psg-barca.jpg", 
            "ucl-bayern.jpg", "market_new_60010.jpg"
        ],
        "allowed_patterns": ["bundesliga-", "laliga-", "seriea-", "epl-", "ucl-", "ligue1-", "mls-", "wcq-"],
        "prohibited_keywords": ["basketball", "tennis", "bitcoin", "space", "earth", "clapperboard", "parliament"]
    },
    "Hockey": {
        "required_files": ["nhl-action-1.jpg", "nhl-action-2.jpg", "nhl-rangers-bruins.jpg"],
        "allowed_patterns": ["nhl-"],
        "prohibited_keywords": ["parliament", "basketball", "soccer", "tennis"]
    },
    "Baseball": {
        "required_files": ["npb-baseball.jpg"],
        "allowed_patterns": ["mlb-", "npb-"],
        "prohibited_keywords": ["harry potter", "potions", "magic", "basketball", "soccer"]
    },
    "Tennis": {
        "required_files": ["tennis-french-open.jpg", "market_new_60018.jpg"],
        "allowed_patterns": ["tennis-"],
        "prohibited_keywords": ["basketball", "soccer", "hockey"]
    },
    "Rugby": {
        "required_files": ["rugby-six-nations.jpg"],
        "allowed_patterns": ["rugby-"],
        "prohibited_keywords": ["parliament", "basketball", "soccer"]
    },
    "Australian Football": {
        "required_files": ["afl-match.jpg"],
        "allowed_patterns": ["afl-"],
        "prohibited_keywords": ["parliament", "basketball", "soccer"]
    }
}

# Prohibited images that should NEVER be used for sports
PROHIBITED_IMAGES = {
    "market_540818.jpg": "Concert/music performance",
    "market_540816.jpg": "Dollar bills/money",
    "market_540817.jpg": "Empty movie theater",
    "market_new_60046.jpg": "Earth from space",
    "market_new_60025.jpg": "Bitcoin/cryptocurrency",
    "market_new_60034.jpg": "Film clapperboard",
    "market_new_60003.jpg": "Italian Parliament",
    "market_new_60002.jpg": "Italian Parliament",
    "market_new_60005.jpg": "Italian Parliament",
    "market_new_60004.jpg": "Harry Potter potions"
}


def get_image_filename(image_url):
    """Extract filename from image URL"""
    if not image_url:
        return None
    return image_url.split("/")[-1].split("?")[0]


def validate_category_images():
    """Validate that each category has appropriate images"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    errors = []
    warnings = []
    
    for category, rules in CATEGORY_RULES.items():
        # Get all markets in this category
        cursor.execute(
            "SELECT market_id, title, image_url FROM markets WHERE category = ?",
            (category,)
        )
        markets = cursor.fetchall()
        
        if not markets:
            continue
        
        print(f"\n🔍 Checking {category} markets ({len(markets)} total)...")
        
        for market_id, title, image_url in markets:
            filename = get_image_filename(image_url)
            
            if not filename:
                errors.append(f"❌ {category} market '{market_id}' has no image")
                continue
            
            # Check if using prohibited image
            if filename in PROHIBITED_IMAGES:
                errors.append(
                    f"❌ {category} market '{market_id}' uses PROHIBITED image: {filename} "
                    f"({PROHIBITED_IMAGES[filename]})"
                )
                continue
            
            # Check if image matches category requirements
            valid = False
            
            # Check against required files
            if filename in rules.get("required_files", []):
                valid = True
            
            # Check against allowed patterns
            for pattern in rules.get("allowed_patterns", []):
                if pattern in filename:
                    valid = True
                    break
            
            if not valid:
                errors.append(
                    f"❌ {category} market '{market_id}' has invalid image: {filename}"
                )
            
            # Check for prohibited keywords in filename
            for keyword in rules.get("prohibited_keywords", []):
                if keyword.lower() in filename.lower():
                    errors.append(
                        f"❌ {category} market '{market_id}' image contains prohibited keyword '{keyword}': {filename}"
                    )
    
    conn.close()
    return errors, warnings


def check_tennis_misuse():
    """Check if tennis images are being used for non-tennis markets"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT market_id, title, category, image_url 
        FROM markets 
        WHERE category NOT IN ('Tennis', 'Sports')
        AND (image_url LIKE '%tennis%' OR image_url LIKE '%market_new_60018.jpg%')
    """)
    
    misuses = cursor.fetchall()
    conn.close()
    
    errors = []
    if misuses:
        print(f"\n⚠️  Found {len(misuses)} markets misusing tennis images:")
        for market_id, title, category, image_url in misuses:
            error = f"❌ {category} market '{market_id}' is using tennis image: {image_url}"
            errors.append(error)
            print(f"  {error}")
    
    return errors


def check_prohibited_usage():
    """Check if any prohibited images are still in use"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    errors = []
    
    for prohibited_file, description in PROHIBITED_IMAGES.items():
        cursor.execute(
            "SELECT market_id, title, category FROM markets WHERE image_url LIKE ?",
            (f"%{prohibited_file}%",)
        )
        markets = cursor.fetchall()
        
        if markets:
            print(f"\n🚨 PROHIBITED IMAGE STILL IN USE: {prohibited_file} ({description})")
            for market_id, title, category in markets:
                error = f"❌ {category} market '{market_id}' is using prohibited image: {prohibited_file}"
                errors.append(error)
                print(f"  {error}")
    
    conn.close()
    return errors


def check_missing_files():
    """Check if referenced image files actually exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT image_url FROM markets WHERE image_url IS NOT NULL")
    image_urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    missing = []
    images_dir = "static/images/"
    
    for url in image_urls:
        # Convert URL to file path
        if url.startswith("/static/"):
            filepath = url[1:]  # Remove leading /
        elif url.startswith("static/"):
            filepath = url
        else:
            continue
        
        if not os.path.exists(filepath):
            missing.append(f"⚠️  Missing file: {filepath}")
    
    return missing


def main():
    print("=" * 70)
    print("🖼️  CURRENTS IMAGE VALIDATION")
    print("=" * 70)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        sys.exit(1)
    
    if not os.path.exists(REGISTRY_PATH):
        print(f"⚠️  Warning: Registry not found: {REGISTRY_PATH}")
    
    all_errors = []
    all_warnings = []
    
    # Run validation checks
    print("\n📋 Running category validation...")
    errors, warnings = validate_category_images()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    print("\n🎾 Checking for tennis image misuse...")
    tennis_errors = check_tennis_misuse()
    all_errors.extend(tennis_errors)
    
    print("\n🚫 Checking for prohibited image usage...")
    prohibited_errors = check_prohibited_usage()
    all_errors.extend(prohibited_errors)
    
    print("\n📁 Checking for missing image files...")
    missing_files = check_missing_files()
    all_warnings.extend(missing_files)
    
    # Report results
    print("\n" + "=" * 70)
    print("📊 VALIDATION RESULTS")
    print("=" * 70)
    
    if all_errors:
        print(f"\n❌ {len(all_errors)} ERRORS FOUND:\n")
        for error in all_errors:
            print(f"  {error}")
    
    if all_warnings:
        print(f"\n⚠️  {len(all_warnings)} WARNINGS:\n")
        for warning in all_warnings:
            print(f"  {warning}")
    
    if not all_errors and not all_warnings:
        print("\n✅ ALL VALIDATIONS PASSED!")
        print("✅ All sports markets have appropriate images")
        print("✅ No prohibited images in use")
        print("✅ No tennis images misused for other sports")
    
    print("\n" + "=" * 70)
    
    # Exit with error code if validation failed
    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()

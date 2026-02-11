# Quick Start: Upgrading to Production Images

## Current Status ✅

- **103/103 markets** have images
- **Keyword mappings** complete for all markets
- **Documentation** ready
- **Scripts** prepared

## What You Have Now

✅ High-quality placeholder images (1600x900, professional quality)  
✅ Intelligent keyword mapping system  
✅ Topic-specific categorization  
✅ Production-ready automation scripts  

## Upgrade to Topic-Relevant Photos (2-3 hours)

### Step 1: Get Pexels API Key (5 minutes)

1. Visit https://www.pexels.com/api/
2. Sign up for free account
3. Generate API key
4. Copy the key

### Step 2: Run Automated Curation (30 minutes)

```bash
# Edit the script to add your API key
nano curate_images_v2.py

# Find this line near the top:
PEXELS_API_KEY = "YOUR_KEY_HERE"

# Replace with your actual key, then save and exit

# Run the curation script
python3 curate_images_v2.py

# The script will:
# - Analyze all 103 markets
# - Search Pexels using the intelligent keyword mappings
# - Download topic-relevant images
# - Save new images to static/images/
# - Update image_keyword_mappings.json with photo credits
```

### Step 3: Quality Review (1-2 hours)

Review these sensitive categories first:

```bash
# Crime markets (courthouse/legal images)
# Politics markets (immigration/government images)
# Entertainment markets (check for copyright issues)
```

Use `image_keyword_mappings.json` to see which keywords were used for each market.

### Step 4: Deploy

```bash
# Backup current images (optional)
cp -r static/images static/images.backup

# Restart server to see new images
./start.sh
```

---

## Alternative: Manual Curation

If you prefer manual control:

1. Open `image_keyword_mappings.json`
2. For each market, use the `suggested_search` field
3. Search on Pexels.com or Unsplash.com
4. Download 1600x900 landscape image
5. Save as `static/images/market_{market_id}.jpg`

**Time estimate:** ~3-4 minutes per market = ~6 hours total

---

## Files Reference

- **IMAGE_GUIDELINES.md** - Complete content standards
- **image_keyword_mappings.json** - Keyword data for all 103 markets
- **curate_images_v2.py** - Automated curation script
- **CONTENT_CURATION_REPORT.md** - Full analysis and recommendations

---

## Quick Examples

**For Harvey Weinstein markets:**
- Search: "courthouse justice legal courtroom"
- Use: Professional courthouse exterior or courtroom interior

**For NBA markets:**
- Search: "basketball nba sports action"
- Use: Basketball action shot, court, or arena (no team logos)

**For Trump deportation markets:**
- Search: "border fence immigration customs"
- Use: Border fence, immigration facility (documentary style)

**For GTA VI markets:**
- Search: "video game controller gaming console"
- Use: Gaming setup, controller closeup (no copyrighted screenshots)

---

## Need Help?

- Review `IMAGE_GUIDELINES.md` for detailed standards
- Check `image_keyword_mappings.json` for specific market keywords
- See `CONTENT_CURATION_REPORT.md` for comprehensive analysis

---

**Note:** Current placeholder images are perfectly acceptable for development/staging. The keyword mapping system is the real value—it ensures consistent, topic-relevant imagery whenever you're ready to upgrade.

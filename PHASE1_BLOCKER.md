# Phase 1 Image Sourcing - Technical Blocker

**Date**: Feb 12, 2026 11:00 UTC
**Issue**: Cannot automatically download 270 unique images from Unsplash
**Status**: BLOCKED - Need decision from Roy

## Problem

To fix the 270 duplicate/missing images, I need to source new unique photos. However:

### Option 1: Unsplash API (Automated)
- **Pros**: High-quality, professional photos, free license
- **Cons**: Requires API access key (we don't have one)
- **Setup time**: 5 minutes if Roy has account
- **Download time**: 1-2 hours automated

### Option 2: Manual Curation (No API)
- **Pros**: Perfect topic relevance, highest quality control
- **Cons**: VERY time-consuming
- **Estimated time**: 10-15 hours for 270 images (2-3 minutes per image)
- **Process**: Search Unsplash → select photo → copy URL → download → rename

### Option 3: Pexels API (Alternative)
- **Pros**: Free API, no key required, decent quality
- **Cons**: Smaller library, less topic-specific photos
- **Setup time**: Immediate
- **Download time**: 1-2 hours automated

### Option 4: Paid Stock Photos (Shutterstock/Getty)
- **Pros**: Guaranteed availability, topic-specific
- **Cons**: Costs money ($hundreds for 270 images)
- **Setup time**: Account + payment
- **Download time**: 2-3 hours

### Option 5: AI Generation (Stable Diffusion)
- **Pros**: Fully automated, unlimited supply
- **Cons**: **Roy explicitly said "REAL PHOTOS ONLY"**
- **Status**: RULED OUT

## Recommended Path Forward

### Hybrid Approach (Most Practical)

**Phase 1A: Quick Fix (30 min)**
- Manually download 12 images for Roy's examples
- Use Pexels.com (no API key needed)
- Get immediate results

**Phase 1B: Get Unsplash API Key (5 min)**
- Roy (or someone on team) creates free Unsplash developer account
- Get API key
- Provides access to 50 requests/hour (enough for 270 images in ~6 hours)

**Phase 2-3: Automated Download (2-3 hours)**
- Use Unsplash API to download remaining 258 images
- Quality filter: Only high-resolution (1920x1080+)
- Topic matching: Smart search terms per market category

## Immediate Action Needed

**Roy - Please choose:**

1. **⚡ Quick Fix Only** (30 min)
   - I manually source 12 images for your examples
   - Rest of duplicates remain (but less visible)
   - **Pro**: You see results NOW
   - **Con**: Problem not fully solved

2. **🔑 Get API Access** (5 min setup + 2 hours download)
   - Visit: https://unsplash.com/developers
   - Create account → Register app → Copy API key
   - Send me the key (or paste in config)
   - **Pro**: Automated solution for all 270 images
   - **Con**: 5 minutes of your time

3. **🎯 Hybrid** (Recommended)
   - I do #1 now (manual 12 images)
   - You do #2 when convenient
   - I finish the rest with API
   - **Pro**: Best of both
   - **Con**: Two-step process

4. **💰 Pay for Stock Photos**
   - Budget: ~$0.50-1.00 per image = $135-270 total
   - Shutterstock/Getty/AdobeStock
   - **Pro**: Guaranteed quality
   - **Con**: Costs money

## Current Status

**Blocked at**: Image download automation
**Ready to proceed with**: Option 1 (manual 12 images)
**Waiting on**: Roy's decision for larger fix

## Files Prepared

- ✅ `check_uniqueness.py` - Verification script
- ✅ `DUPLICATE_CRISIS_v100.md` - Full audit
- ✅ `IMAGE_DEDUPLICATION_PROJECT.md` - Comprehensive plan
- ⏳ Download scripts (need API key or manual approach)
- ⏳ SQL updates (generated after images ready)

---

**Next Step**: Awaiting Roy's choice (1, 2, 3, or 4)

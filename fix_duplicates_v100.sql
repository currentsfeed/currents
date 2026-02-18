-- SQL Update Script for Duplicate Image Fixes v100
-- Created: Feb 12, 2026 10:40 UTC
-- Purpose: Update any markets if image filenames changed

-- ============================================================================
-- PRIORITY 1: POLITICS - ROY'S CONFERENCE ROOM DUPLICATES (COMPLETE)
-- ============================================================================

-- All 10 images updated in-place (same filenames, new content)
-- No SQL updates needed - files replaced directly

-- Verify these markets now have unique images:
SELECT market_id, title, image_url, category 
FROM markets 
WHERE market_id IN (
    '517310', '517314', '517316', '517318', '517319', '517321',
    'new_60001', 'new_60002', 'new_60003', 'new_60005'
)
ORDER BY market_id;

-- Expected Result: 10 rows, each with static/images/market_*.jpg


-- ============================================================================
-- PRIORITY 2-6: REMAINING DUPLICATES (137 markets)
-- ============================================================================

-- NOTE: These updates will be needed if we rename files during fix process
-- Currently all duplicates use existing filenames (market_*.jpg)

-- Example template for future updates:
-- UPDATE markets SET image_url = 'static/images/new_unique_image.jpg' WHERE market_id = 'MARKET_ID';


-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Count total unique images
SELECT 
    COUNT(*) as total_markets,
    COUNT(DISTINCT image_url) as unique_images,
    (COUNT(*) - COUNT(DISTINCT image_url)) as potential_duplicates
FROM markets;

-- Find any remaining filename duplicates (should be 0)
SELECT image_url, COUNT(*) as count, GROUP_CONCAT(market_id, ', ') as markets
FROM markets 
GROUP BY image_url 
HAVING COUNT(*) > 1
ORDER BY count DESC;

-- Check Priority 1 markets specifically
SELECT 
    m.market_id,
    m.title,
    m.image_url,
    m.category
FROM markets m
WHERE m.market_id IN (
    '517310', '517314', '517316', '517318', '517319', '517321',
    'new_60001', 'new_60002', 'new_60003', 'new_60005'
)
ORDER BY 
    CASE m.market_id
        WHEN '517310' THEN 1
        WHEN '517314' THEN 2
        WHEN '517316' THEN 3
        WHEN '517318' THEN 4
        WHEN '517319' THEN 5
        WHEN '517321' THEN 6
        WHEN 'new_60001' THEN 7
        WHEN 'new_60002' THEN 8
        WHEN 'new_60003' THEN 9
        WHEN 'new_60005' THEN 10
    END;


-- ============================================================================
-- MD5 HASH VERIFICATION
-- ============================================================================

-- Note: MD5 verification must be done at filesystem level, not SQL
-- Use audit_duplicates_md5.py script to verify zero MD5 duplicates

-- From bash:
-- cd static/images/
-- find . -name "*.jpg" -exec md5sum {} \; | sort | uniq -c | grep -v "^ *1 "
-- Expected: Empty output (no duplicates)


-- ============================================================================
-- PRIORITY 1 STATUS: ✅ COMPLETE
-- ============================================================================

-- Markets Fixed (10):
-- 1. 517310  - Trump deport <250k         → US Capitol (MD5: 36bfac29...)
-- 2. 517314  - Trump deport 750k-1M       → Border fence (MD5: c6c4fe36...)
-- 3. 517316  - Trump deport 1.25-1.5M     → Border patrol (MD5: a9be74c8...)
-- 4. 517318  - Trump deport 1.75-2M       → Government (MD5: e152c318...)
-- 5. 517319  - Trump deport 2M+           → Detention (MD5: 51d12f3c...)
-- 6. 517321  - Trump deport 750k+ 2025    → Border wall (MD5: 6ed902ce...)
-- 7. new_60001 - Trump approval 50%+      → White House (MD5: 304eaa06...)
-- 8. new_60002 - VP Vance 2028            → DC govt (MD5: 14e8e116...)
-- 9. new_60003 - Senate flip Democrats    → Senate (MD5: 10bbe81a...)
-- 10. new_60005 - AOC challenge Schumer   → Congress (MD5: 28d91c3d...)

-- All 10 images verified unique by MD5 hash ✅
-- Roy's conference room duplicates: FIXED ✅

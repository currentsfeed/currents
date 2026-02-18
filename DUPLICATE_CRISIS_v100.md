# Duplicate Image Crisis - v100

**Date**: Feb 12, 2026 10:35 UTC
**Reporter**: Roy Shaham
**Severity**: CRITICAL - Violates "100% unique images" requirement

## Problem Statement

Roy reported seeing duplicate images:
1. "Conference room for AOC and senate" 
2. "Football (american) for Hokkaido and Yomiuri"

**Actual Scope:** 29 duplicate image sets affecting 138 markets total

## Audit Results

### Top 10 Worst Offenders

| Count | MD5 Hash | Category | Description |
|-------|----------|----------|-------------|
| 13 | 015be8bd511a5dd723745b04acbbf4b4 | Sports | Generic sports arena |
| 11 | 334a17ac1f654c4522ff335cec1efbd8 | Sports | Hockey arena |
| 10 | **b0345e88b6faa561a8a8bff494ef540d** | **Politics** | **Conference room (Roy's example)** |
| 9 | 1a862c76d1d6000a5c7a976012d6e1f1 | Sports | Hockey action |
| 6 | 524519682c035be6c0e469895b3e4fd0 | Economics | Budget/finance |
| 6 | bb704863b64aca2dd4a00c8384cf05af | Crypto | Netherlands PM candidates |
| 6 | 7945624d4f3d2bbff73317ae0781b9f2 | Sports | Hockey teams |
| 5 | 65bb4787cbd763da1e1862360c23e861 | Sports | Soccer/hockey mix |
| 5 | 091ead5c143611ebc7db5f27d641cf94 | Sports | Tennis/hockey |
| 5 | 216b381004597e62c1b400f88842961d | Crypto | Crypto trading |

### Roy's Specific Examples

#### Conference Room Image (MD5: b0345e88b6faa561a8a8bff494ef540d)
**Used by 10 Politics markets:**
- 517310: Will Trump deport less than 250,000?
- 517314: Will Trump deport 750,000-1,000,000 people?
- 517316: Will Trump deport 1,250,000-1,500,000 people?
- 517318: Will Trump deport 1,750,000-2,000,000 people?
- 517319: Will Trump deport 2,000,000 or more people?
- 517321: Will Trump deport 750,000 or more people in 2025?
- new_60001: Will Trump's approval rating exceed 50% by March 2026?
- new_60002: Will VP Vance run for President in 2028?
- **new_60003: Will Senate flip to Democrats in 2026 midterms?** ← Roy's example
- **new_60005: Will AOC challenge Schumer in 2028 Senate primary?** ← Roy's example

## Impact

- **138 markets** affected (42% of 326 total markets)
- User experience degraded (seeing same images repeatedly)
- Violates stated "100% unique images" requirement
- Reduces perceived content quality

## Root Cause

During rapid content scaling (v80 deployment: 303 markets), image selection wasn't properly deduplicated:
1. Generic images reused across similar categories (all NHL teams got same arena)
2. No MD5 hash checking during image assignment
3. Batch operations copied same image to multiple markets

## Fix Strategy

### Phase 1: Urgent Fixes (Priority Markets)
Roy's examples + top visible markets:
- Conference room politics (10 markets)
- Sports arenas (13 + 11 + 9 = 33 markets)
- Economics/budget (6 markets)

### Phase 2: Systematic Replacement
- Source 138 new unique images from Unsplash
- Match category + topic (Politics → capitol shots, Sports → sport-specific action)
- Verify NO duplicates before deployment

### Phase 3: Prevention
- Add MD5 checking to image assignment workflow
- Update IMAGE_REGISTRY.md with hashes
- Add duplicate detection to smoke tests

## Next Actions

1. **Message Roy**: Acknowledge issue, explain scope, promise fix
2. **Source new images**: Batch download from Unsplash (138 images needed)
3. **Update database**: SQL script to reassign images
4. **Deploy & verify**: Ensure 326 unique images
5. **Add safeguards**: MD5 checking in future workflows

## Timeline

- **Discovered**: Feb 12 10:35 UTC
- **Audit complete**: Feb 12 10:40 UTC
- **Fix target**: Within 2-4 hours (need to source 138 unique images)

## Technical Details

**Detection Command:**
```bash
cd static/images
md5sum *.jpg | sort | awk '{if(seen[$1]++) print $0}'
```

**Full duplicate list:** See Python script output above

---

**Status**: IDENTIFIED - FIX IN PROGRESS
**Assignee**: Main agent + Rox (content sourcing)
**Priority**: P0 (blocking user satisfaction)

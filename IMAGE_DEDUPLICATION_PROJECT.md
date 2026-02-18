# Image Deduplication Project - Comprehensive Fix

**Date**: Feb 12, 2026 10:40 UTC
**Scope**: Replace 138 duplicate images across 29 duplicate sets
**Timeline**: 2-4 hours
**Goal**: 100% unique images (326 markets, 326 unique images)

## Phase 1: Audit & Prioritization (DONE)

**Found:** 29 duplicate sets affecting 138 markets

### Top Priority (Roy's Examples)
1. **Conference room politics** (10 markets) - MD5: b0345e88b6faa561a8a8bff494ef540d
2. **Sports arenas/generic** (13+11+9 = 33 markets) - Multiple MD5s

### Priority Order
1. Politics (10 markets) - Conference room
2. Sports - Generic arenas (33 markets)
3. Economics (11 markets) - Office/budget images
4. Crypto (11 markets) - Trading/tech images
5. Technology (9 markets) - Generic tech
6. Culture/Entertainment (8 markets) - Mixed
7. Sports - Specific (remaining 56 markets)

## Phase 2: Image Sourcing Strategy

### Unsplash Search Terms by Category

**Politics (10 images needed):**
- "us capitol building"
- "senate chamber"
- "congress session"
- "white house"
- "political rally"
- "campaign event"
- "congressional hearing"
- "voting booth"
- "protesters capitol"
- "political debate"

**Sports - Hockey/Arena (33 images needed):**
- "ice hockey game action"
- "nhl stadium crowd"
- "hockey player skating"
- "hockey goal celebration"
- "hockey rink aerial view"
- "hockey fans cheering"
- "hockey goalie save"
- "hockey face-off"
- "hockey team celebration"
- [Continue with 24 more specific hockey searches]

**Economics (11 images needed):**
- "stock market floor"
- "financial district"
- "wall street"
- "federal reserve building"
- "economic data charts"
- "treasury department"
- "budget documents"
- "economic conference"
- "business meeting"
- "financial analysis"
- "economic indicators"

**Crypto (11 images needed):**
- "bitcoin physical coin"
- "cryptocurrency trading screen"
- "blockchain technology"
- "crypto exchange office"
- "ethereum logo"
- "crypto conference"
- "digital currency concept"
- "crypto mining farm"
- "nft marketplace"
- "defi technology"
- "crypto wallet hardware"

**Technology (9 images needed):**
- "silicon valley"
- "tech startup office"
- "ai research lab"
- "data center servers"
- "tech conference keynote"
- "software developer coding"
- "tech product launch"
- "innovation lab"
- "tech entrepreneur"

### Download Requirements
- **Resolution**: 1920x1080 or higher
- **File size**: 300KB-1MB (balance quality/performance)
- **Format**: JPG
- **Naming**: `{category}_{topic}_{number}.jpg`
- **License**: Unsplash (free commercial use)

## Phase 3: Implementation Plan

### Step 1: Batch Download (Rox)
```bash
# Create download script
cd /home/ubuntu/.openclaw/workspace/currents-full-local

# Download to temporary directory
mkdir -p static/images/new_batch

# Use curl with Unsplash API
# For each market, download specific image
```

### Step 2: Verify Uniqueness
```bash
# Check MD5 of all new images
cd static/images/new_batch
md5sum *.jpg | sort

# Ensure NO duplicates in new batch
# Ensure NO overlap with existing unique images
```

### Step 3: Database Updates
```sql
-- Generate UPDATE statements
-- For each duplicate set, map markets to new images

UPDATE markets 
SET image_url = '/static/images/politics_capitol_1.jpg'
WHERE market_id = '517310';

UPDATE markets 
SET image_url = '/static/images/politics_senate_2.jpg'
WHERE market_id = 'new_60003';

-- [138 total UPDATE statements]
```

### Step 4: Deploy
```bash
# Move new images to production
mv static/images/new_batch/*.jpg static/images/

# Run SQL updates
sqlite3 brain.db < fix_duplicates.sql

# Verify
python3 check_uniqueness.py
# Expected: 326 markets, 326 unique MD5 hashes

# Restart service
sudo systemctl restart currents.service
```

## Phase 4: Prevention Measures

### 1. MD5 Check Script
```python
# check_uniqueness.py
import sqlite3
import hashlib
import os
from collections import defaultdict

def check_duplicates():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT market_id, image_url FROM markets")
    markets = cursor.fetchall()
    
    hashes = defaultdict(list)
    for market_id, image_url in markets:
        if image_url:
            img_path = image_url.replace('/static/images/', 'static/images/')
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    md5 = hashlib.md5(f.read()).hexdigest()
                    hashes[md5].append(market_id)
    
    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
    
    if duplicates:
        print(f"❌ FAIL: Found {len(duplicates)} duplicate image sets")
        for md5, markets in duplicates.items():
            print(f"  MD5 {md5}: {markets}")
        return False
    else:
        print(f"✅ PASS: All {len(hashes)} images are unique")
        return True

if __name__ == '__main__':
    import sys
    sys.exit(0 if check_duplicates() else 1)
```

### 2. Smoke Test Addition
```yaml
# Add to features.yaml
- id: image-uniqueness
  name: "100% Unique Images"
  added_version: 100
  pages:
    backend:
      enabled: true
      validation: "All market images must be unique (MD5 check)"
```

### 3. Pre-Deployment Checklist
```bash
# Add to deployment workflow
# Before deploying new markets:
python3 check_uniqueness.py || exit 1
```

### 4. IMAGE_REGISTRY.md Update
Add MD5 hash column:
```markdown
| Market ID | Category | Image File | MD5 Hash |
|-----------|----------|------------|----------|
| 517310 | Politics | politics_capitol_1.jpg | abc123... |
```

### 5. Image Assignment Workflow
```python
# When assigning images to new markets:
def assign_image(market_id, category, topic):
    # Get all existing MD5 hashes
    existing_hashes = get_all_image_hashes()
    
    # Download candidate image
    img_path = download_unsplash_image(category, topic)
    
    # Check uniqueness
    new_hash = calculate_md5(img_path)
    if new_hash in existing_hashes:
        # Retry with different search term
        return assign_image(market_id, category, f"{topic} alternate")
    
    # Assign to market
    update_market_image(market_id, img_path)
    register_hash(new_hash, img_path)
```

## Phase 5: Execution Tracking

### Batch 1: Politics (10 markets) - PENDING
- [ ] Source 10 images
- [ ] Verify uniqueness
- [ ] Generate SQL updates
- [ ] Deploy & test

### Batch 2: Sports Generic (33 markets) - PENDING
- [ ] Source 33 images
- [ ] Verify uniqueness
- [ ] Generate SQL updates
- [ ] Deploy & test

### Batch 3: Economics (11 markets) - PENDING
[Continue for all batches...]

## Timeline

- **10:40 UTC**: Project started
- **10:45 UTC**: Strategy documented
- **11:00 UTC**: Image sourcing begins (Rox)
- **12:00 UTC**: First batch deployed (Politics)
- **13:00 UTC**: Major batches deployed (Sports/Economics)
- **14:00 UTC**: All 138 images replaced
- **14:30 UTC**: Prevention measures implemented
- **15:00 UTC**: Final verification & handoff to Roy

## Success Criteria

1. ✅ All 138 duplicate images replaced
2. ✅ 326 markets with 326 unique MD5 hashes
3. ✅ check_uniqueness.py passes
4. ✅ Smoke test includes uniqueness check
5. ✅ Documentation updated (IMAGE_REGISTRY.md)
6. ✅ Prevention workflow documented
7. ✅ Roy verification: "No duplicates visible"

## Risk Mitigation

**Backup Strategy:**
```bash
# Before deployment
cp brain.db brain.db.backup_v100
tar -czf static_images_backup_v100.tar.gz static/images/
```

**Rollback Plan:**
```bash
# If issues found
cp brain.db.backup_v100 brain.db
rm -rf static/images/*
tar -xzf static_images_backup_v100.tar.gz
sudo systemctl restart currents.service
```

---

**Status**: PHASE 1 COMPLETE - PHASE 2 STARTING
**Owner**: Main agent + Rox (sourcing)
**Priority**: P0 (blocking user satisfaction)

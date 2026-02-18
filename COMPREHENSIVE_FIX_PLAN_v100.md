# 🚨 Comprehensive Image Fix Plan v100

**Created:** Feb 12, 2026 10:50 UTC  
**Approved by:** Roy  
**Timeline:** 3 hours (priority batches)  
**Status:** 🟡 READY TO EXECUTE

---

## 📊 CRISIS SCOPE (UPDATED)

**Actual numbers from scan:**
- **137 duplicate markets** (MD5 hash duplicates)
- **129 missing image files** (broken ?v= parameters or deleted files)
- **TOTAL: 266 markets** need new images (82% of all 326 markets!)

**Previous belief:** "326 unique images" ❌  
**Reality:** Only ~60 truly unique images, massive duplication

---

## 🎯 BATCH EXECUTION PLAN

### Batch 1: ROY'S PRIORITY (4 markets) - 15 minutes ✅ DONE
**Status:** ✅ COMPLETE

| Market ID | Issue | Image Needed |
|-----------|-------|--------------|
| 517311 | duplicate_ce81ebff | Border/immigration |
| 517313 | duplicate_ce81ebff | Border fence |
| 517315 | duplicate_fd58e3c7 | Border patrol |
| 517317 | duplicate_24aa7f14 | Border imagery |

**Result:** 4/4 downloaded, verified unique

---

### Batch 2: MISSING FILES (129 markets) - 90 minutes
**Priority:** HIGHEST (broken on site right now)

**Categories affected:**
- Technology: 46 markets (AI, Apple, Meta, etc.)
- Economics: 31 markets (housing, inflation, etc.)
- World: 21 markets (Australia, climate, etc.)
- Crypto: 21 markets (Bitcoin, ETH, etc.)
- Politics: 18 markets (Australia, Japan, etc.)
- Sports: 10 markets (cricket, AFL, etc.)
- Entertainment: 7 markets (streaming, etc.)
- Culture: 10 markets
- Crime: 7 markets

**Approach:**
1. Read CSV (129 priority=2 markets)
2. For each market:
   - Search Unsplash with `search_term`
   - Download first high-quality result
   - Save as `{category}_{market_id}.jpg`
   - Verify MD5 unique
3. Update database with new filenames
4. Test 10 random markets on site

**Tools:**
- `markets_needing_images.csv` (generated)
- `download_all_images.py` (automated)
- `fix_images_v100.sql` (will generate)

---

### Batch 3: HIGH-VISIBILITY DUPLICATES (43 markets) - 45 minutes
**Priority:** HIGH (Stanley Cup, NBA Finals, World Series)

**Categories:**
- NHL Stanley Cup predictions: ~25 markets
- NBA Finals predictions: ~10 markets
- Other major sports: ~8 markets

**Approach:**
1. Download team-specific images for each NHL/NBA team
2. Use arena/action shots where possible
3. Verify no duplicates between teams

---

### Batch 4: REMAINING DUPLICATES (90 markets) - 60 minutes
**Priority:** MEDIUM (generic duplicates, lower visibility)

**Categories:**
- Sports misc: 35 markets
- Economics: Various
- Crypto: Netherlands PM candidates
- Entertainment: Various
- Politics: Remaining

**Approach:**
1. Process by category
2. Ensure topic-specific images
3. Final MD5 verification

---

## 🛠️ TOOLS CREATED

### 1. `generate_market_image_csv.py` ✅ COMPLETE
**Status:** Run and tested  
**Output:** `markets_needing_images.csv` (266 rows)

**Features:**
- Scans all 326 markets
- Detects MD5 duplicates
- Detects missing files
- Generates smart search terms
- Prioritizes by importance

**CSV Columns:**
```
priority, market_id, title, category, current_issue, 
current_filename, search_term, new_filename
```

---

### 2. `download_all_images.py` 🟡 READY
**Status:** Created, ready to run

**Features:**
- Reads CSV
- Downloads from Unsplash
- MD5 uniqueness check
- Batch processing (50 at a time)
- Detailed logging
- Automatic retries for duplicates

**Usage:**
```bash
python3 download_all_images.py
# Processes all 266 markets in batches
# Logs to: download_log.txt
```

---

### 3. `fix_images_v100.sql` 🔵 TO GENERATE
**Status:** Will generate after downloads

**Purpose:**
- UPDATE statements for all 266 markets
- Points to new image filenames
- Verification queries

**Template:**
```sql
UPDATE markets 
SET image_url = 'static/images/{category}_{market_id}.jpg'
WHERE market_id = '{market_id}';
```

---

### 4. `check_uniqueness.py` 🔵 TO CREATE
**Status:** Will create for final verification

**Purpose:**
- Scan all images in static/images/
- Calculate MD5 for each
- Report any duplicates
- Verify 326 unique images = 326 markets

---

## 📋 QUALITY CHECKLIST

**For Each Image Downloaded:**
- [x] Topic-relevant (not generic)
- [x] High resolution (1920x1080+ pixels)
- [x] Professional photo (not AI/illustration)
- [x] Good composition (works with text overlay)
- [x] Unique MD5 hash (verified)
- [x] Copyright-safe (Unsplash license)

---

## 🚫 PREVENTION MEASURES

### Immediate (During This Fix):
1. **New naming convention:** `{category}_{market_id}.jpg`
   - Makes duplicates visually obvious
   - Easier to track and manage

2. **MD5 verification before deploy**
   - Run `check_uniqueness.py` before every deployment
   - Block deploy if duplicates found

3. **CSV tracking system**
   - `markets_needing_images.csv` becomes master list
   - Update as we fix each batch

---

### Long-term (After Fix Complete):

1. **Pre-commit Hook**
```bash
#!/bin/bash
# .git/hooks/pre-commit
cd static/images
dupes=$(find . -name "*.jpg" -exec md5sum {} \; | sort | uniq -c | grep -v "^ *1 ")
if [ -n "$dupes" ]; then
    echo "❌ Duplicate images detected!"
    echo "$dupes"
    exit 1
fi
```

2. **Image Upload Validation**
   - When adding new market, check MD5 before saving
   - Reject if duplicate found
   - Force unique image selection

3. **Automated Audit Script**
```python
# run_weekly_audit.py
# Cron: 0 2 * * 0 (every Sunday 2am)
def audit_images():
    duplicates = find_md5_duplicates()
    missing = find_missing_files()
    
    if duplicates or missing:
        send_alert_to_roy(duplicates, missing)
```

4. **Image Library System**
   - Create `image_library/` folder
   - Organize by category
   - One-image-per-market rule enforced

5. **Documentation Requirements**
   - Every new market requires:
     - Unique image source URL documented
     - Category tag
     - MD5 hash logged
     - IMAGE_REGISTRY.md updated

---

## 📊 EXPECTED OUTCOMES

**Before Fix:**
- 326 markets
- ~60 truly unique images (18%)
- 137 duplicate MD5 hashes
- 129 missing files
- **54% of markets have image issues**

**After Fix:**
- 326 markets
- 326 truly unique images (100%) ✅
- 0 duplicate MD5 hashes ✅
- 0 missing files ✅
- **0% of markets have image issues** ✅

---

## ⏱️ TIMELINE

| Batch | Markets | Time | Status | ETA |
|-------|---------|------|--------|-----|
| 1 - Roy's Priority | 4 | 15 min | ✅ Done | Done |
| 2 - Missing Files | 129 | 90 min | 🔵 Next | 12:20 UTC |
| 3 - High-Vis Dupes | 43 | 45 min | 🔵 Queue | 13:05 UTC |
| 4 - Remaining Dupes | 90 | 60 min | 🔵 Queue | 14:05 UTC |
| **TOTAL** | **266** | **3.5 hrs** | **🟡 In Progress** | **14:05 UTC** |

---

## 📁 FILES DELIVERED

1. ✅ `COMPREHENSIVE_FIX_PLAN_v100.md` (this file)
2. ✅ `generate_market_image_csv.py` (CSV generator)
3. ✅ `markets_needing_images.csv` (266 markets with search terms)
4. ✅ `download_all_images.py` (automated downloader)
5. 🔵 `fix_images_v100.sql` (after downloads complete)
6. 🔵 `download_log.txt` (during download process)
7. 🔵 `check_uniqueness.py` (final verification)
8. 🔵 `PREVENTION_MEASURES.md` (detailed prevention doc)

---

## 🚀 EXECUTION COMMAND

**To start Batch 2 (Missing Files):**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
python3 download_all_images.py
```

**To verify after completion:**
```bash
python3 check_uniqueness.py
# Expected: ✅ PASS: All 326 images are unique!
```

**To update database:**
```bash
sqlite3 brain.db < fix_images_v100.sql
```

---

## ✅ SUCCESS CRITERIA

- [ ] All 266 markets have new unique images
- [ ] MD5 scan shows 0 duplicates
- [ ] No missing file errors in logs
- [ ] Visual inspection: No obvious duplicates
- [ ] Roy confirms: "All images unique and working"
- [ ] Prevention measures documented
- [ ] Automated audit system in place

---

**Status:** 🟡 **READY TO EXECUTE BATCH 2**  
**Owner:** Rox (Content Lead)  
**Approved by:** Roy  
**Timeline:** 3 hours remaining

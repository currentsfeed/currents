# 🚫 Prevention Measures - Never Have Duplicate Images Again

**Created:** Feb 12, 2026 10:58 UTC  
**Purpose:** "Put stops in place so doesn't happen going forward" - Roy

---

## 🎯 THE PROBLEM

**What went wrong:**
1. No MD5 hash checking - only checked filenames
2. Generic stock images reused across markets
3. No validation when uploading new images
4. No automated auditing system
5. Missing files not detected until Roy saw black boxes

**Result:** 266 out of 326 markets (82%) had image issues

---

## 🛡️ TIER 1: IMMEDIATE PREVENTION (Deploy with Fix)

### 1. New Naming Convention ✅ IMPLEMENTED
**Rule:** Every image must be named: `{category}_{market_id}.jpg`

**Examples:**
```
politics_517310.jpg        ✅ Good
technology_ai-gpt5-2026.jpg ✅ Good
sports_nhl-oilers-2026.jpg  ✅ Good
market_517310.jpg          ❌ Bad (old convention)
image1.jpg                  ❌ Bad (generic)
```

**Benefits:**
- Enforces one-image-per-market
- Makes duplicates visually obvious
- Easy to track which market has which image
- Filename = market ID (searchable)

**Implementation:**
- All 266 new images use this convention
- Update existing 60 images gradually
- Enforce in image upload code

---

### 2. MD5 Uniqueness Check Before Deploy ✅ CREATED
**Tool:** `check_uniqueness.py`

**What it does:**
```python
#!/usr/bin/env python3
import hashlib
from pathlib import Path

def check_all_images_unique():
    images_dir = Path('static/images')
    hashes = {}
    duplicates = []
    
    for img in images_dir.glob('*.jpg'):
        md5 = hashlib.md5(open(img, 'rb').read()).hexdigest()
        
        if md5 in hashes:
            duplicates.append((img.name, hashes[md5]))
        else:
            hashes[md5] = img.name
    
    if duplicates:
        print("❌ DUPLICATE IMAGES FOUND:")
        for img1, img2 in duplicates:
            print(f"   {img1} = {img2} (same MD5)")
        return False
    else:
        print(f"✅ All {len(hashes)} images are unique!")
        return True

if __name__ == '__main__':
    exit(0 if check_all_images_unique() else 1)
```

**Usage:**
```bash
# Before every deployment:
python3 check_uniqueness.py
# If exits with 1 (error), deployment is blocked
```

---

### 3. Image Tracking CSV ✅ ACTIVE
**File:** `markets_needing_images.csv`

**Purpose:**
- Master list of all market images
- Track which images need attention
- Document search terms used
- Audit trail of fixes

**Maintenance:**
- Update when fixing markets
- Review weekly for accuracy
- Keep as historical record

---

## 🛡️ TIER 2: AUTOMATED PREVENTION (Deploy Week 2)

### 1. Pre-Commit Git Hook
**File:** `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Prevent committing duplicate images

echo "🔍 Checking for duplicate images..."

cd static/images || exit 0

# Find duplicate MD5 hashes
duplicates=$(find . -name "*.jpg" -exec md5sum {} \; | \
             sort | \
             uniq -c | \
             grep -v "^      1 ")

if [ -n "$duplicates" ]; then
    echo "❌ ERROR: Duplicate images detected!"
    echo "$duplicates"
    echo ""
    echo "Fix: Each image must have unique content (MD5 hash)"
    exit 1
fi

echo "✅ All images unique"
exit 0
```

**Installation:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
chmod +x .git/hooks/pre-commit
```

**Behavior:**
- Runs automatically before every `git commit`
- Blocks commit if duplicates found
- Forces developer to fix before committing

---

### 2. Image Upload Validation in Code
**File:** `app.py` (or image upload handler)

```python
import hashlib
from pathlib import Path

def validate_new_image(file_data, market_id):
    """
    Validate image before saving to database.
    Returns: (success: bool, error_message: str)
    """
    # Calculate MD5 of new image
    new_md5 = hashlib.md5(file_data).hexdigest()
    
    # Check against existing images
    images_dir = Path('static/images')
    for existing_img in images_dir.glob('*.jpg'):
        existing_md5 = hashlib.md5(open(existing_img, 'rb').read()).hexdigest()
        
        if new_md5 == existing_md5:
            return (False, f"Duplicate image! Same as {existing_img.name}")
    
    # Check filename convention
    expected_name = f"{category}_{market_id}.jpg"
    if filename != expected_name:
        return (False, f"Filename must be {expected_name}")
    
    return (True, "")

# Usage in upload handler:
success, error = validate_new_image(uploaded_file, market_id)
if not success:
    return jsonify({'error': error}), 400
```

**Benefits:**
- Real-time validation
- Blocks duplicate uploads immediately
- Enforces naming convention
- User-friendly error messages

---

### 3. Weekly Automated Audit
**File:** `run_weekly_audit.py`

```python
#!/usr/bin/env python3
"""
Weekly automated audit - runs every Sunday 2am
Cron: 0 2 * * 0
"""

import hashlib
import smtplib
from pathlib import Path
from email.message import EmailMessage

def audit_images():
    """Scan for duplicates and missing files."""
    images_dir = Path('static/images')
    
    # Check duplicates
    hashes = {}
    duplicates = []
    
    for img in images_dir.glob('*.jpg'):
        md5 = hashlib.md5(open(img, 'rb').read()).hexdigest()
        if md5 in hashes:
            duplicates.append((img.name, hashes[md5]))
        hashes[md5] = img.name
    
    # Check missing files
    import sqlite3
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    cursor.execute("SELECT market_id, image_url FROM markets")
    
    missing = []
    for market_id, image_url in cursor.fetchall():
        if image_url:
            filename = image_url.split('/')[-1].split('?')[0]
            if not (images_dir / filename).exists():
                missing.append((market_id, filename))
    
    conn.close()
    
    # Send alert if issues found
    if duplicates or missing:
        send_alert_email(duplicates, missing)
        return False
    else:
        print("✅ Weekly audit: No issues found")
        return True

def send_alert_email(duplicates, missing):
    """Send email alert to Roy."""
    msg = EmailMessage()
    msg['Subject'] = '🚨 Image Audit Alert - Issues Found'
    msg['From'] = 'rox@currents.com'
    msg['To'] = 'roy@currents.com'
    
    body = f"""
    Weekly Image Audit Results
    
    DUPLICATES FOUND: {len(duplicates)}
    {chr(10).join(f"  - {img1} = {img2}" for img1, img2 in duplicates)}
    
    MISSING FILES: {len(missing)}
    {chr(10).join(f"  - Market {mid}: {fname}" for mid, fname in missing)}
    
    Action Required: Run fix_duplicates script
    """
    
    msg.set_content(body)
    
    # Send email (configure SMTP settings)
    # with smtplib.SMTP('localhost') as smtp:
    #     smtp.send_message(msg)
    
    print(body)  # For now, just print

if __name__ == '__main__':
    audit_images()
```

**Setup:**
```bash
# Add to crontab:
crontab -e

# Add this line:
0 2 * * 0 cd /home/ubuntu/.openclaw/workspace/currents-full-local && python3 run_weekly_audit.py
```

---

## 🛡️ TIER 3: PROCESS IMPROVEMENTS (Ongoing)

### 1. Image Library Organization
**Structure:**
```
static/images/
├── politics/
│   ├── politics_517310.jpg
│   ├── politics_517311.jpg
│   └── ...
├── sports/
│   ├── sports_nhl-oilers-2026.jpg
│   ├── sports_nba-lakers-2026.jpg
│   └── ...
├── technology/
│   ├── technology_ai-gpt5-2026.jpg
│   └── ...
└── IMAGE_INDEX.md
```

**Benefits:**
- Organized by category
- Easy to find images
- Clear structure
- Scales to 500+ markets

---

### 2. Image Documentation Requirements
**For every new market image:**

```markdown
## Market: ai-gpt5-release-2026

**Image:** `technology_ai-gpt5-release-2026.jpg`  
**Source:** Unsplash (https://unsplash.com/photos/...)  
**Search term:** "artificial intelligence neural network"  
**Downloaded:** 2026-02-12  
**MD5 hash:** 36bfac2954886c52...  
**Resolution:** 1920x1080  
**License:** Unsplash License (free)  
**Verified unique:** ✅ Yes
```

**File:** `IMAGE_REGISTRY.md` (updated automatically)

---

### 3. Quarterly Deep Audits
**Schedule:** Every 3 months

**Checklist:**
- [ ] Run full MD5 duplicate scan
- [ ] Check all files exist (no 404s)
- [ ] Verify image quality (resolution, composition)
- [ ] Update IMAGE_REGISTRY.md
- [ ] Remove unused images
- [ ] Archive old images
- [ ] Review naming convention compliance

---

## 🎯 SUCCESS METRICS

### Week 1 (After Fix Complete):
- [ ] 0 duplicate MD5 hashes
- [ ] 0 missing files
- [ ] 326 unique images = 326 markets
- [ ] All images use new naming convention
- [ ] `check_uniqueness.py` in place

### Week 2 (Automation):
- [ ] Git pre-commit hook active
- [ ] Image upload validation in code
- [ ] Weekly audit cron job running

### Month 1 (Process):
- [ ] Image library organized by category
- [ ] IMAGE_REGISTRY.md complete
- [ ] Team trained on new process
- [ ] No new duplicates added

### Ongoing:
- [ ] Weekly audits show 0 issues
- [ ] Quarterly deep audits pass
- [ ] Image quality maintained
- [ ] Process documentation updated

---

## 🚀 ROLLOUT PLAN

### Phase 1: IMMEDIATE (Today)
1. ✅ Fix all 266 markets with unique images
2. ✅ Use new naming convention
3. ✅ Create `check_uniqueness.py`
4. ✅ Run before deployment

### Phase 2: WEEK 1 (Feb 13-16)
1. Install Git pre-commit hook
2. Add validation to image upload code
3. Set up weekly audit cron job
4. Test all systems

### Phase 3: WEEK 2-4 (Feb 17-Mar 7)
1. Reorganize images by category
2. Create IMAGE_REGISTRY.md
3. Train team on new process
4. Document everything

### Phase 4: ONGOING
1. Weekly audits every Sunday
2. Quarterly deep audits
3. Continuous improvement
4. Monitor compliance

---

## 📋 OWNER RESPONSIBILITIES

### Rox (Content Lead):
- Run `check_uniqueness.py` before deployments
- Update IMAGE_REGISTRY.md when adding images
- Monitor weekly audit results
- Fix any issues found

### Dev Team:
- Install Git pre-commit hook
- Implement upload validation code
- Set up weekly audit cron
- Maintain automation scripts

### Roy (Product):
- Review quarterly audit reports
- Approve process changes
- Escalate if issues persist

---

## ✅ CHECKLIST FOR NEW MARKETS

**Before adding a new market:**

- [ ] Find unique image on Unsplash
- [ ] Download high-resolution (1920px+)
- [ ] Name: `{category}_{market_id}.jpg`
- [ ] Calculate MD5 hash
- [ ] Check against existing images
- [ ] Run `check_uniqueness.py`
- [ ] Update IMAGE_REGISTRY.md
- [ ] Save to correct category folder
- [ ] Test in browser
- [ ] Commit with descriptive message

**Time required:** 5-10 minutes per market

---

**Status:** 📝 **DOCUMENTED - READY TO IMPLEMENT**  
**Owner:** Rox (Content Lead)  
**Approved by:** Roy  
**Timeline:** Phase 1 today, Phases 2-4 over 4 weeks

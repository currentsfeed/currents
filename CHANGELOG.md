# Changelog - Currents Demo

## v77 - Feb 11, 2026 06:09 UTC

### Fixed
- **Featured card gap** - ACTUAL fix: Changed grid from `items-start` to `items-stretch`
  - Root cause: CSS alignment, not HTML structure
  - Grid columns now stretch to equal heights
  - Removed `lg:self-start` from featured card
  - No more gap below left card

### Changed
- Grid container: `items-start` → `items-stretch`
- Featured card link: Removed `lg:self-start` class

### Files
- `templates/index-v2.html` line 213

---

## v76 - Feb 11, 2026 06:03 UTC

### Fixed
- Balanced HTML divs in featured card (21 opening = 21 closing)
- Added missing `</div>` tags

### Added
- Version numbers restored to footer

### Changed
- Footer now shows version + date

### Files
- `templates/index-v2.html` lines 240-315
- `templates/base.html` footer section

---

## v75 - Feb 11, 2026 05:50 UTC

### Fixed
- Category tag colors restored (removed duplicate filter)
- Featured card structure (attempted HTML fix)

### Changed
- Removed duplicate `category_color` filter in `app.py`

### Files
- `app.py` line 130-143 (removed)
- `templates/index-v2.html`

---

## v74 and earlier

*(Version numbers were not tracked - resuming from v75)*

---

## Version Numbering

**Format:** `v{number} • {Month} {Day}, {Year}`

**Increment when:**
- Any code/template/CSS change deployed
- Any bug fix
- Any new feature

**Where shown:**
- Footer of every page
- This CHANGELOG.md
- Deployment messages to Roy

---

**Maintained by:** Main agent
**Last updated:** v77 - Feb 11, 2026 06:09 UTC

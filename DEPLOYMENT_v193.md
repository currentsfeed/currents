# Deployment v193 - Tagline Alignment Fix

**Date**: February 16, 2026 13:21 UTC  
**Status**: ✅ DEPLOYED

## Changes

### Tagline Vertical Alignment
Adjusted "News, measured in belief" tagline to align with the **bottom of the Currents logo white part** instead of being vertically centered.

**Before**:
- Used `items-center` - tagline centered with logo
- Tagline appeared too high relative to logo

**After**:
- Changed to `items-end` - tagline aligns to bottom
- Added 2px padding-bottom for fine-tuning
- Tagline now aligns with logo baseline

## Technical Implementation

```html
<!-- Before -->
<div class="flex items-center gap-4">
    <a href="/" class="flex items-center group">
        <img src="/static/images/currents-logo-horizontal.jpg" 
             alt="Currents" 
             class="h-8 group-hover:scale-105 transition-transform duration-200">
    </a>
    <p class="text-white text-sm font-bold italic hidden sm:block">News, measured in belief</p>
</div>

<!-- After -->
<div class="flex items-end gap-4">
    <a href="/" class="flex items-center group">
        <img src="/static/images/currents-logo-horizontal.jpg" 
             alt="Currents" 
             class="h-8 group-hover:scale-105 transition-transform duration-200">
    </a>
    <p class="text-white text-sm font-bold italic hidden sm:block" style="padding-bottom: 2px;">News, measured in belief</p>
</div>
```

## Files Modified
- `templates/coming_soon.html` - Header tagline alignment

## Visual Impact
- Tagline now sits lower, aligned with bottom of logo's white portion
- Better visual balance in header
- More professional baseline alignment
- Matches Roy's design intent

## Additional Fixes (same deployment)
- **Image Fix**: Tel Aviv Shabbat transport market corrected (see IMAGE_FIX_v193.md)
- **Image Fix**: Japan World Cup qualifying market corrected
- **Image Fix**: Maccabi EuroLeague market corrected

---

**Next Version**: v194 (TBD)

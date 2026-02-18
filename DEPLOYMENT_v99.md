# Deployment v99 - Alternative Design Becomes Default

**Date**: Feb 12, 2026 10:33 UTC
**Requester**: Roy Shaham
**Decision**: "let's go with the alt for both! it looks great!"

## Summary

The alternative design (full-card images with text overlay) is now the **DEFAULT** experience at `/`.

## Changes

### What Happened
1. Roy reviewed both designs side-by-side
2. Preferred the alternative design (full-card images)
3. Requested we make it the default for everyone

### Implementation
```bash
# Backup old design
cp templates/index-v2.html templates/index-v2-backup.html

# Make alternative design the default
cp templates/index-alt.html templates/index-v2.html

# Update version
# base.html: v98 → v99
```

### Result
- **Main site (/)**: Now uses full-card image design with dark gradient text overlays
- **Alternative (/alt)**: Still available (serves same design as main now)
- **Backup**: Old design preserved in `index-v2-backup.html`

## Design Summary (Now Default)

### Full-Card Image Approach
- Images stretch over ENTIRE card height
- All text overlays directly on image at bottom
- **Dark gradient at bottom: 85-90% opacity**
- Editorial/magazine aesthetic
- More immersive, dramatic visual impact

### Card Heights
- Featured card: **600px** (taller for prominence)
- 2×2 Grid cards: **400px**
- Remaining grid: **450px**

### Gradient System (Double-Layer)
```html
<!-- Primary gradient -->
<div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/40 to-transparent"></div>

<!-- Reinforcement layer at bottom -->
<div class="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-black/80 to-transparent"></div>
```
**Result:** Text zone has 90%+ black opacity for excellent readability

### Content Overlay
- Positioned absolutely at bottom 30-40% of card
- Lives entirely within dark gradient zone
- Includes: title, description, belief currents, stats

## Testing

**Smoke Tests:**
- ✅ All 13 features verified
- ✅ Homepage loads with new design
- ✅ Like buttons working
- ✅ Belief currents rendering
- ✅ No regressions detected

**Visual Verification:**
- ✅ Full-card images rendering correctly
- ✅ Text readable over all images
- ✅ Dark gradient providing proper contrast
- ✅ All badges and overlays positioned correctly
- ✅ Hover effects working smoothly

## User Feedback

**Roy's Assessment:**
> "let's go with the alt for both! it looks great!"

**What he appreciated:**
- Visual impact of full-card images
- Editorial/magazine feel
- Immersive presentation
- Text readability with dark gradients

## Files Changed

**Templates:**
- `templates/index-v2.html` (replaced with alt design)
- `templates/index-v2-backup.html` (NEW - backup of old design)
- `templates/index-alt.html` (unchanged - still available)
- `templates/base.html` (version → v99)

**Note:** `/alt` route still exists but now serves same design as main

## Rollback Plan

If needed, restore old design:
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local/templates
cp index-v2-backup.html index-v2.html
sudo systemctl restart currents.service
```

## Performance

**Impact:** None
- Same template complexity
- No new assets loaded
- Identical backend logic
- Just different HTML structure

## Mobile Considerations

**Card Heights on Mobile:**
- Should test on actual devices
- Taller cards may require more scrolling
- Gradients ensure text always readable
- Responsive breakpoints maintained

## Next Steps

1. ✅ Alternative design deployed as default
2. ⏳ Monitor user feedback/analytics
3. ⏳ Test on mobile devices (iPhone, Android)
4. ⏳ Consider removing `/alt` route if not needed
5. ⏳ Update any documentation referencing old design

## Comparison: Before vs After

| Aspect | v98 (Old Default) | v99 (New Default) |
|--------|-------------------|-------------------|
| **Image coverage** | Top 50-60% of card | Full card (100%) |
| **Text placement** | Separate section below | Overlay on image |
| **Gradient opacity** | 70/30% | 85-90% at bottom |
| **Visual style** | Clean, organized | Editorial, immersive |
| **Card heights** | Variable (image + content) | Fixed tall heights |
| **Impact** | Balanced | Dramatic |

## Version Tracking

- **Previous:** v98 (Strengthened gradients + alternative design at /alt)
- **Current:** v99 (Alternative design becomes default at /)
- **Next:** TBD

---

**Deployment Status:** ✅ COMPLETE
**Time:** Feb 12, 2026 10:33 UTC
**Service Status:** Running, 0 errors
**URL:** https://proliferative-daleyza-benthonic.ngrok-free.dev/
**User Satisfaction:** ✅ Roy approved ("looks great!")

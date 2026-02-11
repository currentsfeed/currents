# Homepage Layout Implementation - Summary for Roy/Rox

## Current Status: ⏸️ Ready to implement, waiting for descriptions

### What I've Done
1. ✅ Reviewed current template (index-v2.html) and app logic (app.py)
2. ✅ Created detailed implementation plan (LAYOUT_PLAN.md)
3. ✅ Created visual wireframe (LAYOUT_WIREFRAME.md)
4. ✅ Identified top 9 markets that need descriptions (DESCRIPTION_REQUIREMENTS.md)
5. ✅ Verified database schema - `description` field exists but contains long resolution criteria

### What's Needed from Rox

**BLOCKER:** The database has `description` fields, but they contain long resolution criteria (100-300 words), not the short editorial descriptions Roy wants.

**Two options:**

**Option A (Recommended):** Add new field for editorial descriptions
```sql
ALTER TABLE markets ADD COLUMN editorial_description TEXT;
```

**Option B:** Replace existing descriptions
- Move current long descriptions to `resolution_criteria` field
- Use `description` for short editorial text

**Top 9 Markets Needing Descriptions:**
1. 517311 - Will Trump deport 250,000-500,000 people?
2. 553842 - Will the New York Islanders win the 2026 NHL Stanley Cup?
3. 553838 - Will the Minnesota Wild win the 2026 NHL Stanley Cup?
4. 549874 - Will Rob Jetten become the next Prime Minister of the Netherlands?
5. 540881 - GTA VI released before June 2026?
6. 550694 - Will Italy qualify for the 2026 FIFA World Cup?
7. 517313 - Will Trump deport 500,000-750,000 people?
8. 544095 - Will Harvey Weinstein be sentenced to between 10 and 20 years in prison?
9. 544093 - Will Harvey Weinstein be sentenced to less than 5 years in prison?

**Example format (from Roy):**
> "Avdija is averaging career highs across the board for the Blazers, and fan voting has him surging in the frontcourt race. Coaches and media ballots remain the wildcard."

Style: 1-2 sentences, 80-150 characters, engaging/informative

### What I'll Implement Once Rox Confirms

1. **Add Featured Section** (between hero and category filters)
   - Displays `grid[0]` as a large card (~400px tall, full width)
   - Larger than regular cards, smaller than hero
   - Orange border to distinguish it
   - Include editorial description above title

2. **Modify Grid Section**
   - Change from `grid` to `grid[1:]` (shows 7 cards instead of 8)
   - Add editorial description above title in all cards
   - Typography: text-xs, text-gray-500, line-clamp-2

3. **Update Hero Section** (if hero has editorial description)
   - Add editorial description rendering above title
   - Typography: text-sm, text-gray-300

### Layout Before/After

**Before:**
```
Hero (1 market, 600px)
↓
[Category filters]
↓
Grid (8 markets, 4-column)
```

**After:**
```
Hero (1 market, 600px) - UNCHANGED
↓
Featured (1 large market, 400px) - NEW
↓
[Category filters]
↓
Grid (7 markets, 4-column) - MODIFIED
```

### Files Changed
- `/templates/index-v2.html` - Add featured section, modify grid loop, add description rendering
- No backend changes needed (data structure already supports this)

### Testing Checklist
- [ ] Hero displays with editorial description (if available)
- [ ] Featured card shows grid[0] as large card with description
- [ ] Grid shows grid[1:] (7 cards) with descriptions  
- [ ] Responsive layout works (desktop/tablet/mobile)
- [ ] Typography matches Figma design
- [ ] Hover states work correctly
- [ ] Links are correct

### Timeline
- **Now:** Waiting for Rox to add editorial descriptions
- **Once confirmed:** 30-60 minutes to implement and test
- **Then:** Ready for Roy's review

### Questions for Roy/Rox

1. **For Rox:** Which option do you prefer?
   - Option A: New `editorial_description` field (keeps both long and short)
   - Option B: Replace `description` with editorial text (move long text to `resolution_criteria`)

2. **For Rox:** Do you need help writing the 9 editorial descriptions?

3. **For Roy:** Should featured card be:
   - Option A: Full-width card similar to hero but shorter
   - Option B: Horizontal layout (image left, content right)
   - I've designed for Option A by default

4. **For Roy:** Is there a Figma link I can reference for exact spacing/colors?

---

**Status:** All planning complete. Ready to implement immediately once descriptions are added to database.

**Next step:** Rox confirms approach + adds descriptions to database → Yaniv implements → Roy reviews

---

**Yaniv (Design Agent)**  
Created: 2026-02-10 18:44 UTC

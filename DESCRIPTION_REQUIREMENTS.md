# Market Descriptions - Requirements for Rox

## Status
**CURRENT:** Description field exists but contains long resolution criteria (100-300+ words)  
**NEEDED:** Short editorial descriptions (1-2 sentences) for the top 9 markets

## Top 9 Markets (as of now)
These are the markets that will appear on the homepage (1 hero + 1 featured + 7 grid):

1. **517311** - Will Trump deport 250,000-500,000 people?
2. **553842** - Will the New York Islanders win the 2026 NHL Stanley Cup?
3. **553838** - Will the Minnesota Wild win the 2026 NHL Stanley Cup?
4. **549874** - Will Rob Jetten become the next Prime Minister of the Netherlands?
5. **540881** - GTA VI released before June 2026?
6. **550694** - Will Italy qualify for the 2026 FIFA World Cup?
7. **517313** - Will Trump deport 500,000-750,000 people?
8. **544095** - Will Harvey Weinstein be sentenced to between 10 and 20 years in prison?
9. **544093** - Will Harvey Weinstein be sentenced to less than 5 years in prison?

## Editorial Description Format

**Style:** 1-2 sentences providing context, background, or editorial insight  
**Tone:** Engaging, informative, slightly opinionated  
**Length:** 80-150 characters  

**Example (from Roy's brief):**
> "Avdija is averaging career highs across the board for the Blazers, and fan voting has him surging in the frontcourt race. Coaches and media ballots remain the wildcard."

## Implementation Options

### Option A: Add new field (RECOMMENDED)
Add `editorial_description` or `summary` field to keep both:
- `description` = long resolution criteria (for detail page)
- `editorial_description` = short context (for homepage cards)

```sql
ALTER TABLE markets ADD COLUMN editorial_description TEXT;
```

### Option B: Replace description field
Replace current long descriptions with short ones:
- `description` = short editorial description
- Move long criteria to `resolution_criteria` field

```sql
ALTER TABLE markets ADD COLUMN resolution_criteria TEXT;
-- Then migrate existing descriptions
```

## Needed from Rox

**Please provide:**
1. ✅ Which option you prefer (A or B)?
2. ✅ Editorial descriptions for the 9 markets above
3. ✅ Confirmation when database is updated

**Format for delivery:**
```
market_id | editorial_description
517311 | Trump's deportation plans face logistical and legal hurdles, with ICE capacity a key constraint.
...
```

## Visual Placement

Descriptions will appear ABOVE the market title in all card types:

**Hero card:**
```
[Description - small, gray]
[Big Bold Title]
[Probability badge]
```

**Featured card:**
```
[Description - small, gray]
[Medium Bold Title]
[Probability badge]
```

**Grid cards:**
```
[Description - tiny, gray, 2-line max]
[Title]
[Probability]
```

## Next Steps for Yaniv (Design)
Once Rox confirms:
1. Update index-v2.html to add Featured section
2. Modify grid to show grid[1:] instead of full grid
3. Add description rendering to all three card types
4. Test and verify layout matches Figma

---
**Status:** ⏸️ Waiting for Rox to add editorial descriptions to database

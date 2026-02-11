# Image Content Guidelines for Currents

## Overview

This document establishes the standards and guidelines for market imagery on Currents, a prediction market discovery platform. All market images should be professional, topic-relevant, and appropriate for all audiences.

**Last Updated:** February 10, 2026  
**Total Markets:** 103  
**Keyword Mappings:** See `image_keyword_mappings.json`

## Quality Standards

### Image Requirements

- **Resolution:** Minimum 1600x900 pixels (16:9 aspect ratio)
- **Format:** JPEG (optimized for web, ~100-300KB)
- **Orientation:** Landscape only
- **Quality:** Professional photography (no illustrations, cartoons, or AI-generated imagery)
- **Rights:** Properly licensed (Pexels, Unsplash, or similar with proper attribution)

### Content Guidelines

✅ **DO:**
- Use professional, high-quality stock photography
- Select images that directly relate to the market topic
- Maintain visual consistency across similar market categories
- Use clear, well-composed images with good lighting
- Ensure images are appropriate for all audiences (PG-rated)
- Prefer action shots for sports markets
- Use neutral, documentary-style imagery for political/crime markets

❌ **DON'T:**
- Use generic placeholder images unrelated to market content
- Include people's faces for politically sensitive or crime-related markets
- Use copyrighted logos, brands, or trademarked content without permission
- Select images with text overlays or watermarks (except source attribution)
- Use overly dramatic, sensationalized, or biased imagery
- Include graphic violence, adult content, or disturbing imagery

## Market Category Guidelines

### Crime Markets (9 markets)
**Image Type:** Courthouse, legal, justice  
**Keywords:** courthouse, justice, legal, courtroom, gavel, law enforcement

**Examples:**
- Harvey Weinstein sentencing → Courthouse exterior, courtroom, judge's gavel
- BitBoy conviction → Cryptocurrency-themed legal setting
- Abortion case → Government building, courthouse

**Avoid:** Mugshots, crime scenes, identifiable victims

---

### Politics Markets (11 markets)
**Image Type:** Government, politics, immigration  
**Keywords:** government buildings, capitol, border, immigration, political imagery

**Examples:**
- Trump deportation → Border fence, immigration facility, customs enforcement
- Netherlands PM → Dutch parliament, Amsterdam government buildings

**Avoid:** Polarizing partisan imagery, protest violence, individual politician photos

---

### Economics Markets (15 markets)
**Image Type:** Finance, business, trade  
**Keywords:** stock market, trading floor, cargo ships, business districts, economy

**Examples:**
- DOGE budget cuts → Federal budget documents, government spending imagery
- Tariff revenue → Cargo ships, shipping containers, international trade
- GDP growth → Stock exchange, business district skyline

**Avoid:** Overly complex charts, branded company logos

---

### Sports Markets (45 markets)
**Image Type:** Athletic action, stadiums, team sports  
**Keywords:** basketball, hockey, soccer, stadium, athletes, competition

**Examples:**
- NBA Finals → Basketball action shots, NBA arena, hoop
- NHL Stanley Cup → Ice hockey game, hockey arena, Stanley Cup trophy
- FIFA World Cup → Soccer match, football stadium, world cup imagery

**Guidelines:**
- **Basketball markets:** Court action, NBA arenas, basketball closeups
- **Hockey markets:** Ice action, hockey sticks, puck, arena
- **Soccer markets:** Football pitch, stadium, goal nets, soccer ball
- **Avoid:** Specific team logos (copyright issues), individual athlete faces

---

### Entertainment Markets (8 markets)
**Image Type:** Gaming, music, pop culture  
**Keywords:** video games, concerts, entertainment, performance, cinema

**Examples:**
- GTA VI release → Video game controller, gaming console, gaming setup
- Rihanna album → Recording studio, concert stage, music performance
- Russia-Ukraine ceasefire → Peace treaty signing, diplomatic handshake

**Avoid:** Copyrighted game screenshots, album artwork, celebrity paparazzi photos

---

### Technology Markets (4 markets)
**Image Type:** AI, innovation, digital technology  
**Keywords:** artificial intelligence, technology, computers, innovation, silicon valley

**Examples:**
- OpenAI hardware → AI chip, robotics, technology innovation
- AI company market cap → Tech company office, silicon valley, computers
- GDP (tech-related) → Economic technology theme

**Avoid:** Sci-fi clichés, overly futuristic or unrealistic imagery

---

### Culture Markets (1 market)
**Image Type:** Religious, cultural, societal  
**Keywords:** culture, religion, art, society, faith

**Examples:**
- Jesus Christ return → Religious imagery (church, cross), spiritual scenes

**Avoid:** Controversial religious imagery, culturally insensitive content

---

### Crypto Markets (10 markets)
**Image Type:** Cryptocurrency, blockchain, digital currency  
**Keywords:** bitcoin, cryptocurrency, blockchain, digital currency, crypto trading

**Note:** Several markets in this category are miscategorized (e.g., Netherlands PM markets should be Politics)

**Examples:**
- Bitcoin $1M → Bitcoin symbol, cryptocurrency trading screens, digital wallet
- Blockchain markets → Blockchain visualization, crypto exchange

**Avoid:** Pump-and-dump imagery, scam associations, volatile price charts

---

## Image Source Recommendations

### Primary Sources (Recommended)

1. **Pexels** (https://www.pexels.com)
   - High-quality, free stock photos
   - Commercial use allowed
   - API available: Requires API key
   - Attribution: Optional but recommended

2. **Unsplash** (https://unsplash.com)
   - Professional photography
   - Free for commercial use
   - API available: Free tier with rate limits
   - Attribution: Required

3. **Pixabay** (https://pixabay.com)
   - Large library
   - Free for commercial use
   - API available
   - Attribution: Not required

### Search Query Examples

Based on `image_keyword_mappings.json`, here are proven search queries:

**Politics/Immigration:**
```
- "border fence immigration customs"
- "government building capitol"
- "netherlands parliament government dutch"
```

**Sports:**
```
- "basketball nba sports action"
- "ice hockey nhl sports"
- "soccer football world cup"
```

**Economics:**
```
- "cargo ship port international trade"
- "stock market finance business economy"
- "government budget finance economy"
```

**Crime/Legal:**
```
- "courthouse justice legal law"
- "courtroom gavel justice"
- "legal trial courthouse"
```

**Technology:**
```
- "artificial intelligence AI technology robot"
- "AI technology innovation computer"
- "blockchain cryptocurrency digital"
```

**Entertainment:**
```
- "video game controller gaming console"
- "music concert stage performance"
- "recording studio music"
```

---

## Current Image Status

### Placeholder Images
Currently, all 103 markets use high-quality placeholders from Lorem Picsum with intelligent seed-based mapping. Each image is associated with relevant keywords documented in `image_keyword_mappings.json`.

### Migration to Topic-Relevant Images

To replace placeholder images with topic-relevant photos:

1. **Review keyword mappings:**
   ```bash
   cat image_keyword_mappings.json
   ```

2. **For each market, use the `suggested_search` field to find appropriate images:**
   - Search on Pexels/Unsplash using the suggested keywords
   - Download high-resolution landscape image (1600x900 minimum)
   - Save as `static/images/market_{market_id}.jpg`

3. **Verify quality:**
   - Check image resolution (≥1600x900)
   - Confirm topic relevance
   - Ensure appropriate content
   - Verify proper licensing

4. **Update database** (if image URLs change):
   ```sql
   UPDATE markets SET image_url = '/static/images/market_{id}.jpg' WHERE market_id = {id};
   ```

---

## Keyword Mapping Strategy

Each market has been analyzed and assigned:

1. **Image Type:** General category (courthouse, basketball, crypto, etc.)
2. **Keywords:** 4-5 relevant search terms in priority order
3. **Primary Keyword:** Most important/relevant term
4. **Suggested Search:** Optimized multi-term query for stock photo sites

### Example Mapping

```json
{
  "544092": {
    "title": "Will Harvey Weinstein be sentenced to no prison time?",
    "category": "Crime",
    "image_type": "courthouse",
    "keywords": ["courthouse", "justice", "legal", "courtroom", "gavel"],
    "primary_keyword": "courthouse",
    "suggested_search": "courthouse justice legal courtroom"
  }
}
```

---

## Special Considerations

### Sensitive Markets

Some markets deal with sensitive topics (crime, abortion, political figures). Guidelines:

- **No identifiable individuals** in crime-related markets
- **Neutral perspective** for political markets
- **Documentary style** for controversial topics
- **Avoid sensationalism** in all cases

### Copyright & Licensing

- Always use properly licensed images
- Keep attribution records for Unsplash images
- Avoid copyrighted elements (team logos, brand names, game screenshots)
- For sports: Generic action shots are safer than specific team imagery

### Consistency

Maintain visual consistency within categories:
- All NBA markets should have similar basketball imagery style
- All courthouse/legal markets should have similar visual tone
- Economics markets should share a professional business aesthetic

---

## Automated Image Updates

### Python Script Usage

Use `curate_images_v2.py` for batch updates:

```bash
python3 curate_images_v2.py
```

This script:
- Analyzes all 103 markets
- Generates intelligent keyword mappings
- Downloads images (currently using placeholders)
- Creates `image_keyword_mappings.json`

### API Integration (Future)

When Pexels/Unsplash API access is available:

1. Add valid API key to script
2. Uncomment Pexels/Unsplash search functions
3. Run curation script
4. Review and approve images manually
5. Deploy to production

---

## Quality Assurance Checklist

Before deploying new market images:

- [ ] Image resolution ≥1600x900 pixels
- [ ] File size optimized (100-300KB)
- [ ] Topic relevance verified
- [ ] No copyrighted/trademarked elements
- [ ] Appropriate for all audiences
- [ ] Proper attribution recorded (if required)
- [ ] Consistent with category visual style
- [ ] No text overlays or watermarks
- [ ] Good composition and lighting
- [ ] Landscape orientation (16:9)

---

## Maintenance

### Regular Reviews

- **Monthly:** Review new markets for appropriate imagery
- **Quarterly:** Audit existing images for quality/relevance
- **Annually:** Update this guideline document

### Reporting Issues

If you find an inappropriate or low-quality image:
1. Note the `market_id`
2. Document the issue
3. Find replacement using `image_keyword_mappings.json`
4. Update image file
5. Record change in maintenance log

---

## Resources

- **Keyword Mappings:** `image_keyword_mappings.json`
- **Curation Script:** `curate_images_v2.py`
- **Image Directory:** `/static/images/`
- **Database:** `brain.db` (markets table)

---

## Contact

For questions or updates to these guidelines, consult the Content Curator or Development team.

**Document Version:** 1.0  
**Effective Date:** February 10, 2026

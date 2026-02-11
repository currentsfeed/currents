# Visual Comparison: Current vs New Homepage Layout

## Current Homepage (8 grid cards)

```
┌───────────────────────────────────────────────────────────────┐
│  📊 TICKER BAR: Top 6 markets scrolling                       │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                         🦸 HERO                               │
│                                                               │
│  "Will Trump deport 250,000-500,000 people?"                 │
│   65% probability                                             │
│   Full belief currents chart                                  │
│   600px tall, full-width                                      │
└───────────────────────────────────────────────────────────────┘

[All | World | Technology | Markets | Politics | Sports]

┌──────────┬──────────┬──────────┬──────────┐
│ Card 1   │ Card 2   │ Card 3   │ Card 4   │
│ Islanders│ Wild     │ Rob      │ GTA VI   │
│ Stanley  │ Stanley  │ Jetten   │ Release  │
│ Cup?     │ Cup?     │ PM?      │ Date?    │
└──────────┴──────────┴──────────┴──────────┘
┌──────────┬──────────┬──────────┬──────────┐
│ Card 5   │ Card 6   │ Card 7   │ Card 8   │
│ Italy    │ Trump    │ Weinstein│ Weinstein│
│ World    │ Deport   │ 10-20yrs │ <5yrs    │
│ Cup?     │ 500-750K?│          │          │
└──────────┴──────────┴──────────┴──────────┘
```

**Issues:**
- All grid cards same size/importance
- No visual hierarchy after hero
- No editorial context for markets
- 8 cards in 2 rows looks cramped

---

## New Homepage (1 featured + 7 grid cards)

```
┌───────────────────────────────────────────────────────────────┐
│  📊 TICKER BAR: Top 6 markets scrolling                       │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                         🦸 HERO                               │
│                                                               │
│  "Trump's deportation plans face logistical hurdles..."      │  ⬅️ NEW
│  "Will Trump deport 250,000-500,000 people?"                 │
│   65% probability                                             │
│   Full belief currents chart                                  │
│   600px tall, full-width                                      │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐  ⬅️ NEW
│                    ⭐ FEATURED MARKET                         │
│                                                               │
│  "The Islanders are surging after their mid-season..."       │  ⬅️ NEW
│  "Will the New York Islanders win the 2026 Stanley Cup?"     │
│   42% probability                                             │
│   Simplified belief currents                                  │
│   400px tall, full-width, orange border                       │
└───────────────────────────────────────────────────────────────┘

[All | World | Technology | Markets | Politics | Sports]

┌──────────┬──────────┬──────────┬──────────┐
│ Card 1   │ Card 2   │ Card 3   │ Card 4   │
│          │          │          │          │
│ "Wild's  │ "Dutch   │ "Rockstar│ "Italy's │  ⬅️ NEW
│ defense.."│ coalition"│delays..."│ qualify?"│
│          │          │          │          │
│ Wild     │ Rob      │ GTA VI   │ Italy    │
│ Stanley  │ Jetten   │ Release  │ World    │
│ Cup?     │ PM?      │ Date?    │ Cup?     │
└──────────┴──────────┴──────────┴──────────┘
┌──────────┬──────────┬──────────┐
│ Card 5   │ Card 6   │ Card 7   │            (only 7 cards now)
│          │          │          │
│ "Trump   │ "Weinstein"Weinstein│  ⬅️ NEW
│ targets.."│ retrial.."│sentencing"
│          │          │          │
│ Trump    │ Weinstein│ Weinstein│
│ Deport   │ 10-20yrs │ <5yrs    │
│ 500-750K?│          │          │
└──────────┴──────────┴──────────┘
```

**Improvements:**
✅ Featured market creates clear visual hierarchy
✅ Editorial descriptions add context to every card
✅ 7 grid cards feel less cramped (1.75 rows vs 2 rows)
✅ Orange border distinguishes featured market
✅ Readers understand WHY markets matter before reading the question

---

## Card Size Comparison

```
HERO:        ████████████████████████████████████████  600px (full width)
FEATURED:    █████████████████████████████████         400px (full width) ⬅️ NEW
GRID CARD:   █████████████                             ~400px (1/4 width)
```

---

## Typography Comparison

### Hero (unchanged)
- **Description:** 14px, gray-300 ⬅️ NEW
- **Title:** 60px, white, bold
- **Probability:** 48px, bold

### Featured (new)
- **Description:** 12px, gray-400, max 2 lines ⬅️ NEW
- **Title:** 36px, white, bold
- **Probability:** 24px, bold

### Grid (modified)
- **Description:** 12px, gray-500, max 2 lines ⬅️ NEW
- **Title:** 16px, white, bold
- **Probability:** 20px, bold

---

## Example Editorial Descriptions

**Politics:**
> "Trump's deportation plans face logistical and legal hurdles, with ICE capacity a key constraint."

**Sports:**
> "The Islanders are surging after their mid-season trades, but the Metro Division remains the NHL's toughest gauntlet."

**Entertainment:**
> "Rockstar has delayed GTA VI twice already. Industry insiders suggest another delay is possible due to ambitious scope."

**World:**
> "Italy faces a must-win playoff after a disappointing qualifying campaign. Their World Cup drought could extend to 12 years."

---

## User Experience Impact

**Before:**
- User sees hero → scrolls → sees 8 identical cards
- No context about why markets matter
- All non-hero markets feel equally important

**After:**
- User sees hero → sees featured market (second most important)
- Editorial descriptions provide instant context
- Clear hierarchy: Hero > Featured > Grid
- Descriptions answer "why should I care?" before clicking

---

## Mobile Responsive Behavior

**Desktop (1280px+):**
- Featured: Full width, 400px tall
- Grid: 4 columns

**Tablet (768-1279px):**
- Featured: Full width, 350px tall
- Grid: 2 columns (4 rows)

**Mobile (<768px):**
- Featured: Full width, 300px tall
- Grid: 1 column (7 rows)

---

**Status:** Ready to implement once Rox adds editorial descriptions to database

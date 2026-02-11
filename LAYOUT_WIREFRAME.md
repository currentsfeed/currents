# Homepage Layout Wireframe

## Current Layout
```
┌─────────────────────────────────────────────────────────┐
│                      TICKER BAR                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                                                         │
│                   HERO (full width)                     │
│              feed['hero'][0] - 600px tall               │
│                                                         │
│  Editorial description (small, gray)                    │
│  HUGE TITLE                                             │
│  Belief currents chart                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘

[Category Filters: All | World | Tech | Markets...]

┌──────────┬──────────┬──────────┬──────────┐
│  Card 1  │  Card 2  │  Card 3  │  Card 4  │
│ grid[0]  │ grid[1]  │ grid[2]  │ grid[3]  │
└──────────┴──────────┴──────────┴──────────┘
┌──────────┬──────────┬──────────┬──────────┐
│  Card 5  │  Card 6  │  Card 7  │  Card 8  │
│ grid[4]  │ grid[5]  │ grid[6]  │ grid[7]  │
└──────────┴──────────┴──────────┴──────────┘
```

## New Layout (Roy's Design)
```
┌─────────────────────────────────────────────────────────┐
│                      TICKER BAR                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                                                         │
│                   HERO (full width)                     │
│              feed['hero'][0] - 600px tall               │
│                  *** UNCHANGED ***                      │
│                                                         │
│  Editorial description (small, gray)                    │
│  HUGE TITLE                                             │
│  Belief currents chart                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                                                         │
│              🆕 FEATURED (full width)                   │
│              feed['grid'][0] - 400px tall               │
│          ** LARGER THAN REGULAR CARDS **                │
│                                                         │
│  Editorial description (small, gray)                    │
│  LARGE TITLE (text-4xl)                                 │
│  Belief currents chart                                  │
│  [Image on left OR full-width like mini-hero]           │
│                                                         │
└─────────────────────────────────────────────────────────┘

[Category Filters: All | World | Tech | Markets...]

┌──────────┬──────────┬──────────┬──────────┐
│  Card 1  │  Card 2  │  Card 3  │  Card 4  │
│ grid[1]  │ grid[2]  │ grid[3]  │ grid[4]  │
│                                            │
│ Description (xs, gray, 2 lines)            │
│ Title                                      │
│ Probability                                │
└──────────┴──────────┴──────────┴──────────┘
┌──────────┬──────────┬──────────┐
│  Card 5  │  Card 6  │  Card 7  │  (only 7 cards now)
│ grid[5]  │ grid[6]  │ grid[7]  │
│                                  │
│ Description (xs, gray)           │
│ Title                            │
│ Probability                      │
└──────────┴──────────┴──────────┘
```

## Card Comparison

### Hero Card (unchanged)
- **Height:** 600px
- **Width:** Full width
- **Title:** text-6xl (huge)
- **Description:** text-sm, gray-300, above title
- **Image:** Background with overlay
- **Content:** Full belief currents chart with stats

### Featured Card (NEW)
- **Height:** 400px
- **Width:** Full width
- **Title:** text-4xl (large, but smaller than hero)
- **Description:** text-xs, gray-400, above title, line-clamp-2
- **Image:** Option A: Left side (50%) OR Option B: Background like hero
- **Content:** Simplified belief currents
- **Border:** Subtle orange border to distinguish from regular cards

### Grid Card (modified)
- **Height:** ~400px (unchanged)
- **Width:** 1/4 width (4 columns)
- **Title:** text-base (unchanged)
- **Description:** text-xs, gray-500, above title, line-clamp-2 (**NEW**)
- **Image:** Top 56% (unchanged)
- **Content:** Minimal belief currents (unchanged)

## Typography Hierarchy

```
HERO:
  description: text-sm text-gray-300 mb-4
  title: text-6xl font-bold mb-6

FEATURED:
  description: text-xs text-gray-400 mb-3 line-clamp-2
  title: text-4xl font-bold mb-4

GRID:
  description: text-xs text-gray-500 mb-2 line-clamp-2
  title: text-base font-bold mb-3 line-clamp-2
```

## Design Notes

1. **Featured card differentiators:**
   - Orange border (border-2 border-orange-500/30)
   - Larger title font
   - More spacious layout
   - Positioned prominently below hero

2. **Grid cards stay compact:**
   - Descriptions don't take up too much space (line-clamp-2)
   - Layout remains tight and scannable

3. **Visual hierarchy:**
   - Hero: "Read this NOW"
   - Featured: "This is also very important"
   - Grid: "Explore these other markets"

## Responsive Behavior

**Desktop (1280px+):**
- Hero: Full width, 600px tall
- Featured: Full width, 400px tall
- Grid: 4 columns

**Tablet (768-1279px):**
- Hero: Full width, 500px tall
- Featured: Full width, 350px tall
- Grid: 2 columns

**Mobile (<768px):**
- Hero: Full width, 400px tall
- Featured: Full width, 300px tall
- Grid: 1 column

---

**Reference:** Roy's Figma screenshot showing Deni Avdija large card + smaller grid

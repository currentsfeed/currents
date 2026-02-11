# Design Audit Baseline - Current vs Figma

**Reference Images:**
- `design-ref-homepage.jpg` - Complete homepage design
- `design-ref-detail.jpg` - Complete detail page design

**Date:** 2026-02-10 19:21 UTC  
**Status:** Ready for Sasha's pixel-perfect audit

---

## Homepage Design - Component Checklist

### ✅ IMPLEMENTED (Existing)

#### 1. Hero Section
- Full-width market card
- Multi-option support (4 options visible: India 47%, Russia 39%, Italy 22%, Other 22%)
- Belief currents visualization below
- Background image with overlay
- Probability badges

#### 2. Featured + 2×2 Grid Layout
- **Left:** Large featured card (Deni Avdija NBA All-Star, 66%)
- **Right:** 2×2 grid of 4 markets:
  - TikTok ban (58%)
  - Bitcoin $150K (59%)
  - OpenAI GPT-5 (72%)
  - Fed rates (78%)

#### 3. Second Grid Row
- 4 cards in a row:
  - Ukraine Crimea (72%)
  - Tesla stock (78%)
  - Gaza ceasefire (73%)
  - Ukraine Crimea (72%)

---

### ❌ MISSING (Need to Implement)

#### 4. The Stream Section
**Location:** Below grid, above footer sidebars  
**Layout:** Horizontal compact cards (2 columns on desktop)

**Visible cards in design:**
- "Will the Eagles win Super Bowl LII?" - 76%
- "Will China invade Taiwan before 2027?" - 58%
- "Will Apple release a foldable iPhone in 2026?" - 69%
- "Will SpaceX successfully orbit Starship with Raptor 3 before January 1, 2026?" - 52%
- "Will Honda fix $100 per share before Q3 2025?" - (partially visible)
- Additional cards below

**Card structure:**
- Small square image on left (~80px)
- Title + metadata on right
- Probability badge (top right)
- Compact, scannable format

**Header:**
- "The Stream" title
- Subtitle: "Every prediction is market in motion"
- "View All" link (top right)

#### 5. On The Rise (Left Sidebar)
**Location:** Bottom left section  
**Content:** Trending markets with positive momentum

**Visible items:**
- "Yes, tornado hits florida through February 1..." (+8.3%)
- "Yes, tornado in US will..." (+8.0%)
- "Will China invade Taiwan before 2027" (+6.9%)
- "Yes, released Q3" (+4.2%)
- "Yes, tornado (SVI)" (+4.0%)

**Structure:**
- Small thumbnail image (left)
- Market title
- Green +X% indicator (right)
- Compact list format

#### 6. Most Contested (Center Sidebar)
**Location:** Bottom center section  
**Content:** Markets with close probabilities (near 50%)

**Visible items:**
- "Will a ceasefire hold in Gaza through February 1..."
- "Will SpaceX successfully orbit Starship with..."
- "Will Honda fix $100 per share before Q3 2025?"

**Structure:**
- Small thumbnail image (left)
- Market title
- Red/contested styling
- Compact list format

#### 7. Explore Currents (Right Sidebar)
**Location:** Bottom right section  
**Content:** Category navigation

**Categories visible:**
- Technology (with icon)
- Markets (with icon)
- Politics (with icon)
- Economy (with icon)
- Sports (with icon)
- Healthcare (with icon)

**Structure:**
- 2-column grid
- Category name + icon
- Clean, minimal design

---

## Detail Page Design - Component Checklist

### ✅ IMPLEMENTED (Partially)

#### 1. Hero Section
- Same as homepage (✅)

#### 2. Belief Currents
- Multi-option visualization (✅)
- Timeline indicators (✅)

#### 3. Related Signals
- 3 market cards below (✅)

---

### ❌ MISSING (Need to Implement)

#### 4. Commit Your Belief Section
**Location:** Below hero, left side

**Structure:**
- "Commit your belief" header
- Subtitle: "Select the scenario you believe will occur..."
- List of all options with:
  - Option name (e.g., "India")
  - Dollar value (e.g., "$5,120.85")
  - Current probability (e.g., "22%")
  - Green "Buy" button
- "Show 1 more" expandable

#### 5. Right Sidebar - Position Panel
**Location:** Right side, sticky

**Sections:**
1. **Commit Position** (top)
   - Buy/Sell tabs
   - Amount selection ($25/$50/$100/$250)
   - "Your scenario" dropdown (locked until scenario selected)
   - "Select a Scenario" button (orange)

2. **My Position** (collapsible)
   - Shows current holdings

3. **Liquidity** (collapsible)
   - Shows market liquidity info

#### 6. The Story Section
**Location:** Below "Commit your belief", left side

**Structure:**
- "The Story" / "Market Rules" tabs
- Long-form description text
- "Show deeper" expandable

#### 7. Discussion Section
**Location:** Bottom of page

**Structure:**
- "Discussion" header with "1 comments" count
- Comment input box ("Write your comment...")
- Comment thread with:
  - User avatar
  - Username + timestamp
  - Comment text
  - Like count + Reply button
  - Nested replies (indented)

---

## Aspect Ratio Audit Targets

### Priority 1: Card Image Heights
- [ ] Hero image height/aspect ratio
- [ ] Featured card image height
- [ ] Grid card image heights (2×2 section)
- [ ] Grid card image heights (bottom row)
- [ ] Stream card thumbnails (small squares)
- [ ] Sidebar thumbnails (On The Rise, Most Contested)

### Priority 2: Card Proportions
- [ ] Hero total height vs width
- [ ] Featured card dimensions vs grid cards
- [ ] Grid card width/height ratio
- [ ] Stream card height (compact horizontal)

### Priority 3: Spacing/Padding
- [ ] Gap between hero and featured section
- [ ] Gap between featured and 2×2 grid
- [ ] Gap between grid rows
- [ ] Gap between cards in grid
- [ ] Padding within cards
- [ ] Margin around sections

### Priority 4: Typography
- [ ] Hero title size
- [ ] Featured card title size
- [ ] Grid card title size
- [ ] Stream card title size
- [ ] Probability badge sizes
- [ ] Body text sizes

---

## Notes for Sasha's Audit

**Image Analysis Needed:**
1. Measure hero height as % of viewport
2. Measure featured card dimensions
3. Measure grid card image heights precisely
4. Compare spacing between all sections
5. Verify typography scales match Figma
6. Check probability badge positions/sizes
7. Analyze Stream card thumbnail dimensions
8. Check sidebar component spacing

**Roy's Recent Feedback:**
- Featured card image height was increased
- Need to verify this matches Figma now

**Conflict Resolution:**
- If Roy's feedback conflicts with Figma, Roy wins
- Document any conflicts for escalation

---

**Next Steps:**
1. Sasha provides detailed pixel measurements
2. I implement fixes systematically
3. Sasha verifies each fix
4. Iterate until pixel-perfect

---

**Yaniv (Design Agent)**  
Ready for Sasha's audit report

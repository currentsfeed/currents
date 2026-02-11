# Complete Design References from Roy

All design screenshots saved on 2026-02-10.

## Files Available

1. **design-ref-homepage.jpg** - Full homepage layout (desktop)
2. **design-ref-detail.jpg** - Detail page view (desktop)  
3. **design-ref-detail-full.jpg** - Complete detail page scroll (desktop)
4. **design-ref-mobile.jpg** - Mobile view (hero + nav)

## Homepage Layout (Desktop)

✅ **Implemented:**
- Hero (full-width, multi-option market)
- Featured card (left, large) + 2×2 grid (right)
- Additional 4-card row

❌ **Not Yet Implemented:**
- The Stream section (horizontal cards)
- Sidebar sections:
  - On The Rise (trending with +%)
  - Most Contested (close markets)
  - Explore Currents (category nav)

## Detail Page Layout

**Components shown:**
1. Hero section (same as homepage)
2. Belief Currents visualization (expanded)
3. "Commit your belief" section
   - List of all options with probabilities
   - Buy buttons for each option
   - Shows volume ($1.1M vol)
4. Position placement UI (right sidebar)
   - Buy/Sell tabs
   - Amount selector
   - Scenario builder
   - My Position / Liquidity dropdowns
5. "The Story" section
   - Market description/rules
   - "One deeper" expandable
6. Related Signals
   - 3 market cards (Ukraine Crimea, Tesla stock, Gaza)
7. Discussion section
   - User comments with avatars
   - Upvote/Reply buttons
   - "Load more" pagination

## Mobile Layout

**Features:**
- Simplified hero (no full-width)
- Probability badge (top right)
- Belief currents (compact)
- Bottom navigation bar:
  - Feed (home icon)
  - Explore (compass)
  - Ask (question mark)
  - Profile (user icon)
- Stats at bottom (156,432 votes, $4.8M volume, Place Position CTA)

## Implementation Priority

**Current focus:** Homepage core layout ✅

**Next priorities:**
1. The Stream section (homepage)
2. Sidebar sections (homepage)
3. Detail page enhancements
4. Mobile responsive improvements
5. Position placement UI (wallet integration)
6. Discussion/comments system

## Technical Notes

- Multi-option markets show all options on detail page
- Position placement needs Rain SDK integration
- Discussion requires user auth + comment storage
- Mobile nav bar needs implementation

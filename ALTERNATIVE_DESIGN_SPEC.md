# Alternative Overlay Design Specification

**Client:** Roy  
**Requested by:** Yaniv  
**Date:** Feb 12, 2026  
**Urgency:** HIGH

---

## Design Philosophy

**Core Concept:** Full-bleed images with text overlays and aggressive bottom gradients for maximum readability and visual impact.

**Key Differences from Current v97:**
- v97: Images with gradient overlays (70% bottom, 30% mid) + separate text section
- **ALT:** Full-height images with ALL content overlaid, MUCH darker gradient at bottom

---

## Visual Hierarchy & Gradient Strategy

### Gradient Specifications

**Featured Card (Large Left):**
- Height: 100% of card
- Gradient overlay:
  ```
  Bottom 0%:   rgba(0, 0, 0, 0.95) - Nearly opaque black
  Bottom 20%:  rgba(0, 0, 0, 0.85) - Strong black
  Bottom 40%:  rgba(0, 0, 0, 0.40) - Medium fade
  Top 100%:    rgba(0, 0, 0, 0.00) - Transparent
  ```

**Grid Cards (2×2 and 4-column):**
- Height: 100% of card
- Gradient overlay:
  ```
  Bottom 0%:   rgba(0, 0, 0, 0.92) - Very dark
  Bottom 25%:  rgba(0, 0, 0, 0.75) - Dark
  Bottom 50%:  rgba(0, 0, 0, 0.30) - Light fade
  Top 100%:    rgba(0, 0, 0, 0.00) - Transparent
  ```

### Text Content Zones

**Featured Card:**
- Text occupies bottom 30% of card
- Title: 24-28px, bold, white
- Description: 14-16px, rgba(255,255,255,0.9)
- Belief current graph: Small, compact
- Stats: Bottom-aligned, 12px

**Grid Cards:**
- Text occupies bottom 25-30% of card
- Title: 16-18px, bold, white
- Description: 13-14px (truncated to 2 lines max)
- Stats: Bottom-aligned, 11px

---

## Component Breakdown

### 1. Featured Market Card (Left, Large)

**HTML Structure:**
```html
<div class="market-card featured-card overlay-design">
  <!-- Full-bleed background image -->
  <div class="card-image-bg" style="background-image: url(...)"></div>
  
  <!-- Dark gradient overlay -->
  <div class="card-gradient-overlay"></div>
  
  <!-- Content overlay (bottom 30%) -->
  <div class="card-content-overlay">
    <!-- Badges/Tags (top-left) -->
    <div class="card-badges">
      <span class="badge-category">Politics</span>
      <span class="badge-hypothetical">Hypothetical</span>
    </div>
    
    <!-- Main content (bottom) -->
    <div class="card-text-content">
      <h2 class="card-title">Will Trump's approval rating exceed 50% by March 2026?</h2>
      <p class="card-description">Trump's second term started with strong base support but independents remain skeptical...</p>
      
      <!-- Belief Current Mini Graph -->
      <div class="belief-current-mini">
        <svg class="mini-sparkline"><!-- simplified line chart --></svg>
        <span class="current-probability">52%</span>
      </div>
      
      <!-- Stats row -->
      <div class="card-stats">
        <span class="stat-item">
          <svg class="icon">💰</svg>
          $185K volume
        </span>
        <span class="stat-item">
          <svg class="icon">📊</svg>
          2.4K participants
        </span>
        <span class="stat-item">
          <svg class="icon">📅</svg>
          Closes Mar 2026
        </span>
      </div>
    </div>
  </div>
</div>
```

**CSS:**
```css
/* Featured Card */
.featured-card.overlay-design {
  position: relative;
  height: 600px; /* Adjustable */
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.featured-card.overlay-design:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

/* Full-bleed background image */
.card-image-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  z-index: 1;
}

/* Dark gradient overlay - AGGRESSIVE for readability */
.featured-card .card-gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.95) 0%,
    rgba(0, 0, 0, 0.85) 20%,
    rgba(0, 0, 0, 0.40) 40%,
    rgba(0, 0, 0, 0.00) 100%
  );
  z-index: 2;
}

/* Content overlay */
.card-content-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 24px;
  z-index: 3;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Badges (top-left) */
.card-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge-category {
  background: rgba(59, 130, 246, 0.9); /* Blue */
  color: white;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-hypothetical {
  background: rgba(168, 85, 247, 0.9); /* Purple */
  color: white;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

/* Text content (bottom 30%) */
.card-text-content {
  color: white;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.featured-card .card-title {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.3;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.featured-card .card-description {
  font-size: 16px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5);
}

/* Belief Current Mini */
.belief-current-mini {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.mini-sparkline {
  width: 80px;
  height: 24px;
  opacity: 0.8;
}

.current-probability {
  font-size: 20px;
  font-weight: 700;
  color: #10b981; /* Green for positive trend */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Stats row */
.card-stats {
  display: flex;
  gap: 20px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
}

.stat-item .icon {
  width: 16px;
  height: 16px;
  opacity: 0.8;
}
```

---

### 2. Grid Cards (2×2 Right Section)

**HTML Structure:**
```html
<div class="market-card grid-card overlay-design">
  <div class="card-image-bg" style="background-image: url(...)"></div>
  <div class="card-gradient-overlay"></div>
  
  <div class="card-content-overlay">
    <div class="card-badges">
      <span class="badge-category">Sports</span>
    </div>
    
    <div class="card-text-content">
      <h3 class="card-title">Will Real Madrid win Champions League 2026?</h3>
      <p class="card-description">Resolves YES if Real Madrid wins the 2025-26 UEFA Champions League final...</p>
      
      <div class="card-stats-compact">
        <span class="probability-badge">42%</span>
        <span class="volume-text">$185K</span>
      </div>
    </div>
  </div>
</div>
```

**CSS:**
```css
/* Grid Cards */
.grid-card.overlay-design {
  position: relative;
  height: 280px; /* Smaller than featured */
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.grid-card.overlay-design:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

/* Grid card gradient - slightly less aggressive but still strong */
.grid-card .card-gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.92) 0%,
    rgba(0, 0, 0, 0.75) 25%,
    rgba(0, 0, 0, 0.30) 50%,
    rgba(0, 0, 0, 0.00) 100%
  );
  z-index: 2;
}

/* Content overlay for grid cards */
.grid-card .card-content-overlay {
  padding: 16px;
}

.grid-card .card-title {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.3;
  color: #ffffff;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
}

.grid-card .card-description {
  font-size: 14px;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.85);
  margin: 8px 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

/* Compact stats for grid cards */
.card-stats-compact {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
}

.probability-badge {
  background: rgba(16, 185, 129, 0.9); /* Green */
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 700;
}

.volume-text {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}
```

---

### 3. 4-Column Grid Cards (Bottom Section)

**Same structure as 2×2 grid, but potentially smaller:**

```css
/* 4-column grid cards - more compact */
.grid-card-4col.overlay-design {
  height: 240px; /* Slightly smaller */
}

.grid-card-4col .card-title {
  font-size: 16px;
  -webkit-line-clamp: 2;
}

.grid-card-4col .card-description {
  font-size: 13px;
  -webkit-line-clamp: 1; /* Only 1 line for smaller cards */
}

.grid-card-4col .card-content-overlay {
  padding: 14px;
}
```

---

## Mobile Responsiveness

### Breakpoints

**Desktop (1280px+):**
- Featured: 600px height
- Grid 2×2: 280px height
- Grid 4-col: 240px height

**Tablet (768px - 1279px):**
- Featured: 500px height
- Grid changes to 2-column
- Grid cards: 260px height

**Mobile (<768px):**
- All cards stack vertically
- Featured: 400px height
- Grid cards: 220px height
- Text sizes reduced by ~10%
- Padding reduced

```css
@media (max-width: 1279px) {
  .featured-card.overlay-design {
    height: 500px;
  }
  
  .featured-card .card-title {
    font-size: 24px;
  }
  
  .grid-card.overlay-design {
    height: 260px;
  }
}

@media (max-width: 767px) {
  .featured-card.overlay-design {
    height: 400px;
  }
  
  .featured-card .card-title {
    font-size: 22px;
  }
  
  .featured-card .card-description {
    font-size: 14px;
    -webkit-line-clamp: 2;
  }
  
  .featured-card .card-content-overlay {
    padding: 16px;
  }
  
  .grid-card.overlay-design {
    height: 220px;
  }
  
  .grid-card .card-title {
    font-size: 16px;
  }
  
  .grid-card .card-description {
    font-size: 13px;
  }
  
  .card-stats {
    gap: 12px;
  }
}
```

---

## Design Refinements & Best Practices

### 1. Image Selection Criteria
- **Choose images with interesting upper portions** - since text will cover bottom
- **Avoid busy bottom sections** - keep text readable even through gradient
- **Prefer images with sky/clear space at top** - creates better visual hierarchy

### 2. Text Readability Enhancements
- **Text shadows:** All text should have subtle shadows (0 2px 6px rgba(0,0,0,0.5))
- **Gradient opacity:** Bottom gradient at 92-95% black ensures text contrast ratio >4.5:1
- **Line clamping:** Prevent text overflow with -webkit-line-clamp
- **Font weight:** Use 700 (bold) for titles, 500-600 for body

### 3. Interactive States

**Hover:**
```css
.market-card.overlay-design:hover .card-image-bg {
  transform: scale(1.05);
  transition: transform 0.5s ease;
}

.market-card.overlay-design:hover .card-gradient-overlay {
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.97) 0%,  /* Slightly darker on hover */
    rgba(0, 0, 0, 0.87) 20%,
    rgba(0, 0, 0, 0.45) 40%,
    rgba(0, 0, 0, 0.00) 100%
  );
}
```

**Focus (Accessibility):**
```css
.market-card.overlay-design:focus {
  outline: 3px solid #3b82f6;
  outline-offset: 2px;
}
```

### 4. Loading States

```css
.card-image-bg.loading {
  background: linear-gradient(
    90deg,
    #1f2937 0%,
    #374151 50%,
    #1f2937 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

### 5. Accessibility Considerations

- **Alt text:** Ensure all images have meaningful alt text
- **ARIA labels:** Add aria-label to cards describing market question
- **Keyboard navigation:** Ensure tab order is logical
- **Contrast ratios:** Bottom gradient ensures WCAG AA compliance (4.5:1 minimum)

```html
<div class="market-card overlay-design" 
     role="article" 
     aria-label="Market: Will Trump's approval rating exceed 50%?"
     tabindex="0">
  ...
</div>
```

---

## Implementation Checklist

### Phase 1: HTML Structure
- [ ] Update card HTML to include overlay structure
- [ ] Add gradient overlay divs
- [ ] Restructure content to overlay pattern
- [ ] Add proper ARIA labels

### Phase 2: CSS Implementation
- [ ] Implement gradient overlay styles
- [ ] Add text shadow for readability
- [ ] Set up responsive breakpoints
- [ ] Add hover/focus states
- [ ] Test loading states

### Phase 3: Testing
- [ ] Test on multiple screen sizes (320px, 768px, 1024px, 1440px, 1920px)
- [ ] Verify text readability on various image backgrounds
- [ ] Test with light and dark images
- [ ] Verify keyboard navigation
- [ ] Check contrast ratios with accessibility tools

### Phase 4: Comparison
- [ ] Deploy current design to `/`
- [ ] Deploy alternative design to `/alt`
- [ ] Set up A/B testing framework
- [ ] Collect Roy's feedback

---

## Gradient Opacity Reference

**For copy-paste ease:**

```css
/* Featured Card Gradient */
background: linear-gradient(
  to top,
  rgba(0, 0, 0, 0.95) 0%,
  rgba(0, 0, 0, 0.85) 20%,
  rgba(0, 0, 0, 0.40) 40%,
  rgba(0, 0, 0, 0.00) 100%
);

/* Grid Card Gradient */
background: linear-gradient(
  to top,
  rgba(0, 0, 0, 0.92) 0%,
  rgba(0, 0, 0, 0.75) 25%,
  rgba(0, 0, 0, 0.30) 50%,
  rgba(0, 0, 0, 0.00) 100%
);
```

---

## Expected Visual Impact

### What Roy Should See:

1. **Dramatic full-bleed images** - Market topics come alive visually
2. **Confident text overlays** - Dark gradients ensure perfect readability
3. **Clean information hierarchy** - Badges → Title → Description → Stats
4. **Smooth interactions** - Subtle hover effects with image zoom
5. **Professional polish** - Shadows, spacing, typography all dialed in

### Comparison to v97:

| Aspect | v97 (Current) | Alternative (New) |
|--------|---------------|-------------------|
| Image usage | 70-80% of card | 100% of card |
| Text placement | Separate section | Overlaid on image |
| Gradient strength | 70% bottom, 30% mid | 95% bottom → transparent |
| Visual impact | Moderate | High |
| Information density | Higher | Slightly lower |
| Readability | Good | Excellent (with dark gradient) |

---

## Next Steps for Implementation

1. **Create `/alt` route** in Next.js/React app
2. **Copy existing page structure** to new route
3. **Apply overlay CSS classes** to all cards
4. **Test with real market data** and images
5. **Deploy to staging** for Roy's review
6. **Iterate based on feedback**

---

**Designer Notes:**
- This design maximizes visual impact while maintaining excellent readability
- The aggressive gradients (92-95% black) are intentional for text contrast
- Mobile-first approach ensures quality experience on all devices
- Easy to A/B test against current version

**Estimated Implementation Time:** 2-3 hours for complete implementation and testing

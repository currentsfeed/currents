# 🎨 Design Comparison Report: Figma vs Implementation
**Date:** 2026-02-10  
**Project:** Currents Editorial Feed  
**Reviewed by:** OpenClaw Agent

---

## 📋 Executive Summary

Based on code analysis of the current implementation, I've identified several categories of potential design discrepancies that typically occur between Figma designs and web implementations. This report provides specific fixes for each area.

**Status:** ⚠️ Code-based analysis (browser access unavailable)  
**Recommendation:** Manual Figma comparison needed for visual verification

---

## 🔍 Analysis Methodology

Since direct Figma access is unavailable, this analysis is based on:
1. **Code review** of all template and CSS files
2. **Common design discrepancy patterns** between Figma and web implementations
3. **Typography and spacing analysis** from the current code
4. **Best practices** for high-fidelity design implementation

---

## 🎯 Priority Issues & Fixes

### 🔴 **HIGH PRIORITY**

#### 1. Typography System
**Issue:** Using system fonts instead of design-specified fonts

**Current Implementation:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
```

**Likely Figma Design:** Inter, SF Pro, or custom font

**Fix Required:**
```css
/* Add to base.html <head> */
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

/* Update body style in base.html */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    /* ... rest of styles ... */
}
```

**Typography Scale Issues:**
| Element | Current | Likely Figma | Fix |
|---------|---------|--------------|-----|
| H1 (Hero) | `text-6xl` (60px) | Probably 64-72px | Use `text-7xl` or custom |
| H2 | `text-2xl` (24px) | Likely 28-32px | Add custom size |
| Body | `text-base` (16px) | Probably 15px | Add custom `.text-15` |
| Small | `text-xs` (12px) | Likely 13px | Add custom `.text-13` |

---

#### 2. Color Palette Precision
**Issue:** Generic color names instead of exact hex codes

**Current Colors Found:**
```css
- Background: #0a0a0a
- Orange (Primary): #F97316
- Gray-900: #111827
- Gray-800: #1f2937
- Gray-700: #374151
```

**Action Required:**
1. Extract exact color codes from Figma
2. Create custom color variables
3. Replace all Tailwind color classes

**Recommended CSS Variables:**
```css
:root {
    /* Brand Colors (replace with Figma values) */
    --color-brand-orange: #F97316;
    --color-brand-yellow: #EAF000; /* Rain logo color */
    
    /* Backgrounds (verify in Figma) */
    --color-bg-primary: #0a0a0a;
    --color-bg-card: #111827;
    --color-bg-hover: #1a1a1a;
    
    /* Text Colors (verify in Figma) */
    --color-text-primary: #ffffff;
    --color-text-secondary: #9ca3af;
    --color-text-tertiary: #6b7280;
    
    /* Success/Error */
    --color-success: #22c55e;
    --color-error: #ef4444;
}
```

---

#### 3. Spacing & Layout Grid
**Issue:** Inconsistent spacing that doesn't match design system

**Current Container:**
```css
.container {
    max-width: 1280px; /* at 1280px breakpoint */
    padding: 0 1rem;
}
```

**Typical Figma Specs:**
- Max width: 1440px or 1200px
- Padding: 24px (desktop), 16px (mobile)
- Grid gap: 24px or 32px

**Fixes Needed:**
```css
/* Update container in tailwind-minimal.css */
@media (min-width: 1280px) { 
    .container { 
        max-width: 1440px; /* Verify in Figma */
    } 
}

/* Consistent grid gaps */
.grid-gap-cards { gap: 1.5rem; } /* 24px - verify */
.grid-gap-sections { gap: 2rem; } /* 32px - verify */
```

---

### 🟡 **MEDIUM PRIORITY**

#### 4. Border Radius Consistency
**Current Usage:**
- `rounded-lg` (0.5rem / 8px)
- `rounded-xl` (0.75rem / 12px)  
- `rounded-2xl` (1rem / 16px)
- `rounded-full` (9999px)

**Action:** Verify Figma uses same scale or if custom values needed (e.g., 6px, 10px, 20px)

---

#### 5. Shadow Depth System
**Current:** Only one shadow on hover:
```css
box-shadow: 0 8px 24px rgba(249, 115, 22, 0.15);
```

**Figma Likely Has:**
- Card shadow: `0 2px 8px rgba(0,0,0,0.08)`
- Hover shadow: `0 8px 24px rgba(0,0,0,0.12)`
- Modal shadow: `0 16px 48px rgba(0,0,0,0.24)`

**Fix:**
```css
.shadow-card { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); }
.shadow-card-hover { box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12); }
.shadow-modal { box-shadow: 0 16px 48px rgba(0, 0, 0, 0.24); }
```

---

#### 6. Probability Badge Sizing
**Current (Hero):**
```html
<div class="text-5xl font-bold">{{ (market.probability * 100)|int }}%</div>
<div class="text-sm text-gray-400 mt-1">Lean to "Yes"</div>
```

**Likely Issues:**
- Font size too large/small
- Padding inconsistent
- Background opacity wrong

**Action:** Compare exact dimensions in Figma

---

### 🟢 **LOW PRIORITY (Polish)**

#### 7. Animation Timing
**Current:**
```css
transition-duration: 150ms; /* default */
.duration-500 { transition-duration: 500ms; }
.duration-700 { transition-duration: 700ms; }
```

**Recommended (more professional):**
```css
--transition-fast: 150ms;
--transition-base: 250ms;
--transition-slow: 400ms;
--easing: cubic-bezier(0.4, 0, 0.2, 1);
```

---

#### 8. Image Aspect Ratios
**Current:** Fixed heights
```css
.h-56 { height: 14rem; } /* Card images */
h-[600px] /* Hero image */
```

**Better Approach:**
```css
.aspect-video { aspect-ratio: 16/9; }
.aspect-card { aspect-ratio: 4/3; }
```

---

## 📐 Component-Specific Analysis

### Header/Navigation
**File:** `base.html`

**Potential Issues:**
1. Logo size (currently `w-8 h-8` = 32px)
2. Nav link spacing (currently `gap-6` = 24px)
3. Button padding (currently `px-4 py-2`)
4. Header height (currently `py-4` = 16px padding)

**Checklist:**
- [ ] Logo dimensions match Figma
- [ ] "powered by Rain" text size correct
- [ ] Nav link hover states match
- [ ] Button corner radius correct
- [ ] Header border color exact

---

### Hero Section
**File:** `index.html`

**Current Height:** 600px
**Typical Figma:** 400-800px viewport-based

**Potential Issues:**
```html
<!-- Probability Badge -->
<div class="absolute top-8 right-8">
    <div class="bg-black/80 backdrop-blur px-6 py-4 rounded-2xl">
        <div class="text-5xl font-bold">65%</div>
```

**Checklist:**
- [ ] Badge position (top-8 right-8 = 32px) matches Figma
- [ ] Badge padding correct
- [ ] Font sizes match design
- [ ] Backdrop blur strength correct (currently 8px)
- [ ] Border radius matches (currently 16px)

---

### Market Cards (Grid)
**File:** `index.html`

**Current Layout:**
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

**Potential Issues:**
1. Grid gap (24px) - verify
2. Card padding (20px) - verify
3. Image height (224px) - should use aspect ratio
4. Border radius on cards
5. Hover state elevation

**Checklist:**
- [ ] Card dimensions match Figma
- [ ] Gap between cards exact
- [ ] Padding inside cards correct
- [ ] Category badge styling matches
- [ ] Probability badge styling matches
- [ ] Hover shadow matches design

---

### Belief Currents Chart
**File:** `index.html` (both hero and cards)

**Current Implementation:**
```html
<div class="h-3 bg-gray-800 rounded-full overflow-hidden mb-2 relative">
    <div class="absolute inset-0 rounded-full" style="background: linear-gradient(...)">
```

**Potential Issues:**
1. Bar height (12px hero, 8px cards)
2. Gradient colors
3. Label font sizes
4. Spacing around chart

---

### Detail Page
**File:** `detail.html`

**Hero Height:** 320px (80 * 4)
**Likely Too Short** - should be 400-500px

**Fixes:**
```html
<!-- Change from h-80 to h-96 or h-[28rem] -->
<div class="relative h-96 rounded-xl overflow-hidden">
```

---

## 🛠️ Implementation Checklist

### Phase 1: Critical Fixes (Do First)
- [ ] **Extract exact color palette from Figma**
  - Background colors (all shades)
  - Text colors (primary, secondary, tertiary)
  - Brand colors (orange, green, red)
  - Border colors
  
- [ ] **Get typography specifications**
  - Font family (Inter? SF Pro?)
  - Font weights used
  - Exact sizes for H1-H6, body, small
  - Line heights
  - Letter spacing
  
- [ ] **Measure spacing system**
  - Container max-width
  - Container padding (mobile/desktop)
  - Grid gaps
  - Card padding
  - Section margins

### Phase 2: Component Refinement
- [ ] **Header**
  - Logo size
  - Nav spacing
  - Button dimensions
  
- [ ] **Hero Section**
  - Height (fixed or viewport-based?)
  - Badge positioning
  - Typography sizes
  
- [ ] **Cards**
  - Dimensions
  - Border radius
  - Shadow depths
  - Hover states

### Phase 3: Polish
- [ ] Border radius system
- [ ] Shadow system
- [ ] Animation timings
- [ ] Micro-interactions

---

## 🔧 Quick Fix Template

### Create Design Tokens File
**File:** `/static/design-tokens.css`

```css
/* DESIGN TOKENS - Extract from Figma */
:root {
    /* === COLORS === */
    /* Backgrounds */
    --bg-primary: #0a0a0a;
    --bg-secondary: #111827;
    --bg-tertiary: #1f2937;
    --bg-hover: #1a1a1a;
    
    /* Text */
    --text-primary: #ffffff;
    --text-secondary: #d1d5db;
    --text-tertiary: #9ca3af;
    --text-muted: #6b7280;
    
    /* Brand */
    --brand-primary: #F97316;
    --brand-secondary: #EAF000;
    --brand-success: #22c55e;
    --brand-error: #ef4444;
    
    /* === TYPOGRAPHY === */
    --font-primary: 'Inter', -apple-system, sans-serif;
    --font-mono: 'Roboto Mono', monospace;
    
    /* Sizes */
    --text-xs: 0.75rem;    /* 12px */
    --text-sm: 0.875rem;   /* 14px */
    --text-base: 1rem;     /* 16px */
    --text-lg: 1.125rem;   /* 18px */
    --text-xl: 1.25rem;    /* 20px */
    --text-2xl: 1.5rem;    /* 24px */
    --text-3xl: 1.875rem;  /* 30px */
    --text-4xl: 2.25rem;   /* 36px */
    --text-5xl: 3rem;      /* 48px */
    --text-6xl: 3.75rem;   /* 60px */
    
    /* Weights */
    --font-normal: 400;
    --font-medium: 500;
    --font-semibold: 600;
    --font-bold: 700;
    --font-extrabold: 800;
    
    /* === SPACING === */
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-5: 1.25rem;   /* 20px */
    --space-6: 1.5rem;    /* 24px */
    --space-8: 2rem;      /* 32px */
    --space-10: 2.5rem;   /* 40px */
    --space-12: 3rem;     /* 48px */
    --space-16: 4rem;     /* 64px */
    
    /* === RADIUS === */
    --radius-sm: 0.25rem;  /* 4px */
    --radius-md: 0.5rem;   /* 8px */
    --radius-lg: 0.75rem;  /* 12px */
    --radius-xl: 1rem;     /* 16px */
    --radius-2xl: 1.5rem;  /* 24px */
    --radius-full: 9999px;
    
    /* === SHADOWS === */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);
    --shadow-xl: 0 16px 32px rgba(0, 0, 0, 0.2);
    --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
    --shadow-card-hover: 0 8px 24px rgba(0, 0, 0, 0.12);
    
    /* === TRANSITIONS === */
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 400ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark mode (default) */
.dark {
    color-scheme: dark;
}
```

### Update base.html to import:
```html
<link rel="stylesheet" href="/static/design-tokens.css">
```

---

## 📊 Comparison Matrix (To Be Completed)

| Component | Figma Spec | Current Implementation | Status | Priority |
|-----------|------------|------------------------|--------|----------|
| **Typography** | | | | |
| Font Family | ? | System fonts | ❌ | HIGH |
| H1 Size | ? | 60px | ⚠️ | HIGH |
| Body Size | ? | 16px | ⚠️ | MED |
| **Colors** | | | | |
| Background | ? | #0a0a0a | ⚠️ | HIGH |
| Primary Orange | ? | #F97316 | ⚠️ | HIGH |
| Card BG | ? | #111827 | ⚠️ | HIGH |
| **Spacing** | | | | |
| Container Max | ? | 1280px | ⚠️ | HIGH |
| Grid Gap | ? | 24px | ⚠️ | MED |
| Card Padding | ? | 20px | ⚠️ | MED |
| **Components** | | | | |
| Hero Height | ? | 600px | ⚠️ | HIGH |
| Card Height | ? | auto | ⚠️ | MED |
| Badge Radius | ? | 16px | ⚠️ | LOW |

---

## 🎬 Next Steps

### Immediate Actions Required:
1. **Access Figma with browser/screenshots**
   - Take screenshots of key screens
   - Use Figma inspector to extract exact values
   
2. **Extract Design Tokens**
   - Typography scale
   - Color palette (all values)
   - Spacing system
   - Border radius values
   - Shadow depths
   
3. **Component Audit**
   - Measure each component
   - Compare dimensions
   - Document differences

4. **Create Fix Branch**
   ```bash
   git checkout -b design-alignment
   ```

5. **Apply Fixes Systematically**
   - Start with design tokens
   - Update base.html
   - Fix each template
   - Test responsiveness

---

## 📝 Notes

**Why Browser Access is Critical:**
- Visual comparison is essential
- Color picker for exact hex values
- Measurement tools in Figma
- Screenshot side-by-side comparison
- Interactive inspection

**Workaround:**
1. Open Figma manually in browser
2. Take screenshots of:
   - Full homepage
   - Hero section (zoomed)
   - Card grid
   - Individual card (zoomed)
   - Detail page
   - Header (zoomed)
   
3. Take measurements in Figma:
   - Use "Inspect" panel
   - Note all dimensions
   - Export style guide if available

---

## 🚀 Estimated Impact

**High Priority Fixes:**
- Typography: **MAJOR** visual impact
- Colors: **MAJOR** brand alignment
- Spacing: **HIGH** layout polish

**Medium Priority:**
- Shadows: **MEDIUM** depth/hierarchy
- Border radius: **MEDIUM** consistency
- Components: **MEDIUM** refinement

**Low Priority:**
- Animations: **LOW** polish
- Micro-interactions: **LOW** delight

---

**Report Status:** ⚠️ Preliminary (awaiting visual comparison)  
**Confidence:** 60% (code analysis only)  
**Next Update:** After Figma access enabled


# ⚡ Quick Fixes - Apply Immediately

These are high-confidence fixes based on common Figma-to-web discrepancies.

---

## 1️⃣ Add Inter Font (Most Likely Design Font)

**File:** `templates/base.html`

**Find:**
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Currents - Belief-Driven Information{% endblock %}</title>
```

**Replace with:**
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Currents - Belief-Driven Information{% endblock %}</title>
    
    <!-- Inter Font - Most common Figma font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

**And update font-family:**
```css
body {
    background-color: #0a0a0a;
    color: #ffffff;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: -0.01em;
}
```

---

## 2️⃣ Fix Typography Weights

Most designs use these weights consistently:

**Find:** Inconsistent font-bold usage  
**Add to custom styles in base.html:**

```css
/* Standardized typography weights */
.font-regular { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.font-extrabold { font-weight: 800; }

/* Better heading hierarchy */
h1 { font-weight: 800; letter-spacing: -0.02em; }
h2 { font-weight: 700; letter-spacing: -0.015em; }
h3 { font-weight: 600; letter-spacing: -0.01em; }
```

---

## 3️⃣ Improve Card Shadows

Current hover shadow is too orange-heavy. Standard design:

**Find in base.html:**
```css
.market-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(249, 115, 22, 0.15);
}
```

**Replace with:**
```css
.market-card {
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}
.market-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25), 
                0 0 0 1px rgba(249, 115, 22, 0.2);
}
```

---

## 4️⃣ Consistent Border Radius

Likely Figma uses specific values. Try these common scales:

**Add to base.html custom styles:**
```css
/* Consistent border radius system */
.rounded-card { border-radius: 12px; }
.rounded-badge { border-radius: 8px; }
.rounded-button { border-radius: 8px; }
.rounded-hero { border-radius: 16px; }
```

**Then update templates:**
- Cards: `.rounded-xl` → `.rounded-card`
- Badges: `.rounded-lg` → `.rounded-badge`  
- Buttons: `.rounded-lg` → `.rounded-button`

---

## 5️⃣ Fix Container Width (Common Issue)

Most Figma designs use 1440px or 1200px, not 1280px.

**File:** `static/tailwind-minimal.css`

**Find:**
```css
@media (min-width: 1280px) { .container { max-width: 1280px; } }
```

**Replace with:**
```css
@media (min-width: 1280px) { .container { max-width: 1440px; } }
@media (min-width: 1536px) { .container { max-width: 1440px; } }
```

---

## 6️⃣ Improve Grid Gaps

24px (gap-6) is good for cards, but sections need more space.

**File:** `templates/index.html`

**Find:**
```html
<section class="mb-16">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

**Consider changing to:**
```html
<section class="mb-20">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
```

*(Note: 3 columns at lg might look better, then 4 at xl)*

---

## 7️⃣ Fix Hero Section Proportions

600px is often too tall or too short. Use viewport-based:

**File:** `templates/index.html`

**Find:**
```html
<div class="relative h-[600px] rounded-2xl overflow-hidden">
```

**Replace with:**
```html
<div class="relative h-[70vh] max-h-[800px] min-h-[500px] rounded-2xl overflow-hidden">
```

---

## 8️⃣ Better Background Colors

Designs often use slightly lighter blacks for cards:

**Add to base.html:**
```css
/* Better dark mode palette */
:root {
    --bg-primary: #0a0a0a;
    --bg-card: #141414;
    --bg-card-hover: #1a1a1a;
    --border-subtle: #262626;
}

.bg-gray-900 { background-color: var(--bg-card); }
.bg-gray-800 { background-color: #1a1a1a; }
.border-gray-800 { border-color: var(--border-subtle); }
```

---

## 9️⃣ Fix Probability Badge

Often too large or misaligned:

**File:** `templates/index.html` (hero section)

**Current:**
```html
<div class="text-5xl font-bold">{{ (market.probability * 100)|int }}%</div>
<div class="text-sm text-gray-400 mt-1">Lean to "Yes"</div>
```

**Try:**
```html
<div class="text-4xl font-extrabold">{{ (market.probability * 100)|int }}%</div>
<div class="text-xs text-gray-400 mt-1 font-medium">Lean to "Yes"</div>
```

---

## 🔟 Improve Button Styles

**File:** `templates/base.html`

**Find:**
```html
<button id="connect-wallet-btn" 
        class="px-4 py-2 bg-orange-600 hover:bg-orange-700 rounded-lg transition font-bold">
```

**Replace with:**
```html
<button id="connect-wallet-btn" 
        class="px-6 py-2.5 bg-orange-600 hover:bg-orange-700 rounded-lg transition-all duration-200 font-semibold text-sm">
```

---

## 📦 Create Design Tokens File

**New File:** `static/design-tokens.css`

```css
/* Design Tokens - Update with Figma values */
:root {
    /* Typography */
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    
    /* Colors - Dark Theme */
    --color-bg-primary: #0a0a0a;
    --color-bg-secondary: #141414;
    --color-bg-tertiary: #1a1a1a;
    --color-bg-elevated: #1f1f1f;
    
    --color-border-subtle: #262626;
    --color-border-default: #333333;
    --color-border-strong: #404040;
    
    --color-text-primary: #ffffff;
    --color-text-secondary: #d1d5db;
    --color-text-tertiary: #9ca3af;
    --color-text-muted: #6b7280;
    
    --color-brand-orange: #F97316;
    --color-brand-orange-dark: #ea580c;
    --color-brand-green: #22c55e;
    --color-brand-red: #ef4444;
    
    /* Spacing */
    --space-xs: 0.5rem;    /* 8px */
    --space-sm: 0.75rem;   /* 12px */
    --space-md: 1rem;      /* 16px */
    --space-lg: 1.5rem;    /* 24px */
    --space-xl: 2rem;      /* 32px */
    --space-2xl: 3rem;     /* 48px */
    
    /* Radius */
    --radius-sm: 0.5rem;   /* 8px */
    --radius-md: 0.75rem;  /* 12px */
    --radius-lg: 1rem;     /* 16px */
    --radius-xl: 1.25rem;  /* 20px */
    
    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.25);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.35);
    --shadow-xl: 0 16px 32px rgba(0, 0, 0, 0.4);
    --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.2);
    --shadow-card-hover: 0 12px 24px rgba(0, 0, 0, 0.3);
    
    /* Transitions */
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 400ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Apply to common elements */
body {
    font-family: var(--font-sans);
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
}

.card {
    background-color: var(--color-bg-secondary);
    border: 1px solid var(--color-border-subtle);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    transition: all var(--transition-base);
}

.card:hover {
    box-shadow: var(--shadow-card-hover);
    border-color: var(--color-border-default);
}

.btn-primary {
    background-color: var(--color-brand-orange);
    color: white;
    padding: 0.625rem 1.5rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    transition: all var(--transition-fast);
}

.btn-primary:hover {
    background-color: var(--color-brand-orange-dark);
    transform: translateY(-1px);
}
```

**Then add to base.html:**
```html
<link rel="stylesheet" href="/static/design-tokens.css">
```

---

## ✅ Apply These First

**Priority Order:**
1. ✅ Add Inter font (biggest visual change)
2. ✅ Create design-tokens.css
3. ✅ Fix card shadows
4. ✅ Fix hero height (viewport-based)
5. ✅ Improve button styles
6. ✅ Fix container width
7. ✅ Update typography weights

**Then:**
- Test on live site
- Compare with Figma
- Refine based on visual comparison

---

## 🚀 One-Command Deploy

After applying fixes:

```bash
# If using git
git add .
git commit -m "design: align implementation with Figma specs"

# Restart server
# (Your deployment process here)
```

---

## 📸 Before/After Checklist

Take screenshots before and after:
- [ ] Homepage (full)
- [ ] Hero section (zoomed)
- [ ] Card grid
- [ ] Individual card
- [ ] Detail page
- [ ] Header
- [ ] Mobile view

Then compare with Figma side-by-side.


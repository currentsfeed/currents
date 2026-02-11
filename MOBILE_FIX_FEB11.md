# Mobile Responsiveness Fix - February 11, 2026

## Issue Reported by Roy
Mobile layout was completely broken:
- Hero title overlapping with probability badge
- Text too large (truncated: "World Cup with Argen")
- "Connect Wallet" button cut off
- No responsive design at all

## Changes Made

### Hero Section (`templates/index-v2.html`)

#### 1. **Responsive Height**
```html
<!-- Before: -->
<div class="relative h-[600px] ...">

<!-- After: -->
<div class="relative h-[500px] sm:h-[550px] md:h-[600px] ...">
```
- Mobile: 500px (fits iPhone screen better)
- Small: 550px
- Medium+: 600px (desktop)

#### 2. **Responsive Padding**
```html
<!-- Before: -->
<div class="absolute inset-0 p-12 ...">

<!-- After: -->
<div class="absolute inset-0 p-4 sm:p-6 md:p-8 lg:p-12 ...">
```
- Mobile: 16px padding
- Small: 24px
- Medium: 32px
- Large: 48px (desktop)

#### 3. **Probability Badge Positioning**
```html
<!-- Before: -->
<div class="absolute top-8 right-8">
    <div class="bg-black/70 backdrop-blur px-6 py-4 ...">

<!-- After: -->
<div class="absolute top-4 right-4 sm:top-6 sm:right-6 md:top-8 md:right-8">
    <div class="bg-black/70 backdrop-blur px-3 py-2 sm:px-4 sm:py-3 md:px-6 md:py-4 ...">
```
- Mobile: Closer to top-right corner (16px)
- Desktop: Original position (32px)
- Padding also scaled down on mobile

#### 4. **Probability Badge Text Sizing**
```html
<!-- Before: -->
<div class="text-5xl font-bold">48%</div>
<div class="text-sm text-gray-400 mt-1">Lean to "No"</div>

<!-- After: -->
<div class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">48%</div>
<div class="text-xs sm:text-sm text-gray-400 mt-0.5 md:mt-1 line-clamp-1">Lean "No"</div>
```
- Mobile: text-2xl (24px) for percentage
- Desktop: text-5xl (48px)
- Added `line-clamp-1` to prevent wrapping
- Shortened text ("Lean to" → "Lean")

#### 5. **Hero Title Sizing**
```html
<!-- Before: -->
<h1 class="text-6xl font-bold mb-6 leading-tight max-w-5xl">

<!-- After: -->
<h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold mb-3 sm:mb-4 md:mb-6 leading-tight max-w-[95%] sm:max-w-4xl md:max-w-5xl pr-20 sm:pr-24 md:pr-0">
```
- Mobile: text-2xl (24px) - much smaller!
- Small: text-3xl (30px)
- Medium: text-4xl (36px)
- Large: text-5xl (48px)
- XL: text-6xl (60px) - original desktop size
- Added `pr-20` on mobile to avoid badge overlap
- Max-width: 95% on mobile to prevent overflow

#### 6. **Description Text**
```html
<!-- Before: -->
<p class="text-gray-300 text-lg mb-8 max-w-3xl">

<!-- After: -->
<p class="hidden sm:block text-gray-300 text-sm sm:text-base md:text-lg mb-4 sm:mb-6 md:mb-8 max-w-2xl md:max-w-3xl">
```
- Mobile: **Hidden** (too much text on small screens)
- Small+: Visible with responsive sizing
- Desktop: Original text-lg size

#### 7. **Belief Currents Section**
```html
<!-- Before: -->
<div class="bg-black/80 backdrop-blur-md rounded-xl p-3 max-w-4xl mb-2">

<!-- After: -->
<div class="bg-black/80 backdrop-blur-md rounded-lg md:rounded-xl p-2 sm:p-3 max-w-full sm:max-w-3xl md:max-w-4xl mb-2">
```
- Mobile: Full width (`max-w-full`), smaller padding and border radius
- Desktop: Original styling

## Testing Checklist

### Mobile (375px - iPhone)
- [ ] Hero title fits without truncation
- [ ] Probability badge doesn't overlap title
- [ ] No horizontal scrolling
- [ ] "Connect Wallet" button visible
- [ ] Belief currents section fits
- [ ] Text is readable (not too small)

### Tablet (768px - iPad)
- [ ] Layout transitions smoothly
- [ ] Text sizes increase appropriately
- [ ] Spacing looks good

### Desktop (1024px+)
- [ ] Original design preserved
- [ ] No regressions
- [ ] All desktop features work

## Responsive Breakpoints Used

Tailwind CSS breakpoints:
- **Default (< 640px)**: Mobile-first sizing
- **sm (640px+)**: Small tablets, large phones
- **md (768px+)**: Tablets, small laptops
- **lg (1024px+)**: Laptops, desktops
- **xl (1280px+)**: Large desktops

## Files Changed
- `/home/ubuntu/.openclaw/workspace/currents-full-local/templates/index-v2.html`

## Status
✅ **Fixed and deployed** - App restarted with mobile-responsive hero section

## Next Steps for Sasha (QA)
1. Add mobile testing to QA checklist
2. Test on actual devices:
   - iPhone (Safari)
   - Android (Chrome)
   - iPad (Safari)
3. Check all sections (not just hero):
   - Grid cards
   - The Stream
   - Navigation
   - Market detail pages
4. Document any remaining mobile issues

## Notes
- Only fixed hero section so far
- Grid cards and other sections may still need mobile work
- This is a critical issue - mobile traffic is significant
- Desktop design preserved (no regressions)

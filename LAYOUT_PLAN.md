# Homepage Layout Implementation Plan

## Goal
Implement Roy's Figma design with featured market + grid layout

## Current Structure
```
Hero (1 market) - feed['hero'][0]
↓
Grid (8 markets) - feed['grid'][0-7] in 4-column layout
```

## New Structure
```
Hero (1 market) - feed['hero'][0] - UNCHANGED
↓
Featured Market (1 large card) - feed['grid'][0] - NEW
↓
Grid (7 markets) - feed['grid'][1:] in 4-column layout - MODIFIED
```

## Implementation Steps

### 1. Featured Section Design
- Position: Between hero and grid
- Size: Larger than grid cards (options):
  - Option A: Full width, ~400px height (similar to hero but shorter)
  - Option B: 2-column span within grid (takes up 2 of 4 columns)
  - **Recommended: Option A** (clearer visual hierarchy)

### 2. Card Structure Changes
All three card types need descriptions:

**Hero Card:**
- Add description above title
- Style: text-gray-400, text-sm, mb-2

**Featured Card:**
- Layout: Horizontal (image left, content right) OR similar to hero but shorter
- Description above title
- Slightly smaller than hero but larger than grid cards

**Grid Cards:**
- Keep current structure
- Add description above title (text-xs, text-gray-400, mb-2, line-clamp-2)

### 3. Database Field
- Markets need `description` field
- Rox is adding this to brain.db
- Format: 1-2 sentence editorial context

### 4. Template Changes Required

#### index-v2.html modifications:

```html
<!-- After Hero Section, Before Category Filters -->

<!-- Featured Market Section -->
{% if grid and grid|length > 0 %}
<section class="mb-8">
    {% set featured = grid[0] %}
    <a href="/market/{{ featured.market_id }}" class="block group">
        <div class="relative h-96 rounded-2xl overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 border-2 border-orange-500/30 hover:border-orange-500/60 transition-all">
            <!-- Featured card content -->
            <!-- Similar structure to hero but smaller -->
            <!-- Include description above title -->
        </div>
    </a>
</section>
{% endif %}

<!-- Category Filters -->
<!-- (unchanged) -->

<!-- Grid Section - MODIFIED -->
<section class="mb-16">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {% for market in grid[1:] %}  <!-- Changed from grid to grid[1:] -->
        <!-- Add description rendering -->
        <!-- Rest unchanged -->
        {% endfor %}
    </div>
</section>
```

### 5. Typography for Descriptions

**Hero:**
```html
<p class="text-gray-400 text-sm mb-4 max-w-3xl">
    {{ market.description }}
</p>
<h1 class="text-6xl font-bold mb-6">{{ market.title }}</h1>
```

**Featured:**
```html
<p class="text-gray-400 text-xs mb-3 max-w-2xl line-clamp-2">
    {{ market.description }}
</p>
<h2 class="text-4xl font-bold mb-4">{{ market.title }}</h2>
```

**Grid:**
```html
<p class="text-gray-500 text-xs mb-2 line-clamp-2">
    {{ market.description }}
</p>
<h3 class="font-bold text-base mb-3 line-clamp-2">{{ market.title }}</h3>
```

## Testing Checklist
- [ ] Hero displays correctly with description
- [ ] Featured card displays grid[0] as large card with description
- [ ] Grid displays grid[1:] (7 cards) with descriptions
- [ ] Responsive layout works on mobile/tablet/desktop
- [ ] Typography matches Figma spacing
- [ ] Hover effects work
- [ ] Links work correctly

## Coordination with Rox
- **BLOCKER:** Wait for confirmation that market descriptions are added to database
- Need to know exact field name: `description` or `market_description`?
- Need sample data for testing

## Next Steps
1. ✅ Review current template
2. ✅ Create implementation plan
3. ⏸️ **WAIT for Rox:** Confirm descriptions ready
4. ⏸️ Implement featured section
5. ⏸️ Add description rendering to all cards
6. ⏸️ Test layout
7. ⏸️ Verify with Roy's Figma design

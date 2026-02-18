# Typewriter Fix v3 - Synchronous Blocking Script

**Date**: Feb 15, 2026 07:29 UTC  
**Approach**: Synchronous script in head that modifies style BEFORE body renders

---

## Current Implementation

### Structure
```html
<html>
<script>
  // Early HTML class addition (from v2)
  if (window.location.search.includes('typewriter=1')) {
    document.documentElement.classList.add('typewriter-mode');
  }
</script>
<head>
  <style id="tw-hide">
    /* Empty - will be populated by next script */
  </style>
  <script>
    // SYNCHRONOUS script - blocks rendering
    (function() {
      var isTypewriter = window.location.search.indexOf('typewriter=1') !== -1;
      if (isTypewriter) {
        var style = document.getElementById('tw-hide');
        style.textContent = '.snap-card h2 { display: none !important; }';
      }
    })();
  </script>
  ...rest of head...
</head>
<body>
  ...cards render here with style already applied...
</body>
```

### Why This Should Work

1. **Empty style tag created** - No CSSOM overhead
2. **Synchronous script runs** - Blocks HTML parsing
3. **Style populated** - Before body is parsed
4. **Browser continues** - With hiding CSS in place
5. **Body renders** - Text already hidden

---

## If This Still Doesn't Work

### Next Step: Server-Side Detection

Modify the Flask route to detect `?typewriter=1` and pass a flag to the template:

```python
@app.route('/feed')
def feed_mobile():
    typewriter_mode = request.args.get('typewriter') == '1'
    return render_template('feed_mobile.html', 
                         markets=markets,
                         typewriter_mode=typewriter_mode)
```

Then in template:
```html
{% if typewriter_mode %}
<style>
  .snap-card h2 { display: none !important; }
</style>
{% endif %}
```

This is **guaranteed** to work because the style is in the HTML before it reaches the browser.

---

## Nuclear Option: Inline Styles

If even server-side doesn't work (impossible but...), add inline styles:

```html
{% for market in markets %}
<div class="snap-card">
  <h2 {% if typewriter_mode %}style="display:none"{% endif %}>
    {{ market.title }}
  </h2>
</div>
{% endfor %}
```

This is the absolute last resort and will definitely work.

---

## Debugging

**Check if script is running:**
```javascript
// Add console.log in the synchronous script
console.log('[Typewriter] Script executed, isTypewriter:', isTypewriter);
```

**Check if style is populated:**
```javascript
// After script runs
console.log('[Typewriter] Style content:', document.getElementById('tw-hide').textContent);
```

**Check timing:**
```javascript
// At start of script
console.log('[Typewriter] DOMContentLoaded:', document.readyState);
```

---

## Current Status

✅ Synchronous blocking script in `<head>`  
✅ Style tag populated before body  
✅ `display: none !important` (strongest hiding)  
⏳ **Testing...**

If this doesn't work: **Moving to server-side solution**

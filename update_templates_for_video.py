#!/usr/bin/env python3
"""
Update all templates to support video/GIF rendering
Replaces <img> tags with conditional video/image rendering
"""

import os
import re

TEMPLATES_DIR = "templates"

# Pattern to find image tags
IMAGE_PATTERN = r'<img\s+src="{{(.*?)}}"(.*?)>'

# Replacement template
VIDEO_TEMPLATE = '''{% if {url_var}|is_video %}
                    <video autoplay muted loop playsinline class="{classes}">
                        <source src="{{ {url_var} }}" type="video/mp4">
                    </video>
                {% else %}
                    <img src="{{ {url_var} }}" {attrs}>
                {% endif %}'''

def update_template(filepath):
    """Update a single template file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Find all img tags with market.image_url
    def replace_img(match):
        url_var = match.group(1).strip()
        attrs = match.group(2).strip()
        
        # Extract class attribute
        class_match = re.search(r'class="([^"]*)"', attrs)
        classes = class_match.group(1) if class_match else ""
        
        # Only replace if it's a market image
        if 'image_url' in url_var:
            return VIDEO_TEMPLATE.format(
                url_var=url_var,
                classes=classes,
                attrs=attrs
            )
        return match.group(0)
    
    content = re.sub(IMAGE_PATTERN, replace_img, content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all template files"""
    updated = []
    
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith('.html'):
            filepath = os.path.join(TEMPLATES_DIR, filename)
            if update_template(filepath):
                updated.append(filename)
                print(f"✅ Updated: {filename}")
            else:
                print(f"⏭️  Skipped: {filename} (no changes needed)")
    
    print(f"\n📊 Summary: {len(updated)} files updated")
    if updated:
        print("Updated files:", ", ".join(updated))

if __name__ == '__main__':
    main()

#!/bin/bash
# Apply design fixes to Currents implementation
# Run this script from the project root

set -e

echo "🎨 Applying design fixes..."

# 1. Backup originals
echo "📦 Creating backups..."
mkdir -p .backups
cp templates/base.html .backups/base.html.backup
cp static/tailwind-minimal.css .backups/tailwind-minimal.css.backup

# 2. The design-tokens.css file has already been created
echo "✅ Design tokens file created: static/design-tokens.css"

# 3. Update base.html to include Inter font and design tokens
echo "🔤 Adding Inter font to base.html..."

# Check if Inter font already added
if ! grep -q "fonts.googleapis.com" templates/base.html; then
    # Add after the title tag
    sed -i '/<title>/a\    \n    <!-- Inter Font -->\n    <link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">' templates/base.html
    echo "✅ Inter font added"
else
    echo "ℹ️  Inter font already present"
fi

# Check if design-tokens.css already added
if ! grep -q "design-tokens.css" templates/base.html; then
    # Add after tailwind-minimal.css
    sed -i '/tailwind-minimal.css/a\    \n    <!-- Design Tokens -->\n    <link rel="stylesheet" href="/static/design-tokens.css">' templates/base.html
    echo "✅ Design tokens stylesheet linked"
else
    echo "ℹ️  Design tokens already linked"
fi

# 4. Update font family in base.html
echo "🎨 Updating font family..."
sed -i "s/font-family: -apple-system/font-family: 'Inter', -apple-system/" templates/base.html
echo "✅ Font family updated"

# 5. Update container max-width in tailwind-minimal.css
echo "📏 Updating container max-width to 1440px..."
sed -i 's/max-width: 1280px/max-width: 1440px/' static/tailwind-minimal.css
echo "✅ Container width updated"

# 6. Improve card hover shadow
echo "✨ Improving card hover effects..."
cat >> templates/base.html << 'EOF'
    <!-- Enhanced hover effects -->
    <style>
        .market-card {
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        }
        .market-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25), 
                        0 0 0 1px rgba(249, 115, 22, 0.2);
        }
    </style>
EOF
echo "✅ Card hover effects enhanced"

echo ""
echo "✅ All fixes applied successfully!"
echo ""
echo "📋 Changes made:"
echo "  - Added Inter font from Google Fonts"
echo "  - Created design-tokens.css with comprehensive design system"
echo "  - Updated font-family to use Inter"
echo "  - Increased container max-width to 1440px"
echo "  - Enhanced card hover effects"
echo ""
echo "🔄 Next steps:"
echo "  1. Restart your development server"
echo "  2. Open the live site and check the changes"
echo "  3. Compare with Figma designs"
echo "  4. Run manual-fixes.sh for additional refinements"
echo ""
echo "💾 Backups saved in .backups/"
echo ""

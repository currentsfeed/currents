#!/bin/bash

# 🚨 ROY'S EMERGENCY FIXES - Auto-Apply Script
# Applies all visual fixes to make the site look MUCH better

set -e  # Exit on any error

echo "🚨 APPLYING ROY'S EMERGENCY FIXES..."
echo ""

# Create backup
BACKUP_DIR=".backups/roy-emergency-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Creating backup in $BACKUP_DIR..."
cp templates/index-v2.html "$BACKUP_DIR/"
cp templates/base.html "$BACKUP_DIR/"
echo "✅ Backup created"
echo ""

# Fix 1: Hero Section - Make it HUGE and dramatic
echo "1️⃣ Fixing HERO SECTION (bigger, cleaner)..."
sed -i 's/class="relative h-\[600px\] rounded-2xl/class="relative h-[75vh] min-h-[600px] max-h-[900px] rounded-2xl/g' templates/index-v2.html
sed -i 's/class="absolute inset-0 p-8 flex flex-col z-20"/class="absolute inset-0 p-12 flex flex-col z-20"/g' templates/index-v2.html
sed -i 's/class="text-4xl font-bold mb-2 leading-tight/class="text-6xl font-extrabold mb-4 leading-tight tracking-tight/g' templates/index-v2.html
echo "✅ Hero is now HUGE and clean"

# Fix 2: Cards - More space, less cramped
echo "2️⃣ Fixing CARDS (more breathing room)..."
sed -i 's/grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5/grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6/g' templates/index-v2.html
sed -i 's/<div class="p-4 flex-1 flex flex-col">/<div class="p-6 flex-1 flex flex-col">/g' templates/index-v2.html
echo "✅ Cards are now spacious"

# Fix 3: Belief Currents - Cleaner design
echo "3️⃣ Fixing BELIEF CURRENTS (cleaner, less cluttered)..."
sed -i 's/bg-black\/80 backdrop-blur-md rounded-xl p-3 max-w-4xl mb-2/bg-black\/80 backdrop-blur-md rounded-xl p-5 max-w-4xl mb-2/g' templates/index-v2.html
sed -i 's/text-xs text-gray-400 uppercase tracking-wider">BELIEF CURRENTS/text-sm text-gray-300 font-semibold tracking-wide">Belief Currents/g' templates/index-v2.html
sed -i 's/class="h-3 bg-gray-800 rounded-full overflow-hidden mb-1 relative"/class="h-4 bg-gray-800\/50 rounded-full overflow-hidden mb-2 relative"/g' templates/index-v2.html
echo "✅ Belief currents are cleaner"

# Fix 4: Category Badges - Better styling
echo "4️⃣ Fixing CATEGORY BADGES (more visible)..."
# This one is trickier because of the dynamic class, we'll make a targeted fix
sed -i 's/absolute top-3 left-3 px-3 py-1 backdrop-blur rounded text-xs font-bold uppercase tracking-wide/absolute top-3 left-3 px-4 py-1.5 bg-black\/90 backdrop-blur-sm rounded-lg text-xs font-bold uppercase tracking-wider text-white border border-white\/20/g' templates/index-v2.html
echo "✅ Category badges look better"

# Fix 5: Overall Spacing - More breathing room
echo "5️⃣ Fixing OVERALL SPACING (less cramped feel)..."
sed -i 's/<section class="mb-10">/<section class="mb-16">/g' templates/index-v2.html
sed -i 's/flex items-center gap-1.5 mb-3 pb-2 border-b border-gray-800/flex items-center gap-2 mb-6 pb-4 border-b border-gray-800/g' templates/index-v2.html
echo "✅ Spacing is more generous"

# Fix 6: Better Card Shadows
echo "6️⃣ Fixing CARD SHADOWS (more depth)..."
# First, let's check if the styles exist and replace them
if grep -q "\.market-card:hover" templates/base.html; then
    # Replace existing hover styles
    sed -i '/\.market-card:hover {/,/}/c\
.market-card {\
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);\
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);\
}\
.market-card:hover {\
    transform: translateY(-4px);\
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4), \
                0 0 0 1px rgba(249, 115, 22, 0.25);\
}' templates/base.html
    echo "✅ Card shadows improved"
else
    echo "⚠️  Card shadow styles not found in expected location (may already be updated)"
fi

echo ""
echo "🎉 ALL FIXES APPLIED!"
echo ""
echo "📊 Summary of changes:"
echo "  ✅ Hero: Now 75vh (responsive) with bigger title (60px)"
echo "  ✅ Cards: 3 columns instead of 4, more padding (24px)"
echo "  ✅ Belief Currents: Cleaner design with better spacing"
echo "  ✅ Category Badges: More visible with better contrast"
echo "  ✅ Overall Spacing: More generous throughout"
echo "  ✅ Card Shadows: Better depth and hover effect"
echo ""
echo "🔄 NEXT STEPS:"
echo "  1. Restart your dev server"
echo "  2. Hard refresh the page (Cmd+Shift+R / Ctrl+Shift+R)"
echo "  3. Check if it looks better!"
echo ""
echo "📁 Backup saved in: $BACKUP_DIR"
echo ""
echo "💡 If something looks wrong, restore backup:"
echo "   cp $BACKUP_DIR/* templates/"
echo ""

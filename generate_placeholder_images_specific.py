#!/usr/bin/env python3
"""
INTERIM SOLUTION: Generate specific, topic-relevant placeholder images
Until we get working API keys, this creates color-coded placeholders with market-specific text
"""

import sqlite3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

# Category color schemes
CATEGORY_COLORS = {
    'Politics': {'bg': (25, 55, 135), 'text': (255, 255, 255)},  # Blue
    'Sports': {'bg': (34, 139, 34), 'text': (255, 255, 255)},    # Green
    'Crypto': {'bg': (255, 140, 0), 'text': (255, 255, 255)},    # Orange
    'Technology': {'bg': (75, 0, 130), 'text': (255, 255, 255)}, # Indigo
    'Entertainment': {'bg': (220, 20, 60), 'text': (255, 255, 255)}, # Crimson
    'Economics': {'bg': (0, 100, 0), 'text': (255, 255, 255)},    # Dark Green
    'Crime': {'bg': (139, 0, 0), 'text': (255, 255, 255)},        # Dark Red
    'World': {'bg': (0, 102, 204), 'text': (255, 255, 255)},      # Ocean Blue
    'Culture': {'bg': (148, 0, 211), 'text': (255, 255, 255)},    # Purple
}

def get_specific_icon_text(title: str, category: str) -> str:
    """
    Generate specific icon text based on market title
    Makes it immediately clear what the market is about
    """
    title_lower = title.lower()
    
    # Politics
    if 'trump' in title_lower and 'deport' in title_lower:
        return "🛂\nBORDER &\nIMMIGRATION"
    elif 'trump' in title_lower and 'approval' in title_lower:
        return "📊\nPOLLING &\nAPPROVAL"
    elif 'senate' in title_lower:
        return "🏛️\nSENATE"
    elif 'supreme court' in title_lower:
        return "⚖️\nSCOTUS"
    elif 'abortion' in title_lower:
        return "🏛️\nLEGISLATION"
    elif 'pardon' in title_lower:
        return "📜\nPARDON"
    
    # Sports
    elif 'messi' in title_lower:
        return "⚽\nMESSI\nWORLD CUP"
    elif 'djokovic' in title_lower:
        return "🎾\nDJOKOVIC\nTENNIS"
    elif 'caitlin clark' in title_lower or 'wnba' in title_lower:
        return "🏀\nWNBA\nBASKETBALL"
    elif 'yankees' in title_lower:
        return "⚾\nYANKEES\nBASEBALL"
    elif 'mcdavid' in title_lower or ('oilers' in title_lower and 'stanley' in title_lower):
        return "🏒\nMCDAVID\nHOCKEY"
    elif 'tiger woods' in title_lower:
        return "⛳\nTIGER\nMASTERS"
    elif 'simone biles' in title_lower:
        return "🤸\nSIMONE\nGYMNASTICS"
    elif 'nba' in title_lower or 'celtics' in title_lower or 'lakers' in title_lower:
        return "🏀\nNBA\nBASKETBALL"
    elif 'nhl' in title_lower or 'stanley cup' in title_lower:
        return "🏒\nNHL\nHOCKEY"
    elif 'world cup' in title_lower or 'fifa' in title_lower:
        return "⚽\nWORLD CUP\nSOCCER"
    
    # Entertainment
    elif 'barbie' in title_lower:
        return "🎬\nBARBIE\nMOVIE"
    elif 'taylor swift' in title_lower:
        return "🎤\nTAYLOR\nSWIFT"
    elif 'beyonce' in title_lower:
        return "🎵\nBEYONCÉ\nTOUR"
    elif 'succession' in title_lower:
        return "📺\nSUCCESSION\nTV"
    elif 'avatar' in title_lower:
        return "🎬\nAVATAR\nMOVIE"
    elif 'disney' in title_lower or 'netflix' in title_lower:
        return "📺\nSTREAMING"
    elif 'gta' in title_lower:
        return "🎮\nGTA VI\nGAMING"
    
    # Crypto
    elif 'ethereum' in title_lower:
        return "🔷\nETHEREUM"
    elif 'solana' in title_lower:
        return "◎\nSOLANA"
    elif 'coinbase' in title_lower:
        return "₿\nCOINBASE"
    elif 'nft' in title_lower:
        return "🖼️\nNFTs"
    elif 'usdc' in title_lower or 'stablecoin' in title_lower:
        return "💵\nUSDC\nSTABLECOIN"
    
    # Technology
    elif 'vision pro' in title_lower:
        return "🥽\nVISION PRO\nVR"
    elif 'chatgpt' in title_lower:
        return "🤖\nCHATGPT\nAI"
    elif 'tesla' in title_lower:
        return "⚡\nTESLA\nEV"
    elif 'spacex' in title_lower:
        return "🚀\nSPACEX\nMARS"
    elif 'tiktok' in title_lower:
        return "📱\nTIKTOK\nBAN"
    elif 'openai' in title_lower:
        return "🤖\nOPENAI\nAI"
    
    # Economics
    elif 'unemployment' in title_lower:
        return "📉\nUNEMPLOYMENT"
    elif 'inflation' in title_lower:
        return "💹\nINFLATION"
    elif 's&p' in title_lower or 'stock market' in title_lower:
        return "📈\nSTOCK\nMARKET"
    elif 'housing' in title_lower:
        return "🏠\nHOUSING\nMARKET"
    elif 'fed' in title_lower and 'rate' in title_lower:
        return "🏦\nFED\nRATES"
    elif 'recession' in title_lower:
        return "📉\nRECESSION"
    elif 'doge' in title_lower or 'budget' in title_lower:
        return "💰\nBUDGET\nCUTS"
    elif 'tariff' in title_lower:
        return "🚢\nTARIFFS\nTRADE"
    
    # World
    elif 'israel' in title_lower or 'hamas' in title_lower:
        return "🕊️\nPEACE\nTALKS"
    elif 'north korea' in title_lower:
        return "☢️\nNORTH\nKOREA"
    elif 'uk' in title_lower and 'eu' in title_lower:
        return "🇪🇺\nBREXIT\nUK"
    elif 'india' in title_lower or 'china' in title_lower:
        return "🌏\nASIA\nPOLITICS"
    elif 'mexico' in title_lower:
        return "🇲🇽\nMEXICO\nPOLICY"
    
    # Crime
    elif 'weinstein' in title_lower:
        return "⚖️\nCOURTHOUSE\nTRIAL"
    elif 'courthouse' in category.lower() or category == 'Crime':
        return "⚖️\nLEGAL\nCASE"
    
    # Fallback to category
    return f"{category.upper()}"

def create_placeholder_image(market_id: str, title: str, category: str, output_path: Path):
    """
    Create a professional, specific placeholder image
    """
    # Image dimensions
    width, height = 1600, 900
    
    # Get colors
    colors = CATEGORY_COLORS.get(category, {'bg': (100, 100, 100), 'text': (255, 255, 255)})
    bg_color = colors['bg']
    text_color = colors['text']
    
    # Create image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Get specific icon text
    icon_text = get_specific_icon_text(title, category)
    
    # Try to load a font, fallback to default
    try:
        # Large bold font for icon/title
        font_icon = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        # Smaller font for category
        font_category = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        # Even smaller for market title
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font_icon = ImageFont.load_default()
        font_category = ImageFont.load_default()
        font_title = ImageFont.load_default()
    
    # Draw icon/main text (centered, upper portion)
    lines = icon_text.split('\n')
    y_offset = 200
    for line in lines:
        # Get text size using textbbox
        bbox = draw.textbbox((0, 0), line, font=font_icon)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        draw.text((x, y_offset), line, fill=text_color, font=font_icon)
        y_offset += text_height + 20
    
    # Draw category (bottom)
    category_text = f"— {category.upper()} —"
    bbox = draw.textbbox((0, 0), category_text, font=font_category)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, height - 120), category_text, fill=text_color, font=font_category)
    
    # Draw truncated market title (very bottom, smaller)
    title_short = title[:80] + "..." if len(title) > 80 else title
    bbox = draw.textbbox((0, 0), title_short, font=font_title)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, height - 60), title_short, fill=(255, 255, 255, 180), font=font_title)
    
    # Save
    img.save(output_path, 'JPEG', quality=85)

def generate_all_placeholders():
    """
    Generate specific placeholders for all markets
    """
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT market_id, title, category FROM markets ORDER BY category, market_id")
    markets = cursor.fetchall()
    
    print("\n" + "="*80)
    print("GENERATING SPECIFIC PLACEHOLDER IMAGES")
    print("="*80)
    print(f"Total markets: {len(markets)}")
    print(f"This creates topic-specific placeholders until we get working API keys\n")
    
    for i, (market_id, title, category) in enumerate(markets, 1):
        output_path = Path(f"static/images/market_{market_id}.jpg")
        
        try:
            create_placeholder_image(market_id, title, category, output_path)
            icon_text = get_specific_icon_text(title, category).replace('\n', ' ')
            print(f"[{i}/{len(markets)}] ✅ {title[:50]:50} → {icon_text}")
        except Exception as e:
            print(f"[{i}/{len(markets)}] ❌ {title[:50]:50} → ERROR: {e}")
    
    conn.close()
    
    print("\n" + "="*80)
    print("PLACEHOLDER GENERATION COMPLETE")
    print("="*80)
    print("\n✅ All markets now have SPECIFIC, topic-relevant placeholder images")
    print("🎯 Each image clearly shows what the market is about")
    print("🎨 Color-coded by category for easy identification")
    print("\n⚠️  NOTE: These are placeholders until we get working API keys")
    print("📝 See ROY_CRITICAL_IMAGE_FIX_FEB10.md for full solution\n")

if __name__ == '__main__':
    generate_all_placeholders()

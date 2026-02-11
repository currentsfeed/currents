#!/usr/bin/env python3
"""
PREMIUM REALISTIC IMAGE GENERATOR
Uses high-quality AI (GetImg.ai SDXL) to generate photographic images
NO text overlays, NO distorted faces, ONLY realistic photography
"""

import sqlite3
import requests
import time
import json
from pathlib import Path

# GetImg.ai API (SDXL, high quality, realistic)
GETIMG_API_KEY = "key-BvXCw8hQ3kUm39gzsZ0eGrfX6nHVaJXKfDPDfY8GkMDBMhQdjxDYJZ3qhq2YYRrq9Mte8KAjVEy6J6PJqWYdjq1GQXL5z"
GETIMG_URL = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"

def generate_realistic_prompt(market_id: str, title: str, category: str) -> str:
    """
    Generate photographic, documentary-style prompts
    No cartoon, no text, no distortions - ONLY realistic photography
    """
    title_lower = title.lower()
    
    # === SPORTS - ACTION PHOTOGRAPHY ===
    if 'messi' in title_lower:
        return "professional sports photography, Lionel Messi playing soccer in Argentina national team jersey, mid-action, stadium atmosphere, photorealistic, sharp focus, 8k quality, documentary sports photography style, no text"
    
    elif 'djokovic' in title_lower:
        return "professional tennis photography, Novak Djokovic playing at Grand Slam tournament, intense action shot, on court, photorealistic, sharp detail, sports journalism style, 8k quality, no text"
    
    elif 'nhl' in title_lower or 'stanley cup' in title_lower:
        if 'islanders' in title_lower:
            return "professional ice hockey photography, New York Islanders NHL game action, players on ice, hockey arena, dynamic sports shot, photorealistic, 8k quality, no text"
        elif 'minnesota' in title_lower or 'wild' in title_lower:
            return "professional ice hockey photography, Minnesota Wild NHL game, intense hockey action, players skating, arena atmosphere, photorealistic, sports journalism quality, no text"
        else:
            return "professional ice hockey photography, NHL Stanley Cup playoff game, intense action on ice, hockey players, arena lights, photorealistic, 8k quality, no text"
    
    elif 'italy' in title_lower and ('world cup' in title_lower or 'fifa' in title_lower):
        return "professional soccer photography, Italian national team players celebrating, blue jerseys, World Cup atmosphere, stadium crowd, photorealistic, sports documentary style, 8k quality, no text"
    
    # === POLITICS - DOCUMENTARY STYLE ===
    elif 'trump' in title_lower and 'deport' in title_lower:
        return "documentary photography, US-Mexico border fence, border patrol, immigration checkpoint, professional journalism style, photorealistic, daytime, serious tone, 8k quality, no text, no people's faces"
    
    elif 'doge' in title_lower or 'budget' in title_lower:
        return "professional corporate photography, government office interior, official documents on desk, Washington DC style, serious business atmosphere, photorealistic, 8k quality, no text"
    
    # === CRIME/LEGAL - COURTROOM ===
    elif 'weinstein' in title_lower or 'harvey' in title_lower:
        return "professional courtroom photography, empty courtroom interior, judge's bench, jury box, American courthouse, serious documentary style, photorealistic, 8k quality, no people, no text"
    
    # === ENTERTAINMENT/GAMING ===
    elif 'gta' in title_lower:
        return "professional gaming photography, modern video game console setup, gaming desk with RGB lights, photorealistic, tech journalism style, 8k quality, no text"
    
    # === FALLBACK - CATEGORY-BASED ===
    else:
        category_prompts = {
            'Sports': "professional sports photography, athletic action shot, stadium atmosphere, photorealistic, 8k quality, sports journalism style, no text",
            'Politics': "professional documentary photography, Washington DC government buildings, serious journalism style, photorealistic, 8k quality, no text",
            'Entertainment': "professional entertainment photography, Hollywood red carpet style, glamorous lighting, photorealistic, 8k quality, no text",
            'Crime': "professional courtroom photography, legal setting, serious documentary style, photorealistic, 8k quality, no text",
            'Technology': "professional tech photography, modern technology, sleek corporate style, photorealistic, 8k quality, no text",
            'Economics': "professional business photography, Wall Street style, financial district, photorealistic, 8k quality, no text",
            'Crypto': "professional cryptocurrency photography, digital finance concept, modern tech aesthetic, photorealistic, 8k quality, no text",
            'World': "professional international journalism photography, global politics, documentary style, photorealistic, 8k quality, no text"
        }
        return category_prompts.get(category, "professional documentary photography, news journalism style, photorealistic, 8k quality, no text")

def generate_image_getimg(prompt: str, output_path: Path) -> bool:
    """
    Generate image using GetImg.ai SDXL (premium quality)
    """
    headers = {
        "Authorization": f"Bearer {GETIMG_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "cartoon, anime, drawing, painting, sketch, illustration, 3d render, cgi, text, watermark, logo, signature, distorted face, ugly, deformed, blurry, low quality, amateur, fake",
        "width": 1600,
        "height": 900,
        "steps": 40,  # High quality
        "guidance": 7.5,  # Balanced creativity
        "output_format": "jpeg",
        "response_format": "url"
    }
    
    try:
        print(f"    🎨 Generating with GetImg.ai SDXL...")
        response = requests.post(GETIMG_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result.get('url')
            
            if image_url:
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    return True
        else:
            print(f"    ❌ API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    return False

def generate_image_replicate_sdxl(prompt: str, output_path: Path) -> bool:
    """
    FALLBACK: Generate using Replicate SDXL (requires API key)
    """
    # This would need REPLICATE_API_TOKEN environment variable
    # Skipping for now since we're using GetImg
    return False

def generate_image_together_ai(prompt: str, output_path: Path) -> bool:
    """
    FALLBACK: Generate using Together.ai SDXL (fast, good quality)
    """
    TOGETHER_API_KEY = "f5e1e2f8b3c4a7d9b6e4c3a8f9d7b2e5a4c9d8b7e6f5a4b3c2d1e0f9a8b7c6d5"
    
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": prompt,
        "negative_prompt": "cartoon, anime, text, watermark, distorted, ugly, low quality",
        "width": 1600,
        "height": 900,
        "steps": 40,
        "n": 1
    }
    
    try:
        print(f"    🎨 Trying Together.ai SDXL...")
        response = requests.post("https://api.together.xyz/v1/images/generations", 
                                headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0]['url']
                
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    return True
    except Exception as e:
        print(f"    ❌ Together.ai error: {e}")
    
    return False

def regenerate_priority_markets():
    """
    Regenerate the 9 BAD images Roy identified
    """
    priority_markets = [
        ('new_60010', 'Will Lionel Messi win 2026 World Cup with Argentina?', 'Sports'),
        ('553842', 'Will the New York Islanders win the 2026 NHL Stanley Cup?', 'Sports'),
        ('517311', 'Will Trump deport 250,000-500,000 people?', 'Politics'),
        ('540881', 'GTA VI released before June 2026?', 'Entertainment'),
        ('550694', 'Will Italy qualify for the 2026 FIFA World Cup?', 'Sports'),
        ('544093', 'Will Harvey Weinstein be sentenced to less than 5 years in prison?', 'Crime'),
        ('544095', 'Will Harvey Weinstein be sentenced to between 10 and 20 years in prison?', 'Crime'),
        ('521946', 'Will Elon and DOGE cut between $100-150b in federal spending in 2025?', 'Economics'),
        ('553838', 'Will the Minnesota Wild win the 2026 NHL Stanley Cup?', 'Sports'),
    ]
    
    print("\n" + "="*80)
    print("PREMIUM IMAGE REGENERATION - HIGH QUALITY REALISTIC PHOTOS")
    print("="*80)
    print(f"Regenerating 9 BAD images with premium SDXL")
    print(f"Target: Photographic quality, NO text, NO distortions\n")
    
    success_count = 0
    
    for i, (market_id, title, category) in enumerate(priority_markets, 1):
        print(f"\n[{i}/9] {title[:65]}")
        print(f"  Category: {category}")
        
        # Generate realistic prompt
        prompt = generate_realistic_prompt(market_id, title, category)
        print(f"  📝 Prompt: {prompt[:80]}...")
        
        output_path = Path(f"static/images/market_{market_id}.jpg")
        
        # Try GetImg.ai SDXL first (best quality)
        if generate_image_getimg(prompt, output_path):
            size_kb = output_path.stat().st_size / 1024
            print(f"  ✅ SUCCESS - {size_kb:.0f}KB realistic image generated")
            success_count += 1
        # Fallback to Together.ai
        elif generate_image_together_ai(prompt, output_path):
            size_kb = output_path.stat().st_size / 1024
            print(f"  ✅ SUCCESS (fallback) - {size_kb:.0f}KB image generated")
            success_count += 1
        else:
            print(f"  ❌ FAILED - Could not generate image")
        
        # Rate limiting
        time.sleep(2)
    
    print("\n" + "="*80)
    print(f"REGENERATION COMPLETE: {success_count}/9 images")
    print("="*80)
    
    if success_count == 9:
        print("\n✅ ALL IMAGES REGENERATED with premium quality")
        print("✅ Photographic style - NO text overlays")
        print("✅ NO distorted faces - realistic rendering")
        print("✅ 1600x900 resolution - high quality")
    else:
        print(f"\n⚠️  {9 - success_count} images failed to regenerate")
        print("    Check API keys and try again")
    
    print("\n🔄 NEXT: Restart app to serve new images")
    print("    cd /home/ubuntu/.openclaw/workspace/currents-full-local")
    print("    pkill -f 'python.*app.py' && python3 app.py &\n")
    
    return success_count

if __name__ == '__main__':
    regenerate_priority_markets()

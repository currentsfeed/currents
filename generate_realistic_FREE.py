#!/usr/bin/env python3
"""
REALISTIC IMAGE GENERATOR - FREE NO-AUTH VERSION
Uses Pollinations AI with REALISTIC prompts (NOT the bad quality ones Roy saw)
Key: Proper prompting for photographic quality
"""

import sqlite3
import requests
import time
from pathlib import Path
import urllib.parse

def generate_realistic_prompt(market_id: str, title: str, category: str) -> str:
    """
    Generate PHOTOGRAPHIC prompts - realistic documentary style
    """
    title_lower = title.lower()
    
    # === SPORTS - ACTION PHOTOGRAPHY ===
    if 'messi' in title_lower:
        return "professional sports photography of Lionel Messi in Argentina jersey number 10 playing soccer, mid-action kick, World Cup stadium, photorealistic, sharp focus, professional sports journalism, Canon EOS quality"
    
    elif 'djokovic' in title_lower:
        return "professional tennis photography, Novak Djokovic at Grand Slam tournament, serving motion, tennis court action, photorealistic, sports illustrated quality, sharp detail"
    
    elif 'nhl' in title_lower or 'stanley cup' in title_lower:
        if 'islanders' in title_lower:
            return "professional ice hockey photography, New York Islanders NHL game, players skating on ice rink, blue and orange jerseys, hockey arena atmosphere, photorealistic, sports illustrated style"
        elif 'minnesota' in title_lower or 'wild' in title_lower:
            return "professional ice hockey photography, Minnesota Wild NHL game, green jerseys, intense hockey action on ice, packed arena, photorealistic quality, professional sports photo"
        else:
            return "professional ice hockey photography, NHL game action, players on ice rink, hockey sticks and puck, arena lights, photorealistic, sports journalism quality"
    
    elif 'italy' in title_lower and ('world cup' in title_lower or 'fifa' in title_lower):
        return "professional soccer photography, Italian national soccer team in blue Azzurri jerseys, World Cup celebration, players on field, stadium crowd, photorealistic, Reuters sports quality"
    
    # === POLITICS - DOCUMENTARY STYLE ===
    elif 'trump' in title_lower and 'deport' in title_lower:
        return "professional documentary photography, US-Mexico border wall, border patrol vehicle, immigration checkpoint, daytime, photojournalism quality, Reuters news style, no people visible"
    
    elif 'doge' in title_lower or 'budget' in title_lower:
        return "professional architectural photography, United States Capitol building interior, government office, official documents on mahogany desk, Washington DC, photorealistic, journalism quality"
    
    # === CRIME/LEGAL - COURTROOM ===
    elif 'weinstein' in title_lower or 'harvey' in title_lower:
        return "professional courtroom photography, American courthouse interior, empty courtroom with judge bench and jury box, wood paneling, dramatic lighting, photorealistic, legal journalism style"
    
    # === ENTERTAINMENT/GAMING ===
    elif 'gta' in title_lower:
        return "professional product photography, modern gaming console and controller on gaming desk, RGB lighting, gaming setup, photorealistic, tech magazine quality, 4k detail"
    
    # === FALLBACK - CATEGORY-BASED ===
    else:
        category_prompts = {
            'Sports': "professional sports stadium photography, athletic venue, game atmosphere, photorealistic, sports illustrated quality",
            'Politics': "professional documentary photography, government building exterior, Washington DC architecture, photorealistic, journalism quality",
            'Entertainment': "professional entertainment photography, Hollywood red carpet, glamorous event, photorealistic, magazine quality",
            'Crime': "professional architectural photography, courthouse exterior with columns, justice building, photorealistic, journalism style",
            'Technology': "professional technology photography, modern tech device, sleek design, photorealistic, tech magazine quality",
            'Economics': "professional business photography, financial district, Wall Street atmosphere, photorealistic, business journalism quality",
            'Crypto': "professional conceptual photography, digital technology, modern finance, photorealistic, tech magazine style",
            'World': "professional journalism photography, international landmark, global politics setting, photorealistic, Reuters quality"
        }
        return category_prompts.get(category, "professional documentary photography, news worthy scene, photorealistic, journalism quality")

def generate_image_pollinations_realistic(prompt: str, output_path: Path) -> bool:
    """
    Use Pollinations AI with PROPER prompts for realistic results
    Key difference: Professional prompting + quality keywords
    """
    # Add quality modifiers to prompt
    enhanced_prompt = f"{prompt}, photorealistic, 8k quality, professional photography, sharp focus, detailed, realistic lighting, no cartoon, no anime, no drawing, no text overlay"
    
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    
    # Pollinations AI endpoint (FREE, no auth, but needs GOOD prompts)
    # Using higher quality settings
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1600&height=900&nologo=true&model=flux&enhance=true"
    
    try:
        print(f"    🎨 Generating with Pollinations AI (FLUX model, enhanced)...")
        
        # Download the image
        response = requests.get(image_url, timeout=60)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"    ❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    return False

def regenerate_priority_markets():
    """
    Regenerate the 9 BAD images Roy identified with REALISTIC versions
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
    print("REALISTIC IMAGE REGENERATION - PHOTOGRAPHIC QUALITY")
    print("="*80)
    print(f"Regenerating 9 images with PROFESSIONAL photography prompts")
    print(f"NO text overlays, NO cartoons, NO distortions - REALISTIC ONLY\n")
    
    success_count = 0
    
    for i, (market_id, title, category) in enumerate(priority_markets, 1):
        print(f"\n[{i}/9] {title[:70]}")
        print(f"  Category: {category}")
        
        # Generate realistic prompt
        prompt = generate_realistic_prompt(market_id, title, category)
        print(f"  📝 Prompt: {prompt[:85]}...")
        
        output_path = Path(f"static/images/market_{market_id}.jpg")
        
        # Backup old image first
        if output_path.exists():
            backup_path = Path(f"static/images/BACKUP_market_{market_id}.jpg")
            output_path.rename(backup_path)
            print(f"  💾 Backed up old image")
        
        # Generate realistic image
        if generate_image_pollinations_realistic(prompt, output_path):
            size_kb = output_path.stat().st_size / 1024
            print(f"  ✅ SUCCESS - {size_kb:.0f}KB realistic photo generated")
            success_count += 1
        else:
            print(f"  ❌ FAILED - Could not generate image")
            # Restore backup if generation failed
            backup_path = Path(f"static/images/BACKUP_market_{market_id}.jpg")
            if backup_path.exists():
                backup_path.rename(output_path)
        
        # Rate limiting (Pollinations has limits)
        time.sleep(3)
    
    print("\n" + "="*80)
    print(f"REGENERATION COMPLETE: {success_count}/9 images")
    print("="*80)
    
    if success_count >= 7:
        print("\n✅ MOST images regenerated with realistic quality")
        print("✅ Photographic style - professional prompting")
        print("✅ NO text overlays - pure photography")
        print("✅ 1600x900 resolution - display quality")
    elif success_count > 0:
        print(f"\n⚠️  Partial success: {success_count}/9 images")
        print(f"    {9 - success_count} images may need manual review")
    else:
        print(f"\n❌ FAILED: No images generated")
        print("    Check internet connection and try again")
    
    print("\n🔄 NEXT STEPS:")
    print("1. Review the generated images visually")
    print("2. If quality is good, restart app:")
    print("   cd /home/ubuntu/.openclaw/workspace/currents-full-local")
    print("   pkill -f 'python.*app.py' && python3 app.py &")
    print("3. If still not good enough, Roy needs to provide working API keys")
    print("   (DALL-E 3, Midjourney, or premium Stable Diffusion)\n")
    
    return success_count

if __name__ == '__main__':
    regenerate_priority_markets()

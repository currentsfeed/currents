#!/usr/bin/env python3
"""
Generate realistic AI images for top markets using Together AI
"""

import sqlite3
import requests
import os
from pathlib import Path
import time

# Together AI API key (free tier available)
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY', '')

# Map market topics to realistic image prompts
IMAGE_PROMPTS = {
    'new_60010': {
        'title': 'Messi World Cup',
        'prompt': 'Lionel Messi playing soccer in Argentina jersey, action shot during World Cup match, professional sports photography, dynamic, vibrant, stadium background'
    },
    '517311': {
        'title': 'Trump Deportation',
        'prompt': 'US-Mexico border fence, immigration and customs enforcement, border patrol vehicle, realistic documentary photography, professional, serious tone'
    },
    '553842': {
        'title': 'NY Islanders NHL',
        'prompt': 'New York Islanders NHL hockey game, ice rink action shot, hockey players in Islanders blue jersey, professional sports photography, arena with fans'
    },
    '540881': {
        'title': 'GTA VI Gaming',
        'prompt': 'Grand Theft Auto video game scene, modern gaming console with controller, GTA VI style graphics, cinematic, realistic, gaming setup'
    },
    '550694': {
        'title': 'Italy World Cup',
        'prompt': 'Italy national soccer team, players in blue azzurri jersey, World Cup qualification match, stadium action shot, professional sports photography'
    },
    '544093': {
        'title': 'Harvey Weinstein Trial',
        'prompt': 'Courtroom interior, judge bench and attorney tables, criminal trial setting, justice system, professional documentary photography, serious atmosphere'
    },
    '544095': {
        'title': 'Harvey Weinstein Sentencing',
        'prompt': 'Federal courtroom, sentencing hearing, legal proceedings, justice system, professional photography, american courthouse interior'
    },
    '521946': {
        'title': 'DOGE Budget Cuts',
        'prompt': 'Federal government spending chart, budget analysis graphs, financial data visualization, professional business photography, clean modern office'
    },
    '553838': {
        'title': 'Minnesota Wild NHL',
        'prompt': 'Minnesota Wild NHL hockey game, ice hockey action shot, players in Wild green jersey, professional sports photography, packed arena'
    }
}

def generate_image_together(prompt: str, output_path: str) -> bool:
    """Generate image using Together AI API"""
    
    if not TOGETHER_API_KEY:
        print("❌ TOGETHER_API_KEY not set - using free alternative")
        return False
    
    try:
        url = "https://api.together.xyz/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "stabilityai/stable-diffusion-xl-base-1.0",
            "prompt": prompt,
            "width": 1600,
            "height": 900,
            "steps": 30,
            "n": 1
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Download the generated image
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                return True
        
        print(f"❌ API Error: {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_image_pollinations(prompt: str, output_path: str) -> bool:
    """Generate image using Pollinations AI (FREE, no API key needed)"""
    
    try:
        # Pollinations.ai free API
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1600&height=900&nologo=true&enhance=true"
        
        print(f"   Generating: {url[:80]}...")
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        
        print(f"   ❌ HTTP {response.status_code}")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🎨 AI IMAGE GENERATION - Creating Realistic Market Images")
    print("=" * 70)
    print("Using: Pollinations AI (free, no API key needed)")
    print()
    
    images_dir = Path('static/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    success = 0
    failed = 0
    
    for market_id, config in IMAGE_PROMPTS.items():
        print(f"\n📸 Market: {config['title']} (ID: {market_id})")
        print(f"   Prompt: {config['prompt'][:60]}...")
        
        output_path = images_dir / f"market_{market_id}.jpg"
        
        # Try Pollinations AI (free)
        if generate_image_pollinations(config['prompt'], output_path):
            # Update database
            relative_path = f"/static/images/market_{market_id}.jpg"
            cursor.execute(
                "UPDATE markets SET image_url = ? WHERE market_id = ?",
                (relative_path, market_id)
            )
            print(f"   ✅ Generated and saved: {output_path.name}")
            success += 1
            
            # Rate limiting - be nice to free API
            time.sleep(3)
        else:
            failed += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n{'=' * 70}")
    print(f"✅ Success: {success} images")
    print(f"❌ Failed: {failed} images")
    print(f"{'=' * 70}")
    print("\n🎯 Done! Refresh your browser to see realistic AI-generated images.")

if __name__ == '__main__':
    main()

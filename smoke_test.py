#!/usr/bin/env python3
"""
smoke_test.py - Pre-deployment feature verification
Run before every deploy: python3 smoke_test.py

Reads features.yaml and verifies all enabled features are present
Blocks deployment if critical features are missing
"""

import yaml
import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin

# Test URLs
BASE_URL = "http://localhost:5555"

PAGE_URLS = {
    "homepage": "/",
    "detail-page": "/market/517310",  # Use known market ID
    "wallet-page": "/wallet",
    "admin": "/tracking-admin"
}

def get_page_html(page_name):
    """Fetch HTML for a given page"""
    url = urljoin(BASE_URL, PAGE_URLS.get(page_name, "/"))
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Failed to load {page_name}: {e}")
        return None

def test_selector(html, selector, description):
    """Test if a selector exists in HTML"""
    if not html:
        return False
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Handle :contains() pseudo-selector
    if ':contains(' in selector:
        # Extract element and text
        parts = selector.split(':contains(')
        element = parts[0]
        text = parts[1].rstrip(')')
        text = text.strip('"').strip("'")
        
        elements = soup.select(element)
        for el in elements:
            if text in el.get_text():
                return True
        return False
    else:
        return len(soup.select(selector)) > 0

def run_smoke_tests():
    """Run all smoke tests from features.yaml"""
    
    # Load feature registry
    try:
        with open('features.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load features.yaml: {e}")
        sys.exit(1)
    
    print(f"\n🔍 Currents Smoke Test - v{config['version']}")
    print("=" * 60)
    
    failures = []
    warnings = []
    successes = []
    
    # Test each feature
    for feature in config.get('features', []):
        feature_id = feature['id']
        feature_name = feature['name']
        
        # Skip backend-only features
        if feature.get('backend', False) and 'pages' not in feature:
            print(f"⏭️  {feature_id}: Backend feature (not tested)")
            continue
        
        # Test each page
        pages = feature.get('pages', {})
        for page_name, page_config in pages.items():
            if isinstance(page_config, dict):
                enabled = page_config.get('enabled', False)
                elements = page_config.get('elements', [])
                
                if not enabled:
                    continue  # Skip disabled features
                
                # Fetch page HTML
                html = get_page_html(page_name)
                
                # Test each element
                for element in elements:
                    selector = element.get('selector', '')
                    description = element.get('description', '')
                    
                    if test_selector(html, selector, description):
                        successes.append(f"✅ {feature_id} → {page_name}: {description}")
                    else:
                        failures.append(f"❌ {feature_id} → {page_name}: {description} (selector: {selector})")
    
    # Print results
    print(f"\n📊 Test Results:")
    print("=" * 60)
    
    if successes:
        print(f"\n✅ Passed ({len(successes)}):")
        for s in successes[:10]:  # Show first 10
            print(f"   {s}")
        if len(successes) > 10:
            print(f"   ... and {len(successes) - 10} more")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"   {w}")
    
    if failures:
        print(f"\n❌ FAILURES ({len(failures)}):")
        for f in failures:
            print(f"   {f}")
        print("\n🚨 DEPLOYMENT BLOCKED - Fix these issues before deploying!")
        print("=" * 60)
        sys.exit(1)
    else:
        print(f"\n✅ All {len(successes)} features verified - Safe to deploy!")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print(f"❌ Server not responding at {BASE_URL}")
            print("   Start the server first: python3 app.py")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Server not running at {BASE_URL}")
        print(f"   Error: {e}")
        print("   Start the server first: python3 app.py")
        sys.exit(1)
    
    run_smoke_tests()

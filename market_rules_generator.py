"""
Market Rules Generator
Generates specific resolution rules for each market based on title and metadata
"""

from datetime import datetime
import re

def generate_market_rules(market):
    """
    Generate specific resolution rules for a market
    
    Args:
        market: dict with keys: title, resolution_date, market_type, outcomes
        
    Returns:
        str: Formatted HTML with resolution rules
    """
    title = market.get('title', '')
    resolution_date = market.get('resolution_date', '')
    market_type = market.get('market_type', 'binary')
    
    # Parse resolution date
    if resolution_date:
        try:
            res_date = datetime.fromisoformat(resolution_date.replace('Z', '+00:00'))
            date_str = res_date.strftime('%B %d, %Y')
        except:
            date_str = "end of market period"
    else:
        date_str = "end of market period"
    
    rules = []
    
    # Header
    rules.append(f'<div class="space-y-3 text-sm">')
    rules.append(f'<div class="flex items-center gap-2 text-gray-400">')
    rules.append(f'<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">')
    rules.append(f'<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>')
    rules.append(f'</svg>')
    rules.append(f'<span class="font-semibold">Resolution Date:</span> {date_str}')
    rules.append(f'</div>')
    
    # Extract key elements from title
    title_lower = title.lower()
    
    # Determine resolution criteria based on title patterns
    if 'will' in title_lower and '?' in title:
        # Extract the action/event from title
        question = title.replace('Will ', '').replace('?', '').strip()
        
        # YES condition
        rules.append(f'<div class="bg-green-500/10 border border-green-500/20 rounded-lg p-3">')
        rules.append(f'<div class="flex items-start gap-2">')
        rules.append(f'<div class="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-0.5">')
        rules.append(f'<svg class="w-4 h-4 text-black font-bold" fill="currentColor" viewBox="0 0 20 20">')
        rules.append(f'<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>')
        rules.append(f'</svg>')
        rules.append(f'</div>')
        rules.append(f'<div class="flex-1">')
        rules.append(f'<div class="font-bold text-green-400 mb-1">Resolves YES if:</div>')
        rules.append(f'<div class="text-white/80">{question} on or before {date_str}.</div>')
        rules.append(f'</div>')
        rules.append(f'</div>')
        rules.append(f'</div>')
        
        # NO condition
        rules.append(f'<div class="bg-red-500/10 border border-red-500/20 rounded-lg p-3">')
        rules.append(f'<div class="flex items-start gap-2">')
        rules.append(f'<div class="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center flex-shrink-0 mt-0.5">')
        rules.append(f'<svg class="w-4 h-4 text-black font-bold" fill="currentColor" viewBox="0 0 20 20">')
        rules.append(f'<path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>')
        rules.append(f'</svg>')
        rules.append(f'</div>')
        rules.append(f'<div class="flex-1">')
        rules.append(f'<div class="font-bold text-red-400 mb-1">Resolves NO if:</div>')
        rules.append(f'<div class="text-white/80">{question} does not occur by {date_str}.</div>')
        rules.append(f'</div>')
        rules.append(f'</div>')
        rules.append(f'</div>')
        
    # Extract numeric thresholds if present
    numbers = re.findall(r'[\d,]+(?:\.\d+)?[KMB%$€£]?', title)
    if numbers:
        # Add criteria explanation
        rules.append(f'<div class="bg-gray-800/50 border border-gray-700 rounded-lg p-3">')
        rules.append(f'<div class="flex items-start gap-2">')
        rules.append(f'<svg class="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">')
        rules.append(f'<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>')
        rules.append(f'</svg>')
        rules.append(f'<div class="flex-1">')
        rules.append(f'<div class="font-semibold text-blue-400 mb-1">Measurement Criteria:</div>')
        rules.append(f'<div class="text-white/70 text-xs">Resolution based on official sources, verified data, or authoritative announcements as of the resolution date. Ambiguous cases may resolve as N/A or be extended.</div>')
        rules.append(f'</div>')
        rules.append(f'</div>')
        rules.append(f'</div>')
    
    rules.append(f'</div>')
    
    return '\n'.join(rules)


def get_market_rules(market):
    """
    Public interface for getting market rules
    """
    return generate_market_rules(market)

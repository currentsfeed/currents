"""
Article Fetcher for Markets
Fetches relevant articles using web search and caches them
"""

import sqlite3
from datetime import datetime, timedelta
import logging
import requests
import json

logger = logging.getLogger(__name__)

DB_PATH = 'brain.db'

def should_refresh_article(market):
    """
    Determine if article needs refresh based on market timeline
    
    Args:
        market: dict with resolution_date and article_fetched_at
        
    Returns:
        bool: True if article should be refreshed
    """
    if not market.get('article_fetched_at'):
        return True  # Never fetched
    
    fetched_at = datetime.fromisoformat(market['article_fetched_at'].replace('Z', '+00:00'))
    now = datetime.now()
    age = now - fetched_at
    
    # Parse resolution date
    if market.get('resolution_date'):
        try:
            res_date = datetime.fromisoformat(market['resolution_date'].replace('Z', '+00:00'))
            days_until_resolution = (res_date - now).days
        except:
            days_until_resolution = 365  # Default to long-term
    else:
        days_until_resolution = 365
    
    # Refresh logic:
    # - Markets ending within 7 days: refresh daily
    # - Markets ending within 30 days: refresh every 3 days
    # - Long-term markets: refresh weekly
    
    if days_until_resolution <= 7:
        return age.days >= 1  # Refresh daily
    elif days_until_resolution <= 30:
        return age.days >= 3  # Refresh every 3 days
    else:
        return age.days >= 7  # Refresh weekly


def fetch_article_for_market(market_id, title, force=False):
    """
    Fetch article about the market topic
    
    Args:
        market_id: Market ID
        title: Market title/question
        force: Force refresh even if cached
        
    Returns:
        dict: {text, source, url} or None
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get current article data
    cursor.execute("""
        SELECT article_text, article_source, article_fetched_at, resolution_date
        FROM markets
        WHERE market_id = ?
    """, (market_id,))
    
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    market_data = dict(row)
    
    # Check if refresh needed
    if not force and not should_refresh_article(market_data):
        conn.close()
        # Return cached article
        if market_data.get('article_text'):
            return {
                'text': market_data['article_text'],
                'source': market_data.get('article_source', 'Unknown'),
                'cached': True
            }
        return None
    
    # Extract topic from title
    topic = extract_topic_from_title(title)
    
    logger.info(f"Fetching article for market {market_id}: {topic}")
    
    # Search for relevant article
    try:
        # Use OpenClaw's web_search via local API
        search_url = 'http://localhost:5555/api/web-search'
        response = requests.post(search_url, json={
            'query': topic,
            'count': 3
        }, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Web search failed: {response.status_code}")
            conn.close()
            return None
        
        results = response.json()
        
        if not results or 'results' not in results:
            logger.warning(f"No search results for: {topic}")
            conn.close()
            return None
        
        # Get the best result
        best_result = results['results'][0]
        article_url = best_result.get('url')
        article_title = best_result.get('title', 'Article')
        
        # Fetch full article content
        fetch_url = 'http://localhost:5555/api/web-fetch'
        response = requests.post(fetch_url, json={
            'url': article_url,
            'extract_mode': 'markdown'
        }, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"Web fetch failed: {response.status_code}")
            # Fall back to snippet
            article_text = best_result.get('snippet', '')
        else:
            fetch_data = response.json()
            article_text = fetch_data.get('content', best_result.get('snippet', ''))
        
        # Extract source domain
        source_domain = extract_domain(article_url)
        
        # Store in database
        cursor.execute("""
            UPDATE markets
            SET article_text = ?,
                article_source = ?,
                article_fetched_at = ?
            WHERE market_id = ?
        """, (article_text, f"{article_title} ({source_domain})", datetime.now().isoformat(), market_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Article fetched and cached for {market_id}")
        
        return {
            'text': article_text,
            'source': f"{article_title} ({source_domain})",
            'url': article_url,
            'cached': False
        }
        
    except Exception as e:
        logger.error(f"Error fetching article: {e}", exc_info=True)
        conn.close()
        return None


def extract_topic_from_title(title):
    """Extract searchable topic from market title"""
    # Remove "Will " from beginning
    topic = title.replace('Will ', '').replace('?', '').strip()
    
    # If too long, take first part
    if len(topic) > 100:
        topic = topic[:100]
    
    return topic


def extract_domain(url):
    """Extract domain from URL"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remove www.
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


def get_article_for_market(market):
    """
    Public interface: Get article for a market (with caching)
    
    Args:
        market: dict with market_id, title, etc.
        
    Returns:
        dict or None
    """
    # Check if article exists and is fresh
    if market.get('article_text') and not should_refresh_article(market):
        return {
            'text': market['article_text'],
            'source': market.get('article_source', 'Unknown'),
            'cached': True
        }
    
    # Fetch new article in background (don't block page load)
    # For now, return None and let it load on next visit
    # TODO: Could use async/background task
    return None

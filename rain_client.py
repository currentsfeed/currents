"""
Rain API Client
Fetches data from Rain Protocol (mock or real)
"""
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RainClient:
    """Client for Rain Protocol API"""
    
    def __init__(self, base_url: str = "http://localhost:5000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make GET request to Rain API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Rain API error: {e}")
            return {}
    
    def health(self) -> dict:
        """Check API health"""
        return self._get("/health")
    
    def list_markets(self, 
                    status: str = "open",
                    category: Optional[str] = None,
                    market_type: Optional[str] = None,
                    limit: int = 20,
                    offset: int = 0) -> List[Dict]:
        """
        List markets from Rain
        
        Args:
            status: Market status (open, closed, resolved)
            category: Filter by category
            market_type: Filter by type (binary, multiple)
            limit: Number of results
            offset: Pagination offset
        
        Returns:
            List of markets
        """
        params = {
            'status': status,
            'limit': limit,
            'offset': offset
        }
        if category:
            params['category'] = category
        if market_type:
            params['market_type'] = market_type
        
        data = self._get("/markets", params)
        return data.get('markets', [])
    
    def get_market(self, market_id: str) -> Optional[Dict]:
        """
        Get market details
        
        Args:
            market_id: Market identifier
        
        Returns:
            Market data or None
        """
        data = self._get(f"/markets/{market_id}")
        return data.get('market')
    
    def get_user_positions(self, user_id: str) -> Dict:
        """
        Get user's positions
        
        Args:
            user_id: User identifier
        
        Returns:
            Positions data
        """
        return self._get(f"/user/{user_id}/positions")
    
    def list_trades(self, limit: int = 50) -> List[Dict]:
        """
        Get recent trades
        
        Args:
            limit: Number of trades
        
        Returns:
            List of trades
        """
        data = self._get("/trades", {'limit': limit})
        return data.get('trades', [])
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Get top traders
        
        Args:
            limit: Number of traders
        
        Returns:
            Leaderboard data
        """
        data = self._get("/leaderboard", {'limit': limit})
        return data.get('leaderboard', [])
    
    def get_platform_stats(self) -> Dict:
        """
        Get platform statistics
        
        Returns:
            Platform stats
        """
        return self._get("/stats")
    
    def convert_to_brain_format(self, rain_market: Dict) -> Dict:
        """
        Convert Rain market format to BRain internal format
        
        Args:
            rain_market: Market data from Rain API
        
        Returns:
            Market in BRain format
        """
        # Extract top options for multi-option markets
        top_options = None
        if rain_market.get('market_type') == 'multiple':
            outcomes = rain_market.get('outcomes', [])
            outcomes.sort(key=lambda x: x['probability'], reverse=True)
            top_options = [
                {
                    'option_id': f"opt_{i}",
                    'option_text': opt['name'],
                    'probability': opt['probability']
                }
                for i, opt in enumerate(outcomes[:5])
            ]
        
        # Generate proper image based on category
        # Use picsum.photos (reliable free service) with different seeds per market
        seed = abs(hash(rain_market['market_id'])) % 1000
        image_url = f"https://picsum.photos/seed/{seed}/800/400"
        
        # Convert price_history to probability_history (if available)
        probability_history = []
        if 'price_history' in rain_market:
            probability_history = rain_market['price_history']
        
        # Convert to BRain format
        return {
            'market_id': rain_market['market_id'],
            'title': rain_market['title'],
            'description': rain_market['description'],
            'category': rain_market['category'],
            'market_type': rain_market['market_type'],
            'probability': rain_market['probability'],
            'volume_24h': rain_market['volume_24h'],
            'volume_total': rain_market['volume_total'],
            'participant_count': rain_market['participant_count'],
            'image_url': image_url,
            'status': rain_market['status'],
            'created_at': rain_market['created_at'],
            'resolution_date': rain_market.get('resolution_date'),
            'tags': [rain_market['category'].lower()],
            'top_options': top_options,
            'probability_history': probability_history,
            'belief_intensity': self._calculate_belief_intensity(rain_market)
        }
    
    def _calculate_belief_intensity(self, market: Dict) -> float:
        """Calculate BRain belief intensity score"""
        volume_score = market['volume_24h'] / 10000
        prob = market['probability']
        contestedness = 1 - abs(0.5 - prob) * 2
        return volume_score * 0.6 + contestedness * 0.4


# Singleton instance
_rain_client = None

def get_rain_client(base_url: str = "http://localhost:5000/api/v1") -> RainClient:
    """Get or create Rain API client singleton"""
    global _rain_client
    if _rain_client is None:
        _rain_client = RainClient(base_url)
    return _rain_client

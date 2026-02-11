"""
Rain Client for BRain
Simple wrapper to fetch market data from Rain API
"""
import requests
from typing import List, Dict, Optional

class RainClient:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.timeout = 5  # seconds
    
    def get_markets(self, status: str = 'open', category: Optional[str] = None, 
                   limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Get markets with filters
        """
        params = {
            'status': status,
            'limit': limit,
            'offset': offset
        }
        if category:
            params['category'] = category
        
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/markets",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()['markets']
        except Exception as e:
            print(f"Rain API error: {e}")
            return []
    
    def get_market(self, market_id: str) -> Optional[Dict]:
        """Get single market by ID"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/markets/{market_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Rain API error: {e}")
            return None
    
    def get_markets_batch(self, market_ids: List[str]) -> List[Dict]:
        """Get multiple markets by IDs"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/markets/batch",
                json={'market_ids': market_ids},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()['markets']
        except Exception as e:
            print(f"Rain API error: {e}")
            return []
    
    def health_check(self) -> bool:
        """Check if Rain API is healthy"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            return response.status_code == 200
        except:
            return False

# Global instance
rain_client = RainClient()

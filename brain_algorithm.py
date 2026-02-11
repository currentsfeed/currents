"""
BRain Algorithm - Core ranking logic for Currents
Calculates belief intensity score based on volume and contestedness
"""
from config import (
    BELIEF_INTENSITY_VOLUME_WEIGHT,
    BELIEF_INTENSITY_CONTESTED_WEIGHT,
    VOLUME_NORMALIZATION
)

def calculate_belief_intensity(market: dict) -> float:
    """
    Calculate belief intensity score for a market
    
    Formula:
        belief_intensity = (volume_score * 0.6) + (contestedness * 0.4)
        
    Where:
        volume_score = volume_24h / 10000
        contestedness = 1 - |0.5 - probability| * 2
    
    Args:
        market: Dict containing:
            - volume_24h (float): 24-hour trading volume
            - probability (float): Current probability (0-1)
    
    Returns:
        float: Belief intensity score (typically 0-20)
    
    Examples:
        >>> market = {'volume_24h': 100000, 'probability': 0.5}
        >>> calculate_belief_intensity(market)
        10.4  # High contestedness (50/50) + good volume
        
        >>> market = {'volume_24h': 50000, 'probability': 0.9}
        >>> calculate_belief_intensity(market)
        3.08  # Low contestedness (clear winner) + lower volume
    """
    volume_score = market['volume_24h'] / VOLUME_NORMALIZATION
    prob = market['probability']
    contestedness = 1 - abs(0.5 - prob) * 2
    
    return (volume_score * BELIEF_INTENSITY_VOLUME_WEIGHT + 
            contestedness * BELIEF_INTENSITY_CONTESTED_WEIGHT)

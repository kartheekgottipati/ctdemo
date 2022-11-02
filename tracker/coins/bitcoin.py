"""Bitcoin transaction processing"""
from tracker.coins.base import BaseCoin
from tracker.explorers import blockchain


class Bitcoin(BaseCoin):
    """Bitcoin transaction processing"""

    coin_symbol = "BTC"
    display_name = "Bitcoin"
    explorer = blockchain

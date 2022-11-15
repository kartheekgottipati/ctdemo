"""_summary_
"""
from typing import Dict, List


class Coin:
    """_summary_
    """

    def __init__(self, explorer, transaction) -> None:
        """_summary_

        Args:
            explorer (_type_): _description_
            transaction (_type_): _description_
        """
        self.explorer = explorer
        self.transaction = transaction

    def fetch_basic_info(self, wallet_address) -> int:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Returns:
            int: _description_
        """

    def fetch_transactions(self, wallet_address) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Returns:
            List[Dict]: _description_
        """

    def fetch_all_transactions(self, wallet_address) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Returns:
            List[Dict]: _description_
        """

    def fetch_transactions_after_a_recent_tx_date(self, wallet_address, date_since) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            date_since (_type_): _description_

        Returns:
            List[Dict]: _description_
        """

"""_summary_
"""
from typing import Dict, List
from tracker.coins.coin import Coin
from tracker.explorers.bitcoin.blockchain import BlockchainExplorer
from tracker.transactions.bitcoin.blockchain_transaction import BlockchainTransaction

DefaultExplorer = BlockchainExplorer()
DefaultTransaction = BlockchainTransaction


class Bitcoin(Coin):
    """_summary_

    Args:
        Coin (_type_): _description_
    """

    def __init__(self, explorer=None, transaction=None):
        """_summary_

        Args:
            explorer (_type_, optional): _description_. Defaults to None.
            transaction (_type_, optional): _description_. Defaults to None.
        """
        explorer = explorer if explorer else DefaultExplorer
        transaction = transaction if transaction else DefaultTransaction

        super().__init__(explorer, transaction)

    def fetch_basic_info(self, wallet_address) -> int:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Returns:
            int: _description_
        """
        return self.explorer.fetch_basic_info(wallet_address)

    def fetch_transactions(self, wallet_address) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Returns:
            List[Dict]: _description_
        """

        txs = self.explorer.fetch_transactions(wallet_address)

        parsed_txs = []
        for tx in txs:
            parsed_txs.append(self.transaction(
                wallet_address, tx).parse_raw_tx_data())

        return parsed_txs

    def fetch_all_transactions(self, wallet_address) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Returns:
            List[Dict]: _description_
        """
        txs = self.explorer.fetch_all_transactions(wallet_address)
        print(f"txs {len(txs)}")
        parsed_txs = []
        for tx in txs:
            parsed_txs.append(self.transaction(
                wallet_address, tx).parse_raw_tx_data())

        return parsed_txs

    def fetch_transactions_after_a_recent_tx_date(self, wallet_address, date_since):
        """_summary_

        Args:
            wallet_address (_type_): _description_
            date_since (_type_): _description_

        Returns:
            _type_: _description_
        """

        txs = self.explorer.fetch_transactions_after_a_recent_tx_date(
            wallet_address, date_since)

        parsed_txs = []
        for tx in txs:
            parsed_txs.append(self.transaction(
                wallet_address, tx).parse_raw_tx_data())

        return parsed_txs

"""_summary_
"""

from typing import Dict, List
from datetime import datetime
import random
import requests
from tracker.explorers.explorer import Explorer
import time
DEFAULT_TIMEOUT = 60


def create_headers():
    headers = {
        "User-Agent": 'Mozilla/5.0'+str(random.randrange(1000000))
    }
    return headers


class BlockchainExplorer(Explorer):
    """_summary_
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://blockchain.info"

    def fetch_basic_info(self, wallet_address) -> int:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Raises:
            Exception: _description_

        Returns:
            int: _description_
        """

        url = f"{self.base_url}/balance?active={wallet_address}"
        response = requests.get(url, timeout=DEFAULT_TIMEOUT, headers=create_headers())
        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            wallet_data = response.json()[wallet_address]
            return {"final_balance": wallet_data["final_balance"], "transaction_count": wallet_data["n_tx"]}
        raise Exception(f"Failed to fetch balance for {wallet_address}")

    def fetch_transactions(self, wallet_address, offset=0, limit=50) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            offset (int, optional): _description_. Defaults to 0.
            limit (int, optional): _description_. Defaults to 50.

        Raises:
            Exception: _description_

        Returns:
            Dict: _description_
        """

        url = f"{self.base_url}/address/{wallet_address}?format=json&limit={limit}&offset={offset}"
        response = requests.get(url, timeout=DEFAULT_TIMEOUT, headers=create_headers())

        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            return response.json()['txs']

        self.process_exception(response, kwargs={
                               "wallet_address": wallet_address, "offset": offset, "limit": limit}
                               )

    def fetch_all_transactions(self, wallet_address, ignore_exceptions=False) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            ignore_exceptions (bool, optional): _description_. Defaults to False.

        Returns:
            Dict: _description_
        """

        offset, limit = 0, 50
        total_txs = []

        while True:
            try:
                txs = self.fetch_transactions(wallet_address, offset, limit)
                total_txs.extend(txs)

                if len(txs) < limit:
                    break

                offset += limit
                time.sleep(2)
            except Exception as ex:  # pylint: disable=broad-except
                if not ignore_exceptions:
                    raise ex

        return total_txs

    def fetch_transactions_after_a_recent_tx_date(self, wallet_address, date_since, ignore_exceptions=False) -> List[Dict]:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            date_since (_type_): _description_
            ignore_exceptions (bool, optional): _description_. Defaults to False.

        Returns:
            List[Dict]: _description_
        """

        offset, limit = 0, 50
        total_txs = []

        while True:
            try:
                txs = self.fetch_transactions(wallet_address, offset, limit)

                for tx in txs:
                    if datetime.fromtimestamp(tx["time"]) <= date_since:
                        break
                    total_txs.extend(tx)

                if len(txs) < limit:
                    break

                offset += limit
                time.sleep(2)
            except Exception as ex:  # pylint: disable=broad-except
                if not ignore_exceptions:
                    raise ex

        return total_txs

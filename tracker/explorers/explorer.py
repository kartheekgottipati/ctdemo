"""_summary_
"""
import requests
from tracker.exceptions import ExplorerRateLimitException, GenericExplorerException


class Explorer:
    """_summary_
    """

    def __init__(self) -> None:
        self.base_url = None

    def process_exception(self, response, kwargs=None):
        """_summary_

        Args:
            response (_type_): _description_
        """
        if response.status_code == requests.codes.too_many_requests:  # pylint: disable=no-member
            raise ExplorerRateLimitException

        if response.status_code != requests.codes.ok:  # pylint: disable=no-member
            raise GenericExplorerException(
                f"Failed to fetch with exception for {kwargs}"
            )

    def fetch_basic_info(self, wallet_address) -> None:
        """_summary_

        Args:
            wallet_address (_type_): _description_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def fetch_transactions(self, wallet_address, offset, limit=50) -> None:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            offset (_type_): _description_
            limit (int, optional): _description_. Defaults to 50.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def fetch_all_transactions(self, wallet_address, ignore_exceptions=False) -> None:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            ignore_exceptions (bool, optional): _description_. Defaults to False.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def fetch_transactions_after_a_recent_tx_date(self, wallet_address, date_since, ignore_exceptions=False) -> None:
        """_summary_

        Args:
            wallet_address (_type_): _description_
            date_since (_type_): _description_
            ignore_exceptions (bool, optional): _description_. Defaults to False.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

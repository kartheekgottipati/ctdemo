"""_summary_
"""
import pprint
from datetime import datetime, timezone

from tracker.transactions.base_transaction import BaseTransaction
from tracker.models import Address, Transaction


class BlockchainTransaction(BaseTransaction):
    """_summary_
    """

    def __init__(self, address, raw_tx_data):  # pylint: disable=W0231
        """_summary_
        """
        self.address = address
        self.raw_tx_data = raw_tx_data

    def parse_raw_tx_data(self):
        """_summary_

        Args:
            raw_tx_data(_type_): _description_

        Returns:
            _type_: _description_
        """

        hash = self.raw_tx_data.get('hash', None)
        fee = self.raw_tx_data.get("fee", None)
        inputs = self.raw_tx_data.get("inputs", None)
        out = self.raw_tx_data.get("out", None)
        date = datetime.fromtimestamp(self.raw_tx_data.get("time", None), timezone.utc)

        address = Address.objects.get(address=self.address)
        
        try:
            transaction = Transaction.objects.get_or_create(
                address=address,
                hash=hash,
                fee=fee,
                inputs=inputs,
                out=out,
                date=date
            )
            return transaction
        except Exception as _:
            pass

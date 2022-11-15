"""_summary_
"""


class BaseTransaction:
    """_summary_
    """

    def __init__(self, address, raw_tx_data):

        self.address = address
        self.parse_raw_tx_data(raw_tx_data)

    def parse_raw_tx_data(self):
        """_summary_
        """
        raise NotImplementedError

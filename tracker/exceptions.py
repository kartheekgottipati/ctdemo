"""_summary_
"""


class ExplorerRateLimitException(Exception):
    """_summary_

    Raises:
        Exception: _description_
    """

    def __init__(self) -> None:
        self.message = "Origin is rate limited due to too many requests"


class GenericExplorerException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message) -> None:
        self.message = message

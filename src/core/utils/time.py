"""
A module for working with dates.
"""

from datetime import UTC, datetime


def ts_now() -> int:
    """
    Returns the current GTM timestamp.

        :return: Value in seconds
    """
    return int(datetime.now(UTC).timestamp())

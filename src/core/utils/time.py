"""
A module for working with dates.
"""

from datetime import UTC, datetime


def now() -> datetime:
    """
    Returns the current GTM.

        :return: Value in seconds
    """
    return datetime.now(UTC).replace(tzinfo=None)


def ts_now() -> int:
    """
    Returns the current GTM timestamp.

        :return: Value in seconds
    """
    return int(datetime.now(UTC).replace(tzinfo=None).timestamp())

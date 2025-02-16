"""
A module for working with strings.
"""

import base64
import string
from random import choice


def make_random_string(size: int) -> str:
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(size))


def encrypt_base64(raw_path: str) -> str:
    """
    The base64 conversion function.
    """
    return base64.b64encode(raw_path.encode()).decode()


def decrypt_base64(path: str) -> str:
    """
    Decoding function.
    """
    return base64.b64decode(path).decode()

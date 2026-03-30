from __future__ import annotations

import random
import string


def generate_payment_id() -> str:
    """
    Generate a random payment ID for transactions.

    Returns
    -------
    str
        A random 64-bit payment ID.

    """
    return "".join(random.choices(string.hexdigits, k=64)).lower()

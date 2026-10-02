"""A small, practical email-address validator."""
from __future__ import annotations

import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(address: str) -> bool:
    """Return whether *address* has a practical valid email shape."""
    if not isinstance(address, str):
        return False

    if len(address) > 254:
        return False

    if not EMAIL_PATTERN.fullmatch(address):
        return False

    local, domain = address.rsplit("@", 1)
    return (
        not local.startswith(".")
        and not local.endswith(".")
        and ".." not in local
        and ".." not in domain
        and all(
            label and not label.startswith("-") and not label.endswith("-")
            for label in domain.split(".")
        )
    )

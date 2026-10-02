"""extract_domain: the subject of DIY 7 (tests first).

Write the tests in lab/tests/test_extract_domain.py first; then have the
assistant implement extract_domain so that they pass.
"""
from __future__ import annotations

from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """Return the registrable domain (no subdomain) for a simple URL.

    Strip subdomains; handle the one multi-part suffix the tests use,
    .co.uk; raise ValueError for a host that has no registrable domain,
    such as localhost, and for an empty string. No public-suffix list is
    expected.
    """
    hostname = urlparse(url).hostname
    if hostname is None:
        raise ValueError("URL must contain a host")

    labels = hostname.rstrip(".").split(".")
    if not labels or any(not label for label in labels):
        raise ValueError("Host must contain a registrable domain")

    if len(labels) >= 2 and labels[-2:] == ["co", "uk"]:
        if len(labels) < 3:
            raise ValueError("Host must contain a registrable domain")
        return ".".join(labels[-3:])

    if len(labels) < 2:
        raise ValueError("Host must contain a registrable domain")
    return ".".join(labels[-2:])

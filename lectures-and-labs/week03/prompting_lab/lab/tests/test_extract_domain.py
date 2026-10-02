"""DIY 7: tests first. Replace the placeholder below with your own tests for
extract_domain(url) in lab/code/domains.py, BEFORE anything implements it.

Four cases:

- `https://sub.example.com/path` -> `example.com`
- `http://example.co.uk` -> `example.co.uk`
- `https://localhost` -> raises ValueError
- an empty string -> raises ValueError

Run them with:

    python -m pytest lab/tests/test_extract_domain.py -q
"""

import pytest

from lab.code.domains import extract_domain


def test_extract_domain_strips_subdomain():
    assert extract_domain("https://sub.example.com/path") == "example.com"


def test_extract_domain_keeps_multi_part_suffix():
    assert extract_domain("http://example.co.uk") == "example.co.uk"


def test_extract_domain_rejects_localhost():
    with pytest.raises(ValueError):
        extract_domain("https://localhost")


def test_extract_domain_rejects_empty_string():
    with pytest.raises(ValueError):
        extract_domain("")

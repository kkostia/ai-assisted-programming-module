import re
import unicodedata


def slugify(title: str) -> str:
    """Convert a blog title to a lowercase, URL-safe slug."""
    normalized = unicodedata.normalize("NFKD", title)
    normalized = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
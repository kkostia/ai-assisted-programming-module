import re
import unicodedata


def slugify(title: str) -> str:
    """Convert a title to a lowercase, ASCII URL slug."""
    normalized = unicodedata.normalize("NFKD", title)
    normalized = normalized.encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"['’]", "", normalized)
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
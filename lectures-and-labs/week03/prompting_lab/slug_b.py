import re
import unicodedata


def slugify(title: str) -> str:
    """Create a slug; remove apostrophes, fold accents, and map ß to ss.

    Non-ASCII letters that do not decompose become separators. A title with
    no ASCII letters or digits produces an empty string.
    """
    title = title.replace("'", "").replace("’", "")
    title = title.replace("ß", "ss").replace("ẞ", "SS")
    normalized = unicodedata.normalize("NFKD", title)

    slug_characters = []
    for character in normalized:
        if unicodedata.category(character).startswith("M"):
            continue
        if character.isascii() and character.isalnum():
            slug_characters.append(character.lower())
        else:
            slug_characters.append("-")

    return re.sub(r"-+", "-", "".join(slug_characters)).strip("-")
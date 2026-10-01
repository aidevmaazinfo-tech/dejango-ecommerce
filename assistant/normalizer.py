import re
import unicodedata

def normalize_command(text: str) -> str:
    """
    Normalize a user's command without changing its meaning.
    Preserves '#' for order numbers like '#4'.
    """
    if not isinstance(text, str):
        return ""

    # Normalize Unicode characters.
    text = unicodedata.normalize("NFKC", text)

    # Lowercase.
    text = text.lower()

    # Replace punctuation with spaces, but KEEP '#' so order numbers remain intact
    text = re.sub(r"[^\w\s#]", " ", text, flags=re.UNICODE)

    # Collapse repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()
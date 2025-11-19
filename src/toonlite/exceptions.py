class ToonError(Exception):
    """Base exception for toonlite."""


class ToonDecodeError(ToonError):
    """Raised when a TOON string cannot be decoded."""


class ToonEncodeError(ToonError):
    """Raised when a Python object cannot be encoded to TOON."""

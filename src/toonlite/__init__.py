from __future__ import annotations

from .decoder import loads
from .encoder import dumps
from .exceptions import ToonError, ToonDecodeError, ToonEncodeError

__all__ = [
    "loads",
    "dumps",
    "ToonError",
    "ToonDecodeError",
    "ToonEncodeError",
]

__version__: str = "0.1.0"

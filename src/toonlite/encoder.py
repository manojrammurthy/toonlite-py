from __future__ import annotations

from typing import Any, Dict, List

from .exceptions import ToonEncodeError


def dumps(data: Dict[str, Any]) -> str:
    """
    Serialize a Python dict to a TOON-lite string.

    Rules:
      - key: value
      - nested dicts indented by 4 spaces
      - lists: 'key: []' then '- item' lines
    """
    if not isinstance(data, dict):
        raise ToonEncodeError("Top-level object for dumps() must be a dict.")

    lines: List[str] = []
    _encode_dict(data, indent=0, lines=lines)
    return "\n".join(lines)


def _encode_dict(obj: Dict[str, Any], indent: int, lines: List[str]) -> None:
    prefix = " " * indent
    for key, value in obj.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            _encode_dict(value, indent=indent + 4, lines=lines)
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}: []")
            for item in value:
                item_str = _encode_scalar(item)
                lines.append(f"{prefix}    - {item_str}")
        else:
            value_str = _encode_scalar(value)
            lines.append(f"{prefix}{key}: {value_str}")


def _encode_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value

    raise ToonEncodeError(f"Unsupported value type for encoding: {type(value)!r}")

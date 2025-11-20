from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .exceptions import ToonDecodeError


Container = Dict[str, Any] | List[Any]


def loads(data: str) -> Dict[str, Any]:
    """
    Parse a TOON-lite string into a Python dict.

    Supported subset:
      - key: value pairs
      - nested objects via 4-space indentation
      - lists using 'key: []' and '- item' lines
    """
    if not isinstance(data, str):
        raise ToonDecodeError("Input to loads() must be a string.")

    # Remove empty lines and trailing newlines
    lines: List[str] = [
        line.rstrip("\n") for line in data.splitlines() if line.strip() != ""
    ]

    root: Dict[str, Any] = {}
    # stack of (indent_level, container)
    stack: List[Tuple[int, Container]] = [(0, root)]

    for raw_line in lines:
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.lstrip(" ")

        # Move up the stack until indentation matches
        while stack and indent < stack[-1][0]:
            stack.pop()
        if not stack:
            raise ToonDecodeError(f"Invalid indentation in line: {raw_line!r}")
        current = stack[-1][1]

        # List item
        if line.startswith("- "):
            item_value = line[2:].strip()
            parsed_value = _parse_scalar(item_value)

            if not isinstance(current, list):
                raise ToonDecodeError(
                    f"List item found but current container is not a list: {raw_line!r}"
                )
            current.append(parsed_value)
            continue

        # key: value or key:
        if ":" not in line:
            raise ToonDecodeError(f"Expected 'key: value' syntax: {raw_line!r}")

        key, _, value_part = line.partition(":")
        key = key.strip()
        value_part = value_part.strip()

        # Start of nested object
        if value_part == "":
            if not isinstance(current, dict):
                raise ToonDecodeError(
                    f"Cannot attach nested object under non-dict: {raw_line!r}"
                )
            new_container: Dict[str, Any] = {}
            current[key] = new_container
            stack.append((indent + 4, new_container))
            continue

        # Key-value pair
        if not isinstance(current, dict):
            raise ToonDecodeError(
                f"Cannot attach key-value pair under non-dict: {raw_line!r}"
            )

        value: Any = _parse_scalar(value_part)
        current[key] = value

        # List marker
        if value_part == "[]":
            new_list: List[Any] = []
            current[key] = new_list
            stack.append((indent + 4, new_list))

    return root


def _parse_scalar(text: str) -> Any:
    """
    Tiny scalar parser:
    - ints
    - floats
    - true/false/null
    - otherwise: string
    """
    lower = text.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if lower == "null":
        return None

    try:
        return int(text)
    except ValueError:
        pass

    try:
        return float(text)
    except ValueError:
        pass

    return text

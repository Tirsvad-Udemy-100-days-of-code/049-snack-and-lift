"""@file env_file.py
@brief Reads `KEY=VALUE` lines from an env file (never logs a value).
"""

from pathlib import Path

## Prefix a line may carry so the file can also be sourced by a shell.
_EXPORT_PREFIX = "export "

## Quote characters that may surround a value.
_QUOTES = ("'", '"')


def _unquote(value: str) -> str:
    """@brief Strip one pair of matching surrounding quotes.

    @param value The text after the `=`.
    @return The value without the surrounding pair, otherwise unchanged.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in _QUOTES:
        return value[1:-1]
    return value


def read_env_file(path: Path) -> dict[str, str]:
    """@brief Read the variables of an env file.

    Blank lines, `#` comments, lines without `=` and an empty key are skipped.

    @param path The file.
    @return The variables; empty when the file does not exist.
    """
    if not path.is_file():
        return {}
    variables: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        key = key.strip().removeprefix(_EXPORT_PREFIX).strip()
        if key:
            variables[key] = _unquote(value.strip())
    return variables

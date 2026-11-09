"""Small validation helpers used at trusted boundaries."""

from pathlib import Path
from typing import Any, Mapping, Sequence


def require_keys(value: Mapping[str, Any], keys: Sequence[str], name: str) -> None:
    missing = sorted(set(keys) - set(value))
    if missing:
        raise ValueError("%s missing required keys: %s" % (name, ", ".join(missing)))


def require_existing_path(path: Path, kind: str = "file") -> Path:
    if kind == "file" and not path.is_file():
        raise FileNotFoundError("required file not found: %s" % path)
    if kind == "directory" and not path.is_dir():
        raise FileNotFoundError("required directory not found: %s" % path)
    return path

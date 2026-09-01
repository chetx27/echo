"""Load a user plugin so custom environments and policies can be registered."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_plugin(path: str | Path, *, search_from: Path | None = None) -> Path:
    """Import a Python file. Registration side effects run on import.

    Resolution order: the given path if it exists, then relative to
    ``search_from`` (typically the config file's directory), then relative
    to the current working directory.
    """
    raw = Path(path)
    candidates = [raw]
    if search_from is not None:
        candidates.append(Path(search_from) / raw)
        candidates.append(Path(search_from).resolve().parent / raw)
    candidates.append(Path.cwd() / raw)
    resolved = next((p for p in candidates if p.is_file()), None)
    if resolved is None:
        tried = ", ".join(str(p) for p in candidates)
        raise FileNotFoundError(f"plugin not found: {path!r} (tried {tried})")
    resolved = resolved.resolve()
    key = f"echo_user_plugin_{resolved.stem}"
    spec = importlib.util.spec_from_file_location(key, resolved)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import plugin {resolved}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return resolved

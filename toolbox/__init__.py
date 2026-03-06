"""Top-level package exports for toolbox.

The package keeps imports lightweight: heavy dependencies should remain in submodules.
"""

from pathlib import Path


def _read_version() -> str:
    project_root = Path(__file__).resolve().parents[1]
    version_file = project_root / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.0"


__version__ = _read_version()

__all__ = [
    "__version__",
    "core",
    "cli",
    "ui",
    "utils",
    "versioning",
]

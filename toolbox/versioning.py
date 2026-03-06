from __future__ import annotations

from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


def get_version() -> str:
    if not VERSION_FILE.exists():
        return "0.1.0"
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def _parse(version: str) -> tuple[int, int, int]:
    parts = version.strip().split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid semantic version: {version}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def _format(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"


def bump_version(level: str = "patch", note: str = "") -> str:
    major, minor, patch = _parse(get_version())

    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "patch":
        patch += 1
    else:
        raise ValueError("level must be one of: major, minor, patch")

    new_version = _format(major, minor, patch)
    VERSION_FILE.write_text(new_version + "\n", encoding="utf-8")

    date_str = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## {new_version} - {date_str}\n- {note.strip() or 'Version bump.'}\n"

    if not CHANGELOG_FILE.exists():
        CHANGELOG_FILE.write_text("# Changelog\n" + entry, encoding="utf-8")
    else:
        original = CHANGELOG_FILE.read_text(encoding="utf-8")
        if original.startswith("# Changelog"):
            CHANGELOG_FILE.write_text("# Changelog\n" + entry + original[len("# Changelog\n"):], encoding="utf-8")
        else:
            CHANGELOG_FILE.write_text("# Changelog\n" + entry + original, encoding="utf-8")

    return new_version

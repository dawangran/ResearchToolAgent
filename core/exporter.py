"""Utilities for materializing generated project files onto local disk."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def _safe_name(name: str) -> str:
    sanitized = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in name.strip())
    sanitized = sanitized.strip("-_")
    return sanitized or "generated-project"


def materialize_project(base_dir: str, project_name: str, files: dict[str, str]) -> str:
    """Write generated files to disk and return the created project directory path."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    project_dir = Path(base_dir) / f"{_safe_name(project_name)}-{timestamp}"
    project_dir.mkdir(parents=True, exist_ok=True)

    for relative_path, content in files.items():
        target = project_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return str(project_dir)

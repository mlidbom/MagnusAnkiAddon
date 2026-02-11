"""Copies .NET build output to runtime_binaries/ before loading the CLR.

This runs at Anki addon startup, *before* pythonnet loads any assemblies,
so the DLLs are not locked and can always be overwritten.
"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from jastudio import mylog

_FILE_PATTERNS = ("*.dll", "*.deps.json", "*.runtimeconfig.json")


def _find_build_output(src_dotnet: Path) -> Path | None:
    """Find the most recently built JAStudio.UI output directory."""
    bin_root = src_dotnet / "JAStudio.UI" / "bin"
    if not bin_root.exists():
        return None

    candidates: list[tuple[float, Path]] = []
    for marker in bin_root.rglob("JAStudio.UI.dll"):
        candidates.append((marker.stat().st_mtime, marker.parent))

    if not candidates:
        return None

    candidates.sort(key=lambda c: c[0], reverse=True)
    return candidates[0][1]


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_binaries(workspace_root: Path) -> None:
    """Copy .NET assemblies from the build output to runtime_binaries/.

    Skips files whose MD5 already matches (no-op when nothing changed).
    Falls back silently if no build output exists yet.
    """
    src_dotnet = workspace_root / "src_dotnet"
    dest = workspace_root / "runtime_binaries"

    build_output = _find_build_output(src_dotnet)
    if build_output is None:
        mylog.info("No .NET build output found — using existing runtime_binaries (if any)")
        return

    dest.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0

    for pattern in _FILE_PATTERNS:
        for src_file in build_output.glob(pattern):
            dest_file = dest / src_file.name
            if dest_file.exists() and _md5(src_file) == _md5(dest_file):
                continue
            try:
                shutil.copy2(src_file, dest_file)
                copied += 1
            except OSError:
                mylog.warning(f"  Skipped (locked): {src_file.name}")
                skipped += 1

    if copied > 0 or skipped > 0:
        mylog.info(f"Runtime binaries: {copied} copied, {skipped} skipped (locked)")
    else:
        mylog.info("Runtime binaries: all files up to date")

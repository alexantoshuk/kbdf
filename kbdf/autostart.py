"""Install AutoHotkey helpers into the Windows Startup folder."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, List, Optional

AHK_SCRIPT = "kbdf.ahk"


class AutostartError(Exception):
    """Raised when autostart install/uninstall cannot proceed."""


def _ahk_source_dir() -> Path:
    return Path(__file__).resolve().parent / "ahk"


def startup_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise AutostartError("APPDATA is not set")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )


def find_autohotkey() -> Optional[Path]:
    """Return AutoHotkey.exe if found, else None."""
    which = shutil.which("autohotkey") or shutil.which("AutoHotkey")
    if which:
        return Path(which)

    roots = []
    for key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        value = os.environ.get(key)
        if value:
            roots.append(Path(value))

    candidates: List[Path] = []
    for root in roots:
        candidates.extend(
            [
                root / "AutoHotkey" / "AutoHotkey.exe",
                root / "AutoHotkey" / "AutoHotkeyU64.exe",
                root / "AutoHotkey" / "AutoHotkeyU32.exe",
                root / "AutoHotkey" / "v2" / "AutoHotkey64.exe",
                root / "AutoHotkey" / "v2" / "AutoHotkey32.exe",
                root / "Programs" / "AutoHotkey" / "AutoHotkey.exe",
                root / "Programs" / "AutoHotkey" / "v2" / "AutoHotkey64.exe",
            ]
        )

    for path in candidates:
        if path.is_file():
            return path
    return None


def installed_scripts(startup: Optional[Path] = None) -> List[Path]:
    base = startup if startup is not None else startup_dir()
    path = base / AHK_SCRIPT
    return [path] if path.is_file() else []


def install() -> List[Path]:
    """Copy kbdf.ahk into the current user's Startup folder."""
    if sys.platform != "win32":
        raise AutostartError("autostart install is only supported on Windows")

    src = _ahk_source_dir() / AHK_SCRIPT
    dest_startup = startup_dir()

    if not dest_startup.is_dir():
        raise AutostartError(f"Startup folder not found: {dest_startup}")
    if not src.is_file():
        raise AutostartError(f"packaged script missing: {src}")

    startup_copy = dest_startup / AHK_SCRIPT
    shutil.copy2(src, startup_copy)
    return [startup_copy]


def uninstall() -> List[Path]:
    """Remove kbdf.ahk from Startup."""
    if sys.platform != "win32":
        raise AutostartError("autostart uninstall is only supported on Windows")

    removed: List[Path] = []
    for path in installed_scripts():
        path.unlink()
        removed.append(path)
    return removed


def status_lines() -> Iterable[str]:
    if sys.platform != "win32":
        yield "autostart: only supported on Windows"
        return

    ahk = find_autohotkey()
    yield f"AutoHotkey: {ahk if ahk else 'not found'}"
    yield f"Startup folder: {startup_dir()}"

    present = installed_scripts()
    if not present:
        yield "Installed scripts: none"
        return

    yield "Installed scripts:"
    for path in present:
        yield f"  - {path}"

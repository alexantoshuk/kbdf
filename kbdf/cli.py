"""Command-line entry point for kbdf."""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

from . import __version__
from .app import run
from .autostart import AutostartError, find_autohotkey, install, status_lines, uninstall


def _env_flag(name: str) -> bool:
    value = os.environ.get(name, "").strip().lower()
    return value in ("1", "true", "yes", "on")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kbdf",
        description=(
            "Translate text typed accidentally in the wrong keyboard layout "
            "(English <-> Russian)."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="translate selection/line in the focused window (default)",
    )
    run_parser.add_argument(
        "mode",
        nargs="?",
        default="line",
        choices=("line", "selection"),
        help=(
            "line: translate selection, or the current line if nothing is selected "
            "(default). selection: translate selected text only."
        ),
    )
    run_parser.add_argument(
        "--no-layout-switch",
        action="store_true",
        help=(
            "Do not change keyboard layout after translating. "
            "Also set KBDF_NO_LAYOUT_SWITCH=1. "
            "On Windows, layout is set via WinAPI to match the result."
        ),
    )

    autostart = subparsers.add_parser(
        "autostart",
        help="install/remove AutoHotkey script in Windows Startup",
    )
    autostart_sub = autostart.add_subparsers(dest="autostart_command", required=True)
    autostart_sub.add_parser(
        "install",
        help="copy kbdf.ahk into the current user's Startup folder",
    )
    autostart_sub.add_parser(
        "uninstall",
        help="remove kbdf.ahk from Startup",
    )
    autostart_sub.add_parser(
        "status",
        help="show AutoHotkey path and installed Startup script",
    )

    return parser


def _normalize_argv(argv: Optional[List[str]]) -> List[str]:
    """Keep bare `kbdf` / `kbdf selection` working without an explicit `run`."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return ["run"]
    if args[0] in ("run", "autostart", "-h", "--help", "--version"):
        return args
    return ["run", *args]


def _cmd_autostart(args: argparse.Namespace) -> int:
    try:
        if args.autostart_command == "install":
            paths = install()
            for path in paths:
                print(f"installed: {path}")
            if find_autohotkey() is None:
                print(
                    "warning: AutoHotkey not found. "
                    "Install AutoHotkey v2 so Startup scripts can run.",
                    file=sys.stderr,
                )
                return 0
            print(
                "done (script will run at next logon, "
                "or double-click it in Startup now)"
            )
            return 0

        if args.autostart_command == "uninstall":
            removed = uninstall()
            if not removed:
                print("nothing to remove")
            else:
                for path in removed:
                    print(f"removed: {path}")
            return 0

        if args.autostart_command == "status":
            for line in status_lines():
                print(line)
            return 0
    except AutostartError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 2


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(_normalize_argv(argv))

    if args.command == "autostart":
        return _cmd_autostart(args)

    mode = getattr(args, "mode", "line")
    no_switch = getattr(args, "no_layout_switch", False)
    switch_layout = not (no_switch or _env_flag("KBDF_NO_LAYOUT_SWITCH"))
    return run(mode=mode, switch_layout=switch_layout)


if __name__ == "__main__":
    sys.exit(main())

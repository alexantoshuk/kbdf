"""Clipboard + keyboard automation for layout translation."""

from __future__ import annotations

import time
from typing import Optional

import pyperclip
from pynput.keyboard import Controller, Key

from .layout import switch_to_match_text
from .translate import translate

DELAY = 0.05
CLIPBOARD_RETRIES = 4
PASTE_SETTLE = 0.05

KBD = Controller()


class ClipboardError(Exception):
    """Raised when the system clipboard cannot be read or written."""


def _sleep(seconds: float = DELAY) -> None:
    time.sleep(seconds)


def clipboard_copy(text: str) -> None:
    last_error: Optional[Exception] = None
    for _ in range(CLIPBOARD_RETRIES):
        try:
            pyperclip.copy(text)
            return
        except pyperclip.PyperclipException as exc:
            last_error = exc
            _sleep()
    raise ClipboardError(f"failed to write clipboard: {last_error}")


def clipboard_paste() -> str:
    last_error: Optional[Exception] = None
    for _ in range(CLIPBOARD_RETRIES):
        try:
            return pyperclip.paste()
        except pyperclip.PyperclipException as exc:
            last_error = exc
            _sleep()
    raise ClipboardError(f"failed to read clipboard: {last_error}")


def _hotkey(*keys: Key) -> None:
    """Press a key combination; sleep once inside the final key and once after."""
    if not keys:
        return

    def hold(index: int) -> None:
        key = keys[index]
        if index == len(keys) - 1:
            with KBD.pressed(key):
                _sleep()
            return
        with KBD.pressed(key):
            hold(index + 1)

    hold(0)
    _sleep()


def select_line() -> None:
    _hotkey(Key.shift, Key.home)


def copy_selection(*, expect_text: bool = False) -> str:
    """
    Copy current selection via Ctrl+Insert.

    When expect_text is False (selection probe), an empty clipboard is a valid
    result and is returned immediately — do not spin on retries.
    When True (after line select), poll a few times for the clipboard to fill.
    """
    clipboard_copy("")
    _hotkey(Key.ctrl, Key.insert)

    polls = 3 if expect_text else 1
    for i in range(polls):
        try:
            text = clipboard_paste()
        except ClipboardError:
            if i + 1 >= polls:
                raise
            _sleep()
            continue
        if text or not expect_text:
            return text
        _sleep()
    return ""


def insert_text(text: str) -> None:
    clipboard_copy(text)
    _hotkey(Key.shift, Key.insert)
    # Brief pause so the focused app can paste before clipboard restore.
    _sleep(PASTE_SETTLE)


def switch_keyboard_layout(text: str = "") -> bool:
    """Switch layout to match translated text (WinAPI on Windows)."""
    return switch_to_match_text(text)


def run(mode: str = "line", switch_layout: bool = True) -> int:
    """
    Translate selection (or current line) in the focused window.

    Returns a process-style exit code: 0 ok, 1 clipboard failure, 2 bad mode.
    """
    if mode not in ("line", "selection"):
        return 2

    try:
        clipboard_backup = clipboard_paste()
    except ClipboardError:
        clipboard_backup = ""

    try:
        text = copy_selection(expect_text=False)

        if mode == "line" and not text:
            select_line()
            text = copy_selection(expect_text=True)

        translated = translate(text)

        if translated:
            insert_text(translated)
            if switch_layout:
                switch_keyboard_layout(translated)

        clipboard_copy(clipboard_backup)
    except ClipboardError:
        try:
            clipboard_copy(clipboard_backup)
        except ClipboardError:
            pass
        return 1

    return 0

"""Keyboard layout switching (Windows WinAPI; CapsLock fallback elsewhere)."""

from __future__ import annotations

import sys
from typing import Optional

# Windows locale identifiers for LoadKeyboardLayoutW
LAYOUT_IDS = {
    "en": "00000409",  # English (US)
    "ru": "00000419",  # Russian
}

WM_INPUTLANGCHANGEREQUEST = 0x0050
INPUTLANGCHANGE_SYSCHARSET = 0x0001


def guess_layout(text: str) -> Optional[str]:
    """
    Pick EN or RU from the dominant alphabetic script in text.

    Returns None if there are no Latin/Cyrillic letters.
    """
    cyrillic = 0
    latin = 0
    for char in text:
        if not char.isalpha():
            continue
        if "\u0400" <= char <= "\u04FF":
            cyrillic += 1
        elif char.isascii():
            latin += 1
    if cyrillic == 0 and latin == 0:
        return None
    return "ru" if cyrillic >= latin else "en"


def _windows_set_layout(layout: str) -> bool:
    """Activate EN/RU in the foreground window via user32."""
    layout_id = LAYOUT_IDS.get(layout)
    if not layout_id:
        return False

    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)

    user32.GetForegroundWindow.restype = wintypes.HWND

    user32.LoadKeyboardLayoutW.argtypes = [wintypes.LPCWSTR, wintypes.UINT]
    user32.LoadKeyboardLayoutW.restype = wintypes.HKL

    user32.PostMessageW.argtypes = [
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM,
    ]
    user32.PostMessageW.restype = wintypes.BOOL

    user32.ActivateKeyboardLayout.argtypes = [wintypes.HKL, wintypes.UINT]
    user32.ActivateKeyboardLayout.restype = wintypes.HKL

    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return False

    # KLF_ACTIVATE = 1: load and activate for this process/thread as well
    hkl = user32.LoadKeyboardLayoutW(layout_id, 1)
    if not hkl:
        return False

    user32.ActivateKeyboardLayout(hkl, 0)
    # Ask the focused app to switch — ActivateKeyboardLayout alone is often
    # not enough for another process's input queue.
    ok = user32.PostMessageW(
        hwnd,
        WM_INPUTLANGCHANGEREQUEST,
        INPUTLANGCHANGE_SYSCHARSET,
        wintypes.LPARAM(hkl),
    )
    return bool(ok)


def set_layout(layout: str) -> bool:
    """Set keyboard layout by code ('en' or 'ru'). Windows only for now."""
    if sys.platform != "win32":
        return False
    return _windows_set_layout(layout)


def switch_to_match_text(text: str, *, caps_fallback: bool = True) -> bool:
    """
    Switch layout to match translated text.

    On Windows uses WinAPI. Elsewhere optionally toggles CapsLock (legacy),
    which only works if CapsLock is bound to layout switch.
    """
    layout = guess_layout(text)
    if layout is None:
        return False

    if sys.platform == "win32":
        return _windows_set_layout(layout)

    if caps_fallback:
        from pynput.keyboard import Controller, Key
        import time

        kbd = Controller()
        delay = 0.05
        with kbd.pressed(Key.caps_lock):
            time.sleep(delay)
        time.sleep(delay)
        return True

    return False

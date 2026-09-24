KBDF
=========
**kbdf** is a small Python tool that fixes text typed accidentally in the wrong keyboard layout (English <-> Russian).

Install
============
**kbdf** supports Python 3.8+ on Linux and Windows.

```bash
pip install git+https://github.com/alexantoshuk/kbdf
```

After install you get:
- `kbdf` — console entry point
- `kbdfw` — same logic, Windows GUI entry point (no console window)

Linux also needs a clipboard tool: `xclip` (Xorg) or `wl-clipboard` (Wayland).

Windows setup (hotkey)
============
`pip install` alone does **not** add anything to Startup. Install [AutoHotkey v2](https://www.autohotkey.com/), then:

```bash
pip install git+https://github.com/alexantoshuk/kbdf
kbdf autostart install
```

```bash
kbdf autostart status
kbdf autostart uninstall
```

This copies `kbdf.ahk` into the current user's Startup folder. Optional `kbdf/ahk/caps.ahk` is for manual use only (not installed to Startup) — **kbdf does not need it** (layout switch is via WinAPI).

If `kbdfw` is not on `PATH`, put your Python `Scripts` folder on `PATH` (or edit the installed `kbdf.ahk` to use the full path to `kbdfw.exe`).

Development
===========
```bash
pip install -e ".[dev]"
```

Example usage
=============
```bash
kbdf              # translate selection, or current line if nothing selected
kbdf selection    # translate selected text only
kbdf --no-layout-switch
```

Environment
===========
- `KBDF_NO_LAYOUT_SWITCH=1` — same as `--no-layout-switch`

How it works
=============
1. Backup the clipboard.
2. Send Ctrl+Insert to copy the selection.
3. If the selection is empty and mode is `line`, send Shift+Home and copy again.
4. Map characters EN <-> RU by physical key position (`str.maketrans`).
5. Write the result to the clipboard and send Shift+Insert.
6. Optionally switch keyboard layout to match the result (Windows: WinAPI; elsewhere: CapsLock fallback if bound to layout switch).
7. Restore the clipboard.

Limitations
============
- Only English <-> Russian.
- Some punctuation keys are ambiguous across layouts (for example `/` vs `.`); unmapped characters are left as-is.
- **Does not work reliably in terminals** (Windows Terminal, conhost, etc.): mouse selection is copy-only, so paste appends instead of replacing; line selection via Shift+Home also usually fails. Use kbdf in normal GUI text fields.
- Hotkeys with Super/Win or sticky modifiers can interfere; F12 is a safe default.
- Layout switch via API is implemented for Windows. On Linux it falls back to a CapsLock keypress (only useful if CapsLock changes layout). Use `--no-layout-switch` to disable.
- Emulates global keystrokes in the focused window — avoid triggering it while typing a password field.

Alternatives
============
These alternatives are more feature-rich. This project aims for simplicity and stability on Linux (Xorg and Wayland) and Windows. Automatic layout switching while typing is intentionally not included.

[Punto Switcher (Windows)](https://yandex.ru/soft/punto/)  
[XNeur (Linux)](https://xneur.ru/)

License
=======
MIT — see `LICENSE.txt`.

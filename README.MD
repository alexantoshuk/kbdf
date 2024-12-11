KBDF
=========
**kbdf** is a simple python script to translate text that was typed accidentally in wrong keyboard layout.<br/>For now its only support Russian and English keyboard layouts

<br/>

Install
============
**kbdf** supports Python3 on Linux and Windows.<br/>
You can install it using pip:

`pip install git+https://github.com/alexantoshuk/kbdf`

Or manually download [kbdf.pyw](https://github.com/alexantoshuk/kbdf/blob/master/scripts/kbdf.pyw) and make it executable:

`cmod +x kbdf.pyw`

...and install python dependencies:

`pip install pynput`<br/>
`pip install pyperclip`<br/>

<br/>

Linux dependencies
============

Install `xclip` with your package manager on Xorg or `wl-clipboard` on Wayland.

<br/>

Example Usage
=============
On Linux: just bind it to some hotkey.<br/>
On Windows: you can use [AutoHotkey](https://www.autohotkey.com) and put [caps.ahk](https://github.com/alexantoshuk/kbdf/blob/master/caps.ahk) and [kbdf.ahk](https://github.com/alexantoshuk/kbdf/blob/master/kbdf.ahk) to autostart.

`kbdf.pyw` - translate last typed line, or selection if exists<br/>
`kbdf.pyw selection` - translate selected text only<br/>

<br/>

How it works
=============
Simple!

1) Backup current clipboard content.
2) Emit <kbd>ctrl+insert</kbd> to copy selection to clipboard.
3) If selection is not empty, go to (6).
4) Emit <kbd>shift+home</kbd> for line selection (if not in 'selection' mode).
5) Emit <kbd>ctrl+insert</kbd> to copy selection to clipboard.
6) Get clipboard content and translate text word by word.
7) Write translated text to clipboard.
8) Emit <kbd>shift+insert</kbd> to replace selection with clipboard content.
9) Restore clipboard content from backup.

<br/>

Limitations
============
* For now it can switch only between Russian and English keyboard layouts.
* It doesn't work in the terminal (except if terminal support to select line by <kbd>shift+home</kbd> and copy/paste by <kbd>ctrl+insert</kbd> <kbd>shift+insert</kbd>).
* Undefined behavior when bind this script to hotkeys with <kbd>super</kbd> and some other modifiers. I am just bind it to F12.

<br/>

Alternatives
============
The alternatives is much more functional. But goal of this project is simplicity, stability, work on Linux (Xorg and Wayland) and Windows. And in my opinion, automatic switching creates more problems than it solves, so in **kbdf** there is no such possibility.

[PuntoSwitcher (Windows only)](https://yandex.ru/soft/punto/)<br/>
[XNeur  (Linux only)](https://xneur.ru/)


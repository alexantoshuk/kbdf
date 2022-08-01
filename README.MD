KBDF
=========
**kbdf** is a simple python script to translate text that was typed accidentally in wrong keyboard layout.<br/>


Install
============
**kbdf** supports Python3 on Linux and Windows(not tested yet).<br/>
You can install it using pip:

`pip install git+https://github.com/alexantoshuk/kbdf`

Or manually download [kbdf.py](https://raw.githubusercontent.com/alexantoshuk/kbdf/master/scripts/kbdf.py) and make it executable:

`cmod +x kbdf.py`

...and install python dependencies:

`pip install pyautogui`<br/>
`pip install pyperclip`

Also Linux needs the `xclip` installed.


Example Usage
=============
You must bind it to some hotkey

`kbdf.py line` - translate last typed line, or selection if exists (default)<br/>
`kbdf.py selection` - translate selected text<br/>


How it works
=============
Simple!

1) Backup current clipboard content.
2) Emit <kbd>shift+home</kbd> for line selection (in 'line' mode only).
3) Emit <kbd>ctrl+c</kbd> to copy selection to clipboard.
4) Get clipboard content and translate text word by word.
5) Write translated text to clipboard.
6) Emit <kbd>ctrl+v</kbd> to replace selection with clipboard content.
7) Restore clipboard content from backup.


Limitations
============
* For now it can switch only between Russian and English keyboard layouts.
* It doesn't work in the terminal (except if terminal support to select line by <kbd>shift+home</kbd> and copy/paste by <kbd>ctrl+c</kbd> <kbd>ctrl+v</kbd>).
* Undefined behavior when bind this script to hotkeys with <kbd>super</kbd> modifier.


Alternatives
============
The alternatives is much more functional. But goal of this project is simplicity, stability, work on Linux and Windows. And in my opinion, automatic switching creates more problems than it solves, so in **kbdf** there is no such possibility.

[PuntoSwitcher (Windows only)](https://yandex.ru/soft/punto/)<br/>
[XNeur  (Linux only)](https://xneur.ru/)


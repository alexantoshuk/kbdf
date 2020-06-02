kbdf
=========
kbdf is a simple python script to translate text that was typed accidentally in wrong keyboard layout


Limitations
============
For now it can switch only between Russian and English keyboard layouts.
Not work in terminal (except if terminal support to select line by `shift+home` and copy/paste by `ctrl+c/ctrl+v`).

Install
============
kbdf supports Python 2 and 3.

You can install kbdf using pip:

`pip install git+https://github.com/alexantoshuk/kbdf`

Or manually download kbdf.py and make it executable:

`cmod +x kbdf.py`

...and install python dependencies:

`pip install pyautogui`

`pip install pyperclip`

Also Linux needs the xclip installed.


Example Usage
=============
You must bind it to some hotkey

`kbdf.py line` - translate last typed line (default)

`kbdf.py word` - translate last typed word

`kbdf.py selection` - translate selected text


How it works
=============
1) Backup current clipboard content.
2) Emit `shift+home` for line selection (in line/word mode).
3) Emit `ctrl+c` to copy selection to clipboard.
4) Get clipboard content and translate text word by word.
5) Write translated text to clipboard.
6) Emit `ctrl+v` to replace selection with clipboard content.
7) Restore clipboard from backup.

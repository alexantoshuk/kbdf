kbdf
=========

kbdf is a simple python script to translate text that was typed accidentally in wrong keyboard layout

Installation
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


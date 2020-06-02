kbdf
=========

kbdf is a simple python script to translate text that was typed accidentally in wrong keyboard layout

`pip install kbdf`


Source code available at https://github.com/alexantoshuk/kbdf


Dependencies
============

kbdf supports Python 2 and 3. If you are installing kbdf from PyPI using pip:

Windows has no dependencies.
Linux needs the xclip installed.

Example Usage
=============
You must bind it to some hotkey

`kbdf [Mode]`

Available modes:

`--line` - translate last typed line (default)

`--word` - translate last typed word

`--selection` - translate selected text


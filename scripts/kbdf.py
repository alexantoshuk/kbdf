#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Install:
    Install it with pip: pip install git+https://github.com/alexantoshuk/kbdf
    or manualy:
        Install dependency:
            pip install pyautogui
            pip install pyperclip
            Install 'xclip' on Linux
        Make kbdf.py executable on Linux:
            chmod +x kbdf.py

Usage:
    
    `kbdf.py line` - translate last typed line (default)

    `kbdf.py word` - translate last typed word

    `kbdf.py selection` - translate selected text
    
    Just bind it to some hotkey!

"""

import pyautogui
import pyperclip as clipboard
import time
import sys

EN = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?!@#$%^&"""
RU = """ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,!"№;%:?"""

EN_RU = str.maketrans(EN, RU)
RU_EN = str.maketrans(RU, EN)


def is_RU(word):
    chars = "ёйцукенгшщзхъфывапролджэячсмитьбю"
    for char in word.lower():
        if char in chars:
            return True
    return False


def up_modifiers():
    pyautogui.press(['ctrl'] * 2)
    # pyautogui.press(['alt']*2)
    pyautogui.press(['shift'] * 2)


def select_text():
    pyautogui.hotkey('shiftleft', 'home')
    time.sleep(0.05)


def get_selected_text():
    clipboard.copy("")
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)
    _text = clipboard.paste()
    return _text


def insert_text(text):
    clipboard.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.05)


def switch_keyboard_layout():
    pyautogui.hotkey('capslock')  # Change to your keyboard combo
    time.sleep(0.05)


def main(mode='line'):
    # save current clipboard content
    clipboard_backup = clipboard.paste()

    up_modifiers()

    _text = None
    if mode != 'selection':
        if mode == 'line':
            _text = get_selected_text()

        if not _text:
            select_text()

    if not _text:
        _text = get_selected_text()

    text = _text.rstrip(' ')
    trailing_spaces = len(_text) - len(text)

    if not text:
        # restore clipboard content
        clipboard.copy(clipboard_backup)
        return

    words = iter(text.split(" "))
    words = ["".join([" ", next(words)])
             if not w else w for w in words]
    if not words:
        # restore clipboard content
        clipboard.copy(clipboard_backup)
        return

    result = []
    if mode == 'word':
        result = words[:-1]
        words = words[-1:]

    for word in words:
        if is_RU(word):
            word = word.translate(RU_EN)
        else:
            word = word.translate(EN_RU)

        result.append(word)

    if trailing_spaces:
        result.append(" " * trailing_spaces)

    text = " ".join(result)

    insert_text(text)
    switch_keyboard_layout()

    # restore clipboard content
    clipboard.copy(clipboard_backup)


if __name__ == "__main__":
    mode = 'line'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    main(mode)

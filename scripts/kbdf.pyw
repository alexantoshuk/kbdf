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
    
    `kbdf.py line` - translate last typed line, or selection if exists (default)

    `kbdf.py selection` - translate selected text
    
    Just bind it to some hotkey!

"""

import pyautogui
import pyperclip as clipboard
import time
import sys
import platform

EN = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?!@#$%^&"""
RU = """ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,!"№;%:?"""
RU_CHARS = frozenset(RU[:33])

EN_RU = str.maketrans(EN, RU)
RU_EN = str.maketrans(RU, EN)

DELAY = 0.01


def is_RU(word):
    for char in word.lower():
        if char in RU_CHARS:
            return True
    return False


def release_modifiers():
    """
    Double press modifiers keys to prevent some strange bugs
    """
    pyautogui.press(['ctrl'] * 2)
    # pyautogui.press(['alt']*2)
    pyautogui.press(['shift'] * 2)


def select_text():
    pyautogui.hotkey('shift', 'shift', 'home')
    time.sleep(DELAY)


def get_selected_text():
    clipboard.copy('')  # empty clipboard
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(DELAY)
    return clipboard.paste()


def insert_text(text):
    clipboard.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(DELAY)


if platform.system() == 'Windows':
    def switch_keyboard_layout():
        # change it to your keyboard combo
        pyautogui.hotkey('altleft', 'shiftleft')
        time.sleep(DELAY)
else:
    def switch_keyboard_layout():
        pyautogui.hotkey('capslock')  # change it to your keyboard combo
        time.sleep(DELAY)


def translate(text):
    text_ = text.rstrip(' ')
    if not text_:
        return

    trailing_spaces_num = len(text) - len(text_)
    iwords = iter(text_.split(' '))
    words = [''.join([' ', next(iwords)]) if not w else w for w in iwords]

    if not words:
        return

    result = [word.translate(RU_EN) if is_RU(
        word) else word.translate(EN_RU) for word in words]

    if trailing_spaces_num:
        result.append(' ' * trailing_spaces_num)

    return ' '.join(result)


def main(mode='line'):
    clipboard_backup = clipboard.paste()  # save current clipboard content

    release_modifiers()

    text = get_selected_text()
    if (mode == 'line') and (not text):
        select_text()
        text = get_selected_text()

    translated_text = translate(text)
    if translated_text:
        insert_text(translated_text)
        switch_keyboard_layout()

    clipboard.copy(clipboard_backup)  # restore clipboard content


if __name__ == "__main__":
    mode = 'line'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    main(mode)

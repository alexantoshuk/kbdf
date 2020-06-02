#!python

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


EN = "`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
RU = "ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"

EN_RU = str.maketrans(EN, RU)
RU_EN = str.maketrans(RU, EN)


def is_RU(word):
    chars = "ёйцукенгшщзхъфывапролджэячсмитьбю"
    for char in word.lower():
        if char in chars:
            return True
    return False


def main(mode='line'):
    clipboard_backup = clipboard.paste()

    if mode != 'selection':
        pyautogui.hotkey('shiftleft', 'home')
        time.sleep(0.05)

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)
    _text = clipboard.paste()

    text = _text.rstrip(' ')
    trailing_spaces = len(_text) - len(text)

    if not text:
        clipboard.copy(clipboard_backup)
        return

    word_list = iter(text.split(" "))
    word_list = ["".join([" ", next(word_list)])
                 if not w else w for w in word_list]
    if not word_list:
        clipboard.copy(clipboard_backup)
        return

    result = []
    if mode == 'word':
        result = word_list[:-1]
        word_list = word_list[-1:]

    for word in word_list:
        if is_RU(word):
            word = word.translate(RU_EN)
        else:
            word = word.translate(EN_RU)

        result.append(word)

    if trailing_spaces:
        result.append(" "*trailing_spaces)

    text = " ".join(result)

    clipboard.copy(text)

    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.05)

    clipboard.copy(clipboard_backup)


if __name__ == "__main__":
    mode = 'line'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    main(mode)

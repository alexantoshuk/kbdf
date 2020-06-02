#!python

"""

Installation:
    Install it with pip: pip install git+https://github.com/alexantoshuk/kbdf
    or manualy:
        Install dependency:
            pip install pyautogui
            pip install pyperclip
            Install 'xclip' on Linux
    You can make it executable on Linux:
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


def main(mode='line'):
    clipboard_backup = clipboard.paste()

    if mode != 'selection':
        pyautogui.hotkey('shiftleft', 'home')

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)
    text = clipboard.paste()

    result = []
    splitted = text.split(" ")
    if not splitted:
        clipboard.copy(clipboard_backup)
        return

    if mode == 'word':
        result = splitted[:-1]
        splitted = splitted[-1:]

    for word in splitted:
        try:
            first = word[0]
        except:
            continue
        if first in EN:
            word = word.translate(EN_RU)
        elif first in RU:
            word = word.translate(RU_EN)

        result.append(word)

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

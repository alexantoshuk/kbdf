#!python

"""

Installation:
    Dependency:
        pip install pyautogui
        pip install pyperclip
        Install 'xclip' on Linux with your package manager
    Make it executable:
        chmod +x kbdf.py

Usage:
    python kbdf.py [args]
    args:
        --line: translate line (default)
        --word: translate word
        --selection: translate selected text
    
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

if __name__ == "__main__":
    arg = '--line'
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    clipboard_backup = clipboard.paste()

    if arg != '--selection':
        pyautogui.hotkey('shiftleft', 'home')

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.01)
    text = clipboard.paste()

    result = []
    for word in text.split(" "):
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
    time.sleep(0.01)

    clipboard.copy(clipboard_backup)

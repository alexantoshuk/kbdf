#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Install:
    Install it with pip: pip install git+https://github.com/alexantoshuk/kbdf
    or manualy:
        Install dependency:
            pip install pynput
            pip install pyperclip
            Install 'xclip' on Linux Xorg
            Install 'wl-clipboard' on Linux Wayland
        Make kbdf.py executable on Linux:
            chmod +x kbdf.py

Usage:

    `kbdf.py line` - translate last typed line, or selection if exists (default)

    `kbdf.py selection` - translate selected text

    Just bind it to some hotkey!

"""

import logging
import sys
import time

import pyperclip as clipboard
from pynput.keyboard import Controller, Key

from pathlib import Path

# logfile = str(Path.home().joinpath("kbdf.log"))
# logging.basicConfig(
#     filename=logfile,
#     filemode="a",
#     format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
#     datefmt="%H:%M:%S",
#     level=logging.DEBUG,
# )


EN = r"""`qwertyuiop[]asdfghjkl;'zxcvbnm,.~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>#&ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ№?"""
RU = r"""ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ№?`qwertyuiop[]asdfghjkl;'zxcvbnm,.~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>#&"""

EN_RU = str.maketrans(EN, RU)


DELAY = 0.05
KBD = Controller()


def release_modifiers():
    """
    Release modifiers keys to prevent some strange bugs
    #"""
    # KBD.release(Key.ctrl)
    # KBD.release(Key.ctrl)
    # time.sleep(DELAY)
    # KBD.release(Key.alt)
    # KBD.release(Key.alt)
    # time.sleep(DELAY)
    # KBD.release(Key.shift)
    # KBD.release(Key.shift)
    # time.sleep(DELAY)

    return


def select_text():
    with KBD.pressed(Key.shift):
        with KBD.pressed(Key.home):
            time.sleep(DELAY)
    time.sleep(DELAY)


def get_selected_text():
    clipboard.copy('')  # empty clipboard

    with KBD.pressed(Key.ctrl):
        with KBD.pressed(Key.insert):
            time.sleep(DELAY)
    time.sleep(DELAY)

    try:
        return clipboard.paste()
    except:
        return ''


def insert_text(text):
    clipboard.copy(text)

    with KBD.pressed(Key.shift):
        with KBD.pressed(Key.insert):
            time.sleep(DELAY)
    time.sleep(DELAY)


def switch_keyboard_layout():
    time.sleep(DELAY)
    with KBD.pressed(Key.caps_lock):  # change it to your keyboard combo
        time.sleep(DELAY)
    time.sleep(DELAY)
    return


def translate(text):
    if not text.strip():
        return text

    return text.translate(EN_RU)


def main(mode="line"):
    logging.debug("start")
    try:
        clipboard_backup = clipboard.paste()  # save current clipboard content
    except:
        clipboard_backup = ''

    logging.debug(f"clipboard_backup - '{clipboard_backup}'")
    release_modifiers()

    text = get_selected_text()
    logging.debug(f"get_selected_text - '{text}'")

    if (mode == "line") and (not text):
        select_text()
        text = get_selected_text()
        logging.debug(f"select_and_get_selected_text - '{text}'")

    translated_text = translate(text)
    logging.debug(f"translated_text - '{translated_text}'")

    if translated_text:
        insert_text(translated_text)
        switch_keyboard_layout()

    clipboard.copy(clipboard_backup)  # restore clipboard content
    logging.debug("end")


if __name__ == "__main__":
    mode = "line"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    main(mode)

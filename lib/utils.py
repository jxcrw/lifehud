#!/usr/bin/env python3
"""Misc utilities"""

import subprocess

from ahk import AHK

from cfg.config import DURATION_MS, EDITOR, FONT, FONT_SIZE, HEX_BG, ROWCOL


def underline(string: str) -> str:
    """Underline the specified string for display in terminal."""
    string = "\033[4m" + string + "\033[0m"
    return string


def toast(message: str, hex_color: str) -> None:
    """Display a toast message."""
    ahk = AHK()
    script = f'''
        SplashImage,, B1 FS{FONT_SIZE} CW{HEX_BG} CT{hex_color}, {message},,, {FONT}
        Sleep, {DURATION_MS}
        SplashImage
        SplashImage, Off
    '''
    ahk.run_script(script)


def autoopen(path: str) -> None:
    """Open the specified path in the configured text editor."""
    subprocess.run([EDITOR, f'{path}{ROWCOL}'])

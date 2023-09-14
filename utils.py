#!/usr/bin/env python3
"""Random utilities"""

from ahk import AHK

from _cfg.config import COLOR_BG


def underline(string: str) -> str:
    """Underline given string for display in terminal."""
    string = "\033[4m" + string + "\033[0m"
    return string


def toast(message: str, color: str) -> None:
    """Display a toast message."""
    ahk = AHK()
    script = f'''
        SplashImage,, B1 FS12 CW{COLOR_BG} CT{color}, {message},,, Consolas
        Sleep, 3000
        SplashImage
        SplashImage, Off
    '''
    ahk.run_script(script)

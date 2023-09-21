#!/usr/bin/env python3
"""Misc utilities"""

import subprocess
import time

from ahk import AHK

from cfg.config import COLOR_BG


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


def sync_anki() -> None:
    """Sync the Anki database by opening and closing Anki."""
    subprocess.run(['anki.cmd'])
    time.sleep(30)
    ahk = AHK()
    script = '''
        winTitle := "ahk_exe anki.exe"
        if WinExist(winTitle) {
            WinClose
        }
    '''
    ahk.run_script(script)
    time.sleep(5)


if __name__ == '__main__':
    sync_anki()

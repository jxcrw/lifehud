#!/usr/bin/env python3
"""Sync Anki database by opening and closing Anki"""

import subprocess
import time

from ahk import AHK


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


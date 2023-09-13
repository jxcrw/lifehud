#!/usr/bin/env python3
"""Random utilities"""

def underline(string: str) -> str:
    """Underline given string for display in terminal."""
    string = "\033[4m" + string + "\033[0m"
    return string

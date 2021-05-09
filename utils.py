import sys


def is_linux():
    # 1 for Linux and 0 for Windows
    return sys.platform == 'linux'

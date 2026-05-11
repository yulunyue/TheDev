import pygetwindow as gw
import ctypes
import win32gui
import re
import sys
import ctypes
from ctypes import wintypes
import win32process
import os
import _thread
import time

kernel32 = ctypes.windll.kernel32

mk_file_time = 0


def update():
    global mk_file_time
    cur_time = os.path.getmtime("a.txt")
    if cur_time != mk_file_time:
        with open("a.txt", "r") as f:
            ctypes.windll.kernel32.SetConsoleTitleW(f.read())
        mk_file_time = cur_time


def run():
    ctypes.windll.kernel32.SetConsoleTitleW("aa")
    input("xx")
    _thread.start_new_thread(os.system, ("opencode",))
    while True:
        update()
        time.sleep(2)


if __name__ == "__main__":
    run()

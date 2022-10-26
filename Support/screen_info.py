#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3

"""module to set variables related to window dimensions and icons
    should be imported as
    import screen_info as scr
"""
# pylint disables
    #pylint:disable=redefined-builtin
    #pylint:disable=unused-import

if "imports":

    import sys
    import os
    import screeninfo

    import rich
    from rich import print
    from rich import inspect
    from rich.console import Console
    import PySide6.QtCore as C

    console = Console()

if __name__ == '__main__':
    console.clear()
    print("screen_info.py - [red]Not for solo run\n")
    sys.exit()

if "screeninfo":
    """The following variables can be used to position PySide6 windows in different monitors"""
    # https://doc.qt.io/qt-6/qscreen.html
    # https://pypi.org/project/screeninfo/

    if "set default window dimensiones globally,  for any project,  on any system":
        """
        Following calculates a default postion for windows and dependent message boxes, depending on current screen size(s).
        Adjusts for dual (identical) monitors,  if present ...
        """
        screen_number = 0
        for monitor in screeninfo.get_monitors():
            #print(monitor)
            screen_number = screen_number + 1

        if "get screen dimensions":
            screen_width = int(screeninfo.get_monitors()[0].width)
            screen_height = int(screeninfo.get_monitors()[0].height)

        if "calculate window dimensions based on screen dimensions":
            win_width = int(screen_width*0.75)
            win_height = int(screen_height*.80)

        if "calculate window margins based on window dimensions":
            win_top_margin = int((screen_height - win_height)/2)
            win_left_margin = int((screen_width - win_width)/2)

        if "adjust for second monitor,  if present":
            """assumes dual monitors are equal, putting default windows on second screen"""
            if screen_number > 1:
                win_left_margin = screen_width + win_left_margin

        #C.QRect(x, y, w, h)
        window_rect = C.QRect(win_left_margin, win_top_margin, win_width, win_height)

        msg_box_height = 300
        msg_box_width = 400
        _x = win_left_margin + (win_width - msg_box_width)/2
        _y = win_top_margin + (win_height - msg_box_height)/2
        msg_box_rect = C.QRect(_x, _y, msg_box_height, msg_box_width)

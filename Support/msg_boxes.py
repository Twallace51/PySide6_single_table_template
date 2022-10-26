#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3

"""customized QMessageBox instances

   see msg_boxes.md for custom styling and other options

   Note:  this module can run solo to test default instances.
"""

# pylint disables
    #pylint:disable=redefined-builtin
    #pylint:disable=unused-import
    #pylint:disable=missing-function-docstring

if "imports":
    import sys

    try:
        from dev_tools import log, print, console, inspect, bp
        import screen_info as scr
    except ModuleNotFoundError:
        from Support.dev_tools import log, print, console, inspect, bp
        import Support.screen_info as scr

    import PySide6.QtWidgets as W

if __name__ == '__main__':
    console.clear()
    print("msg_boxes.py - [red]Not for solo run\n")
    sys.exit()

if "my QMessagesBoxes":

    q_message_width = 220 # Window Title width sets whole widget width

    def notify(message="Falta mensaje!"):

        msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        msg_box.setWindowTitle("Notification:".ljust(q_message_width))

        msg_box.setText(F'<h2> {message} </h2>')

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Information)
        msg_box.setGeometry(scr.msg_box_rect)

        msg_box.exec()

    def invalid_input(message="Invalid Input!"):

        msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        msg_box.setWindowTitle("Invalid Input:".ljust(q_message_width))

        msg_box.setText(F'<h2 style="color: orange;"> {message} </h2>')

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Information)
        msg_box.setGeometry(scr.msg_box_rect)

        msg_box.exec()

    def pending(message="Under development ....."):

        msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        msg_box.setWindowTitle("Pending:".ljust(q_message_width))

        msg_box.setText(F'<h2 style="color: purple;"> {message} </h2>')

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Information)
        msg_box.setGeometry(scr.msg_box_rect)

        msg_box.exec()

    def confirm(title="Confirmation:", options="Click [Ok] to proceed or [Cancel]"):
        """Confirm or cancel operation - returns True or False"""
        msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        msg_box.setWindowTitle(title.ljust(q_message_width))

        msg_box.setText(F'<h2 style="color: green;"> {options} </h2>')

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.addButton(W.QMessageBox.Cancel)
        msg_box.setIcon(W.QMessageBox.Question)
        msg_box.setGeometry(scr.msg_box_rect)

        if msg_box.exec() == W.QMessageBox.StandardButton.Ok:
            return True
        return False

    def warning(message="... Missing Warning Details ..."):

        msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        msg_box.setWindowTitle("WARNING:".ljust(q_message_width))

        msg_box.setText(F'<h2 style="color: red;"> CUIDADO:  {message}</h2>')  # HTML using CSS formating

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Warning)
        msg_box.setGeometry(scr.msg_box_rect)

        msg_box.exec()

    def unauthorized(current_user_="Guest"):
        """typically used to notify a user that tries to select an restricted operation,
        for example,   administrative functions"""
        msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        msg_box.setWindowTitle("Unauthorized:".ljust(q_message_width))

        msg1 = F"As    {current_user_},     you do not have authorization for this option"
        msg_box.setText(F'<h2 style="color: blue;"> {msg1} </h2>')  # HTML using CSS format

        msg_box.addButton(W.QMessageBox.Ok)
        msg_box.setIcon(W.QMessageBox.Warning)
        msg_box.setGeometry(scr.msg_box_rect)

        msg_box.exec()

if __name__ == '__main__':

    if "start pyside6 application loop":
        app = W.QApplication()
        console.clear()

    if "top level Widget":
        widget_win = W.QWidget()
        widget_win.setWindowTitle("Toplevel QWidget instance,   an empty system window")
        scr.window_rect.adjust(0, 300, 0, 0)
        widget_win.setGeometry(scr.window_rect)
        widget_win.show()

    if "succesive window adjustments":
        scr.msg_box_rect.adjust(0, -200, 0, 0)
        down = 80
        right = 50

    if "demos":
        #p ylint: disable=undefined-variable
        methods = (
            notify,
            invalid_input,
            pending,
            confirm,
            warning,
            unauthorized,
        )
        for method in methods:
            method()
            scr.msg_box_rect.adjust(right, down, 0, 0)

        sys.exit(0)

    if "start app loop":
        app.exec()

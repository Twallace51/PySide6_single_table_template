#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3

"""This is a PySide6 template/demo<p>
  - that can be used to manage a single table database<p>
  - in an office environment<p><p>
  For details - See README.md file
"""

"""Developers note:
- use folding (VSCodium editor) to collapse all following sections,  to see overall structure of this file
- pylint section
  enable/disable as needed during development to look for code and style errors
  section can be deleted in final
"""
    #p ylint:disable=bare-except
    #p ylint:disable=eval-used
    #p ylint:disable=import-error
    #p ylint:disable=invalid-name
    #p ylint:disable=missing-class-docstring
    #p ylint:disable=missing-function-docstring, empty-docstring
    #p ylint:disable=no-member
    #pylint:disable=no-name-in-module
    #p ylint:disable=undefined-variable
    #p ylint:disable=unspecified-encoding
    #p ylint:disable=unused-argument
    #pylint:disable=unused-import
    #pylint:disable=unused-wildcard-import
    #pylint:disable=redefined-builtin
    #pylint:disable=wildcard-import

if "imports":

    import sys
    import os

    # make sure Support folder available - for details see Support/README.md
    if not os.path.isdir(F"{os.getcwd()}/Support"):
        print("/Support  folder was not found!!")
        sys.exit()

    import Support.check_environ               #  optional - checks if assumed base environment is available, makes certain initializations
    import Support.screen_info as scr          #  automatically resizes default window relative to dimensions/number of monitor(s)
    import Support.msg_boxes as mbx            #  customized convenience versions of QMessageBox
    from Support.db_methods import *           #  generic wrappers for sqlite SELECT, INSERT, UPDATE commands
    from Support.dev_tools import bp, inspect, console, log, print   # customized development tools

    import webbrowser
    import subprocess
    import configparser
    import datetime
    from shutil import copyfile

    import PySide6.QtWidgets      as W
    import PySide6.QtCore         as C
    import PySide6.QtGui          as G
    import PySide6.QtPrintSupport as P
    import PySide6.QtSql          as S
    from PySide6.QtCore           import Qt
    from Support.Windows import prj, win, icn   # these are global namespaces, created by and used in Support/Windows and LoginMenu classes
    from Support.Windows import WindowsNewForm, WindowsUpdateForm, WindowsFormList, WindowsFilterForm, WindowsList, PrintPreview, PrintScreen
    from Support.LoginMenus import LoginMenu, PasswordEditor, LoginDialog

# Pacientes classes

class PteMenus():
    """this class adds project menus to MenuWindow """
    def __init__(self):

        # QActions

        self.open_new_form_act = G.QAction()
        self.open_new_form_act.setText("New Record Form")
        self.open_new_form_act.setIcon(icn.default_icon)
        self.open_new_form_act.triggered.connect(self.open_new_form_handler)

        self.formlist_win_act = G.QAction()
        self.formlist_win_act.setText("Form List Window")
        self.formlist_win_act.setIcon(icn.default_icon)
        self.formlist_win_act.triggered.connect(self.formlist_win_handler)

        self.filter_form_act = G.QAction()
        self.filter_form_act.setText("Filter Form")
        self.filter_form_act.setIcon(icn.default_icon)
        self.filter_form_act.triggered.connect(self.filter_form_handler)

        # update menubar

        self.demos_mnu = W.QMenu("&Demos")
        self.menu_mbr.addMenu(self.demos_mnu)
        self.demos_mnu.addAction(self.open_new_form_act)
        self.demos_mnu.addAction(self.formlist_win_act)
        self.demos_mnu.addAction(self.filter_form_act)

    # handlers

    def open_new_form_handler(self):
        if prj.current_user_name not in ["Admin", "Root"]:
            mbx.unauthorized(prj.current_user_name)
        else:
            self.next_win_handler(prj.new_form_demo)

    def filter_form_handler(self):
        self.next_win_handler(prj.filter_form_demo)

    def formlist_win_handler(self):
        self.next_win_handler(prj.form_list_demo)

class PteFields():
    """adds project data fields to Form windows"""

    def __init__(self):
        self.id_lbl =         W.QLabel("id")
        self.nombres_lbl =    W.QLabel("nombres")
        self.paterno_lbl =    W.QLabel("paterno")
        self.materno_lbl =    W.QLabel("materno")
        self.cumpleanos_lbl = W.QLabel("cumpleanos")
        self.carnet_lbl =     W.QLabel("carnet")
        self.ultima_lbl =     W.QLabel("ultima visita")

        self.id_led =         W.QLineEdit()
        self.nombres_led =    W.QLineEdit()
        self.paterno_led =    W.QLineEdit()
        self.materno_led =    W.QLineEdit()
        self.cumpleanos_led = W.QLineEdit()
        self.carnet_led =     W.QLineEdit()
        self.ultima_led =     W.QLineEdit()

        self.form_grid_layout.addWidget(self.id_lbl,         1, 0)
        self.form_grid_layout.addWidget(self.nombres_lbl,    2, 0)
        self.form_grid_layout.addWidget(self.paterno_lbl,    3, 0)
        self.form_grid_layout.addWidget(self.materno_lbl,    4, 0)
        self.form_grid_layout.addWidget(self.cumpleanos_lbl, 5, 0)
        self.form_grid_layout.addWidget(self.carnet_lbl,     6, 0)
        self.form_grid_layout.addWidget(self.ultima_lbl,     7, 0)

        self.form_grid_layout.addWidget(self.id_led,         1, 1)
        self.form_grid_layout.addWidget(self.nombres_led,    2, 1)
        self.form_grid_layout.addWidget(self.paterno_led,    3, 1)
        self.form_grid_layout.addWidget(self.materno_led,    4, 1)
        self.form_grid_layout.addWidget(self.cumpleanos_led, 5, 1)
        self.form_grid_layout.addWidget(self.carnet_led,     6, 1)
        self.form_grid_layout.addWidget(self.ultima_led,     7, 1)

        self.form_grid_layout.setColumnStretch(2, 1000)

        self.id_led.setFixedWidth(40)
        self.nombres_led.setFixedWidth(200)
        self.paterno_led.setFixedWidth(120)
        self.materno_led.setFixedWidth(120)
        self.cumpleanos_led.setFixedWidth(80)
        self.carnet_led.setFixedWidth(80)
        self.ultima_led.setFixedWidth(80)

        self.cal01 = W.QCalendarWidget()
        self.cal01.setLocale(C.QLocale.Spanish)
        self.cal01.setFixedWidth(500)
        self.cal01.hide()
        self.form_grid_layout.addWidget(self.cal01, 8, 1)

        self.cal01.selectionChanged.connect(self.pte_update_ultima_handler)
        self.cal01.clicked.connect(self.pte_update_ultima_handler)

        self.form_fields_lst =  [
            self.id_led,
            self.nombres_led,
            self.paterno_led,
            self.materno_led,
            self.cumpleanos_led,
            self.carnet_led,
            self.ultima_led
            ]

    # -----------------------------------------------------------

    def pte_update_ultima_handler(self):
        self.ultima_led.setText(self.cal01.selectedDate().toString(Qt.ISODate))
        self.cal01.setVisible(False)

    def set_form_fields_to_default_values(self):
        self.id_led.setText("")
        self.nombres_led.setText("")
        self.paterno_led.setText("")
        self.materno_led.setText("")
        self.cumpleanos_led.setText("")
        self.carnet_led.setText("")
        self.ultima_led.setText("")

    def pte_set_fields_to_current_record(self, record):
        self.id_led.setText(str(record.value(0)))
        self.nombres_led.setText(record.value(1))
        self.paterno_led.setText(record.value(2))
        self.materno_led.setText(record.value(3))
        self.cumpleanos_led.setText(record.value(4))
        self.carnet_led.setText(record.value(5))
        self.ultima_led.setText(record.value(6))

    def pte_update_filters(self):
        """Note: following searches for matches only from begining of field strings """
        _tmp = ""
        _str = self.id_led.text().strip()
        if _str:
            _tmp = F"id = {int(self.id_led.text())}"

        _str = self.nombres_led.text().strip()
        if _str:
            if _tmp:
                _tmp += F"AND nombres LIKE '{_str}%'"
            else:
                _tmp += F"nombres LIKE '{_str}%'"

        _str = self.paterno_led.text().strip()
        if _str:
            if _tmp:
                _tmp += F"AND paterno LIKE '{_str}%'"
            else:
                _tmp += F"paterno LIKE '{_str}%'"

        _str =  self.materno_led.text().strip()
        if _str:
            if _tmp:
                _tmp += F"AND materno LIKE '{_str}%'"
            else:
                _tmp += F"materno LIKE '{_str}%'"

        _str = self.cumpleanos_led.text().strip()
        if _str:
            if _tmp:
                _tmp += F"AND cumpleanos LIKE '{_str}%'"
            else:
                _tmp += F"cumpleanos LIKE '{_str}%'"

        _str = self.carnet_led.text().strip()
        if _str:
            if _tmp:
                _tmp += F"AND carnet LIKE '{_str}%'"
            else:
                _tmp += F"carnet LIKE '{_str}%'"

        _str = self.ultima_led.text().strip()
        if _str:
            if _tmp:
                _tmp += F"AND ultima LIKE '{_str}%'"
            else:
                _tmp += F"ultima LIKE '{_str}%'"

        return _tmp

class PteQueries():
    """Provides methods using SQL to
    - check if entered data is acceptable
    - insert data to database
    - update a record with new data
    - delete a record
    """
    def __init__(self):
        self.table_fields_str = "id, nombres, paterno, materno, cumpleanos, carnet, ultima"  # include all table fields
        self.table_name = "Pacientes"

    def data_is_valid(self):
        if self.paterno_led.text().strip():  # paterno input is required
            return True
        else:
            mbx.warning("Insert canceled - paternal name missing")
        return False

    def insert_handler(self):

        if self.data_is_valid():
            insert_values_str = F"\
                NULL,\
                '{self.nombres_led.text()}',\
                '{self.paterno_led.text()}',\
                '{self.materno_led.text()}',\
                '{self.cumpleanos_led.text()}',\
                '{self.carnet_led.text()}',\
                '{self.ultima_led.text()}' "

            insert_str = F"INSERT INTO Pacientes ({self.table_fields_str}) VALUES ({insert_values_str})"
            query = run_insert(insert_str, not "verbose")
            if query:
                mbx.notify("Insert successful")
                self.previous_win_handler()
            else:
                mbx.warning("Insert UNsuccessful")

    def delete_handler(self):
        if prj.current_user_name not in ["Root"]:
            mbx.unauthorized(prj.current_user_name)
            return
        if mbx.confirm("Confirm?"):
            delete_str = F"DELETE FROM Pacientes WHERE  id = {int(self.id_led.text())}"
            query = run_delete(delete_str, not "verbose")
            if query:
                mbx.notify("Record deleted")
                self.previous_win_handler()
                return
        mbx.warning("Record NOT deleted")

    def update_handler(self):
        if self.data_is_valid():
            update_str = F"UPDATE {self.table_name} SET\
                nombres = '{self.nombres_led.text()}',\
                paterno = '{self.paterno_led.text()}',\
                materno = '{self.materno_led.text()}',\
                cumpleanos = '{self.cumpleanos_led.text()}', \
                carnet = '{self.carnet_led.text()}',\
                ultima = '{self.ultima_led.text()}'\
                WHERE id = {int(self.id_led.text())}"
            query = run_update(update_str, not "verbose")
            if query:
                mbx.notify("Update saved")
                self.previous_win_handler()
            else:
                mbx.warning("Update NOT saved")

# demo window classes

class LoginMenuDemo(LoginMenu, PteMenus):
    """Demo window based on Windows.LoginMenu class
    for managing a simple database"""
    def __init__(self):
        LoginMenu.__init__(self)
        PteMenus.__init__(self)

        # update root menu

        self.backup_db_act = G.QAction("Respaldar database")
        self.backup_db_act.setIcon(G.QIcon("Support/icons/system-help.png"))
        self.backup_db_act.triggered.connect(self.backup_db_handler)
        self.root_mnu.addAction(self.backup_db_act)

    def backup_db_handler(self):
        """Note:  copyfile() silently overwites any prexisting file with same name"""
        try:
            os.mkdir("db_backups")
        except FileExistsError:
            ...
        src = "archivos.db"
        dest = F"db_backups/archivos_{str(datetime.date.today())}.db"
        copyfile(src, dest)
        mbx.notify(F"COPIED - archivos.db copied to \n{dest}")

class NewFormDemo(PteQueries, PteFields, WindowsNewForm):
    """Window with an empty form to accept data for a new Paciente record"""
    def __init__(self):
        WindowsNewForm.__init__(self) # order is important for inheritance
        PteFields.__init__(self)
        PteQueries.__init__(self)

        self.id_led.setVisible(False)

        for field in iter(self.form_fields_lst):
            field.installEventFilter(self)

    def eventFilter(self, obj, event):

        if obj in self.form_fields_lst and event.type() is C.QEvent.ShortcutOverride:
            self.set_toolbar_to_edit_mode()
            self.cal01.setVisible(False)

        if obj is self.ultima_led and event.type() is C.QEvent.MouseButtonRelease:
            self.set_toolbar_to_edit_mode()
            self.ultima_led.setText(str(datetime.date.today()))
            self.cal01.setVisible(True)

        return False

    def showEvent(self, event):
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()
        self.cal01.setVisible(False)

    def cancel_handler(self):
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()

    def about_win_handler(self):
        mbx.notify(self.__doc__)

class UpdateFormDemo(PteQueries, PteFields, WindowsUpdateForm, PrintScreen):
    """Window to show a record,  with options to update or delete record"""
    def __init__(self):
        WindowsUpdateForm.__init__(self)
        PteFields.__init__(self)
        PteQueries.__init__(self)
        PrintScreen.__init__(self)

        self.id_led.setEnabled(False)

        for field in iter(self.form_fields_lst):
            field.installEventFilter(self)

    def undo_handler(self):
        mbx.notify("New data discarded")
        self.pte_set_fields_to_current_record(prj.current_record)
        self.set_toolbar_to_default_mode()

    def eventFilter(self, obj, event):
        if obj in self.form_fields_lst and event.type() is C.QEvent.ShortcutOverride:
            if prj.current_user_name not in ["Root", "Admin"]:
                mbx.unauthorized(prj.current_user_name)
                return False
            self.set_toolbar_to_edit_mode()

        if obj is self.ultima_led and event.type() is C.QEvent.MouseButtonRelease:
            if prj.current_user_name not in ["Root", "Admin"]:
                mbx.unauthorized(prj.current_user_name)
                return False
            self.set_toolbar_to_edit_mode()
            self.cal01.setVisible(True)

        return False

    def showEvent(self, event):
        self.pte_set_fields_to_current_record(prj.current_record)
        self.set_toolbar_to_default_mode()

    def about_win_handler(self):
        mbx.notify(self.__doc__)

class FormListWindowDemo(PteFields, WindowsFormList):
    """A dual Form and List Window <p>
    to display a list of records, <p>
    filtered by contents of the form fields"""
    def __init__(self):
        WindowsFormList.__init__(self)
        PteFields.__init__(self)

        for field in iter(self.form_fields_lst):
            field.installEventFilter(self)

    def eventFilter(self, obj, event):

        if obj in self.form_fields_lst and event.type() is C.QEvent.KeyRelease:
            self.remove_filter_act.setEnabled(True)
            self.cal01.setVisible(False)
            self.update_list_widget("Pacientes", self.pte_update_filters(), [], [50, 300], not "verbose")

        if obj is self.ultima_led and event.type() is C.QEvent.MouseButtonRelease:
            self.cal01.setVisible(True)

        return False

    def showEvent(self, event):
        self.cal01.setVisible(False)
        self.set_form_fields_to_default_values()
        self.update_list_widget("Pacientes", "", None, [50, 300], not "verbose")
        self.set_toolbar_to_default_mode()
        self.remove_filter_handler()

    # handlers

    def remove_filter_handler(self):
        self.update_list_widget("Pacientes", "", None, [50, 300], not "verbose")
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()

    def list_widget_click_handler(self, row, col):
        pte_id = self.list_widget.item(row, 0).text()
        prj.current_record = run_select(F"SELECT * FROM Pacientes WHERE id = {pte_id}")
        self.next_win_handler(prj.update_form_demo)

    def open_new_form_handler(self):
        if prj.current_user_name not in ["Admin", "Root"]:
            mbx.unauthorized(prj.current_user_name)
        else:
            self.next_win_handler(prj.new_form_demo)

    def pte_update_ultima_handler(self):
        self.ultima_led.setText(self.cal01.selectedDate().toString(Qt.ISODate))
        self.cal01.setVisible(False)
        self.remove_filters_act.setEnabled(True)
        self.update_list_widget("Pacientes", self.pte_update_filters(), None, [50, 300], not "verbose")
        self.set_toolbar_to_edit_mode()

    def about_win_handler(self):
        mbx.notify(self.__doc__)

class FilterFormDemo(PteFields, WindowsFilterForm):
    """FilterFormWindow to accept full or partial data in fields,<p>
    then used to generate a filter string for database """
    def __init__(self):
        WindowsFilterForm.__init__(self)
        PteFields.__init__(self)
        self.form_widget_header.setText("Enter first letters of item to search for")
        for field in iter(self.form_fields_lst):
            field.installEventFilter(self)

        self.set_toolbar_to_default_mode()
        self.showEvent = self.show_event_handler

    def eventFilter(self, obj, event):

        if obj in self.form_fields_lst and event.type() in [C.QEvent.MouseButtonRelease, C.QEvent.KeyRelease]:
            self.cal01.setVisible(False)
            self.set_toolbar_to_edit_mode()

        if obj is self.ultima_led and event.type() is C.QEvent.MouseButtonRelease:
            self.cal01.setVisible(True)
            self.set_toolbar_to_edit_mode()

        return False

    # handlers

    def cancel_handler(self):
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()

    def show_event_handler(self, event):
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()

    def remove_filter_handler(self):
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()

    def run_filter_handler(self):
        prj.filter_str = self.pte_update_filters()
        self.next_win_handler(prj.list_window_demo)

    def about_win_handler(self):
        mbx.notify(self.__doc__)

class ListWindowDemo(WindowsList, PrintPreview):
    """Window to show a list of (possibly filtered) records<p>
     with option to preview/print list as a document"""
    def __init__(self):
        WindowsList.__init__(self)
        PrintPreview.__init__(self)

        self.tool_bar.addAction(self.print_preview_act)
        self.run_filter_act.setVisible(False)

    def generate_doc(self):
        document = G.QTextDocument()
        cursor = G.QTextCursor(document)

        # QText formats

        empty_block = G.QTextBlockFormat()

        char_format = G.QTextCharFormat()
        char_format.setFont(G.QFont("Helvitica", 10))

        block_format = G.QTextBlockFormat()
        block_format.setAlignment(Qt.AlignLeft)

        block_format_right = G.QTextBlockFormat()
        block_format_right.setAlignment(Qt.AlignRight)

        # header block

        cursor.insertText(F"Filtered list with {prj.filter_str}", char_format)
        cursor.insertBlock(empty_block)
        cursor.insertBlock(empty_block)

        # QTextTable formating

        table_format = G.QTextTableFormat()
        table_format.setCellPadding(0)
        table_format.setCellSpacing(1)

        table_format.setBorderStyle(G.QTextTableFormat.BorderStyle_None)
        table_format.setHeaderRowCount(0)
        table_format.setAlignment(Qt.AlignLeft)

        constraints = [
            G.QTextLength(G.QTextLength.PercentageLength, 6),
            G.QTextLength(G.QTextLength.PercentageLength, 20),
            G.QTextLength(G.QTextLength.PercentageLength, 12),
            G.QTextLength(G.QTextLength.PercentageLength, 12),
            G.QTextLength(G.QTextLength.PercentageLength, 14),
            G.QTextLength(G.QTextLength.PercentageLength, 14),
            G.QTextLength(G.QTextLength.PercentageLength, 14),
            ]

        table_format.setColumnWidthConstraints(constraints)

        # create QTextTable

        rows = self.list_widget.rowCount()
        cols = self.list_widget.columnCount()
        table = cursor.insertTable(rows, cols, table_format)  # pylint: disable = unused-variable
        cursor.setCharFormat(char_format)

        # insert data to table

        for row in range(rows):
            for col in range(cols):
                cursor.insertText(self.list_widget.item(row, col).text())
                cursor.movePosition(G.QTextCursor.NextCell)

        return document

    def showEvent(self, event):
        table_name = "Pacientes"
        table_fields_lst = None
        table_fields_width_lst = [50, 300]
        self.update_list_widget(table_name, prj.filter_str, table_fields_lst, table_fields_width_lst, not "verbose")

    def about_win_handler(self):
        mbx.notify(self.__doc__)

if "setStyleSheet for project":
    # https://doc.qt.io/qtforpython/overviews/stylesheet-reference.html
    # https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html

    # TODO consider setting font-size based on current screen size

    global_style = (
        "QLabel {"
        " font-family: Times; "
        " font-size: 20px;"
        "}"
        "QLineEdit {"
        " font-family: Times;"
        " font-size: 16px;"
        " selection-background-color: blue;"
        " selection-color: green;"
        "}")

    ''' equivalent alternative uses a qss file instead
        with open('styles.qss', 'r', encoding='UTF-8') as f:
            style = f.read()
    '''

if "start pyside6 application":

    app = W.QApplication()
    app.setStyleSheet(global_style)

    mbx.notify(__doc__)

    # open demo database

    #log.debug("database opening")
    open_database("archivos.db", not "verbose")  # update to `True` or `"verbose"` for terminal output

    # create project windows

    prj.update_form_demo = UpdateFormDemo()
    prj.list_window_demo = ListWindowDemo()
    prj.form_list_demo = FormListWindowDemo()
    prj.filter_form_demo = FilterFormDemo()
    prj.new_form_demo = NewFormDemo()

    # open main menu

    win.password_editor_win = PasswordEditor()
    win.login_dialog = LoginDialog()

    prj.main_menu_demo = LoginMenuDemo()
    prj.main_menu_demo.show()

    # set auto logout time

    prj.auto_logout_seconds = float(300)

    # start app loop

    app.exec()

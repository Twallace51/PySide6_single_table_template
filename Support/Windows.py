#!/usr/bin/env python3              #pylint: disable=invalid-name
# -*- coding: utf-8 -*-
# cython: language_level=3

"""[green]Description[black]

 This module tries to provide a better alternative to using QMenuWindow<p>
 for developing windows in a large project, including menus, lists, forms and formlist windows.<p>
<p>
 The following classes provide a framework for various types of windows for any project.<p>
 A specific project will use instances of these classes,<p>
 plus code to add content and handle events, database records and reports.
<p>
 It assumes a locally available Support folder is available, with the correct files and images.<p>
 See [Support/README.md](Support/README.md) file for details.<p>
<p>
It is also an example of how to avoid monolithic code, hard to read and debug, by using<p>
- python classes to avoid duplicate code<p>
- code blocks to identify related code<p>
<p>
 Finally, this module was written in a style that assumes use of an editor with code folding (VSCodium recommended)<p>
 Collapse all folds to see what is effectively a table of contents for this module.
"""
# following section is for debugging using pylint,   and can be deleted in final version.

#pylint:disable=empty-docstring, missing-function-docstring, missing-class-docstring, useless-suppression
#pylint:disable=unused-import, redefined-builtin
#pylint:disable=unused-argument, unused-variable

if "imports":
    import sys
    try:
        from Support.dev_tools import bp, log, print, console, inspect
    except ModuleNotFoundError:  # in case this module run solo
        from dev_tools import bp, log, print, console, inspect

if __name__ == '__main__':
    console.clear()
    print(__doc__)
    print("\n[red]Windows.py module NOT written to be run alone\n")
    sys.exit()

if "more imports":

    from types import SimpleNamespace
    import os
    import subprocess

    try:                                     # where $pwd == project folder
        import Support.screen_info as scr
        import Support.msg_boxes as mbx
        from Support.db_methods import run_select
    except ModuleNotFoundError:              # where used locally in Support folder
        import screen_info as scr
        import msg_boxes as mbx
        from db_methods import run_select

    import PySide6.QtWidgets as W
    import PySide6.QtCore as C
    import PySide6.QtGui as G
    import PySide6.QtPrintSupport as P
    from PySide6.QtCore import Qt           #pylint:disable=no-name-in-module

if "create global namespaces":
    prj = SimpleNamespace()
    win = SimpleNamespace()
    icn = SimpleNamespace()

if "set default fonts":
    prj.serifFont = G.QFont("Times", 16)
    prj.serifFontBold = G.QFont("Times", 16, G.QFont.Bold)

if "security":
    prj.current_user_name = "Guest"  # default user name

    def current_user_is(permitted_user_list=[]):   #pylint:disable=dangerous-default-value
        """used to limit access to listed users"""
        if prj.current_user_name in permitted_user_list:
            return True   # authorized to continue
        else:
            mbx.unauthorized(prj.current_user_name)
        return False      # cancel continuing

if "locale":
    import locale
    prj.locale = locale.getlocale()[0][0:2]     # for LANG prefix [es, en , ...]

if "images":
    prj.images_folder = F"{os.getcwd()}/Support/images"

class WinStack():
    """window navigation handler provides
     a stack for object addresses of all windows created in a project,  where all are automatically hidden except for the last
     previous_win_handler() method to easily close current and show previous window
     next_win_handler(window) method to open a new window and hide previous
    """
    def __init__(self):
        icn.previous_win = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/go-previous.png")
        win.win_stack = [] # current window stack - must be in project scope namespace to work

        if "previous window action":  # see corresponding handler note below """
            self.previous_win_act = G.QAction()
            self.previous_win_act.setIcon(icn.previous_win)
            self.previous_win_act.setText({'en':'Previous Window',
                                           'es':'Ventana Previa'}[prj.locale])
            self.previous_win_act.triggered.connect(self.previous_win_handler)

    def previous_win_handler(self):
        """The .pop().show()  statement below will automatically return to and open previous window on win_stack"""
        try:
            #log.debug(F"\nBefore pop \nwindow stack (top is latest window)\n{win.win_stack}")
            win.win_stack.pop().show()
            #log.debug(F"\nAfter pop\n window stack\n{win.win_stack}\n")
            self.hide()
        except IndexError:
            print("[red]win.win_stack.pop().show()\n"
                "IndexError: pop from empty list\n"
                "[yellow]Note: previous_win_handler() inherited from Windows class should be automatic,\n"
                "as long as next_win_handler() was used previously to open window...\n")

    def next_win_handler(self, next_win):
        """saves current window (self) to stack and hides it, then shows new window (next_win)"""
        win.win_stack.append(self)
        self.hide()
        next_win.show()

class Window(W.QWidget, WinStack):
    """ Window class provides
     basis for both menu bar and toolbar windows (forms, lists, images etc)
     close events like Ctrl-C and click on [x],  are disabled by default
        -    unless CloseEvent is subclassed again in a child class
     window layout set to grid layout type,  adding a default header field
     adds QActions and handlers for info options
        'About Qt'
        'read project documentation README.md'
        'about current window'
     adds QActions and handlers for window navigation
        'previous_win' and 'next_win handlers'      allowing automatic navigation between windows - see WinStack class
    """
    def __init__(self):
        W.QWidget.__init__(self)
        WinStack.__init__(self)
        self.setGeometry(scr.window_rect)
        self.setWindowTitle("self.setWindowTitle() - Basic Window")

        # icons

        icn.about_win = G.QIcon("/usr/share/icons/oxygen/base/32x32/categories/system-help.png")
        icn.readme = G.QIcon("/usr/share/icons/oxygen/base/32x32/mimetypes/text-x-readme.png")
        icn.about_qt = G.QIcon("/usr/share/doc/qt/global/template/images/Qt-logo.png")
        icn.quit = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/application-exit.png")

        #icn.default_icon = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/draw-star.png")
        icn.default_icon = G.QIcon("/usr/share/doc/qt6/global/template/images/spinner.gif")

        # QGridLayout window layout for all content

        #assumes all children windows will use QGridLayout for menubars, toolbars and content widgets etc
        self.window_grid_layout = W.QGridLayout()
        self.setLayout(self.window_grid_layout)
        self.window_grid_layout.setRowStretch(20, 100) # push all current and future widgets to top of window layout
        #PySide6.QtWidgets.QGridLayout.addItem(item, row, column[, rowSpan=1[, columnSpan=1[, alignment=Qt.Alignment()]]])
        #self.window_grid_layout.addLayout(W.QGridLayout, 0, 0,  columnSpan=3)

        # window grid header

        self.window_grid_header = W.QLabel()
        self.window_grid_header.setFont(prj.serifFontBold)
        self.window_grid_header.setText("subclass self.window_grid_header.setText()")
        self.window_grid_layout.addWidget(self.window_grid_header, 1, 0, 1, 4)

        # window grid footer

        self.window_grid_footer = W.QLabel()
        self.window_grid_footer.setFont(prj.serifFont)
        self.window_grid_footer.setText("subclass self.window_grid_footer.setText()")
        # addWidget later, after any other content

        # QActions

        # about current window - see corresponding handler note below

        self.about_win_act = G.QAction()
        self.about_win_act.setIcon(icn.about_win)
        self.about_win_act.triggered.connect(self.about_win_handler)
        self.about_win_act.setText({'en':'About Window',
                                    'es':'Info sobre Ventana'}[prj.locale])

        # use a browser to open the project README.md file":
        self.readme_act = G.QAction()
        self.readme_act.setIcon(icn.readme)
        self.readme_act.triggered.connect(self.readme_handler)
        self.readme_act.setText({'en':'About Project README.md',
                                 'es':'Info Proyecto en README.md'}[prj.locale])

        # about Qt

        self.about_qt_act = G.QAction()
        self.about_qt_act.setIcon(icn.about_qt)
        self.about_qt_act.triggered.connect(W.QApplication.instance().aboutQt)
        self.about_qt_act.setText({'en':'Show the Qt6 About box',
                                   'es':'Info sobre Qt'}[prj.locale])

        #self.installEventFilter(self)

    # handlers

    def about_win_handler(self):
        mbx.pending("about_win_handler() for this window needs subclassing")

    def readme_handler(self):
        """following assumes README file located in project's folder"""
        #webbrowser.open("www.google.com")
        try:
            subprocess.run(['vscodium', 'README.md'], check=False) # dont check for non zero exit code
        except FileNotFoundError:
            mbx.warning("VSCodium was not available to read README.md - install or use Featherpad")

class MenuWindow(Window):
    """MenuWindow(Window) class documentation
     provides a basis for a project startup menu/main window:
     subclasses system close events (Ctrl-C,  click on [X] button)
     creates default menu bar
     adds clickable image to screen
     has no login utilities - See LoginMenus.py module
    """
    def __init__(self):
        Window.__init__(self)

        icn.qt_logo = G.QIcon("/usr/share/doc/qt/global/template/images/logo.png")
        pixmap = G.QPixmap(G.QImage("/usr/share/doc/qt/global/template/images/logo.png"))

        #  quit QAction

        self.quit_act = G.QAction()
        self.quit_act.setIcon(icn.quit)
        self.quit_act.triggered.connect(self.quit_handler)
        self.quit_act.setText({'en':' Quit ',
                               'es':' Salir '}[prj.locale])

        # create initial menu bar and add to window layout

        self.menu_mbr = W.QMenuBar()
        self.menu_mbr.setFont(prj.serifFont)
        self.menu_mbr.addAction(self.quit_act)

        self.window_grid_layout.setMenuBar(self.menu_mbr)

        # create About subMenu

        self.about_mnu = W.QMenu()
        self.about_mnu.setTitle("&About")
        self.about_mnu.setFont(prj.serifFont)
        self.about_mnu.addAction(self.about_win_act)
        self.about_mnu.addAction(self.readme_act)
        self.about_mnu.addAction(self.about_qt_act)
        self.menu_mbr.addMenu(self.about_mnu)

        # add an image to main menu window

        self.image01 = W.QLabel()
        self.image01.setPixmap(pixmap)

        self.window_grid_layout.addWidget(self.image01, 1, 2)
        self.image01.installEventFilter(self)
        self.ctrl_key_pressed = False

    def closeEvent(self, event):
        """change default reponse to Ctrl-C or clicking window [x]"""
        if mbx.confirm("Really quit?"):
            self.quit_handler()    #required to force exit from app loop and return to desktop
        event.ignore()

    def quit_handler(self):
        sys.exit(0)    #exit from app loop and return to desktop

    def about_win_handler(self):
        mbx.pending(str(self.__doc__).ljust(100))   # Note:  __doc__ corresponds to class docstring

class ToolWindow(Window):
    """ ToolWindow adds to Window class
        - a default right side toolbar,  as a basis for form and/or list windows
        - places previously defined 'about window' and 'previous window' images in toolbar,  plus corresponding default handlers
        Note: ToolWindow does not include a QAction for Quit,  since this would normally be placed in menubar of a project's main menu
    """
    def __init__(self):
        Window.__init__(self)

        self.list_font = G.QFont("Times", 12)

        # icons

        icn.cancel = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/dialog-cancel.png")

        icn.insert = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/document-save.png")  # insert new record
        icn.update = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/edit-text-frame-update.png") # update current record
        icn.undo = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/edit-undo.png") # undo any unsaved updates
        icn.delete = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/archive-remove.png")

        icn.open_new_form = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/list-add.png") # open new record input form
        #icn.open_filters_form_icn = "/usr/share/icons/oxygen/base/32x32/actions/view-filter.png"

        icn.remove_filter = G.QIcon(F"{prj.images_folder}/list-unfilter.png")
        icn.run_filter = G.QIcon(F"{prj.images_folder}/list-filter.png")     # open filtered list window

        # create right side toolbar

        self.tool_bar = W.QToolBar()
        self.tool_bar.setLayoutDirection(Qt.RightToLeft)
        self.window_grid_layout.addWidget(self.tool_bar, 0, 0, 1, 4)

        # QActions

        if "cancel":
            self.cancel_act = G.QAction()
            self.cancel_act.setIcon(icn.cancel)
            self.cancel_act.triggered.connect(self.cancel_handler)
            self.cancel_act.setText({'en':' Cancel ',
                                     'es':' Cancelar '}[prj.locale])

        if "update":
            self.update_act = G.QAction()
            self.update_act.setIcon(icn.update)
            self.update_act.triggered.connect(self.update_handler)
            self.update_act.setText({'en':'Save',
                                     'es':'Guardar'}[prj.locale])

        if "undo":
            self.undo_act = G.QAction()
            self.undo_act.setIcon(icn.undo)
            self.undo_act.triggered.connect(self.undo_handler)
            self.undo_act.setText({'en':'Restore values...',
                                   'es':'Restorar valores ...'}[prj.locale])

        if "insert":
            self.insert_act = G.QAction()
            self.insert_act.setIcon(icn.insert)
            self.insert_act.triggered.connect(self.insert_handler)
            self.insert_act.setText({'en':'Add A New Record to List',
                                     'es':'Agregar nuevo a la lista'}[prj.locale])

        if "open new":
            self.open_new_form_act = G.QAction()
            self.open_new_form_act.setIcon(icn.open_new_form)
            self.open_new_form_act.triggered.connect(self.open_new_form_handler)
            self.open_new_form_act.setText({'en':'Accept new data',
                                            'es':'Aceptar nuevos datos'}[prj.locale])

        if "remove filter":
            self.remove_filter_act = G.QAction()
            self.remove_filter_act.setIcon(icn.remove_filter)
            self.remove_filter_act.setEnabled(False) # should be False by default until input
            self.remove_filter_act.triggered.connect(self.remove_filter_handler)
            self.remove_filter_act.setText({'en':'Remove filters',
                                            'es':'Quitar filtros'}[prj.locale])

        if "run filter":
            self.run_filter_act = G.QAction()
            self.run_filter_act.setIcon(icn.run_filter)
            self.run_filter_act.triggered.connect(self.run_filter_handler)
            self.run_filter_act.setText({'en':'Run filters',
                                         'es':'Aplicar filtros'}[prj.locale])

        if "delete":
            self.delete_act = G.QAction()
            self.delete_act.setIcon(icn.delete)
            self.delete_act.triggered.connect(self.delete_handler)
            self.delete_act.setText({'en':'Delete ...',
                                     'es':'Borrar ...'}[prj.locale])

        # common Actions to all toolbars

        self.tool_bar.addAction(self.previous_win_act)
        self.tool_bar.addAction(self.about_win_act)

    # handlers

    def about_win_handler(self):
        mbx.pending("about_win_handler()<p>"
        "for this window needs subclassing")

    def cancel_handler(self):
        mbx.pending("cancel_handler(), including confirm msgbox<p>"
        "for this window needs subclassing")
        self.set_toolbar_to_default_mode()

    def update_handler(self):
        mbx.pending("update_handler(), including confirm msgbox<p>"
        "for this window needs subclassing")
        self.set_toolbar_to_default_mode()

    def undo_handler(self):
        mbx.pending("undo_handler() and<p>"
        "set_form_fields_to_default_values()<p>"
        "for this window need subclassing")
        self.set_form_fields_to_default_values()
        self.set_toolbar_to_default_mode()

    def insert_handler(self):
        mbx.pending("insert_handler() <p>"
        "for this window needs subclassing")
        self.set_toolbar_to_default_mode()

    def remove_filter_handler(self):
        mbx.pending("remove_filter_handler()<p>"
        "for this window needs subclassing")
        self.set_form_fields_to_default_values()
        self.remove_filter_act.setEnabled(False)

    def run_filter_handler(self):
        mbx.pending("run_filter_handler()<p>"
        "for this window needs subclassing")

    def delete_handler(self):
        mbx.pending("delete_handler()<p>"
        "for this window needs subclassing")

    def open_new_form_handler(self):
        mbx.pending("open_new_form_handler()<p>"
        "for this window needs subclassing")

    # events

    def closeEvent(self, event):
        mbx.warning("closeEvent()<p>"
        "for this window needs to be subclassed<p>"
        "Currently set to return to previous window")
        self.previous_win_handler()

    def showEvent(self, event):
        mbx.warning("showEvent()<p>"
        "for ~next~ window needs to be subclassed")

    # methods

    def set_toolbar_to_default_mode(self):
        mbx.pending("set_toolbar_to_default_mode()<p>"
        "for this window needs subclassing")

    def set_form_fields_to_default_values(self):
        mbx.pending("set_form_fields_to_default_values()<p>"
        "for this window needs subclassing")

#-----------------------------------------------------------------------------

class FormWidget():
    """Form Widget class
     Note: layout will automatically adjust widget size in window that inherits FormWidget class
     """
    def __init__(self):

        self.form_grid_layout = W.QGridLayout()
        self.form_widget = W.QWidget()
        self.form_widget.setLayout(self.form_grid_layout)

        self.form_widget_header = W.QLabel()
        self.form_widget_header.font().setBold(True)
        self.form_widget_header.setText("subclass self.form_widget_header.setText()")

class ListWidget():
    """List Widget class
    include generic function to populate list_widget,   given table, filter, fields, widths"""
    def __init__(self):

        self.list_widget = W.QTableWidget()  # Note: actual cols and rows are set in children classes
        self.list_widget.setFont(self.list_font)

        self.list_header = W.QLabel()
        self.list_header.font().setBold(True)
        self.list_header.setText("subclass self.list_header.setText() - Click on row to open corresponding record")

        self.list_widget.cellClicked.connect(self.list_widget_click_handler)

    def update_list_widget(self, table_name,  filter_str="", table_fields_lst=None, widths_lst=None, verbose=False):
        """this is a generic function to fill self.list_widget,   depending on table, filter, fields, widths
        Assumes single table only - will need to subclass for multi table queries
        """
        if "adjust filter string":
            filter_str = filter_str.strip()
            if filter_str:
                if not filter_str.count("'%%'"):
                    filter_str = F" WHERE {filter_str}"
                else:
                    filter_str = ""

        if "get total rows":
            query = run_select(F"SELECT COUNT (*) FROM {table_name} {filter_str}", verbose)
            total_rows = query.value(0)

        if "adjust table_fields string and list":
            if not table_fields_lst:  # == None or []
                table_fields_lst = []
                table_fields_str = '*'  # all fields
            else:
                table_fields_str = ', '.join(table_fields_lst)

        if "get indicated records":
            query = run_select(F"SELECT {table_fields_str} FROM {table_name} {filter_str}", verbose)
            total_columns = query.record().count()

        if table_fields_str == '*':
            for col in range(total_columns):
                table_fields_lst.append(query.record().fieldName(col))

        if "recreate table rows, cols and headers":
            self.list_widget.setRowCount(total_rows)
            self.list_widget.setColumnCount(total_columns)
            self.list_widget.setHorizontalHeaderLabels(table_fields_lst)

        if "set column widths":
            if widths_lst is None:
                widths_lst = []

            #for col in range(len(widths_lst)):
            #    self.list_widget.setColumnWidth(col, widths_lst[col])

            for tpl in enumerate(widths_lst):
                col, width = tpl
                self.list_widget.setColumnWidth(col, width)

        if "put query records in table":
            self.list_widget.setSortingEnabled(False)

            for row in range(total_rows):
                for col in range(total_columns):
                    if col == 0:
                        self.list_widget.setItem(row, col, W.QTableWidgetItem(str(query.value(col)).rjust(5))) # needed for proper sorting
                    else:
                        self.list_widget.setItem(row, col, W.QTableWidgetItem(str(query.value(col))))
                query.next()

            self.list_widget.setSortingEnabled(True)

    def list_widget_click_handler(self, row, col):
        mbx.pending(F"list_widget_click_handler() needs subclassing in this window<p>"
        F"Cell clicked {row}, {col}<p>"
        F"record id = {self.list_widget.item(row, 0).text()}")

#-----------------------------------------------------------------------------

class PrintScreen():
    """PrintScreen class
     Note:  this works on any window that inherits PrintScreen and has print_screen_act enabled in tool_bar     """

    def __init__(self):

        icn.print_screen = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/document-print-direct.png")
        self.print_screen_act = G.QAction()
        self.print_screen_act.setIcon(icn.print_screen)
        self.print_screen_act.triggered.connect(lambda: self.print_screen_handler(self))
        self.print_screen_act.setText({'en':'Print Screen',
                                       'es':'Imprimir Pantalla'}[prj.locale])


        self.tool_bar.addAction(self.print_screen_act)

    def print_screen_handler(self, win_prm):
        """generic,  works on any screen """
        if mbx.confirm("Confirm Screen Print ..."):
            printer = P.QPrinter()
            painter = G.QPainter()
            painter.begin(printer)
            screen_ = win_prm.grab()  # to print whole window
            #painter.drawPixmap(10, 10, screen_)
            painter.end()

class PrintDocument():
    """ """
    def __init__(self):

        icn.print_document = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/document-print.png")

        if "create document and cursor":
            self.doc = G.QTextDocument()
            self.cursor = G.QTextCursor(self.doc)
            self.root_frame = self.cursor.currentFrame()

        if "QAction":

            self.print_document_act = G.QAction()
            self.print_document_act.setIcon(icn.print_document)
            self.print_document_act.triggered.connect(self.print_document_handler)
            self.print_document_act.setText({'es':'Imprimir datos directamente',
                                             'en':'Print directly'}[prj.locale])

    def generate_doc(self):
        self.doc.clear()
        if "place default content - assumes content already available locally from windows's showEvent()":
            content = "inherited generate_doc() needs to be subclassed here"
            #cursor.insertBlock(block_format, char_format)
            self.cursor.insertBlock() # using default formats
            self.cursor.insertText(content)

    def print_document_handler(self):
        """handler for print directly QAction"""
        self.generate_doc()
        dialog = P.QPrintPreviewDialog()
        self.doc.print_(dialog.printer())

class PrintPreview():
    """ """
    def __init__(self):

        icn.print_preview = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/document-print-preview.png")

        if "QAction":
            self.print_preview_act = G.QAction()
            self.print_preview_act.setIcon(icn.print_preview)
            self.print_preview_act.triggered.connect(self.print_preview_handler)
            self.print_preview_act.setText({'es':'Prevista de Impression',
                                            'en':'Print Preview'}[prj.locale])

    def generate_doc(self):
        """
        when generate_doc() subclassed,
        content for doc should already be available locally from parent windows's showEvent()
        """
        doc = G.QTextDocument()

        cursor = G.QTextCursor(doc)
        root_frame = cursor.currentFrame()                            #pylint:disable=unused-variable

        char_format = G.QTextCharFormat()
        block_format = G.QTextBlockFormat()

        if "place demo content":

            content = ("<h1>inherited<br>"
                "<i>Windows.PrintPreview.generate_doc()</i><br>"
                "needs to be subclassed here for correct output</h1>")

            if "insert blocks and content":

                block_format.setBackground(Qt.Dense7Pattern) # See https://doc.qt.io/qtforpython/PySide6/QtGui/QBrush.html
                cursor.insertBlock(block_format)

                char_format.setFontPointSize(20.0)
                block_format.setBackground(Qt.NoBrush)
                cursor.insertBlock(block_format, char_format)

                ##cursor.insertText(content)
                cursor.insertHtml(content)

                block_format.setBackground(Qt.Dense7Pattern)
                cursor.insertBlock(block_format)

        return doc

    def print_preview_handler(self):
        """handler for print preview QAction"""
        doc = self.generate_doc()
        dialog = P.QPrintPreviewDialog()
        dialog.paintRequested.connect(lambda: doc.print_(dialog.printer()))
        dialog.exec()

#-----------------------------------------------------------------------------

class WindowsNewForm(ToolWindow, FormWidget):
    """NewFormWindow for accepting data of a new record

     Subclass needs to
      - put labels, fields and any other widgets in self.form_widget for given table
      - update eventFilter for widget_form events"""

    def __init__(self):
        ToolWindow.__init__(self)
        FormWidget.__init__(self)

        # attributes

        self.setWindowTitle("subclass self.setWindowTitle - New Form Window Class")
        self.window_grid_header.setText("subclass self.window_grid_header.setText() - New Record Form")
        self.form_widget_header.setText("subclass self.form_widget_header.setText() - Enter data for new record below")

        # place form widgets

        self.window_grid_layout.addWidget(self.form_widget_header, 2, 0, 1, 4)
        self.window_grid_layout.addWidget(self.form_widget, 3, 0, 1, 4)

        # update toolbar

        self.tool_bar.addAction(self.insert_act)
        self.tool_bar.addAction(self.cancel_act)

        self.set_toolbar_to_default_mode()

    # toolbar modes

    def set_toolbar_to_default_mode(self):
        self.insert_act.setEnabled(False)
        self.cancel_act.setEnabled(False)
        self.previous_win_act.setEnabled(True)

    def set_toolbar_to_edit_mode(self):
        self.insert_act.setEnabled(True)
        self.cancel_act.setEnabled(True)
        self.previous_win_act.setEnabled(False)

class WindowsUpdateForm(ToolWindow, FormWidget):
    """Window for updating or deleting a given record """

    def __init__(self):
        ToolWindow.__init__(self)
        FormWidget.__init__(self)

        # attributes

        self.setWindowTitle("subclass self.setWindowTitle - Update Form Window Class")
        self.window_grid_header.setText("subclass self.window_grid_header.setText() - Update Record Form")

        # place form widgets":

        self.window_grid_layout.addWidget(self.form_widget_header, 2, 0, 1, 4)
        self.window_grid_layout.addWidget(self.form_widget, 3, 0, 1, 4)

        # add QActions to toolbar

        self.tool_bar.addAction(self.update_act)
        self.tool_bar.addAction(self.delete_act)
        self.tool_bar.addAction(self.undo_act)

        self.set_toolbar_to_default_mode()

    # methods

    def set_form_fields_to_default_values(self):
        mbx.pending("UpdateFormToolbar.set_form_fields_to_default_values() needs subclassing")

    # toolbar modes

    def set_toolbar_to_default_mode(self):
        self.undo_act.setEnabled(False)
        self.update_act.setEnabled(False)
        self.delete_act.setEnabled(True)
        self.previous_win_act.setEnabled(True)

    def set_toolbar_to_edit_mode(self):
        self.undo_act.setEnabled(True)
        self.update_act.setEnabled(True)
        self.delete_act.setEnabled(False)
        self.previous_win_act.setEnabled(False)

class WindowsList(ToolWindow, ListWidget):
    """WindowsList to show a list of (possibly filtered) records
     Note: the term list used here is actually a table of one or more columns.

     a child window needs to
       - create columns, rows and headers of list_widget, depending on given query <- prj.current_table_query
       - display records in given query"""
    def __init__(self):
        ToolWindow.__init__(self)
        ListWidget.__init__(self)

        # attributes

        self.setWindowTitle("subclass self.setWindowTitle() - List Window Class")
        self.window_grid_header.setText("subclass self.window_grid_header.setText() - List of Records")

        # place form widgets

        self.window_grid_layout.addWidget(self.list_header, 2, 0, 1, 4)
        self.window_grid_layout.addWidget(self.list_widget, 3, 0, 1, 4)
        self.window_grid_layout.addWidget(self.window_grid_footer, 4, 0, 1, 4)

        self.window_grid_layout.setRowStretch(3, 800) # layout will expand list to fill window

        # toolbar update

        self.tool_bar.addAction(self.open_new_form_act)
        self.tool_bar.addAction(self.run_filter_act)

        self.set_toolbar_to_default_mode()

    # toolbar modes

    def set_toolbar_to_default_mode(self):
        self.open_new_form_act.setEnabled(True)
        self.previous_win_act.setEnabled(True)

        self.run_filter_act.setEnabled(False)
        self.remove_filter_act.setEnabled(False)

    def set_toolbar_to_edit_mode(self):
        self.run_filter_act.setEnabled(True)
        self.remove_filter_act.setEnabled(True)

class WindowsFormList(ToolWindow, FormWidget, ListWidget):
    """WindowsFormList to display a list of records filtered by contents of the form contents<p>
    Primarily used for selecting a record to view/edit"""

    def __init__(self):
        ToolWindow.__init__(self)
        FormWidget.__init__(self)
        ListWidget.__init__(self)

        # attributes

        self.setWindowTitle("subclass self.setWindowTitle() - FormListWindow Class")
        self.window_grid_header.setText("subclass self.window_grid_header.setText() - List - Filtered by Form")
        self.form_widget_header.setText("subclass self.form_widget_header.setText() - Enter full or partial data to filter list")

        # place form widgets

        self.window_grid_layout.addWidget(self.form_widget_header, 2, 0, 1, 4)
        self.window_grid_layout.addWidget(self.form_widget, 3, 0, 1, 4)
        self.window_grid_layout.addWidget(self.list_header, 4, 0, 1, 4)
        self.window_grid_layout.addWidget(self.list_widget, 5, 0, 1, 4)
        self.window_grid_layout.setRowStretch(5, 800) # layout will expand list to fill window

        # toolbar update

        self.tool_bar.addAction(self.remove_filter_act)
        self.tool_bar.addAction(self.open_new_form_act)

    # toolbar modes

    def set_toolbar_to_default_mode(self):
        self.remove_filter_act.setEnabled(False)
        self.previous_win_act.setEnabled(True)

    def set_toolbar_to_edit_mode(self):
        self.remove_filter_act.setEnabled(True)

class WindowsFilterForm(ToolWindow, FormWidget):
    """FilterFormWindow to accept data,  then used to generate a filter string for database """
    def __init__(self):
        ToolWindow.__init__(self)
        FormWidget.__init__(self)

        # attributes

        self.setWindowTitle("subclass self.setWindowTitle - Filter Form Window Class")
        self.window_grid_header.setText("subclass self.window_grid_header.setText() - Form to generate filters")
        self.form_widget_header.setText("subclass self.form_widget_header.setText() - Enter full or partial data to generate search")

        # place form widgets

        self.window_grid_layout.addWidget(self.form_widget_header, 2, 0, 1, 4)
        self.window_grid_layout.addWidget(self.form_widget, 3, 0, 1, 4)

        # toolbar update

        self.tool_bar.addAction(self.remove_filter_act)
        self.tool_bar.addAction(self.run_filter_act)

        self.set_toolbar_to_default_mode()

        ##self.cancel_act.setVisible(False)

    # toolbar modes

    def set_toolbar_to_default_mode(self):
        self.remove_filter_act.setEnabled(False)
        self.run_filter_act.setEnabled(False)
        self.previous_win_act.setEnabled(True)

    def set_toolbar_to_edit_mode(self):
        self.remove_filter_act.setEnabled(True)
        self.run_filter_act.setEnabled(True)
        self.previous_win_act.setEnabled(True)

# Note: Since this is a large module,  test code usually found here,  is in a seperate module.

#!/usr/bin/env python3            #pylint: disable=invalid-name

"""[green]Login Menus Class -  for details see LoginMenus.md[black]<p>
<p>
Provides:<p>
- main menu with Login/Logout option for different user names<p>
- current user name is kept in `prj.current_user_name` variable, based on entering correct password<p>
- allow individual and group names,  including default `Guest`, `User`, `Admin` and `Root` names,
  where `Guest` is the passwordless default<p>
- enable code to accept/deny various operations,  depending on current user name,<p>
  for example only authorizing Root for editing password list<p>
- hide/restore user name:password list to/from an encrypted file<p>
- autologout to `Guest` when screen inactive for `prj.auto_logout_seconds`<p>
- add a backdoor to `Root` user for use during development (press Ctrl + wheel on image)<p>
<p>
Also see Notes/Topics/Login/README.md
"""

#pylint:disable=empty-docstring, missing-function-docstring, missing-class-docstring, useless-suppression
#pylint:disable=unused-import
#pylint:disable=no-name-in-module
#pylint:disable=import-error
#pylint:disable=unused-argument
#pylint:disable=redefined-builtin

if "initial imports":
    import sys
    try:
        from Support.dev_tools import console, log, bp, print, inspect
    except ModuleNotFoundError:
        from dev_tools import console, log, bp, print, inspect

if __name__ == '__main__':
    console.clear()
    print(__doc__)
    print("[red][bold]\nLoginMenus module not for solo run")
    sys.exit()

if "imports":

    import os
    #import re
    from threading import Timer
    import pyAesCrypt

    import PySide6.QtWidgets as W
    import PySide6.QtCore as C
    import PySide6.QtGui as G
    from PySide6.QtCore import Qt

    import Support.msg_boxes as mbx
    import Support.screen_info as scr
    from Support.Windows import ToolWindow, MenuWindow, prj, win, icn

class LoginMenuBase():
    """Add [login/Logout], Root options to menubar

    Default password_list is:
    password   user_name
        'user'   'User'
        'admin'  'Admin'
        'root'   'Root'
    Note: guest is the default, passwordless user name
    """
    def __init__(self):
        """ """
        # QAction - user login

        self.login_act = G.QAction(self)
        #self.login_act.setText("Login") # not needed here - toggled below
        self.login_act.triggered.connect(self.login_handler)

        # update menubar

        self.menu_mbr.addAction(self.login_act)
        self.root_mnu = W.QMenu("Root")
        self.menu_mbr.addMenu(self.root_mnu)

        # default user name

        prj.current_user_name = "Guest"
        self.update_login_menu()

    def update_login_menu(self):
        """enable menu options based on current_user
        module run whenever current user changes,  by __init__, login handler or shortcut functions
        """

        if prj.current_user_name == "Guest":
            self.login_act.setText("[  Login  ]")
            #console.clear()
        else:
            self.login_act.setText("[  Logout ]")

        if prj.current_user_name == "Root":
            ##prj.current_user_name = '<font color=#FF0000>Root</font>'
            self.root_mnu.setEnabled(True)
        else:
            self.root_mnu.setEnabled(False)

        self.update_window_grid_header()

    def update_window_grid_header(self):
        self.window_grid_header.setText({'es':F"Usuario actual es: {prj.current_user_name}",
                                         'en':F"Current user is: {prj.current_user_name}"}[prj.locale])

    def login_handler(self):  #Note: subclassed below in AutoLogout class
        if prj.current_user_name == 'Guest':
            win.login_dialog.exec()
        else:
            prj.current_user_name = 'Guest'
        self.update_login_menu()

    def showEvent(self, event):
        self.update_window_grid_header()

class AutoLogout():          # add autologout
    """Adds auto logout to prevent unauthorized access to User, Admin or Root menu options,
    in an unattended computer    """

    def __init__(self):
        """ """
        #set default auto logout time - needs to be float type

        #prj.auto_logout_seconds = float(0)   # timer disabled
        #prj.auto_logout_seconds = float(300) # 300 = 5 minutes  -  copy and enable in project start module
        prj.auto_logout_seconds = float(15)   # short for testing purposes

        #print(F"[blue]Auto logout set to {prj.auto_logout_seconds} seconds")

    # handlers

    def login_handler(self):    # subclassed from above
        LoginMenuBase.login_handler(self)
        self.reset_logout_timer(not "verbose")

    def auto_logout_to_guest_handler(self):
        prj.current_user_name = "Guest"
        self.update_login_menu()
        if prj.locale == "es":
            self.window_grid_header.setText(F"Usuario actual:  Guest  - despues de auto-logout por {prj.auto_logout_seconds} segundo 'timeout'")
        else:
            self.window_grid_header.setText(F"Current user:  Guest  - after timed {prj.auto_logout_seconds} second auto-logout event")

    def quit_handler(self):    #subclassed from MenuWindow()
        if prj.current_user_name != 'Guest':
            try:
                prj.auto_logout_timer.cancel()
            except AttributeError:
                pass
        if prj.current_user_name == "Root":
            sys.exit(0)    #exit from app loop and return to desktop
        if prj.locale == "es":
            if mbx.confirm("Realmente Salir?"):
                sys.exit(0)
        else:
            if mbx.confirm("Really quit?"):
                sys.exit(0)

    # method

    def reset_logout_timer(self, verbose=False):
        if prj.current_user_name != 'Guest':
            # create/recreate logout timer thread after each login
            if prj.auto_logout_seconds:
                try:
                    prj.auto_logout_timer.cancel()
                except AttributeError:
                    pass
                prj.auto_logout_timer = Timer(prj.auto_logout_seconds, self.auto_logout_to_guest_handler)
                prj.auto_logout_timer.start()

                if verbose:
                    print(F"[red]{prj.auto_logout_seconds} second auto_logout_timer (re)started ....")

        else: # in Guest mode - cancel timer
            if verbose:
                print("[red] auto_logout_timer canceled for Guest ....")
            try:
                prj.auto_logout_timer.cancel()
            except AttributeError:
                pass

class DecryptPasswords():    # add load and decrypt file into prj.passwords_list
    """Loads an encrypted passwords file, then
    decrypts file into prj.passwords_list

    Adds menu option to Root menu,   allowing
        updates to password list
        then encrypted and saved to passwords_list.txt.aes file
    Although this security is good enough for casual users,
    this source should be compiled with Cython, against more determine/capable users.
    """
    def __init__(self):
        """ """
        icn.passwords = G.QIcon("/usr/share/icons/oxygen/base/32x32/apps/preferences-desktop-user-password.png")

        self.get_password_list() # from encrypted file

        # edit password list

        self.password_editor_act = G.QAction("Edit passwords list", self)
        self.password_editor_act.setIcon(icn.passwords)

        self.root_mnu.addAction(self.password_editor_act)
        self.password_editor_act.triggered.connect(lambda: self.next_win_handler(win.password_editor_win))

    def get_password_list(self):

        prj.default_password_list = [("root", "Root"),("admin", "Admin"),("user", "User")]

        # password.txt encryption variables

        prj.password_file_str = "passwords.txt"
        prj.encrypted_file_str = "passwords.txt.aes"
        prj.root_password_str = "root"
        prj.buffer_size_int = 64 * 1024

        # decrypt passwords file on startup
        ##print(prj.password_file_str, prj.encrypted_file_str, prj.root_password_str, prj.buffer_size_int)
        try:
            pyAesCrypt.decryptFile(prj.encrypted_file_str, prj.password_file_str, prj.root_password_str, prj.buffer_size_int)

            if "return password list from passwords.txt file":
                # Note: auto closes file
                with open("passwords.txt", encoding="utf-8") as file:
                    password_list = file.read()
                prj.password_list = eval(password_list)                  #pylint:disable=eval-used
                # turns list of lists string into a list of tuples

            if "delete passwords.txt file":
                os.remove("passwords.txt")

        except ModuleNotFoundError:
            log.debug("")
            print("[red]\n\nModuleNotFoundError:   possibly cffi_backend not found error"
            "probably due to cffi module for installed pyAesCrypt  was not compiled for current version of Python"
            "#TODO how to fix ??? ")
            sys.exit()

        except ValueError:
            log.debug("\n")
            print(F"""[yellow]ERROR\n Encrypted password file ____ {prj.encrypted_file_str} ____ was not found or is invalid""")

            if not "in debug mode":
                log.debug("\n[orange]IN DEBUG MODE TO RECUPERATE encrypted password file\n")
                print("[yellow]Default password list is now enabled - with Root password was set to 'root'"
                    "(re)create new password list under Root menu and save")
                print("[red]\n Debug mode should be disabled in production version since it shortcuts security"
                    "a valid encrypted password file should be kept offsite for emergencies\n")
                prj.password_list = prj.default_password_list
            else:
                print("[red]\npassword file must be copied to project directory by administrator, from a valid encrypted offsite backup copy")
                ##sys.exit()

        # set inital user":
        prj.current_user_name = "Guest"

class LoginMenu(DecryptPasswords, AutoLogout, LoginMenuBase, MenuWindow):
    """Login Menu - with
    - AutoLogout
    - root shortcut
    - password list editing by root """

    def __init__(self):
        """ """
        MenuWindow.__init__(self)
        LoginMenuBase.__init__(self)
        AutoLogout.__init__(self)
        DecryptPasswords.__init__(self)

        self.setWindowTitle("subclass self.setWindowTitle() - Login Menu Window")
        self.ctrl_key_pressed=False

    # events

    def eventFilter(self, obj, event):
        # following will need to be copied to eventFilter() in child class
        if obj is self.image01 and event.type() == C.QEvent.Wheel and self.ctrl_key_pressed:
            self.root_login_shortcut()
        return False

    def keyPressEvent(self, event):
        if event.key() == 16777249:    #Left  Ctrl
            self.ctrl_key_pressed = True

    def keyReleaseEvent(self, event):
        if event.key() == 16777249:    #Left  Ctrl
            self.ctrl_key_pressed = False

    def showEvent(self, event):
        self.update_login_menu()
        self.reset_logout_timer(not "verbose")

    # methods

    def root_login_shortcut(self):
        self.ctrl_key_pressed = False
        prj.current_user_name = "Root"
        mbx.warning("Dev mode - current user set to Root")
        print("[red]\nTHIS BACKDOOR SHOULD BE DISABLED IN PRODUCTION VERSION OF PROJECT")
        self.update_login_menu()

class LoginDialog(W.QDialog):
    """This dialog accepts a password and if found in passwords_list,  updates current_user_name to corresponding name
    Note: passwords can be for a unique user name,  or share a single generic user name  """
    def __init__(self):
        W.QDialog.__init__(self)

        # attributes

        self.resize(450, 150)

        # widgets

        self.text_pass = W.QLabel("Access to other menu options requires entry of a registered password.\n\nEnter your Password here:", self)

        self.input_pass = W.QLineEdit(self)
        self.input_pass.setEchoMode(W.QLineEdit.Password)
        self.input_pass.setClearButtonEnabled(True)

        self.login_btn = W.QPushButton(self)
        self.login_btn.setText('Click to Login')

        #self.login_btn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        self.login_btn.setStyleSheet('QPushButton {background-color: darkGray; color: darkBlue;}')

        # layout

        layout = W.QVBoxLayout(self)
        layout.addWidget(self.text_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.login_btn)

        # connection

        self.login_btn.clicked.connect(self.login_messages)
        #self.login_btn.clicked.connect(lambda: self.login_message_handler) #does not work

        # message box

        self.msg_box = W.QMessageBox(W.QApplication.instance().activeWindow())
        self.msg_box.setIcon(W.QMessageBox.Information)
        self.msg_box.setGeometry(scr.msg_box_rect)
        self.msg_box.setText("Password Validation:".ljust(120))
        self.msg_box.setStandardButtons(W.QMessageBox.Ok)

    def login_messages(self):
        self.login_message_handler()

    def login_message_handler(self):
        prj.current_user_name = "Guest"
        for item in prj.password_list:
            if item[0] == self.input_pass.text():
                prj.current_user_name = item[1]
                self.msg_box.setWindowTitle("VALID PASSWORD")
                green_ = '<font color="#009900">'
                self.msg_box.setInformativeText(green_ + 'Password ACCEPTED for ' + item[1])
                break

        if prj.current_user_name == "Guest":
            self.msg_box.setWindowTitle("ERROR")
            red_ = '<font color="#ff0000">'
            self.msg_box.setInformativeText(red_ + 'Password - INVALID      Current user now set to "Guest"')

        self.input_pass.clear()
        self.hide()
        self.msg_box.exec()

class PasswordEditor(ToolWindow):
    """Password Editor"""
    def __init__(self):
        ToolWindow.__init__(self)

        # icons

        icn.document_save = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/document-save.png")
        icn.document_reload = G.QIcon("/usr/share/icons/oxygen/base/32x32/actions/document-revert.png")

        #attributes

        self.setWindowTitle("Passwords Editor")
        self.setGeometry(scr.window_rect) # x, y, w, h
        self.setGeometry(C.QRect(1200, 200, 700, 700)) # x, y, w, h

        # widgets

        if "create editor widget":
            self.editor = W.QTextEdit()   #    https://doc.qt.io/qtforpython/PySide6/QtWidgets/QTextEdit.html?highlight=textedit#more
            self.window_grid_layout.addWidget(self.editor, 2, 0)

        if "add default tool_bar to window layout":
            self.window_grid_layout.addWidget(self.tool_bar, 0, 0)

        if "set headers":
            self.window_grid_header.setText("click info icon for details of use\nUse format 'password_str', 'user_name_str'")

        # QActions

        if "save edits ":
            self.update_act = G.QAction(self)
            self.update_act.setIcon(icn.document_save)
            self.update_act.triggered.connect(self.convert_updates_to_password_lst_handler)
            self.update_act.setText("Save Update...")

        if "restore_defaults_act":
            self.restore_defaults_act = G.QAction(self)
            self.restore_defaults_act.setIcon(icn.document_reload)
            self.restore_defaults_act.triggered.connect(self.restore_defaults_handler)
            self.restore_defaults_act.setText("Restore defaults")

        if "update toolbar":
            self.tool_bar.addAction(self.restore_defaults_act)
            self.tool_bar.addAction(self.update_act)

            self.restore_defaults_act.setEnabled(True)
            self.update_act.setEnabled(False)

        if "enable event filters":
            self.editor.installEventFilter(self)

    # events

    def showEvent(self, event):
        lines_str = ""
        for tpl in prj.password_list:
            lines_str = lines_str + str(tpl) + "\n"
        self.editor.setPlainText(lines_str)

    def eventFilter(self, obj, event):
        """check for editing activity"""

        if obj == self.editor and event.type() == C.QEvent.KeyRelease:
            self.update_act.setEnabled(True)
        return False

    # handlers

    def convert_updates_to_password_lst_handler(self, verbose=False):
        """convert updated password list string in editor,   back to list of password tuples for prj.password_list"""

        if "get updated string":
            lines_txt = self.editor.toPlainText()

        if verbose:
            print("original updates")
            print(lines_txt)
            print("\nabove input now cleaned up:")

        if "remove lines starting with space, # or empty lines and add rest to new password_list":
            password_lst = []

            for line_str in lines_txt.split("\n"):
                line_str = line_str.strip().replace(' ', '')
                if line_str and line_str[0] != "#" and len(line_str.strip()) > 0:  # remove comments, preceding spaced and blank lines
                    # evaluate string as a python command and return object
                    try:
                        passwd_tpl = eval(line_str)                 #pylint:disable=eval-used
                    except AttributeError:
                        mbx.warning(F"Invalid password string - {line_str}")
                        return

                    password_lst.append(passwd_tpl)  #add tuple to password_lst

            if verbose:
                for passwd_tpl in password_lst:
                    print(passwd_tpl)
                print(F"\npassword_lst    = {password_lst}  {type(password_lst)}")
                print(F"password_lst[0] = {password_lst[0]}  {type(password_lst[0])}")

        if "make sure essential Root account is present":
            root_found =  False
            for passwd_tpl in password_lst:
                if passwd_tpl[1] == "Root":
                    root_found = True
            if not root_found:
                mbx.warning("Missing essential 'Root' acct")
                return

        if "update prj.password_list":
            prj.password_list = eval(str(password_lst))            #pylint:disable=eval-used

        if "save password_list to password.txt file":
            with open("passwords.txt", "w", encoding="utf-8") as text_file:
                print(password_lst, file=text_file)

        if "encrypt passwords.txt and delete":
            pyAesCrypt.encryptFile(prj.password_file_str, prj.encrypted_file_str, prj.root_password_str, prj.buffer_size_int)

            os.remove(prj.password_file_str)
            self.update_act.setEnabled(False)
            mbx.notify("Updated password list now available - and has been saved to encrypted passwords.txt file")

        self.hide()
        self.previous_win_handler()

    def restore_defaults_handler(self):
        if mbx.confirm("Really restore defaults?"):
            lines_txt = ""
            for tpl in prj.default_password_list:
                lines_txt = lines_txt + str(tpl) + "\n"

            self.editor.setPlainText(lines_txt)
            self.update_act.setEnabled(True)
            mbx.notify("Defaults restored")
        else:
            mbx.notify("Restore canceled")

    def about_win_handler(self):
        about_password_list_msg = """
            This window displays current contents of prj.password_list variable
            and allows local editing of the list.

            The default password_list is:

            prj.password_list = [
                ("root", "Root"),
                ("admin", "Admin"),
                ("user", "User"),
                ]
            where each row is a tuple,  like (password: str, user_name: str)

            Note: Root user name is required for the proper function of LoginMenu module,
            DO NOT CHANGE NAME OR DELETE

            However,  for better security in a runtime project that will be used by others,
            the password for Root SHOULD be updated by Root user.

            Saving updates will:
                check for some errors
                save any updates in a password.txt file
                encrypt password.txt file to password.txt.aes
                delete plain text file passwords.txt    """

        W.QMessageBox.about(self, "Edit Passwords List".ljust(200), about_password_list_msg)

# Note: Since this is a large module,  the module test code normally placed here, was placed in Demos folder

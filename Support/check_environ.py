#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Optional module that confirms that the current local environment,
- is complete, and
- with correct minimal versions for a project.

Can be run
- solo (verbose mode) or
- optionally imported once, early in a project's main module.

import Support/check_environ
"""

# pylint disables
    #pylint:disable=unused-import
    #p ylint:disable=multiple-statements
    #pylint:disable=eval-used
    #pylint:disable=redefined-builtin
    #p ylint:disable=unused-argument

verbose = eval("__name__ == '__main__'")

print("\u001b[2J\u001b[H")  # clear terminal

if "__inits__":

    if "imports":
        import sys
        import os
        import subprocess

    if "get shell environment":
        _HOME = os.environ['HOME']
        _USER = os.environ['USER']
        _SHELL = os.environ['SHELL']
        _PWD = os.getcwd()        # os.environ['PWD']  returns /home/$USER if project Run in Konsole
        sys.path.append(_PWD)

    if "set minimal python3 version":
        major:int = 10
        micro:int = 7

def run_subprocess(_statement:str):
    """wraps subprocess.run to catch any errors"""
    try:
        subprocess.run(_statement, check=True)
    except subprocess.CalledProcessError:
        print(F"CalledProcessError for statement\n {_statement})")
        sys.exit(1) #  since following will not run correctly if any errors with _statement

if "rich":
    """improved print, inspect and console functions  """
    #https://rich.readthedocs.io/en/stable/introduction.html
    #https://github.com/Textualize/rich

    try:
        from rich import print
        if verbose:
            print("[cyan][bold]Checking if current environment is properly installed ....\n ")
            print("rich                  [green]is available\n")
    except ModuleNotFoundError:
        print("\nrich module not found - install with"
        "    pip3 install --user rich\n")
        run_subprocess("pip3 install --user rich")

if "PySide6":
    """
    base system         https://pypi.org/project/PySide6/
    Examples            https://pypi.org/project/PySide6-Addons/
    Additional classes  https://pypi.org/project/PySide6-Essentials/
    """
    try:
        import PySide6
        if verbose: print("PySide6               [green]is available - base classes")

    except ModuleNotFoundError:
        print("\n[red]PySide6 not found..."
        "Make sure PySide6 was installed with"
        "    pip3 install PySide6-Addons"
        "    pip3 install PySide6-Essentials")
        run_subprocess("pip3 install --user PySide6")

    if verbose:
        if os.path.exists(F"/home/{_USER}/.local/lib/python3.{str(major)}/site-packages/PySide6"):
            print("PySide6-Addons        [green]is available - examples")
            print("PySide6-Essentials    [green]is available - more classes\n")
        else:
            print("PySide6-Addons        [red]not available")
            print("PySide6-Essentials    [red]not available\n")

if "sqlite3":
    """alternative to using  QSqlDatabase class"""
    # https://www.sqlite.org/download.html
    try:
        import sqlite3
        if verbose: print("sqlite3               [green]is available\n")

    except ModuleNotFoundError:
        print("\n sqlite3 module not found - try installing with"
        "   sudo apt install sqlite3  or"
        "   pacman -S sqlite3")
        run_subprocess("pacman -S sqlite")

if "pyAesCrypt":
    """cryptography tools,  used in my login menus class"""
    # https://pypi.org/project/pyAesCrypt/
    try:
        import pyAesCrypt
        if verbose: print("pyAesCrypt            [green]is available\n")
    except ModuleNotFoundError:
        print("\npyAesCrypt module not found - install with"
        "   pip3  install  pyAesCrypt"
        "and update PYTHONPATH variable if needed")
        run_subprocess("pip3 install --user pyAesCrypt")

if "num2words":
    """ensure available in projects that convert numbers <-> words"""
    # https://pypi.org/project/num2words/
    try:
        import num2words
        if verbose: print("num2words             [green]is available\n")
    except ModuleNotFoundError:
        print("\n num2words module not found - try installing with"
        "   pip3 install num2words \n")
        run_subprocess("pip3 install --user num2wtoords")

if "screeninfo":
    """python module to find current monitor dimensions for project window layouts"""
    # https://doc.qt.io/qt-6/qscreen.html
    # https://pypi.org/project/screeninfo/
    try:
        import screeninfo
        if verbose: print("screeninfo            [green]is available\n")

    except ModuleNotFoundError:
        print("\n screeninfo module not found - try\n"
            "pip3 show screeninfo\n"
            "and update MRO\n"
            "If not found,  install withnnn\n"
            "pip3  install --user  screeninfo \n")
        run_subprocess("pip3 install --user screeninfo")

if "oxygen":
    # https://github.com/KDE/oxygen-icons5
    if os.path.exists("/usr/share/icons/oxygen"):
        if verbose: print("KDE oxygen icons      [green]are available\n")
    else:
        print("[red]KDE Oxygen icons are not available\n"
        "App will run without error - install icons with\n"
        "`git clone https://github.com/KDE/oxygen-icons.git`\n "
        )

if "Support/images":
    """place to put my default images - ensure availability
    Note: need to cover cases where module run
    - solo in Terminal with 'Run in Konsole'   PWD == HOME
    - solo in IDE terminal                     PWD == Support folder
    - as normal project startup                PWD == project folder
    """

    if "look for Support/images folder":
        _images_folder = ""

        if os.path.isdir(F"{_PWD}/images"):          # for when check_environ run VSCodium
            _images_folder = F"{_PWD}/images"
        elif os.path.isdir(F"{_PWD}/Support/images"):  # for when called by a project
            _images_folder = F"{_PWD}/Support/images"

        if _images_folder:
            if verbose: print(F"Folder Support/images [green] is available as \n"
            F"[purple]   {_images_folder}\n")
        else:
            print(F"[red]Folder Support/images   is not available from\n"
            F"[black]   {_PWD}\n")

if "current user":

    if verbose: print(F"Current user          is [blue]{_USER}")

if "current shell":

    if verbose: print(F"Current shell         is [blue]{_SHELL}")
    if _SHELL == "/usr/bin/zsh":
        CONFIG:str =  '~/.zshrc'
    elif _SHELL == "/usr/bin/bash":
        CONFIG:str =  '~/.bashrc'
    else:
        CONFIG:str =  'UNKOWN'

if "locale":
    try:
        import locale
        if verbose: print(F"Current locale        is[blue] {locale.getlocale()[0]}\n")
    except ModuleNotFoundError:
        print("[red]\nmodule `locale` was not found")

if "virtual environment" and verbose:
    # https://docs.python.org/3/tutorial/venv.html

    if sys.prefix == sys.base_prefix:
        print("running in virtual environment?      [red] False\n")
    else:
        print("running in virtual environment?      [green] True\n")

if "python3_version":

    if sys.version_info[0] == 3 or  sys.version_info[1] >= major:
        if verbose:
            print(F"This script was written for Python version 3.{major}.{micro}\n"
                  "[green]Currently running")
            print(F"{sys.version_info}\n")
    else:
        print(F"This script was written for Python version 3.{major}.{micro}\n"
            "[red]Currently running")
        print(F"{sys.version_info}\n")

if "set PATH":
    """ `pip --user install <package>`   will install <package> into   /home/user/.local/bin
    make sure it is in python's MRO (module resolucion order)    """

    bash_paths = os.environ["PATH"].split(":")
    if F"/home/{_USER}/.local/bin" not in bash_paths:
        print(F"[red]Need to add '/home/{_USER}/.local/bin' to PATH in {CONFIG}")
    elif verbose:
        print("[yellow]Current Bash PATH:")
        print(bash_paths)
        print(F"[yellow]PATH has been updated for '/home/{_USER}/.local/bin'\n"
             F"    (probably in {CONFIG}) \n")

if "PYTHONPATH" and verbose:
    """can be used to update MRO for all python sessions but not normally practical nor needed"""
    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH

    print("[yellow]Current Python MRO:")
    print(sys.path)
    try:
        python_paths = os.environ["PYTHONPATH"].split(":")
        print("[yellow]Current PYTHONPATH")
        print(python_paths)
    except KeyError:
        print("[yellow]PYTHONPATH system variable is apparently not set or needed\n")

if "README.md":
    """markdown file for project related notes, guides, comments, observations, whatever ... """

    if os.path.exists(F"{_PWD}/README.md"):
        if verbose:
            print("[green]local README.md found")
            print(F"[black]{_PWD}/README.md\n")
    else:
        print("[yellow]local README.md not found in")
        print("[black]    {_PWD}\n")

if verbose:
    print("[cyan]Note: This module is optional and only needs to be imported once.\n"
    "Place first in list of imports in main module of a project.")
else:
    print("\n[blue]check_environ module was run\n")

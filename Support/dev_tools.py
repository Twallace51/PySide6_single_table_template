#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""[cyan][bold]Checking if development environment is properly installed ....[not bold]\n
Note:
[green]This module should be always be imported by the main module of a project under development,
since among other things,  `logging` is configured here, for all modules in a project
[black]   import Support/dev-tools
[green]Then,  each project module under development should import the following:"
[black]   from Support/dev_tools import bp, console, log, print, inspect
"""

#pylint disables

    #pylint:disable=empty-docstring, missing-function-docstring, missing-class-docstring, useless-suppression

    #p ylint:disable=import-self
    #p ylint:disable=import-error
    #p ylint:disable=no-member
    #p ylint:disable=no-name-in-module
    #p ylint:disable=unused-import
    #p ylint:disable=unused-wildcard-import
    #p ylint:disable=wildcard-import

    #p ylint:disable=invalid-name
    #p ylint:disable=undefined-variable
    #p ylint:disable=unused-argument
    #p ylint:disable=too-many-lines

verbose = eval("__name__ == '__main__'")    #pylint:disable=eval-used

if "imports":
    import sys
    import os

if "get shell environment":
    _HOME = os.environ['HOME']
    _USER = os.environ['USER']
    _SHELL = os.environ['SHELL'] # /usr/bin/bash or /usr/bin/zsh
    _PWD = os.getcwd()        # os.environ['PWD']  returns /home/$USER if project Run in Konsole
    sys.path.append(_PWD)

if "rich":
    """module provides improved print, inspect and console functions """
    # https://github.com/Textualize/rich
    try:
        import rich                  #pylint:disable=unused-import
    except ModuleNotFoundError:
        print("\u001b[2J\u001b[H") # clear screen
        msg = ("\nrich module not found - install with\n   pip3 install --user rich")
        print(F"\u001b[38;5;196m {msg} \u001b[0m")
        sys.exit() # since following depends on rich imports

    from rich import print    #pylint:disable=redefined-builtin

    from rich import inspect  #pylint:disable=unused-import
    """For comparison,  refer to `inspect` module documentation https://docs.python.org/3/library/inspect.html"""

    from rich.console import Console
    console = Console()

    if verbose:
        console.clear()
        print(__doc__)
        print("rich[green]                  module is available")
        print("[blue]print, console and inspect functions are imported")

if "logging":
    """Allows sending messages to terminal during project execution, including module, method, line
    Usage requires a string argument,  even if only "" - see examples below

    Note: Logging can only be customized by first import of logging module in a project,
    so initial logging configuration,  including rich handler extension,  is placed in this module
    """
    # https://docs.python.org/3/library/logging.html
    # https://docs.python.org/3/howto/logging.html
    # https://rich.readthedocs.io/en/stable/logging.html
    try:
        import logging
    except ModuleNotFoundError:
        print("[red]\n logging module not found - FATAL ERROR"
            "Should have been installed automatically with Python!")
        sys.exit()

    logging.getLogger('asyncio').setLevel(logging.WARNING)

    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format = '%(filename)s:%(lineno)d   %(funcName)s      %(message)s',
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
        )

    log = logging.getLogger("rich")

    if verbose:
        print("\nlogging module        [green]is available and configured")
        print("[blue]\nlogging examples:")
        log.debug("\ndebug msg")
        log.warning("\nwarning msg")
        log.info("\ninformation msg")

if "ipython":
    """Improved Python interpreter and debugger"""
    # https://ipython.org/install.html
    # https://pypi.org/project/ipdb/
    try:
        import ipdb
        bp = ipdb.set_trace
        if verbose: print("\nipython and ipdb      [green]are available and configured")
    except ModuleNotFoundError:
        bp = breakpoint
        print("[yellow]\nOptional IPython support was not found - consider running"
        "    pip3 install -U ipython ipdb")
    if verbose: print(F"breakpoint() shortcut set to  bp() = {bp.__module__}.{bp.__name__}()\n")

if "custom pylintrc":
    # https://pylint.pycqa.org/en/latest/
    if os.path.exists(F"{_PWD}/pylintrc"):
        if verbose: print("local pylintrc      [green] found and will be used for this project\n")
    elif os.path.exists(F"{_HOME}/.config/pylintrc"):
        if verbose: print("[black]~/.config/pylintrc  [green] found and will be used as default settings for current user\n")
    elif os.path.exists("/etc/pylintrc"):
        if verbose: print("/etc/pylintrc       [green] found and used globally by all users\n")
    else:
        print(F"[red]pylintrc       not found locally, in {_HOME}/.config nor in /etc \n")

if "git" and verbose:
    """highly recommended version control """
    if not os.path.isdir(F"{_PWD}/.git"):
        print(".git [yellow]        is not installed in current folder\n"
        F"[purple]   {_PWD}\n")
    else:
        print(F".git [green]       is installed in current folder\n"
        F"[purple]   {_PWD}\n")


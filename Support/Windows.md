# Windows.py classes

## Description

This module tries to provide a better alternative to using QMainMenu for developing windows in a large project,  
including menus, lists, forms and filtering formlist windows.

Better alternative in the sense that

- instead of a window with a ton of attributes that you may not need (or fully understand?),  
  this module allows constructing window objects, with selected specific attributes.
- adds a secure login system for controlling user authority in the project
- adds an easy system to manage navigation from main menu to/from subwindows
- adds project level/global namespaces for windows and variables

Using this class in a project assumes a locally available Support folder is available, with the correct files and icons.  
See [Support/README.md](README.md) file for details.

It is also an general example of using the properties of python classes,  to avoid the problems of

- finding and correcting errors, by avoiding duplicate code sections
- reading and understanding monolithic code blocks, by isolating related code in classes

Finally, this module was written in a style that assumes use of an editor with code folding (VSCodium + pylint recommended)  
Collapse all folds in the module, to see what is effectively a table of contents.

## Note: classes vs templates

The following classes provide a framework for various types of windows for any project,  
allowing import and use of these classes without any customization.

Templates on the otherhand,  are folders/modules that should be copied, renamed and customized,  
to handle events, database records and reports, for a specific project.  
The project folder should have a valid link to a Support folder,  where `Windows.py` and other generic modules can be found.  
See `myWindows-Demo.py` template for an example.

## Note:  about window navigation handlers

The next and previous window handlers in `Windows` are generic and inherited by all `Window` class children.  
They are coded to make window navigation simpler,  with the only requirement is that they must always be used to open/close windows within a project.

All windows, including menus,  use `next_win_handler(<next_window>)` to

- update (push) stack with current window,
- hide current window
- then show indicated window

ToolWindow based windows use `previous_win_handler()` to

- hide current
- automatically reshow (pop) previous window.

## Note: about project scope namespaces

As the base class, `Windows` is convenient for defining project scope attributes

- `win` is for windows managed by WinStack()
- `prj` is for project level or global variables

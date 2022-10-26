# Support folder

This folder is for files that that will shared by multiple projects,  
without requiring customization for any specific project.

# Usage

To use the files in `/Support` during development of a project,  
put a link to this folder in project's folder.

Once development is finished,  make the project folder independent by replacing the link to `/Support` with a local copy of `/Support` folder,  
into which should be copied only those files that have been used by the project.

# Details

Important Support files,   among others are

## generic modules

custom generic python modules - example

- [check_environ.py](check_environ.py)  
run at the beginning of any project to ensure system meets general requirements for all projects

- [screen_info.py](screen_info.py)  
to set some project scope variables like icon path, screen dimensions, etc in `scr` namespace

- [dev_tools.py](dev_tools.py)  
module for setting configurations for optional development utilities,

- [date_time.py](date_time.py)  
ensure a date string is in expected format

For more details,  see  corresponding markdown files.

## customized  classes

- [Windows.py](Windows.py)  
Classes for different types of forms and/or lists  
See [Windows.md](Windows.md) for more details.

- [LoginMenus.py](LoginMenus.py)  
replacement for PySide6.QMainMenu class,  adding
  - default menubar
  - login/logout security features
  - removes often unused QMainMenu features - example docking

  See [LoginMenus.md](LoginMenus.md)  for more details.

## selected images in /images

- [images/win-help.png](images/win-help.png)  
used as a default icon - a place holder image while developing code

- [images/Qt.png](images/Qt.png)

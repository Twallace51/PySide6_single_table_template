# Single Database Table Demo/Template

by twallace51@gmail.com    2022-10-10

This project deals with using PySide6 to manage a database `Archivos`,  with one table named `Pacientes`.

## As a demo

Demo in the sense that I wrote this to demonstrate/test my Support folder,  used as a basis for this project.

The Support folder contains generic files,  in the sense that they can be shared unmodified by different projects.

Support includes

- Class modules `Windows` and `LoginMenu`,  as a more flexible/capable alternative to QMainMenu
- `dev-tools.py` with customized tools useful during project development
- customized methods for dealing with json files, sqlite files, dates, QMessageBoxes, monitor screens, etc
- `check_environ.py` which should be runby a project initially, to ensure correct environment and configurations are available

## As a template

Template in the sense that it can be copied and modified to quickly develop a similar project

Usage:

- copy this file to a new folder
- add a link to Support folder
- create new database
- modify code to use new database

## Details:

### Security

Login is by password only,  initially for users

`Guest(default), User, Admin, Root`

Code sections can test if the current user has authorization to proceed or not,    
which will need to be updated by the developer, depending on the current registered users.  
The default passwords are found in the code.  
Root can access the encripted username:password file to add/delete users and change passwords. 

This is adequate security for casual users,  but the final code should compiled to deter more determined/capable users.  
There is no provision for using an encrypted database however.  

Note:  during development, there is a temporary shortcut to root user login using  
`press Ctrl key + move mouse wheel on image`  
Remove in the final version.

### Database management

Provides management of a simple sqlite database,  using forms to
search, add new, update and delete records

Includes examples of:

- printing screens (forms)
- previewing and printing QDocuments, generated from (filtered) lists
- dated database backups

It should be relatively easy for a developer to create a new database and modify the code to manage it instead.

### Translations

Since the target population for this template is in Latin America (my employees), I included automatic English/Spanish translations.
However, it was easier to simply put the translations in-line,  rather than use QTranslations.
# PySide6_single_table_template

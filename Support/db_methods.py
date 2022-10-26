#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3

"""Goals and Concepts
Methods to open sqlite database and to execute SELECT, DELETE, UPDATE, INSERT statements
with error handling and option for verbose diagnostics during development

See below for usage examples
"""
#pylint:disable=empty-docstring, missing-function-docstring, missing-class-docstring, useless-suppression

if "imports":
    import sys
    import PySide6.QtSql as S
    #pylint:disable=unused-import, redefined-builtin
    try:
        import msg_boxes as mbx
        from dev_tools import bp, log, print, console, inspect
    except ModuleNotFoundError:
        import Support.msg_boxes as mbx
        from Support.dev_tools import bp, log, print, console, inspect

if __name__ == '__main__':
    print("[red][bold]\ndb_methods.py is not designed to run solo\n"
    "[blue]Note: This module should be imported by all project modules, that may need these database functions.")
    sys.exit()

def open_database(_database_name, _verbose_diagnostics=False):
    """ """
    conn = S.QSqlDatabase.addDatabase("QSQLITE")
    conn.setDatabaseName(_database_name)
    if not conn.open("", ""):
        msg1 = F"""Cannot open database {_database_name}, Unable to establish a database connection."""
        print(F"[red]{conn.databaseName()} {msg1}")
        sys.exit(1)

    if _verbose_diagnostics:
        print("\n[green]Database Connection:")
        print(F"con               = {conn}")
        print(F"database name     = {conn.databaseName()}")
        #print(F"conn.lastError()  = {conn.lastError().text()}")
        print(F"conn.tables       = {conn.tables()}", end='  ')

        print("\n\nTable fields:")
        for table_ in conn.tables():
            print(table_.rjust(15), end=" > ")
            count_ = conn.record(table_).count()
            for field_ in range(0, count_):
                print(conn.record(table_).fieldName(field_), end=",  ")
            print()
        print()

def run_query(_sql_str):
    """shared by following """
    query = S.QSqlQuery()
    # query.exec() returns False if query was unsuccessful
    if not query.exec(_sql_str):
        print(F"\n{_sql_str}")
        print(F"[red]\n{query.lastError()}")
        sys.exit(1)
    return query

def run_select(_select_str, _verbose=False):
    """returns query to parent module so can use query.isValid(), query.value(), query.next() as needed
     SELECT [column1, column2, columnN | * ] FROM table_name [WHERE condition]
     SELECT COUNT [* | column_name] FROM table_name [WHERE condition]
     SELECT SUM(column_name) FROM table_name [WHERE condition]
     """

    query = run_query(_select_str)
    query.first()
    if _verbose:
        print(F"\n{query.lastQuery()}")
        if query.isValid():
            if _verbose:
                print("[green]SELECT query successful\n")
            else:
                print("[yellow]query okay but found no records\n")
    return query

def run_insert(_insert_str, _verbose=False):
    """returns query to parent module so can get query.lastInsertId(), if needed
     INSERT INTO table (column1 [, column2, column3 ... ]) VALUES (value1 [, value2, value3 ... ])"""

    query = run_query(_insert_str)
    if _verbose:
        print(F"\n{query.lastQuery()}")
        print(F"[green]INSERT query succesful - inserted to index {query.lastInsertId()}")
    return query

def run_delete(_delete_str, _verbose=False):
    """query returned to parent,  in case needed
     DELETE FROM table_name WHERE [condition];"""

    query = run_query(_delete_str)
    if _verbose:
        print(F"\n{query.lastQuery()}")
        print("[green]DELETE query succesful")
    return query

def run_update(_update_str, _verbose=False):
    """query returned to parent,  in case needed
     UPDATE table_name SET column_name = value [, column_name = value ...] [WHERE condition]"""

    query = run_query(_update_str)
    if _verbose:
        print(F"\n{query.lastQuery()}")
        print("[green]UPDATE query succesful")
    return query

"""Usage Examples

QSqlRecord =  PySide6.QtSql.QSqlDatabase.record(tablename)
field_names_rec = conn.record(tableName)

query = run_select(F"SELECT COUNT(*) FROM {table} {where_str} ", "verbose")
total_rows = query.value(0)

query = run_select(F"SELECT * FROM {table} {where_str} ", not "verbose")
total_columns = query.record().count()

query = run_delete(F"DELETE FROM {table} {where_str} ", not "verbose")



"""

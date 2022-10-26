#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""datetime utilities
Note:
for todays date, use

from datetime import date
print(date.isoformat(date.today()))

"""
# pylint disables
    #pylint:disable=redefined-builtin
    #pylint:disable=unused-import
    #pylint:disable=invalid-name

if "imports":
    import sys
    import datetime
    import re
    try:
        from Support.dev_tools import console, log, bp, print, inspect
    except ModuleNotFoundError:
        from dev_tools import console, log, bp, print, inspect

if __name__ == '__main__':
    console.clear()
    print("[red]\nThis module not designed as a run alone module\n")
    sys.exit(0)

def is_valid_date(date_str):
    """is date_text format 'YYYY-MM-DD' ???
    Does 'YYYY-MM-DD' correspond to a real date ???
    returns boolean"""

    if date_str.strip() == "" or date_str is None:
        return False

    if re.fullmatch("20[0-2][0-9]-[0-1][0-9]-[0-3][0-9]", date_str) is None:
        print(F'[red]date {date_str} is in invalid format')
        return False
    """is 'YYYY-MM-DD' a valid date? """

    Y = int(date_str[0:4])
    M = int(date_str[5:7])
    D = int(date_str[8:10])
    try:
        datetime.date(Y, M, D)
    except ValueError:
        print(F'[red]date {date_str} is an invalid date')
        return False
    return True

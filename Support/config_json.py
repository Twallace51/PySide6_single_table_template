#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utilities for loading and updating json type configuration files

Note: string vs object
    config_json_file below is a file with a serialized comma seperated, key:value string
    config_dict is python key:value dictionary object
    The following functions deal with converting between
    - a file type stream of bytes
    - a python dict type object
"""
# https://docs.python.org/3/library/json.html
# https://realpython.com/python-json/

# pylint disables
    #pylint: disable = redefined-builtin
    #pylint: disable = unused-import

if "imports":
    import json
    import sys

    try:
        from Support.dev_tools import console, log, bp, print, inspect
    except ModuleNotFoundError:
        from dev_tools import console, log, bp, print, inspect

if __name__ == '__main__':
    console.clear()
    print("[red][bold]\nconfig_json.py not designed as a run alone module\n")
    sys.exit(0)

def open_json(config_json_file, verbose=False):
    """returns dict variable with contents of config file,  False if any errors"""

    try:                        # test if config.json present
        with open(config_json_file, "r", encoding='UTF-8') as config_file:

            try:                # test if file has valid JSON data
                if "load text in config.json as a python dict object":
                    config_dict = json.load(config_file)
                    if verbose:
                        print(F"[green]loading {config_json_file} was succesful")
                    return config_dict

            except json.JSONDecodeError:
                if verbose:
                    print(F"[red]{config_json_file} not found - set defaults for current session,  \nthen {config_json_file} should be created/updated when session closes ...")
                return False

    except FileNotFoundError:
        if verbose:
            print(F"[red]{config_json_file} not found - set defaults for current session,  \nthen {config_json_file} should be created/updated when session closes ...")

    return False

def save_json(config_dict, config_json_file, verbose=False):
    try:
        json.dump(config_dict, open(config_json_file, 'w', encoding='UTF-8'))  # todo use with here???   apends or overwrites???
        if verbose:
            print(F"[green]creating/overwriting {config_json_file} was succesful")
    except ModuleNotFoundError:
        if verbose:
            print(F"[red]error in dumping to {config_json_file}")

if __name__ == '__main__':
    print("[red]#todo put test code here\n")

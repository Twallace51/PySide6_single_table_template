#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Decorator functions


This fold contains my custom decorators

"""
#https://peps.python.org/pep-0318/
#https://realpython.com/primer-on-python-decorators/
#https://everyday.codes/python/why-do-you-need-decorators-in-your-python-code/

if "debugging decorator":
    """
    decorator that sends to terminal the name, arguments and return value of decorated function
    - returns a subclassed function
    - handles arbitrary new function arguments
    - returns original function return values
    """
    def print_debugger(fxn):
        def new_function(*args, **kwargs):
            print(F"Calling {fxn.__name__} with {args = } and {kwargs = }.")
            ret = fxn(*args, **kwargs)
            print(F"Done with result = {ret}.")
            return ret
        return new_function

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date        : Tue Oct 20 00:02:56 CEST 2020
Autor       : Leonid Burmistrov
Description : Simple example of a decorators in Python.

              A decorator is a design pattern in Python that allows a
              user to add new functionality to an existing object without 
              modifying its structure. Decorators are usually 
              called before the definition of a function you want 
              to decorate.

              Functions in Python are first class citizens. 
              This means that they support operations such as 
              being passed as an argument, returned from a function, 
              modified, and assigned to a variable. 
              
              This is a fundamental concept to understand Python decorators.
"""

import json
import os.path

def plus_one_old(number):
    """
    Simple increment of one
    @param number to be incremented by 1 
    """
    return number + 1

def plus_one(number):
    """
    Defining Functions Inside other Functions
    """
    def add_one_new(number):
        return number + 1
    result = add_one_new(number)
    return result

def function_call(function):
    """
    Passing Functions as Arguments to other Functions
    """
    number_to_add = 3
    return function(number_to_add)

def hello_function():
    """
    Functions Returning other Functions
    """
    def say_hi():
        return "Hi"
    return say_hi

def print_message(message):
    """
    Nested Functions have access to the Enclosing Function's 
    Variable Scope.
    Enclosing Function
    """
    def message_sender():
        """
        Nested Function
        """
        print(message)
    message_sender()

def uppercase_decorator(function):
    """
    Creating Decorators
    """
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

def split_string(function):
    """
    Creating Decorators
    """
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string

    return wrapper


def say_hello():
    return "hello there"

@uppercase_decorator
def say_hello_deco():
    return "hello there"

@split_string
@uppercase_decorator
def say_hello_deco_deco():
    return "hello there"
    
def main():
    add_one = plus_one
    print(add_one(5))
    print(plus_one(4))
    print(function_call(plus_one))
    print(hello_function())
    hello = hello_function()
    print(hello())
    print_message("Some random message")
    #############
    decorate = uppercase_decorator(say_hello)
    print(decorate())
    print(say_hello_deco())
    print(say_hello_deco_deco())
    #############
    print('plus_one_old.__name__ : ', plus_one_old.__name__)
    print('plus_one_old.__doc__  : ', plus_one_old.__doc__)

if __name__ == "__main__":
    """
    Run as main script (use for testing only)
    """
    main()

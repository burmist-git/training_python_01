#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date        : Tue Oct 20 11:18:08 CEST 2020
Autor       : Leonid Burmistrov
Description : Example of the simple class in Python.
"""

class student:
    """
    Simple class to demonstrate self
    """
    def __init__(self,name):
        """
        Constructor
        @param name : student name
        """
        self.name = name
        self.marks = []
        print("Hi {}".format(name))
        
    def addmarks(self,mark):
        """
        Function to add marks
        @param mark : student mark
        """
        self.marks.append(mark)
        
    def avg(self):
        """
        Function to add marks
        @param mark : Function to calculate average mark
        """
        return sum(self.marks)/len(self.marks)

class animal(object):
    def __init__(self, name):
        self.name = name
    def fly(self):
        print('{} is flying or it is not flying ?'.format(self.name))

class dog(animal):
    """
    Class to demonstrate constructor overloading (super())
    """
    def __init__(self, name, food):
        super (dog, self).__init__(name)
        self.food = food
    def fly(self):
        print('{} can not fly.'.format(self.name))
    def eat(self):
        print('{} is fetching {}'.format(self.name, self.food))

class A(object):
    def __init__(self):
        pass
    def printThis(self):
        print('Doing this in A')
        
class B(A):
    def printBC(slef):
        print('This is B')

class C(object):
    def printThis(self):
        print('Doing this in C')
    def printBC(slef):
        print('This is C')

class D(B,C):
    """
    Multiple inheritance - depth - first
    """
    pass

class E(C,B):
    pass

class F(C,B):
    def printBC(slef):
        print('This is F')
        
def main():
    s = student('leonid')
    s.addmarks(5)
    s.addmarks(5)
    s.addmarks(4)
    s.addmarks(5)
    s.addmarks(5)
    print(s.marks)
    print(s.avg())
    print('student.__name__          : ', student.__name__)
    print('student.__doc__           : ', student.__doc__)
    print('student.__dir__           : ', student.__dir__)
    print('student.__getattribute__  : ', student.__getattribute__)
    print('student.__module__        : ', student.__module__)
    print('')
    print('student.addmarks.__name__ : ', student.addmarks.__name__)
    print('student.addmarks.__doc__  : ', student.addmarks.__doc__)
    print(dir(student))
    print('')
    print('dog.__name__              : ', dog.__name__)
    print('dog.__doc__               : ', dog.__doc__)
    print(dir(dog))
    print('')
    a = animal('Generic animal')
    a.fly()
    d = dog('Wolf','meat')
    d.fly()
    d.eat()
    print('')
    print('D.__name__                 : ', D.__name__)
    print('D.__doc__                  : ', D.__doc__)
    print('D.__mro__                  : ', D.__mro__)
    print(dir(dog))
    print('')
    A().printThis()
    B().printThis()
    C().printThis()
    D().printThis()
    D().printBC()
    E().printBC()
    F().printBC()
    
if __name__ == "__main__":
    print(__name__)
    main()

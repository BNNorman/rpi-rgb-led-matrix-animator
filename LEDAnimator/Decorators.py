'''
Decorators.py

Tools for debugging

from stackoverflow.com

use like this:-

from LedAnimator.Decorators import *

then

@benchmark
def myfunction():
    blah

'''

def benchmark(func):
    """
    a decorator to print the time a function takes to execute

    This decorator expects to precede a class function as it uses arg[0] to get
    the class name

    :param func func: The function to execute
    :return : whatever func returns
    """
    import time
    def wrapper(*args,**kwargs):
        t1=time.clock()
        result=func(*args,**kwargs)
        t2=time.clock()

        # did we call a class method or a function?
        try:
            x=str(type(args[0]))
            if x[1:6]=="class":
                print args[0].__class__.__name__,"{0}() ran for {1:f}s".format(func.__name__,t2-t1)
            else:
                print "{0}() ran for {1:f}s".format(func.__name__, t2 - t1)
        except IndexError:
            print "{0}() ran for {1:f}s".format(func.__name__, t2 - t1)

        return result
    return wrapper

def logging(func):
    """
    Just an example - prints the function anme and arguments
    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        result=func(*args,**kwargs)
        # did we call a class method or a function?
        try:
            x = str(type(args[0]))
            if x[1:6] == "class":
                print args[0].__class__.__name__, "{0}() ran for {1:f}s".format(func.__name__, t2 - t1)
            else:
                print "{0}() ran for {1:f}s".format(func.__name__, t2 - t1)
        except IndexError:
            print "{0}() ran for {1:f}s".format(func.__name__, t2 - t1)
        return result

    return wrapper


def counter(func):
    """
    counts the number of times a method has been called
    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        wrapper.count+=1
        result=func(*args,**kwargs)
        # did we call a class method or a function?
        try:
            x = str(type(args[0]))
            if x[1:6] == "class":
                print args[0].__class__.__name__, " has been used {1} times".format(func.__name__, wrapper.count)
            else:
                print "{0} has been used {1} times".format(func.__name__, wrapper.count)
        except IndexError:
            print "{0} has been used {1} times".format(func.__name__, wrapper.count)
        return result

    wrapper.count=0
    return wrapper

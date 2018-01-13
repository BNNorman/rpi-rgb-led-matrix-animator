"""
PathSetter.py

Solves a problem running the examples on the Pi where the parent folder isn't on the sys.path

"""

import sys
import os.path


parent=os.path.abspath(os.path.join(os.getcwd(), os.pardir))

if not parent in sys.path:
    sys.path.insert(0,parent)
    print "PathSetter.py: Parent folder added to sys.path"
else:
    print "PathSetter.py: Parent folder [",parent,"] already exists in sys.path"







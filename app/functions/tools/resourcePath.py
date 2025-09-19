import sys
import os 

def resourcePath():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    else:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

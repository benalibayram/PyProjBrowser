# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:17:42 2021

@author: benal
"""

"""A setup script to demonstrate the use of sqlite3"""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ScanGUI",
    version="0.1",
    description="MRI scan GUI with SQLite3",
    executables=[Executable("ScanGUI.py", base=base)],
)
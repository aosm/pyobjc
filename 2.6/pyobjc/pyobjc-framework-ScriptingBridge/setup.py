''' 
Wrappers for the "ScriptingBrige" framework on MacOSX 10.5 or later. This 
framework provides an easy way to use the scripting functionality of 
applications ("AppleScript") from Cocoa applications.

The functionality of this framework is comparable to that off "appscript",
although the latter is better tuned for use in Python applications and is
available on MacOSX 10.4 as well.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import *

setup(
    min_os_level='10.5',
    name='pyobjc-framework-ScriptingBridge',
    version="2.3.2a0",
    description = "Wrappers for the framework ScriptingBridge on Mac OS X",
    packages = [ "ScriptingBridge" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
    ],
)

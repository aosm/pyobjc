''' 
Wrappers for "InstantMessage" framework on MacOSX 10.5 or later. This framework
allows you to access iChat information, as well as a way to provide an 
auxilliary video source to iChat Theater.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import setup
setup(
    min_os_level='10.5',
    name='pyobjc-framework-InstantMessage',
    version="2.3.2a0",
    description = "Wrappers for the framework InstantMessage on Mac OS X",
    packages = [ "InstantMessage" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
        'pyobjc-framework-Quartz>=2.3.2a0',
    ],
)

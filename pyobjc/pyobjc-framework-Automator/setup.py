''' 
Wrappers for the "Automator" framework on MacOSX. The Automator framework
supports the development of actions for the Automator application, as well 
as the ability to run a workflow in developer applications. An action is 
a bundle that, when loaded and run, performs a specific task.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import setup

setup(
    name='pyobjc-framework-Automator',
    version="2.3.2a0",
    description = "Wrappers for the framework Automator on Mac OS X",
    packages = [ "Automator" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
    ],
)

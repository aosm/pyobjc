''' 
Wrappers for the "CoreData" framework on MacOSX. The Core Data framework 
provides generalized and automated solutions to common tasks associated 
with object life-cycle and object graph management, including persistence.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import *
setup(
    name='pyobjc-framework-CoreData',
    version="2.3.2a0",
    description = "Wrappers for the framework CoreData on Mac OS X",
    packages = [ "CoreData" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
    ],
)

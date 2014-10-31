''' 
Wrappers for the "SearchKit" framework on MacOSX. SearchKit is a content
indexing and search solution.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks

NOTE: These wrappers are pretty fragile, sadly enough not all run-time
information that needed to build reliable wrappers is exported from 
the framework.
'''
from pyobjc_setup import setup

setup(
    min_os_level='10.5',
    name='pyobjc-framework-SearchKit',
    version="2.3.2a0",
    description = "Wrappers for the framework SearchKit on Mac OS X",
    packages = [ "SearchKit" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
    ],
)

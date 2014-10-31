''' 
Wrappers for the "SyncServices" framework on MacOSX. 

Sync Services is a framework containing all the components you need 
to sync your applications and devices. If your application uses 
Sync Services, user data can be synced with other applications and 
devices on the same computer, or other computers over the network via 
MobileMe.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import setup

setup(
    name='pyobjc-framework-SyncServices',
    version="2.3.2a0",
    description = "Wrappers for the framework SyncServices on Mac OS X",
    packages = [ "SyncServices" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
        'pyobjc-framework-CoreData>=2.3.2a0',
    ],
)

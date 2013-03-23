''' 
Wrappers for the "CalendarStore" on MacOSX 10.5 and later. The CalendarStore
frameworks provides access to the iCal data. It's possible to fetch iCal
records, such as calendars and tasks, as well as modify them and get 
notifications when records change in iCal.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
'''
from pyobjc_setup import setup

setup(
    min_os_level='10.5',
    name='pyobjc-framework-CalendarStore',
    version="2.3.2a0",
    description = "Wrappers for the framework CalendarStore on Mac OS X",
    packages = [ "CalendarStore" ],
    install_requires = [ 
        'pyobjc-core>=2.3.2a0',
        'pyobjc-framework-Cocoa>=2.3.2a0',
    ],
)

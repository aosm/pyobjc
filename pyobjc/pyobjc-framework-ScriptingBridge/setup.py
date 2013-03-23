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
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
try:
    from PyObjCMetaData.commands import extra_cmdclass, extra_options
except ImportError:
    extra_cmdclass = {}
    extra_options = lambda name: {}

setup(
    name='pyobjc-framework-ScriptingBridge',
    version='2.2b3',
    description = "Wrappers for the framework ScriptingBridge on Mac OS X",
    long_description = __doc__,
    author='Ronald Oussoren',
    author_email='pyobjc-dev@lists.sourceforge.net',
    url='http://pyobjc.sourceforge.net',
    platforms = [ "MacOS X" ],
    packages = [ "ScriptingBridge" ],
    package_dir = { '': 'Lib' },
    install_requires = [ 
        'pyobjc-core>=2.2b3',
        'pyobjc-framework-Cocoa>=2.2b3',
    ],
    package_data = { 
        '': ['*.bridgesupport'] 
    },
    test_suite='PyObjCTest',
    cmdclass = extra_cmdclass,
    options = extra_options('ScriptingBridge'),
    zip_safe = True,
)

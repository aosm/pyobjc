#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

import sys
import os
import glob
import site
import platform

if 'MallocStackLogging' in os.environ:
    del os.environ['MallocStackLogging']
if 'MallocStackLoggingNoCompact' in os.environ:
    del os.environ['MallocStackLoggingNoCompact']

# See the news file:
#os.environ['MACOSX_DEPLOYMENT_TARGET']='10.5'

# We need at least Python 2.3
MIN_PYTHON = (2, 3)

if sys.version_info < MIN_PYTHON:
    vstr = '.'.join(map(str, MIN_PYTHON))
    raise SystemExit('PyObjC: Need at least Python ' + vstr)

USE_SYSTEM_FFI = False
if int(os.uname()[2].split('.')[0]) >= 10:
	USE_SYSTEM_FFI = True

SDKROOT = os.environ.get('SDKROOT')
if SDKROOT is None or SDKROOT is '':
    SDKROOT = '/'
def fixsdk(arg):
    if arg.startswith('-I/'):
        arg = '-I' + os.path.join(SDKROOT, arg[3:])
    elif arg.startswith('-L/'):
        arg = '-L' + os.path.join(SDKROOT, arg[3:])
    return arg


# Some PiPy stuff
LONG_DESCRIPTION="""
PyObjC is a bridge between Python and Objective-C.  It allows full
featured Cocoa applications to be written in pure Python.  It is also
easy to use other frameworks containing Objective-C class libraries
from Python and to mix in Objective-C, C and C++ source.

Python is a highly dynamic programming language with a shallow learning
curve.  It combines remarkable power with very clear syntax.

The installer package installs a number of Xcode templates for
easily creating new Cocoa-Python projects.

PyObjC also supports full introspection of Objective-C classes and
direct invocation of Objective-C APIs from the interactive interpreter.

PyObjC requires MacOS X 10.4 or later.  This beta release requires
MacOS X 10.5.
"""

from setuptools import setup, Extension, find_packages
from setuptools.command import build_ext, install_lib
import os

class pyobjc_install_lib (install_lib.install_lib):
    def get_exclusions(self):
        result = install_lib.install_lib.get_exclusions(self)
        for fn in install_lib._install_lib.get_outputs(self):
	    if 'PyObjCTest' in fn:
                result[fn] = 1

	return result

class pyobjc_build_ext (build_ext.build_ext):
    def run(self):
        build_ext.build_ext.run(self)
        extensions = self.extensions
        self.extensions = [
                e for e in extensions if e.name.startswith('PyObjCTest') ]
        self.copy_extensions_to_source()
        self.extensions = extensions

def frameworks(*args):
    lst = []
    for arg in args:
        lst.extend(['-framework', arg])
    return lst

def IfFrameWork(name, packages, extensions, headername=None):
    """
    Return the packages and extensions if the framework exists, or
    two empty lists if not.
    """
    import os
    for pth in ('/System/Library/Frameworks', '/Library/Frameworks'):
        basedir = os.path.join(pth, name)
        if os.path.exists(basedir):
            if (headername is None) or os.path.exists(os.path.join(basedir, "Headers", headername)):
                return packages, extensions
    return [], []

# Double-check
if sys.platform != 'darwin':
    print "You're not running on MacOS X, and don't use GNUstep"
    print "I don't know how to build PyObjC on such a platform."
    print "Please read the ReadMe."
    print ""
    raise SystemExit("ObjC runtime not found")

from distutils.sysconfig import get_config_var
cc = get_config_var('CC')

CFLAGS=[ ]

if cc == 'XXXgcc':
    # This is experimental code that tries to avoid refering to files in 
    # /Library/Frameworks or /usr/local.
    # 
    # NOTE: This is not enabled by default because the linker will still look
    # in /usr/local/lib and /Library/Frameworks...

    fp = os.popen('cpp -v </dev/null 2>&1', 'r')
    dirs = []
    started = False
    for ln in fp:
        if not started:
            if ln.startswith('#include <...> search starts here:'):
                started=True
            continue

        else:
            ln = ln.strip()
            if not ln.startswith('/'):
                break

            if ln == '/usr/local/include':
                continue

            elif ln == '/Library/Frameworks':
                continue

            if ln.endswith('(framework directory)'):
                dirs.append(('framework', ln.split()[0]))
            else:
                dirs.append(('system', ln))

    if dirs:
        CFLAGS.append('-nostdinc')
        for k, d in dirs:
            CFLAGS.append('-i%s%s'%(k,d))

# Enable 'PyObjC_STRICT_DEBUGGING' to enable some costly internal 
# assertions. 
CFLAGS.extend([

# The following flags are an attempt at getting rid of /usr/local
# in the compiler search path.
    "-DPyObjC_STRICT_DEBUGGING",
    "-DMACOSX", # For libffi
    "-DPyObjC_BUILD_RELEASE=%02d%02d"%(tuple(map(int, platform.mac_ver()[0].split('.')[:2]))),
    #"-Wno-long-double",
    #"-Wselector",
    #"-Wstrict-overflow",
    "-g",
    #"-fobjc-gc",
    "-fexceptions",

    ## Arghh, a stupid compiler flag can cause problems. Don't 
    ## enable -O0 if you value your sanity. With -O0 PyObjC will crash
    ## on i386 systems when a method returns a struct that isn't returned
    ## in registers. 
    #"-O0",
    "-O1",
    #"-O2",
    #"-O3",
    #'-arch', 'x86_64', '-arch', 'ppc64',

    # Loads of warning flags
    "-Wall", "-Wstrict-prototypes", "-Wmissing-prototypes",
    "-Wformat=2", "-W", "-Wshadow",
    "-Wpointer-arith", #"-Wwrite-strings",
    "-Wmissing-declarations",
    "-Wnested-externs",
    "-Wno-long-long",
    #"-Wfloat-equal",

    # These two are fairly useless:
    #"-Wunreachable-code",
    #"-pedantic",

    "-Wno-import",
    #"-Werror",

    # use the same optimization as Python, probably -O3,
    # but can be overrided by one of the following:

    # no optimization, for debugging
    #"-O0",

    # g4 optimized
    #"-fast", "-fPIC", "-mcpu=7450",

    # g5 optimized
    #"-fast", "-fPIC",
    ])


OBJC_LDFLAGS = frameworks('CoreFoundation', 'Foundation', 'Carbon')

if not os.path.exists(os.path.join(SDKROOT, 'usr/include/objc/runtime.h')):
    CFLAGS.append('-DNO_OBJC2_RUNTIME')

else:
    # Force compilation with the local SDK, compilation of PyObC will result in
    # a binary that runs on other releases of the OS without using a particular SDK.
    CFLAGS.extend([])
    OBJC_LDFLAGS.extend([])


# We're using xml2, check for the flags to use:
def xml2config(arg):
    import os, shlex
    ln = os.popen('xml2-config %s'%(arg,), 'r').readline()
    ln = ln.strip()

    return map(fixsdk, shlex.split(ln))

CFLAGS.extend(xml2config('--cflags'))
OBJC_LDFLAGS.extend(xml2config('--libs'))



CFLAGS.append('-Ibuild/codegen/')

# Patch distutils: it needs to compile .S files as well.
from distutils.unixccompiler import UnixCCompiler
UnixCCompiler.src_extensions.append('.S')
del UnixCCompiler


# 
# Support for an embedded copy of libffi
#
FFI_CFLAGS=['-Ilibffi-src/include', '-Ilibffi-src/powerpc']

# The list below includes the source files for all CPU types that we run on
# this makes it easier to build fat binaries on Mac OS X.
FFI_SOURCE=[
    "libffi-src/ffi.c",
    "libffi-src/types.c",
    "libffi-src/powerpc/ppc-darwin.S",
    "libffi-src/powerpc/ppc-darwin_closure.S",
    "libffi-src/powerpc/ppc-ffi_darwin.c",
    "libffi-src/powerpc/ppc64-darwin_closure.S",
    "libffi-src/x86/darwin64.S",
    "libffi-src/x86/x86-darwin.S",
    "libffi-src/x86/x86-ffi64.c",
    "libffi-src/x86/x86-ffi_darwin.c",
]



#
# Calculate the list of extensions: objc._objc + extensions for the unittests
#

if USE_SYSTEM_FFI:
	ExtensionList =  [ 
	    Extension("objc._objc",
		list(glob.glob(os.path.join('Modules', 'objc', '*.m'))),
		extra_compile_args=CFLAGS + ['-I' + os.path.join(SDKROOT, "usr/include/ffi")],
		extra_link_args=OBJC_LDFLAGS + ["-lffi"],
	    )
	]

else:
	ExtensionList =  [ 
	    Extension("objc._objc",
		FFI_SOURCE + list(glob.glob(os.path.join('Modules', 'objc', '*.m'))),
		extra_compile_args=CFLAGS + FFI_CFLAGS,
		extra_link_args=OBJC_LDFLAGS,
	    )
	]

for test_source in glob.glob(os.path.join('Modules', 'objc', 'test', '*.m')):
    name, ext = os.path.splitext(os.path.basename(test_source))

    ExtensionList.append(Extension('PyObjCTest.' + name,
        [test_source],
        extra_compile_args=['-IModules/objc'] + CFLAGS,
        extra_link_args=OBJC_LDFLAGS))

def package_version():
    fp = open('Modules/objc/pyobjc.h', 'r')
    for ln in fp.readlines():
        if ln.startswith('#define OBJC_VERSION'):
            fp.close()
            return ln.split()[-1][1:-1]

    raise ValueError, "Version not found"

CLASSIFIERS = filter(None,
"""
Development Status :: 5 - Production/Stable
Environment :: Console
Environment :: MacOS X :: Cocoa
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Natural Language :: English
Operating System :: MacOS :: MacOS X
Programming Language :: Python
Programming Language :: Objective C
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: User Interfaces
""".splitlines())

dist = setup(
    name = "pyobjc-core", 
    version = package_version(),
    description = "Python<->ObjC Interoperability Module",
    long_description = LONG_DESCRIPTION,
    author = "Ronald Oussoren, bbum, SteveM, LeleG, many others stretching back through the reaches of time...",
    author_email = "pyobjc-dev@lists.sourceforge.net",
    url = "http://pyobjc.sourceforge.net/",
    platforms = [ 'MacOS X' ],
    ext_modules = ExtensionList,
    packages = [ 'objc', 'PyObjCTools' ], 
    #namespace_packages = ['PyObjCTools'],
    package_dir = { '': 'Lib', 'PyObjCTest': 'PyObjCTest' },
    extra_path = "PyObjC",
    cmdclass = {'build_ext': pyobjc_build_ext, 'install_lib': pyobjc_install_lib },
    options = {'egg_info': {'egg_base': 'Lib'}},
    classifiers = CLASSIFIERS,
    license = 'MIT License',
    download_url = 'http://pyobjc.sourceforge.net/software/index.php',
    test_suite='PyObjCTest.loader.makeTestSuite',
    zip_safe = False,
)

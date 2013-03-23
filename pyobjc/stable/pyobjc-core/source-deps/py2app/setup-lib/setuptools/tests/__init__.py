"""Tests for the 'setuptools' package"""

from unittest import TestSuite, TestCase, makeSuite
import distutils.core, distutils.cmd
from distutils.errors import DistutilsOptionError, DistutilsPlatformError
from distutils.errors import DistutilsSetupError
import setuptools, setuptools.dist
from setuptools import Feature
from distutils.core import Extension
from setuptools.depends import extract_constant, get_module_constant
from setuptools.depends import find_module, Require
from distutils.version import StrictVersion, LooseVersion
from distutils.util import convert_path
import sys, os.path


def makeSetup(**args):
    """Return distribution from 'setup(**args)', without executing commands"""

    distutils.core._setup_stop_after = "commandline"

    # Don't let system command line leak into tests!
    args.setdefault('script_args',['install'])

    try:
        return setuptools.setup(**args)
    finally:
        distutils.core_setup_stop_after = None













class DependsTests(TestCase):

    def testExtractConst(self):

        from setuptools.depends import extract_constant

        def f1():
            global x,y,z
            x = "test"
            y = z

        # unrecognized name
        self.assertEqual(extract_constant(f1.func_code,'q', -1), None)

        # constant assigned
        self.assertEqual(extract_constant(f1.func_code,'x', -1), "test")

        # expression assigned
        self.assertEqual(extract_constant(f1.func_code,'y', -1), -1)

        # recognized name, not assigned
        self.assertEqual(extract_constant(f1.func_code,'z', -1), None)


    def testFindModule(self):
        self.assertRaises(ImportError, find_module, 'no-such.-thing')
        self.assertRaises(ImportError, find_module, 'setuptools.non-existent')
        f,p,i = find_module('setuptools.tests'); f.close()

    def testModuleExtract(self):
        from distutils import __version__
        self.assertEqual(
            get_module_constant('distutils','__version__'), __version__
        )
        self.assertEqual(
            get_module_constant('sys','version'), sys.version
        )
        self.assertEqual(
            get_module_constant('setuptools.tests','__doc__'),__doc__
        )

    def testRequire(self):

        req = Require('Distutils','1.0.3','distutils')

        self.assertEqual(req.name, 'Distutils')
        self.assertEqual(req.module, 'distutils')
        self.assertEqual(req.requested_version, '1.0.3')
        self.assertEqual(req.attribute, '__version__')
        self.assertEqual(req.full_name(), 'Distutils-1.0.3')

        from distutils import __version__
        self.assertEqual(req.get_version(), __version__)
        self.failUnless(req.version_ok('1.0.9'))
        self.failIf(req.version_ok('0.9.1'))
        self.failIf(req.version_ok('unknown'))

        self.failUnless(req.is_present())
        self.failUnless(req.is_current())

        req = Require('Distutils 3000','03000','distutils',format=LooseVersion)
        self.failUnless(req.is_present())
        self.failIf(req.is_current())
        self.failIf(req.version_ok('unknown'))

        req = Require('Do-what-I-mean','1.0','d-w-i-m')
        self.failIf(req.is_present())
        self.failIf(req.is_current())

        req = Require('Tests', None, 'tests', homepage="http://example.com")
        self.assertEqual(req.format, None)
        self.assertEqual(req.attribute, None)
        self.assertEqual(req.requested_version, None)
        self.assertEqual(req.full_name(), 'Tests')
        self.assertEqual(req.homepage, 'http://example.com')

        paths = [os.path.dirname(p) for p in __path__]
        self.failUnless(req.is_present(paths))
        self.failUnless(req.is_current(paths))



    def testDependsCmd(self):
        path1 = convert_path('foo/bar/baz')
        path2 = convert_path('foo/bar/baz/spam')

        dist = makeSetup(
            extra_path='spam',
            script_args=[
                'install','--install-lib',path1, '--prefix',path2,
                'build','--compiler=mingw32',
            ]
        )

        cmd = dist.get_command_obj('depends')
        cmd.ensure_finalized()

        self.assertEqual(cmd.temp, dist.get_command_obj('build').build_temp)
        self.assertEqual(cmd.search_path, [path2,path1]+sys.path)

        self.assertEqual(cmd.unsafe_options,
            {'install':['--install-lib',path1]}
        )
        self.assertEqual(cmd.safe_options, {
            'build':['--compiler','mingw32'],
            'install':['--prefix',os.path.abspath(path2)]
        })
















class DistroTests(TestCase):

    def setUp(self):
        self.e1 = Extension('bar.ext',['bar.c'])
        self.e2 = Extension('c.y', ['y.c'])

        self.dist = makeSetup(
            packages=['a', 'a.b', 'a.b.c', 'b', 'c'],
            py_modules=['b.d','x'],
            ext_modules = (self.e1, self.e2),
            script_args = [
                'build', '-q', 'build_ext', '-i',
                'install', '--prefix=/usr/lib', '--install-lib','/test'
            ],
            package_dir = {},
        )


    def testDistroType(self):
        self.failUnless(isinstance(self.dist,setuptools.dist.Distribution))


    def testExcludePackage(self):
        self.dist.exclude_package('a')
        self.assertEqual(self.dist.packages, ['b','c'])

        self.dist.exclude_package('b')
        self.assertEqual(self.dist.packages, ['c'])
        self.assertEqual(self.dist.py_modules, ['x'])
        self.assertEqual(self.dist.ext_modules, [self.e1, self.e2])

        self.dist.exclude_package('c')
        self.assertEqual(self.dist.packages, [])
        self.assertEqual(self.dist.py_modules, ['x'])
        self.assertEqual(self.dist.ext_modules, [self.e1])

        # test removals from unspecified options
        makeSetup().exclude_package('x')



    def testIncludeExclude(self):
        # remove an extension
        self.dist.exclude(ext_modules=[self.e1])
        self.assertEqual(self.dist.ext_modules, [self.e2])

        # add it back in
        self.dist.include(ext_modules=[self.e1])
        self.assertEqual(self.dist.ext_modules, [self.e2, self.e1])

        # should not add duplicate
        self.dist.include(ext_modules=[self.e1])
        self.assertEqual(self.dist.ext_modules, [self.e2, self.e1])

    def testExcludePackages(self):
        self.dist.exclude(packages=['c','b','a'])
        self.assertEqual(self.dist.packages, [])
        self.assertEqual(self.dist.py_modules, ['x'])
        self.assertEqual(self.dist.ext_modules, [self.e1])

    def testEmpty(self):
        dist = makeSetup()
        dist.include(packages=['a'], py_modules=['b'], ext_modules=[self.e2])
        dist = makeSetup()
        dist.exclude(packages=['a'], py_modules=['b'], ext_modules=[self.e2])

    def testContents(self):
        self.failUnless(self.dist.has_contents_for('a'))
        self.dist.exclude_package('a')
        self.failIf(self.dist.has_contents_for('a'))

        self.failUnless(self.dist.has_contents_for('b'))
        self.dist.exclude_package('b')
        self.failIf(self.dist.has_contents_for('b'))

        self.failUnless(self.dist.has_contents_for('c'))
        self.dist.exclude_package('c')
        self.failIf(self.dist.has_contents_for('c'))




    def testInvalidIncludeExclude(self):
        self.assertRaises(DistutilsSetupError,
            self.dist.include, nonexistent_option='x'
        )
        self.assertRaises(DistutilsSetupError,
            self.dist.exclude, nonexistent_option='x'
        )
        self.assertRaises(DistutilsSetupError,
            self.dist.include, packages={'x':'y'}
        )
        self.assertRaises(DistutilsSetupError,
            self.dist.exclude, packages={'x':'y'}
        )
        self.assertRaises(DistutilsSetupError,
            self.dist.include, ext_modules={'x':'y'}
        )
        self.assertRaises(DistutilsSetupError,
            self.dist.exclude, ext_modules={'x':'y'}
        )

        self.assertRaises(DistutilsSetupError,
            self.dist.include, package_dir=['q']
        )
        self.assertRaises(DistutilsSetupError,
            self.dist.exclude, package_dir=['q']
        )

    def testCmdLineOpts(self):
        self.assertEqual(self.dist.get_cmdline_options(),
            {   'install':{'prefix':'/usr/lib', 'install-lib':'/test'},
                'build': {'quiet':None}, 'build_ext':{'inplace':None},
            }
        )








class FeatureTests(TestCase):

    def setUp(self):
        self.req = Require('Distutils','1.0.3','distutils')
        self.dist = makeSetup(
            features={
                'foo': Feature("foo",standard=True,requires=['baz',self.req]),
                'bar': Feature("bar",  standard=True, packages=['pkg.bar'],
                               py_modules=['bar_et'], remove=['bar.ext'],
                       ),
                'baz': Feature(
                        "baz", optional=False, packages=['pkg.baz'],
                        scripts = ['scripts/baz_it'],
                        libraries=[('libfoo','foo/foofoo.c')]
                       ),
                'dwim': Feature("DWIM", available=False, remove='bazish'),
            },
            script_args=['--without-bar', 'install'],
            packages = ['pkg.bar', 'pkg.foo'],
            py_modules = ['bar_et', 'bazish'],
            ext_modules = [Extension('bar.ext',['bar.c'])]
        )

    def testDefaults(self):
        self.failIf(
            Feature(
                "test",standard=True,remove='x',available=False
            ).include_by_default()
        )
        self.failUnless(
            Feature("test",standard=True,remove='x').include_by_default()
        )
        # Feature must have either kwargs, removes, or requires
        self.assertRaises(DistutilsSetupError, Feature, "test")

    def testAvailability(self):
        self.assertRaises(
            DistutilsPlatformError,
            self.dist.features['dwim'].include_in, self.dist
        )

    def testFeatureOptions(self):
        dist = self.dist
        self.failUnless(
            ('with-dwim',None,'include DWIM') in dist.feature_options
        )
        self.failUnless(
            ('without-dwim',None,'exclude DWIM (default)') in dist.feature_options
        )
        self.failUnless(
            ('with-bar',None,'include bar (default)') in dist.feature_options
        )
        self.failUnless(
            ('without-bar',None,'exclude bar') in dist.feature_options
        )
        self.assertEqual(dist.feature_negopt['without-foo'],'with-foo')
        self.assertEqual(dist.feature_negopt['without-bar'],'with-bar')
        self.assertEqual(dist.feature_negopt['without-dwim'],'with-dwim')
        self.failIf('without-baz' in dist.feature_negopt)

    def testUseFeatures(self):
        dist = self.dist
        self.assertEqual(dist.with_foo,1)
        self.assertEqual(dist.with_bar,0)
        self.assertEqual(dist.with_baz,1)
        self.failIf('bar_et' in dist.py_modules)
        self.failIf('pkg.bar' in dist.packages)
        self.failUnless('pkg.baz' in dist.packages)
        self.failUnless('scripts/baz_it' in dist.scripts)
        self.failUnless(('libfoo','foo/foofoo.c') in dist.libraries)
        self.assertEqual(dist.ext_modules,[])
        self.assertEqual(dist.requires, [self.req])

        # If we ask for bar, it should fail because we explicitly disabled
        # it on the command line
        self.assertRaises(DistutilsOptionError, dist.include_feature, 'bar')

    def testFeatureWithInvalidRemove(self):
        self.assertRaises(
            SystemExit, makeSetup, features = {'x':Feature('x', remove='y')}
        )

class TestCommandTests(TestCase):

    def testTestIsCommand(self):
        test_cmd = makeSetup().get_command_obj('test')
        self.failUnless(isinstance(test_cmd, distutils.cmd.Command))

    def testLongOptSuiteWNoDefault(self):
        ts1 = makeSetup(script_args=['test','--test-suite=foo.tests.suite'])
        ts1 = ts1.get_command_obj('test')
        ts1.ensure_finalized()
        self.assertEqual(ts1.test_suite, 'foo.tests.suite')

    def testDefaultSuite(self):
        ts2 = makeSetup(test_suite='bar.tests.suite').get_command_obj('test')
        ts2.ensure_finalized()
        self.assertEqual(ts2.test_suite, 'bar.tests.suite')

    def testDefaultWModuleOnCmdLine(self):
        ts3 = makeSetup(
            test_suite='bar.tests',
            script_args=['test','-m','foo.tests']
        ).get_command_obj('test')
        ts3.ensure_finalized()
        self.assertEqual(ts3.test_module, 'foo.tests')
        self.assertEqual(ts3.test_suite,  'foo.tests.test_suite')

    def testConflictingOptions(self):
        ts4 = makeSetup(
            script_args=['test','-m','bar.tests', '-s','foo.tests.suite']
        ).get_command_obj('test')
        self.assertRaises(DistutilsOptionError, ts4.ensure_finalized)

    def testNoSuite(self):
        ts5 = makeSetup().get_command_obj('test')
        ts5.ensure_finalized()
        self.assertEqual(ts5.test_suite, None)





testClasses = (DependsTests, DistroTests, FeatureTests, TestCommandTests)

def test_suite():
    return TestSuite([makeSuite(t,'test') for t in testClasses])

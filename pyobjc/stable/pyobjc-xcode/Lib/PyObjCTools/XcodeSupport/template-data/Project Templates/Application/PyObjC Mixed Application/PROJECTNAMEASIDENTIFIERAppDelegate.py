#
#  �PROJECTNAMEASIDENTIFIER�AppDelegate.py
#  �PROJECTNAMEASIDENTIFIER�
#

from Foundation import *
from AppKit import *
from �PROJECTNAMEASIDENTIFIER�PlugIn import *

from PyObjCTools import NibClassBuilder

class �PROJECTNAMEASIDENTIFIER�AppDelegate(NibClassBuilder.AutoBaseClass):

    def applicationDidFinishLaunching_(self, sender):
        if �PROJECTNAMEASIDENTIFIER�PlugIn.alloc().init().plugInLoaded():
            NSLog(u'Objective-C Plug-In Loaded!')
            NSBeep()

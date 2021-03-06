from PyObjCTools.TestSupport import *
from CoreFoundation import *
from Foundation import NSCFAttributedString


class TestAttributedString (TestCase):
    def testTypes(self):
        self.assertIs(CFAttributedStringRef, NSCFAttributedString )
        self.assertIs(CFMutableAttributedStringRef, NSCFAttributedString )
    def testTypeID(self):
        v = CFAttributedStringGetTypeID()
        self.assertIsInstance(v, (int, long))
    def testCreate(self):
        val = CFAttributedStringCreate(None, u"hello", {u'foo': 42})
        self.assertIsInstance(val, CFAttributedStringRef)
        val = CFAttributedStringCreateWithSubstring(None, val, (1,2))
        self.assertIsInstance(val, CFAttributedStringRef)
        val2 = CFAttributedStringCreateCopy(None, val)
        self.assertIs(val2, val)
    def testGetting(self):
        val = CFAttributedStringCreate(None, u"hello", {u'foo': 42, u'bar':'baz'})
        self.assertIsInstance(val, CFAttributedStringRef)
        dta = CFAttributedStringGetString(val)
        self.assertEqual(dta , u"hello" )
        l = CFAttributedStringGetLength(val)
        self.assertEqual(l , 5 )
        v, rng = CFAttributedStringGetAttributes(val, 1, None)
        self.assertEqual(v , {u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , (0, 5) )
        v, rng = CFAttributedStringGetAttributes(val, 1, objc.NULL)
        self.assertEqual(v , {u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , objc.NULL )
        v, rng = CFAttributedStringGetAttribute(val, 1, u"foo", None)
        self.assertEqual(v , 42 )
        self.assertEqual(rng , (0, 5) )
        v, rng = CFAttributedStringGetAttribute(val, 1, u"foo", objc.NULL)
        self.assertEqual(v , 42 )
        self.assertEqual(rng , objc.NULL )
        v, rng = CFAttributedStringGetAttributesAndLongestEffectiveRange(val, 1, (0,5), None)
        self.assertEqual(v , {u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , (0, 5) )
        v, rng = CFAttributedStringGetAttributesAndLongestEffectiveRange(val, 1, (0,5), objc.NULL)
        self.assertEqual(v , {u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , objc.NULL )
        v, rng = CFAttributedStringGetAttributeAndLongestEffectiveRange(val, 1, u'bar', (0,5), None)
        self.assertEqual(v , 'baz' )
        self.assertEqual(rng , (0, 5) )
        v, rng = CFAttributedStringGetAttributeAndLongestEffectiveRange(val, 1, u'bar', (0,5), objc.NULL)
        self.assertEqual(v , 'baz' )
        self.assertEqual(rng , objc.NULL )
    def testMutableCopy(self):
        val = CFAttributedStringCreateMutable(None, 0)
        self.assertIsInstance(val, CFAttributedStringRef)
        orig = CFAttributedStringCreate(None, u"hello", {u'foo': 42, u'bar':'baz'})
        self.assertIsInstance(orig, CFAttributedStringRef)
        val = CFAttributedStringCreateMutableCopy(None, 0, orig)
        self.assertIsInstance(orig, CFAttributedStringRef)
        self.assertIsNot(val, orig)
        CFAttributedStringReplaceString(val, (0,3), "Hal")
        dta = CFAttributedStringGetString(val)
        self.assertEqual(dta , u"Hallo" )
        v = CFAttributedStringGetMutableString(val)
        self.assertIs(v, None )
        CFAttributedStringSetAttributes(val, (0, 2), {u'ronald':99}, False)
        v, rng = CFAttributedStringGetAttributes(val, 1, None)
        self.assertEqual(v , {u'ronald':99, u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , (0, 2) )
        v, rng = CFAttributedStringGetAttributes(val, 3, None)
        self.assertEqual(v , {u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , (2, 3) )
        self.assertIsInstance(rng, CFRange)
        CFAttributedStringSetAttributes(val, (0, 2), {u'ronald':99}, True)
        v, rng = CFAttributedStringGetAttributes(val, 1, None)
        self.assertEqual(v , {u'ronald':99} )
        self.assertEqual(rng , (0, 2) )
        CFAttributedStringSetAttribute(val, (1, 3), u'color', u'blue')
        v, rng = CFAttributedStringGetAttributes(val, 1, None)
        self.assertEqual(v , {u'ronald':99, u'color':u'blue'} )
        self.assertEqual(rng , (1, 1) )
        CFAttributedStringRemoveAttribute(val, (1,3), u'color')
        v, rng = CFAttributedStringGetAttributes(val, 3, None)
        self.assertEqual(v , {u'foo': 42, u'bar': 'baz' } )
        self.assertEqual(rng , (2, 2) )
        rep = CFAttributedStringCreate(None, "dummy", {u'attrib': 99} )
        CFAttributedStringReplaceAttributedString(val, (1,3), rep)
        self.assertEqual(CFAttributedStringGetString(val) , u'Hdummyo')
    def testEditing(self):
        val = CFAttributedStringCreateMutable(None, 0)
        self.assertIsInstance(val, CFAttributedStringRef)
        CFAttributedStringBeginEditing(val)
        CFAttributedStringEndEditing(val)

if __name__ == "__main__":
    main()

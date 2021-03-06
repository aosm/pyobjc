
from PyObjCTools.TestSupport import *
from LaunchServices import *

try:
    unicode
except NameError:
    unicode = str

class TestUTCoreTypes (TestCase):
    def testConstants(self):
        self.assertIsInstance(kUTTypeItem, unicode)
        self.assertIsInstance(kUTTypeContent, unicode)
        self.assertIsInstance(kUTTypeCompositeContent, unicode)
        self.assertIsInstance(kUTTypeApplication, unicode)
        self.assertIsInstance(kUTTypeMessage, unicode)
        self.assertIsInstance(kUTTypeContact, unicode)
        self.assertIsInstance(kUTTypeArchive, unicode)
        self.assertIsInstance(kUTTypeDiskImage, unicode)
        self.assertIsInstance(kUTTypeData, unicode)
        self.assertIsInstance(kUTTypeDirectory, unicode)
        self.assertIsInstance(kUTTypeResolvable, unicode)
        self.assertIsInstance(kUTTypeSymLink, unicode)
        self.assertIsInstance(kUTTypeMountPoint, unicode)
        self.assertIsInstance(kUTTypeAliasFile, unicode)
        self.assertIsInstance(kUTTypeAliasRecord, unicode)
        self.assertIsInstance(kUTTypeURL, unicode)
        self.assertIsInstance(kUTTypeFileURL, unicode)
        self.assertIsInstance(kUTTypeText, unicode)
        self.assertIsInstance(kUTTypePlainText, unicode)
        self.assertIsInstance(kUTTypeUTF8PlainText, unicode)
        self.assertIsInstance(kUTTypeUTF16ExternalPlainText, unicode)
        self.assertIsInstance(kUTTypeUTF16PlainText, unicode)
        self.assertIsInstance(kUTTypeRTF, unicode)
        self.assertIsInstance(kUTTypeHTML, unicode)
        self.assertIsInstance(kUTTypeXML, unicode)
        self.assertIsInstance(kUTTypeSourceCode, unicode)
        self.assertIsInstance(kUTTypeCSource, unicode)
        self.assertIsInstance(kUTTypeObjectiveCSource, unicode)
        self.assertIsInstance(kUTTypeCPlusPlusSource, unicode)
        self.assertIsInstance(kUTTypeObjectiveCPlusPlusSource, unicode)
        self.assertIsInstance(kUTTypeCHeader, unicode)
        self.assertIsInstance(kUTTypeCPlusPlusHeader, unicode)
        self.assertIsInstance(kUTTypeJavaSource, unicode)
        self.assertIsInstance(kUTTypePDF, unicode)
        self.assertIsInstance(kUTTypeRTFD, unicode)
        self.assertIsInstance(kUTTypeFlatRTFD, unicode)
        self.assertIsInstance(kUTTypeTXNTextAndMultimediaData, unicode)
        self.assertIsInstance(kUTTypeWebArchive, unicode)
        self.assertIsInstance(kUTTypeImage, unicode)
        self.assertIsInstance(kUTTypeJPEG, unicode)
        self.assertIsInstance(kUTTypeJPEG2000, unicode)
        self.assertIsInstance(kUTTypeTIFF, unicode)
        self.assertIsInstance(kUTTypePICT, unicode)
        self.assertIsInstance(kUTTypeGIF, unicode)
        self.assertIsInstance(kUTTypePNG, unicode)
        self.assertIsInstance(kUTTypeQuickTimeImage, unicode)
        self.assertIsInstance(kUTTypeAppleICNS, unicode)
        self.assertIsInstance(kUTTypeBMP, unicode)
        self.assertIsInstance(kUTTypeICO, unicode)
        self.assertIsInstance(kUTTypeAudiovisualContent, unicode)
        self.assertIsInstance(kUTTypeMovie, unicode)
        self.assertIsInstance(kUTTypeVideo, unicode)
        self.assertIsInstance(kUTTypeAudio, unicode)
        self.assertIsInstance(kUTTypeQuickTimeMovie, unicode)
        self.assertIsInstance(kUTTypeMPEG, unicode)
        self.assertIsInstance(kUTTypeMPEG4, unicode)
        self.assertIsInstance(kUTTypeMP3, unicode)
        self.assertIsInstance(kUTTypeMPEG4Audio, unicode)
        self.assertIsInstance(kUTTypeAppleProtectedMPEG4Audio, unicode)
        self.assertIsInstance(kUTTypeFolder, unicode)
        self.assertIsInstance(kUTTypeVolume, unicode)
        self.assertIsInstance(kUTTypePackage, unicode)
        self.assertIsInstance(kUTTypeBundle, unicode)
        self.assertIsInstance(kUTTypeFramework, unicode)
        self.assertIsInstance(kUTTypeApplicationBundle, unicode)
        self.assertIsInstance(kUTTypeApplicationFile, unicode)
        self.assertIsInstance(kUTTypeVCard, unicode)
        self.assertIsInstance(kUTTypeInkText, unicode)

if __name__ == "__main__":
    main()

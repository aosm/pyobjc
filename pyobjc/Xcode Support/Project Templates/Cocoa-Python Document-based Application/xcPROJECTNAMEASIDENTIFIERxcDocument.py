#
#  xcPROJECTNAMEASIDENTIFIERxcDocument.py
#  xcPROJECTNAMExc
#
#  Created by xcFULLUSERNAMExc on xcDATExc.
#  Copyright xcORGANIZATIONNAMExc xcYEARxc. All rights reserved.
#

from Foundation import *
from AppKit import *

class xcPROJECTNAMEASIDENTIFIERxcDocument(NSDocument):
    def init(self):
        self = super(xcPROJECTNAMEASIDENTIFIERxcDocument, self).init()
        # initialization code
        return self
        
    def windowNibName(self):
        return u"xcPROJECTNAMEASIDENTIFIERxcDocument"
    
    def windowControllerDidLoadNib_(self, aController):
        super(xcPROJECTNAMEASIDENTIFIERxcDocument, self).windowControllerDidLoadNib_(aController)

    def dataOfType_error_(self, typeName, outError):
        return None
    
    def readFromData_ofType_error_(self, data, typeName, outError):
        return NO

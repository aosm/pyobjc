#include "pyobjc.h"

@interface OC_PythonNumber : NSNumber
{
	PyObject* value;
}

+ newWithPythonObject:(PyObject*)value;
- initWithPythonObject:(PyObject*)value;
-(void)dealloc;
-(PyObject*)__pyobjc_PythonObject__;

@end

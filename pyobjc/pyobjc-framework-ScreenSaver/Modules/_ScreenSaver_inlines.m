#include "Python.h"
#import <ScreenSaver/ScreenSaver.h>

typedef void (*FUNCTION)(void);

struct function_map {
    const char* name;
    FUNCTION    function;
} function_map[] = {
	{"SSCenteredRectInRect", (FUNCTION)&SSCenteredRectInRect },
	{"SSRandomFloatBetween", (FUNCTION)&SSRandomFloatBetween },
	{"SSRandomIntBetween", (FUNCTION)&SSRandomIntBetween },
	{"SSRandomPointForSizeWithinRect", (FUNCTION)&SSRandomPointForSizeWithinRect },
    { 0, 0 }
};

static PyMethodDef mod_methods[] = {
        { 0, 0, 0, 0 } /* sentinel */
};

void init_inlines(void)
{
    PyObject* m = Py_InitModule4("_inlines", mod_methods, NULL, NULL, PYTHON_API_VERSION);

    PyModule_AddObject(m, "_inline_list_", 
        PyCObject_FromVoidPtr(function_map, NULL));
}

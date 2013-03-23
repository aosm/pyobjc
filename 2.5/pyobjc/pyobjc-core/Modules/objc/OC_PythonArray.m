#include "pyobjc.h"
#import "OC_PythonArray.h"

static PyObject* mapTypes = NULL;

@implementation OC_PythonArray 

+ depythonifyObject:(PyObject*)object
{
	Py_ssize_t i, len;
	
	if (mapTypes == NULL) return NULL;

	len = PyList_GET_SIZE(mapTypes);

	for (i = 0; i < len; i++) {
		PyObject* tp = PyList_GET_ITEM(mapTypes, i);
		int r = PyObject_IsInstance(object, tp);
		if (r == -1) {
			return NULL;
		}

		if (!r) continue;

		/* Instance of this type should be pythonifyed as a sequence */
		return [OC_PythonArray newWithPythonObject:object];
	}

	return NULL;
}

+ depythonifyTable
{
	NSObject* result; 

	PyObjC_BEGIN_WITH_GIL

		if (mapTypes == NULL) {
			mapTypes = PyList_New(0);
			if (mapTypes == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			}
		}
		result = PyObjC_PythonToId(mapTypes);
		if (result == NULL) {
			PyObjC_GIL_FORWARD_EXC();
		}

	PyObjC_END_WITH_GIL

	return result;
}

+ newWithPythonObject:(PyObject*)v;
{
	OC_PythonArray* res;

	res = [[OC_PythonArray alloc] initWithPythonObject:v];
	[res autorelease];
	return res;
}

- initWithPythonObject:(PyObject*)v;
{
	self = [super init];
	if (unlikely(self == nil)) return nil;

	Py_INCREF(v);
	Py_XDECREF(value);
	value = v;
	return self;
}

-(PyObject*)__pyobjc_PythonObject__
{
	Py_INCREF(value);
	return value;
}

-(PyObject*)__pyobjc_PythonTransient__:(int*)cookie
{
	*cookie = 0;
	Py_INCREF(value);
	return value;
}

-(void)release
{
	/* See comment in OC_PythonUnicode */
	PyObjC_BEGIN_WITH_GIL
		[super release];
	PyObjC_END_WITH_GIL
}

-(void)dealloc
{
	PyObjC_BEGIN_WITH_GIL
		PyObjC_UnregisterObjCProxy(value, self);
		Py_XDECREF(value);

	PyObjC_END_WITH_GIL

	[super dealloc];
}

-(NSUInteger)count
{
	Py_ssize_t result;

	PyObjC_BEGIN_WITH_GIL
		result = PySequence_Length(value);

	PyObjC_END_WITH_GIL

	if (result > INT_MAX) {
		return INT_MAX;
	}

	return result;
}

-objectAtIndex:(NSUInteger)idx
{
	PyObject* v;
	id result;
	int err;

	PyObjC_BEGIN_WITH_GIL
		if (idx > PY_SSIZE_T_MAX) {
			PyErr_SetString(PyExc_IndexError, "out of range");
			PyObjC_GIL_FORWARD_EXC();
		}

		v = PySequence_GetItem(value, idx);
		if (unlikely(v == NULL)) {
			PyObjC_GIL_FORWARD_EXC();
		}

		err = depythonify_c_value(@encode(id), v, &result);
		if (unlikely(err == -1)) {
			PyObjC_GIL_FORWARD_EXC();
		} else {
			Py_DECREF(v);
		}
	
	PyObjC_END_WITH_GIL

	if (!result) {
		result = [NSNull null];
	}
	return result;
}


-(void)replaceObjectAtIndex:(NSUInteger)idx withObject:newValue;
{
	PyObject* v;

	PyObjC_BEGIN_WITH_GIL
		if (idx > PY_SSIZE_T_MAX) {
			PyErr_SetString(PyExc_IndexError, "out of range");
			PyObjC_GIL_FORWARD_EXC();
		}

		if (unlikely(newValue == [NSNull null])) {
			Py_INCREF(Py_None);
			v = Py_None;

		} else {
			v = PyObjC_IdToPython(newValue);
			if (v == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			}
		}

		if (PySequence_SetItem(value, idx, v) < 0) {
			Py_DECREF(v);
			PyObjC_GIL_FORWARD_EXC();
		}
		Py_DECREF(v);

	PyObjC_END_WITH_GIL;
}

-(void)getObjects:(id*)buffer inRange:(NSRange)range
{
	unsigned int i;

	for (i = 0; i < range.length; i++) {
		buffer[i] = [self objectAtIndex:i+range.location];
	}
}

-(void)addObject:(id)anObject
{
	PyObject* v;
	PyObject* w;

	PyObjC_BEGIN_WITH_GIL

		if (unlikely(anObject == [NSNull null])) {
			Py_INCREF(Py_None);
			v = Py_None;

		} else {
			v = PyObjC_IdToPython(anObject);
			if (v == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			}
		}

		w = PyObject_CallMethod(value, "append", "O", v);
		if (unlikely(w == NULL)) {
			Py_DECREF(v);
			PyObjC_GIL_FORWARD_EXC();
		}
		Py_DECREF(v);
		Py_DECREF(w);

	PyObjC_END_WITH_GIL;
}

-(void)insertObject:(id)anObject atIndex:(NSUInteger)idx
{
	Py_ssize_t theIndex;
	PyObject* v;
	PyObject* w;

	if (idx > PY_SSIZE_T_MAX) {
		PyObjC_BEGIN_WITH_GIL
			PyErr_SetString(PyExc_IndexError, "No such index");
			PyObjC_GIL_FORWARD_EXC();
		PyObjC_END_WITH_GIL
	}
	theIndex = idx;

	PyObjC_BEGIN_WITH_GIL
		if (unlikely(anObject == [NSNull null])) {
			Py_INCREF(Py_None);
			v = Py_None;
		} else {
			v = PyObjC_IdToPython(anObject);
			if (v == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			}
		}

		w = PyObject_CallMethod(value, "insert", "iO", idx, v);
		if (unlikely(w == NULL)) {
			Py_DECREF(v);
			PyObjC_GIL_FORWARD_EXC();
		}
		Py_DECREF(v);
		Py_DECREF(w);

	PyObjC_END_WITH_GIL;
}

-(void)removeLastObject
{
	int r;
	Py_ssize_t idx;

	PyObjC_BEGIN_WITH_GIL
		idx = PySequence_Length(value);
		if (unlikely(idx == -1)) {
			PyObjC_GIL_FORWARD_EXC();
		}

		if (unlikely(idx == 0)) {
			PyErr_SetString(PyExc_ValueError, "pop empty sequence");
			PyObjC_GIL_FORWARD_EXC();
		}

		r = PySequence_DelItem(value, idx-1);
		if (unlikely(r == -1)) {
			PyObjC_GIL_FORWARD_EXC();
		}

	PyObjC_END_WITH_GIL;
}

-(void)removeObjectAtIndex:(NSUInteger)idx;
{
	int r;

	PyObjC_BEGIN_WITH_GIL
		if (unlikely(idx > PY_SSIZE_T_MAX)) {
			PyErr_SetString(PyExc_IndexError, "No such index");
			PyObjC_GIL_FORWARD_EXC();
		}

		r = PySequence_DelItem(value, (Py_ssize_t)idx);
		if (unlikely(r == -1)) {
			PyObjC_GIL_FORWARD_EXC();
		}

	PyObjC_END_WITH_GIL;
}

-(void)encodeWithCoder:(NSCoder*)coder
{
	/*
	 * Instances of 'list' and 'tuple' are encoded directly,
	 * for other sequences use the generic pickle support code.
	 */
	if (PyTuple_CheckExact(value)) {
		if ([coder allowsKeyedCoding]) {
			[coder encodeInt32:1 forKey:@"pytype"];
		} else {
			int v = 1;
			[coder encodeValueOfObjCType:@encode(int) at:&v];
		}
		[super encodeWithCoder:coder];
	} else if (PyList_CheckExact(value)) {
		if ([coder allowsKeyedCoding]) {
			[coder encodeInt32:2 forKey:@"pytype"];
		} else {
			int v = 2;
			[coder encodeValueOfObjCType:@encode(int) at:&v];
		}
		[super encodeWithCoder:coder];
	} else {
		if ([coder allowsKeyedCoding]) {
			[coder encodeInt32:3 forKey:@"pytype"];
		} else {
			int v = 3;
			[coder encodeValueOfObjCType:@encode(int) at:&v];
		}
		PyObjC_encodeWithCoder(value, coder);

	}
}

/*
 * A basic implementation of -initWithObjects:count:. This method is needed
 * to support NSCoding for Python sequences.
 */
-(Class)classForCoder
{
	return [OC_PythonArray class];
}

-(id)initWithObjects:(NSObject**)objects count:(NSUInteger)count
{
	NSUInteger i;
	PyObjC_BEGIN_WITH_GIL
		for  (i = 0; i < count; i++) {
			PyObject* v = PyObjC_IdToPython(objects[i]);
			if (v == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			}
			int r = PyList_Append(value,  v);
			if (r == -1) {
				PyObjC_GIL_FORWARD_EXC();
			}
			Py_DECREF(v);
		}

	PyObjC_END_WITH_GIL
	return self;
}

/* 
 * Helper method for initWithCoder, needed to deal with
 * recursive objects (e.g. o.value = o)
 */
-(void)pyobjcSetValue:(NSObject*)other
{
	PyObject* v = PyObjC_IdToPython(other);
	Py_XDECREF(value);
	value = v;
}

-(id)initWithCoder:(NSCoder*)coder
{
	PyObject* t;
	int code;
	if ([coder allowsKeyedCoding]) {
		code = [coder decodeInt32ForKey:@"pytype"];
	} else {
		[coder decodeValueOfObjCType:@encode(int) at:&code];
	}

	PyObjC_BEGIN_WITH_GIL
		value = PyList_New(0);
		if (value == NULL) {
			PyObjC_GIL_FORWARD_EXC();
		}
	PyObjC_END_WITH_GIL

	switch (code) {
	case 1:
	      [super initWithCoder:coder];
	      PyObjC_BEGIN_WITH_GIL
		      t = value;
		      value = PyList_AsTuple(t);
		      Py_DECREF(t);
		      if (value == NULL) {
				PyObjC_GIL_FORWARD_EXC();
		      }
	      PyObjC_END_WITH_GIL
	      return self;

	case 2:
	      [super initWithCoder:coder];
	      return self;

	case 3:

		if (PyObjC_Decoder != NULL) {
			PyObjC_BEGIN_WITH_GIL
				PyObject* cdr = PyObjC_IdToPython(coder);
				if (cdr == NULL) {
					PyObjC_GIL_FORWARD_EXC();
				}

				PyObject* setValue;
				PyObject* selfAsPython = PyObjCObject_New(self, 0, YES);
				setValue = PyObject_GetAttrString(selfAsPython, "pyobjcSetValue_");

				PyObject* v = PyObject_CallFunction(PyObjC_Decoder, "OO", cdr, setValue);
				Py_DECREF(cdr);
				Py_DECREF(setValue);
				Py_DECREF(selfAsPython);

				if (v == NULL) {
					PyObjC_GIL_FORWARD_EXC();
				}

				Py_XDECREF(value);
				value = v;

				NSObject* proxy = PyObjC_FindObjCProxy(value);
				if (proxy == NULL) {
					PyObjC_RegisterObjCProxy(value, self);
				} else {
					[self release];
					[proxy retain];
					self = (OC_PythonArray*)proxy;
				}


			PyObjC_END_WITH_GIL

			return self;
		}
	}

	[NSException raise:NSInvalidArgumentException
			format:@"decoding Python objects is not supported"];
	[self release];
	return nil;
}


-(id)copyWithZone:(NSZone*)zone
{
	if (PyObjC_CopyFunc) {
		PyObjC_BEGIN_WITH_GIL
			PyObject* copy = PyObject_CallFunctionObjArgs(PyObjC_CopyFunc,
					value, NULL);

			if (copy == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			} 

			NSObject* result = PyObjC_PythonToId(copy);
			Py_DECREF(copy);

			if (PyErr_Occurred()) {
				PyObjC_GIL_FORWARD_EXC();
			}

			[result retain];

			PyObjC_GIL_RETURN(result);

		PyObjC_END_WITH_GIL
	} else {
		return [super copyWithZone:zone];
	}
}

-(id)mutableCopyWithZone:(NSZone*)zone
{
	if (PyObjC_CopyFunc) {
		PyObjC_BEGIN_WITH_GIL
			PyObject* copy = PySequence_List(value);
			if (copy == NULL) {
				PyObjC_GIL_FORWARD_EXC();
			} 

			NSObject* result = PyObjC_PythonToId(copy);
			Py_DECREF(copy);

			if (PyErr_Occurred()) {
				PyObjC_GIL_FORWARD_EXC();
			}

			[result retain];
			PyObjC_GIL_RETURN(result);

		PyObjC_END_WITH_GIL
	} else {
		return [super mutableCopyWithZone:zone];
	}
}
@end /* implementation OC_PythonArray */

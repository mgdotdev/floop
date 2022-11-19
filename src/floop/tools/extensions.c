#include <Python.h>


PyObject* loop(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* _fn;
    PyObject* _args;

    PyObject* result = NULL;

    _fn = PyTuple_GetItem(args, 0);
    _args = PyTuple_GetSlice(args, 1, PyTuple_Size(args));

    for (;;) {
        result = PyObject_Call(_fn, _args, kwargs);
        if (result != Py_None) {
            return result;
        }
    }
}


static PyMethodDef MethodTable[] = {
    {"loop", (PyCFunction) loop, METH_VARARGS|METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Extensions = {
    PyModuleDef_HEAD_INIT,
    "extensions",
    NULL,
    -1,
    MethodTable,
};

PyMODINIT_FUNC PyInit_extensions() {
    return PyModule_Create(&Extensions);
}


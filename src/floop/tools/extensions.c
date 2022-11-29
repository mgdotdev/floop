#include <Python.h>
#include <stdarg.h>


int _keys_match(PyObject* key, char* id) {
    if (PyUnicode_CompareWithASCIIString(key, id) == 0) {
        return 1;
    }
    return 0;
}


PyObject* basic_loop(PyObject* fn, PyObject* args, PyObject* kwargs) {
    PyObject* result = NULL;

    for (;;) {
        result = PyObject_Call(fn, args, kwargs);
        if (result != Py_None) {
            return result;
        }
        Py_DECREF(result);
    }
}


PyObject* configured_loop(PyObject* wrapped, PyObject* args, PyObject* kwargs) {
    PyObject *config = PyObject_GetAttrString(wrapped, "_loop_configuration");
    PyObject *fn = PyObject_GetAttrString(wrapped, "_fn");

    PyObject *result = NULL, *callback = NULL, *cb_result = NULL, *cb_args = NULL;

    long max_iter = 0;

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while (PyDict_Next(config, &pos, &key, &value)) {
        if (_keys_match(key, "callback")) {
            callback = value;
        }
        else if (_keys_match(key, "max_iter")) {
            max_iter = PyLong_AsLong(value);
        }
    }
    Py_DECREF(config);

    for (;;) {
        result = PyObject_Call(fn, args, kwargs);
        if (callback) {
            if (!PyTuple_Check(result)) {
                cb_args = PyTuple_New(1);
                PyTuple_SET_ITEM(cb_args, 0, result);
                Py_INCREF(result);
            }
            else {
                cb_args = result;
                Py_INCREF(cb_args);
            }
            cb_result = PyObject_CallObject(callback, cb_args);
            int check = cb_result == Py_True;
            Py_DECREF(cb_args);
            if (check) {
                Py_DECREF(cb_result);
                Py_DECREF(fn);
                return result;
            }
        }
        if (max_iter) {
            if (max_iter == 1) {
                Py_DECREF(fn);
                return result;
            }
            max_iter -= 1;
        }
        Py_DECREF(result);
    }
}


PyObject* loop(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* _fn = PyTuple_GetItem(args, 0);
    PyObject* _args = PyTuple_GetSlice(args, 1, PyTuple_Size(args));

    PyObject* (*execute)(PyObject*, PyObject*, PyObject*);
    execute = (
        PyObject_HasAttrString(_fn, "_loop_configuration")
        && PyObject_HasAttrString(_fn, "_fn")
        ? &configured_loop : &basic_loop
    );

    PyObject* result = execute(_fn, _args, kwargs);
    Py_DECREF(_args);
    return result;
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


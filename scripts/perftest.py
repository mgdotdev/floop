import time
from collections import deque

from floop import loop as c_loop

TGT = 1_000_000

def py_loop(fn, *args, **kwargs):
    while True:
        if res := fn(*args, **kwargs):
            return res

def main():

    def execute():
        i = 0
        def _execute():
            nonlocal i
            if i == TGT:
                return i
            i += 1
        return _execute

    start=time.perf_counter()
    py_loop(execute())
    end=time.perf_counter()

    print(f"{'py_loop':-<12} {end-start}")

    start=time.perf_counter()
    c_loop(execute())
    end=time.perf_counter()

    print(f"{'c_loop':-<12} {end-start}")

    start=time.perf_counter()
    exe = execute()
    val = None
    while not val:
        val = exe()
    end=time.perf_counter()

    print(f"while-loop-- {end-start}")

    start=time.perf_counter()
    deque(iter(execute(), TGT), maxlen=0)
    end=time.perf_counter()

    print(f"{'deque':-<12} {end-start}")



if __name__ == "__main__":
    main()

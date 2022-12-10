# floop

## functional event loops


The goal of this project is to replace this:

```python
from tasks import process_queue

def main():
    while True:
        process_queue()

if __name__ == "__main__":
    main()
```

with this:

```python
from floop import loop
from tasks import process_queue

if __name__ == "__main__":
    loop(process_queue)
```

floop.loop is a C extension which has an internal event loop that continuously
calls a given function. If the function returns None, the loop continues. If the
function return is not None, or the function raises an error, the result breaks
the loop.

The resulting implementation is ~15-20% faster than the analogous `while` loop.

performance results:
```bash
$+ python ./scripts/perftest.py
py_loop----- 0.06751498499943409
c_loop------ 0.043669621998560615
while-loop-- 0.05094353300228249
deque------- 0.05047171100159176
```

floop.loop is configurable, to allow actions like selective breaks and iter
limits

```python

from floop import loop, config

if __name__ == "__main__":

    @config(callback=lambda coll: len(coll) == 500)
    def fn(coll):
        coll.append(len(coll))
        return coll

    coll = loop(fn, [])

    assert len(coll) == 500

    count = 0
    def fn():
        nonlocal count
        count += 1

    loop(config(fn, max_iter=500))

    assert count == 500
```

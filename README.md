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

performance results:
```
$+ python ./scripts/perftest.py
py_loop: 0.06991245297831483
c_loop: 0.04349226297927089
while-loop: 0.05318959499709308
```

# Service Performance Profiler

!!! warning
     You need to install dependencies for the middleware you want to use

## Introduction to Pyinstrument

Pyinstrument is a statistical python profiler which records call stack every 1
ms rather than recording the whole trace. This is done in order to avoid
profiling overhead which can increase a lot if some functions are getting called
many times and not taking that much time to complete.

This kind of behavior can even distort results by highlighting part of the
code/function which might not be slow but getting called many times completing
faster. In a way it kind of tries to avoid profiling noise by removing profiling
information of faster parts of code.

This kind of behavior also has a drawback that some of the function calls which
ran quite fast will not be recorded but they are already fast.

Pyinstrument uses an OS feature called signals to ask OS to send a signal and
handle signals using a python signal handler (PyEval_SetProfile) for recording
every 1 ms.

### Example

```python
import random

def add(a, b):
    return a+b


def get_sum_of_list():
    final_list = []
    for i in range(1000000):
        rand1 = random.randint(1,100)
        rand2 = random.randint(1,100)
        out = add(rand1, rand2)
        final_list.append(out)
    return final_list


if __name__ == "__main__":
    l = get_sum_of_list()
```

- Below we have profiled script using Pyinstrument without default options.
  Please make a note that we are using the ! symbol which lets us execute a
  shell command from Jupyter Notebook. This command can be run exactly the same
  way from a shell.

> `!pyinstrument profiling_examples/pyinstrument_ex1.py`

#### Output

<div class="termy">

```shell
  _     ._   __/__   _ _  _  _ _/_   Recorded: 16:39:21  Samples:  2192
 /_//_/// /_\ / //_// / //_'/ //     Duration: 2.199     CPU time: 2.197
/   _/                      v3.2.0

Program: profiling_examples/pyinstrument_ex1.py

2.199 <module>  pyinstrument_ex1.py:1
└─ 2.199 get_sum_of_list  pyinstrument_ex1.py:7
   ├─ 1.714 randint  random.py:218
   │     [6 frames hidden]  random
   │        1.442 randrange  random.py:174
   │        ├─ 0.734 [self]
   │        └─ 0.708 _randbelow  random.py:224
   │           ├─ 0.501 [self]
   │           ├─ 0.153 Random.getrandbits  ../<built-in>:0
   │           └─ 0.054 int.bit_length  ../<built-in>:0
   ├─ 0.405 [self]
   ├─ 0.050 add  pyinstrument_ex1.py:3
   └─ 0.030 list.append  ../<built-in>:0

To view this report with different options, run:
    pyinstrument --load-prev 2020-11-12T16-39-21 [options]
```

</div>

> Reference:
> [pyinstrument-statistical-profiler-for-python-code](https://coderzcolumn.com/tutorials/python/pyinstrument-statistical-profiler-for-python-code)

## Middleware Integration

With AuthX the abstract of profiling is easy, it's just about calling the `ProfilerMiddleware` 's class and calling it in `add_middleware(ProfilerMiddleware)` func that FastAPI provides.

### How to install

Make sure to have the necessary dependencies installed:

<div class="termy">

```console
$ pip install authx_extra

---> 100%
```

</div>

### Example

```py
import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from authx_extra.profiler import ProfilerMiddleware


app = FastAPI()
app.add_middleware(ProfilerMiddleware)


@app.get("/test")
async def normal_request():
    return JSONResponse({"retMsg": "Hello World!"})


if __name__ == '__main__':
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(app=f"{app_name}:app", host="0.0.0.0", port=8080, workers=1)
```

### Middleware Options

This class to have 3 functions that expose the profiling information, one is to get the profiling information, one is to get the profiling information in a JSON format and one is to get the profiling information in a HTML format.

```python
app.add_middleware(PyInstrumentProfilerMiddleware, profiler_output_type="html", is_print_each_request=False, html_file_name="profiling.html")
```

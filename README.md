# CuPER - Custom ParsER
Custom parsing module written in Python.

### Getting started

#### **Installation process**
```console
$ # Linux/Mac (Unix)
$ pip3 install "git+https://github.com/marc-dantas/cuper.git#egg=cuper"

$ # Windows
$ pip install "git+https://github.com/marc-dantas/cuper.git#egg=cuper"
```

#### **Simple test example**
```console
$ cat >> example.py
from cuper.core import Parser, stringify
from cuper.util import t
print(stringify(t(), "some text", t()))
$ python3 example.py
<text> 'some text' <text>
```

### Documentation
Go to [documentation](./doc.md).

---

> By Marcio Dantas
# CuPER Documentation

## Models
Most model classes (which come from the `models` module) are the constructors of an `Item` type that are accepted inside an `Expression` (list of `Item`s).

### *The `Argument` class*
The argument class is part of the category of capture items (those that capture the value when combined). Basically, the class maps a specific type that is inside the `Type` enum:
- `Type.INT`: Matches any integer.
- `Type.FLOAT`: Matches any decimal number.
- `Type.CHAR`: Matches any character.
- `Type.UP_CHAR`: Matches any uppercase character.
- `Type.LOW_CHAR`: Matches any lowercase character.
- `Type.TEXT`: Matches anything.

**Example**

This expression `[Argument(Type.NUMBER)]` matches `["69"]`. But it doesn't match `["some text"]`.

**Definition**

```py
class Argument:
    typ: Type
```

### *The literal*
`Literal` is just another name for Python's `str` primitive type. It works as a fixed value.

**Example**

The expression `["print", "cuper"]` matches `["print", "cuper"]`. But it doesn't match `["print", "hello world"]`

**Definition**

```py
Literal = str
```

### *The `Any` class*
The `Any` class works as an OR operator. You can put multiple types from the `Type` enum and it will match if any type matches the value itself.

**Example**

The expression `[Any(Type.TEXT, Type.NUMBER), "test"]` matches `["10", "test"]` and also matches `["test", "test"]`.

**Definition**

```py
class Any:
    items: list[Type]
```

### *The `Option` class*
The `Option` class is very similar to the `Any` class, but it works with the `Literal` item. You can put multiple strings and it will match if any type matches the value itself.

**Example**

The expression `[Option("print", "puts"), Argument(Type.NUMBER)]` matches `["print", "10"]` and also matches `["puts", "25"] `.

**Definition**

```py
class Option:
    items: list[str]
```

## Core
This is the main module of this package. It only contains one class.

### *Parser*
`Parser` is the class that does the pattern-match between expressions and values. Let's take a look at each method in this class.

#### `(Parser).match(...)`
This method is what does the checking. It accepts a list of items that represent an `Expression` (`List[Item]`) and returns the `Result` class, which contains a `bool` saying if there was a match and a `list` with the captured values.

**Definition**
```py
(method) match(self: Self@Parser, expr: Any) -> Result
```

## Util
Util is a module with some functions to reduce the size of expressions.

### *Function `util.t()`*
This function returns `Argument(Type.TEXT)`.

### *Function `util.i()`*
This function returns `Argument(Type.INT)`.

### *Function `util.f()`*
This function returns `Argument(Type.FLOAT)`.

### *Function `util.c()`*
This function returns `Argument(Type.CHAR)`.

### *Function `util.uc()`*
This function returns `Argument(Type.UP_CHAR)`.

### *Function `util.lc()`*
This function returns `Argument(Type.LOW_CHAR)`.

## How to use
To use the library. Import it.
Recommended code:

```py
from cuper.core import Parser, Type, Argument
```

to initialize the parser, place it in a variable and place each value in each argument of the `__init__` method of the class.
Example:
```py
p = Parser(["foo", "10"])
```

To check, use the `match` method. Example:

```py
r = p.match([Option(["foo", "bar"]), Argument(Type.INT)])
print(r.success)  # True
```

Or if you want a more clean and smaller code, you can import the `util` module and write it using its functions:
```py
from cuper.util import i

r = p.match([Option(["foo", "bar"]), i()])
print(r.success)  # True
```


### *Function `stringify()`*
This function serves to display the expression in a more presentable way. It converts an expression to a string.

**Definition**

```py
(function) stringify(*expr: Item) -> str
```

### *Function `count()`*
This function counts how much capture elements are inside given expression. This helps a lot when you need to check the size of `(Result).values` when you match an expression.


**Definition**
`(function) count(expr: Expression) -> int`
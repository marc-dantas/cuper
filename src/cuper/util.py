from .models import Type, Argument


def t() -> Argument:
    return Argument(Type.TEXT)


def i() -> Argument:
    return Argument(Type.INT)


def f() -> Argument:
    return Argument(Type.FLOAT)


def c() -> Argument:
    return Argument(Type.CHAR)


def uc() -> Argument:
    return Argument(Type.UP_CHAR)


def lc() -> Argument:
    return Argument(Type.LOW_CHAR)


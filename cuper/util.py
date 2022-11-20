from .models import Argument, Option, Type, Union, Literal, List


def arguments(*types: Type) -> Argument:
    for typ in types:
        yield Argument(typ)


def any_text() -> Argument:
    return Argument(Type.TEXT)


def any_num() -> Argument:
    return Argument(Type.NUMBER)


def flag(name: str) -> Union[Option, Literal]:
    if len(name) > 1:
        return Option("--%s" % name, "-%s" % name[0].upper())
    else:
        return "-%s" % name


FlagWithArg = Union[List[Union[Option, Argument]], List[Union[Literal, Argument]]]
LitWithArg = List[Union[Literal, Argument]]


def lit_with_arg(name: str, typ: Type) -> LitWithArg:
    return [name, Argument(typ)]

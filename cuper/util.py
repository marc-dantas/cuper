from .models import Type, List, Union, Literal, Argument


def txt() -> Argument:
    return Argument(Type.TEXT)


def num() -> Argument:
    return Argument(Type.NUMBER)


def lit_with_arg(name: str, typ: Type) -> List[Union[Literal, Argument]]:
    return [name, Argument(typ)]

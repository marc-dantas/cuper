from .models import *


# NOTE: A interesting fact is that check_argument is the "core" of parsing types;
# NOTE: Basically, it doesn't matter if we have more types. We just have
# to modify the Type enum and this function and the entire library will work normally
def check_argument(typ: Type, value: str) -> Union[Value, None]:
    """(function) check_argument(typ: Type, value: str) -> (Value | None)

    Args:
        typ (Type): The type that will be checked
        value (str): The value that will be compared with

    Returns:
        Union[Value, None]: Value if some type matched, otherwise None
    """
    TYPE_CHECKS = {
        Type.TEXT: lambda x: x,
        Type.INT: lambda x: int(x) if x.isdigit() else None,
        Type.FLOAT: lambda x: float(x) if x.replace('.', '', 1).isdigit() else None,
        Type.CHAR: lambda x: x if len(x) == 1 else None,
        Type.UP_CHAR: lambda x: x if x.isupper() and len(x) == 1 else None,
        Type.LOW_CHAR: lambda x: x if x.islower() and len(x) == 1 else None
    }
    return TYPE_CHECKS[typ](value) if typ in TYPE_CHECKS else None


def stringify(*expr: Item) -> str:
    """(function) stringify(*expr: Item) -> str

    Args:
        *expr (Item): The items of the expression that will be turned into a string

    Returns:
        str: The processed string
    """
    return " ".join(repr(it) for it in expr)


def count(expr: Expression) -> int:
    """(function) count(expr: Expression) -> int

    Args:
        expr (Expression): The expression

    Returns:
        int: The quantity of capture items inside given expression
    """
    return sum(int(isinstance(i, Argument)) for i in expr)

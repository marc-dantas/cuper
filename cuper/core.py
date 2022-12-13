from .models import *
from typing import Tuple


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


class Parser:

    def __init__(self, values: List[str]):
        self.__values = values

    @staticmethod
    def match_argument(item: Type, value: str) -> Union[Value, None]:
        """(static method) match_argument(item: Type, value: str) -> (Value | None)

        Args:
            item (Type): The type of the argument that is checked
            value (str): The value that is compared with item 

        Returns:
            Union[Value, None]: None if no match otherwise the Value itself
        """
        return check_argument(item, value)
    
    @staticmethod
    def match_any(item: Any, value: str) -> Union[Value, None]:
        """(static method) match_any(item: Any, value: str) -> (Value | None)

        Args:
            item (Any): The instance of `cuper.models.Any` that is checked
            value (str): The value that is compared with item

        Returns:
            Union[Value, None]: None if no match otherwise the Value itself
        """
        return value if any(Parser.match_argument(it, value) for it in item.items) else None
    
    @staticmethod
    def match_literal(item: Literal, value: str) -> str:
        """(static method) match_literal(item: Literal, value: str) -> str

        Args:
            item (Literal): The string that is checked
            value (str): The value that is compared with item

        Returns:
            str: Empty string ('') if no match otherwise the value itself
        """
        return value if value == item else ''
    
    @staticmethod
    def match_option(item: Option, value: str) -> str:
        """(static method) match_option(item: Option, value: str) -> str

        Args:
            item (Option): The instance of `cuper.models.Option` that is checked
            value (str): The value that is compared with item

        Returns:
            str: Empty string ('') if no match otherwise the argument `value` itself
        """
        return value if any(Parser.match_literal(it, value) for it in item.items) else ''

    def __match_model(self, item: Item, value: str) -> Tuple[bool, Union[Value, None]]:
        if isinstance(item, Argument) and (x := self.match_argument(item.typ, value)) is not None:
            return (True, x)
        elif isinstance(item, Literal) and self.match_literal(item, value):
            return (True, None)
        elif isinstance(item, Any) and (x := self.match_any(item, value)) is not None:
            return (True, x)
        elif isinstance(item, Option) and self.match_option(item, value):
            return (True, None)
        return (False, None)

    def match(self, expr: List[Item]) -> Result:
        """(method) match(self: Self@Parser, expr: Any) -> Result
        
        Args:
            expr (List[Item]): The expression that is checked

        Returns:
            Result: (success: bool, values: List[Value])
        """
        values: List[Value] = []
        if len(self.__values) < len(expr):
            return Result(False, [])
        for index, item in enumerate(expr):
            value = self.__values[index]
            match_value = self.__match_model(item, value)
            # NOTE: if match_value[1] is not None, then match_value[0] == True
            # NOTE: but if match_value[0] == True, then match_value[1] can also be None
            if not match_value[0]:
                return Result(False, [])
            elif match_value[1] is not None:
                values.append(match_value[1])
        return Result(True, values)

    def __repr__(self) -> str:
        return f"cuper.core.Parser({self.__values})"

    def __str__(self) -> str:
        return self.__repr__()

from .models import *
from typing import Tuple


def check_argument(typ: Type, value: str) -> Union[Value, None]:
    if typ == Type.TEXT:
        return value
    elif typ == Type.NUMBER:
        return int(value) if value.isdigit() else None
    return None


def stringify(*expr: Item) -> str:
    return " ".join(repr(it) for it in expr)


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
        elif isinstance(item, Literal):
            if self.match_literal(item, value) is None:
                return (False, None)
            else:
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

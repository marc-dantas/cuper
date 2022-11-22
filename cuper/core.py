from .models import *


def check_argument(arg: Argument, value: str) -> Union[Value, None]:
    if isinstance(arg, Argument):
        if arg.typ == Type.TEXT:
            return value
        elif arg.typ == Type.NUMBER:
            return int(value) if value.isdigit() else None
    raise TypeError(f"Type mismatch in check_argument(): Expected `arg` to be Argument, but got `{type(arg).__name__}`.")


def stringify(*expr: Item) -> str:
    return " ".join(repr(it) for it in expr)


class Parser:

    def __init__(self, *values: Item):
        self.__values = list(values)

    @staticmethod
    def match_argument(item: Argument, value: str) -> Union[Value, None]:
        return check_argument(item, value)
    
    @staticmethod
    def match_any(item: Any, value: str) -> Union[Value, None]:
        return value if any(Parser.match_argument(it, value) for it in item.items) else None
    
    @staticmethod
    def match_literal(item: Literal, value: str) -> str:
        return value if value == item else ''
    
    @staticmethod
    def match_option(item: Option, value: str) -> str:
        return value if any(Parser.match_literal(it, value) for it in item.items) else ''

    def match(self, *expr: Item) -> Result:
        values: List[Value] = []
        if len(self.__values) < len(expr):
            return Result(False, [])
        for index, item in enumerate(expr):
            value = self.__values[index]
            if isinstance(item, Argument) and (x := self.match_argument(item, value)):
                values.append(x)
            elif isinstance(item, Literal):
                if not self.match_literal(item, value):
                    return Result(False, [])
            elif isinstance(item, Any) and (x := self.match_any(item, value)):
                values.append(x)
            elif isinstance(item, Option):
                if not self.match_option(item, value):
                    return Result(False, [])
            else:
                return Result(False, [])
        return Result(True, values)
    
    def assert_match(self, message: str, *expr: Item) -> List[Value]:
        if (x := self.match(*expr)):
            return x.values
        print(message)
        exit(1)

    def __repr__(self) -> str:
        return f"cuper.core.Parser({self.__values})"

    def __str__(self) -> str:
        return self.__repr__()


def match(values: List, expr: List[Item]) -> Result:
    return Parser(*values).match(*expr)

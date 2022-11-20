from .models import *


def check_type(arg: Union[Argument, Literal], value: str) -> Union[Value, None]:
    if isinstance(arg, Argument):
        if arg.typ == Type.TEXT:
            return value
        elif arg.typ == Type.NUMBER:
            if value.isdigit():
                return int(value)
            return None
        assert False, 'unreachable'
    elif isinstance(arg, Literal):
        return arg
    else:
        assert False, 'unreachable'


def stringify(expr: Expression) -> str:
    items = []
    for item in expr:
        if isinstance(item, Argument):
            items.append("<%s>" % str(item.typ).split('.', 1)[1].lower())
        elif isinstance(item, Literal):
            items.append(item)
        elif isinstance(item, Option):
            items.append("(%s | %s)" % (str(item.x), str(item.y)))
        else:
            assert False, 'unreachable'
    return " ".join(items)


class Parser:

    def __init__(self, values: List[Literal]):
        self.__values = values
        self.__models = {
            Argument: self.__case_argument,
            Option: self.__case_option,
            Literal: self.__case_literal,
        }

    @staticmethod
    def __case_option(item: Item, value: str, result: List[Value]) -> bool:
        if isinstance(item.x, Option) or isinstance(item.y, Option):
            raise Exception("Option inside option is not allowed.")
        x_check = check_type(item.x, value)
        y_check = check_type(item.y, value)
        if value == item.x and x_check:
            result.append(x_check)
        elif value == item.y and y_check:
            result.append(y_check)
        else:
            return False
        return True

    @staticmethod
    def __case_argument(item: Item, value: str, result: List[Value]) -> bool:
        value = check_type(item, value)
        if not value:
            return False
        result.append(value)
        return True

    @staticmethod
    def __case_literal(item: Item, value: str, result: List[Value]) -> bool:
        if value != item:
            return False
        result.append(item)
        return True

    def match(self, expr: Expression) -> List[Value]:
        values = []
        if len(self.__values) < len(expr):
            return []
        for index, item in enumerate(expr):
            value = self.__values[index]
            assert type(item) in self.__models, 'unreachable'
            if not self.__models[type(item)](item, value, values):
                return []
        return values

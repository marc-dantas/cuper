from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Union


Item = Union['Argument', 'Literal', 'Any', 'Option']
ANY_ITEM = ('Argument', 'Literal', 'Literals', 'Arguments')
Expression = List[Item]
Value = Union[int, str]  # Mapping for: Type.NUMBER | Type.TEXT


def stringify_type(x: 'Type') -> str:
    return 


class Type(Enum):
    TEXT = auto()
    NUMBER = auto()


@dataclass
class Result:
    success: bool
    values: List[Value]
    
    def __repr__(self) -> str:
        return f"Result: success: True, values: {self.values}" if self.success else "Result: success: False, values: []"
        
    def __str__(self) -> str:
        return self.__repr__()


# NOTE: This thing is for now completely useless. Because we have the type TEXT that matches anything.
# When I add more Type variants, it will be useful.
@dataclass
class Any:
    items: List[Type]
    
    def __repr__(self) -> str:
        return f"({' | '.join(repr(Argument(x)) for x in self.items)})"
    
    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Option:
    items: List['Literal']
    
    def __repr__(self) -> str:
        return f"({' | '.join(self.items)})"
    
    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Argument:
    typ: Type

    def __repr__(self) -> str:
        return f"<{str(self.typ).split('.', 1)[1].lower()}>"
    
    def __str__(self) -> str:
        return self.__repr__()

Literal = str

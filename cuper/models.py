from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Union


Item = Union['Argument', 'Literal', 'Option']
Expression = List[Item]
Value = Union[int, str]


class Type(Enum):
    TEXT = auto()
    NUMBER = auto()


# @dataclass
# class Error:
#     unmatched: Item
#     expected: Expression


@dataclass
class Argument:
    typ: Type


@dataclass
class Option:
    x: Union[Argument, 'Literal']
    y: Union[Argument, 'Literal']


Literal = str

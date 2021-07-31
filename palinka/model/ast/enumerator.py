from __future__ import annotations
from os import stat
from typing import Tuple, Union

from .constant_expression import ConstantExpression
from .identifier import Identifier

class Enumerator:
    """
        Represents an enum entry

        Eg: FOO = 1
    """
    def __init__(self, nodes: Union[
        Tuple[Identifier], 
        Tuple[Identifier, ConstantExpression]
    ], discr):
        self.nodes = list(nodes)
        self.discr = discr
    
    @staticmethod
    def first_case(n1: Identifier):
        return Enumerator((n1,), 1)

    @staticmethod
    def second_case(n1: Identifier, n2: ConstantExpression):
        return Enumerator((n1, n2), 2)

    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2      
    
    def __iter__(self):
        return iter(self.nodes)
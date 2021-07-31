from __future__ import annotations
from typing import Optional, Union, Tuple

from .identifier import Identifier
from .enumerator import Enumerator
from ...utils import flatten

class EnumSpecifier:
    """
        Represents an enumerator specifier

        <enum-specifier> ::= enum <identifier> { <enumerator-list> }
                        | enum { <enumerator-list> }
                        | enum <identifier>

        Implicit,
        <enumerator-list> ::= <enumerator> | <enumerator-list>, <enumerator>
    """
    def __init__(self, nodes: Union[
        Tuple[Identifier, list[Enumerator]],
        Tuple[list[Enumerator]],
        Tuple[Identifier]
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = flatten(list(nodes))

    @staticmethod
    def first_case(n1: Identifier, n2: list[Enumerator]):
        return EnumSpecifier((n1, n2), 1)

    @staticmethod   
    def second_case(n1: list[Enumerator]):
        return EnumSpecifier((n1,), 2)

    @staticmethod
    def third_case(n1: Identifier):
        return EnumSpecifier((n1,), 3)

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2
    
    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)
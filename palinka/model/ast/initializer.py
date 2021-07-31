from __future__ import annotations
from typing import Tuple

from ...utils import flatten
from .assignment_expression import AssignmentExpression

class InitializerList:
    """
        <initializer-list> ::= <initializer>
                            | <initializer-list> , <initializer>
    """

class Initializer:
    """
        <initializer> ::= <assignment-expression>
                        | { <initializer-list> }
                        | { <initializer-list> , }


    """
    def __init__(self, nodes: Tuple[AssignmentExpression, list[Initializer]], discr):
        self.discr = discr
        self.nodes = flatten(list(nodes))
    
    @staticmethod
    def first_case(n1: AssignmentExpression) -> Initializer:
        return Initializer((n1,), 1)
    
    @staticmethod
    def second_case(n1: InitializerList) -> Initializer:
        return Initializer((n1,), 2)
    
    @staticmethod
    def third_case(n1: InitializerList) -> Initializer:
        return Initializer((n1,), 3)

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2
    
    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)
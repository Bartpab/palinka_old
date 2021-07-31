from __future__ import annotations
from typing import Optional, Tuple, Type

from ...utils import flatten
from .type_qualifier import TypeQualifier

class Pointer:
    """
        <pointer> ::= * {<type-qualifier>}* {<pointer>}?
    """
    def __init__(self, nodes: Tuple[Optional[list[TypeQualifier]], Optional[Pointer]]):
        self.nodes = flatten(list(filter(lambda n: n is not None, nodes)))
    
    def create(n1: list[TypeQualifier], n2: Optional[Pointer]):
        return Pointer((n1, n2))

    @staticmethod
    def basic():
        return Pointer.create([], None)

    def __iter__(self):
        return iter(self.nodes)
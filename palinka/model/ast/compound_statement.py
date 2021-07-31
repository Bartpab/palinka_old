from __future__ import annotations
from typing import Tuple

from ...utils import flatten
from .declaration import Declaration
from .statement import Statement

class CompoundStatement:
    """
        <compound-statement> ::= { <declaration>* <statement>* }
    """
    def __init__(self, nodes: Tuple[list[Declaration], list[Statement]]):
        self.nodes = flatten(list(nodes))
    
    def create(n1: list[Declaration], n2: list[Statement]) -> CompoundStatement:
        return CompoundStatement((n1, n2))

    def __iter__(self):
        return iter(self.nodes)
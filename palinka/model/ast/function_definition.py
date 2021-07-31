from __future__ import annotations
from typing import Tuple

from ...utils import flatten
from .declaration_specifier import DeclarationSpecifier
from .declarator import Declarator
from .declaration import Declaration
from .compound_statement import CompoundStatement

class FunctionDefinition:
    """
        <function-definition> ::= <declaration-specifier>* <declarator> <declaration>* <compound-statement>
    """
    def __init__(self, nodes: Tuple[list[DeclarationSpecifier], Declarator, list[Declaration], CompoundStatement]):
        self.nodes = flatten(list(nodes))

    @staticmethod
    def create(n1: list[DeclarationSpecifier], n2: Declarator, n3: list[Declaration], n4: CompoundStatement):
        return FunctionDefinition((n1, n2, n3, n4))

    def __iter__(self):
        return iter(self.nodes)
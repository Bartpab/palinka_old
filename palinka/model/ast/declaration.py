from __future__ import annotations
from __future__ import annotations
from typing import Tuple

from ...utils import flatten
import palinka.model.ast.declaration_specifier as declaration_specifier
from .init_declarator import InitDeclarator

class Declaration:
    """
        Represents a declaration.

        <declaration> ::= <declaration-specifier>+ <init-declarator>*;
    """
    def __init__(self, nodes: Tuple[list[declaration_specifier.DeclarationSpecifier], list[InitDeclarator]]):
        if len(nodes[0]) < 1:
            raise Exception("At least on declaration specifier must be set")

        self.nodes = flatten(list(nodes))
    
    @staticmethod
    def create(n1: list[declaration_specifier.DeclarationSpecifier], n2: list[InitDeclarator]):
        return Declaration((n1, n2))

    def __iter__(self):
        return iter(self.nodes)
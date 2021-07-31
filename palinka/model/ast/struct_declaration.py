from __future__ import annotations
from typing import Tuple

from ...utils import flatten
from .specifier_qualifier import SpecifierQualifier
from .struct_declarator import StructDeclarator

class StructDeclaration:
    """
        struct-declaration ::= <specifier_qualifier>* (<struct_declarator> (, <struct_declarator>)*)
    """
    def __init__(self, nodes: Tuple[list[SpecifierQualifier], list[StructDeclarator]]):
        self.case = nodes
        self.nodes = flatten(list(nodes))
    
    def __iter__(self):
        return iter(self.nodes)
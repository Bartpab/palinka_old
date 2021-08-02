from __future__ import annotations

from typing import Optional, Tuple
from ...utils import flatten

import palinka.model.ast.specifier_qualifier as specifier_qualifier
import palinka.model.ast.abstract_declarator as abstract_declarator

class TypeName:
    """
        <type-name> ::= {<specifier-qualifier>}+ {<abstract-declarator>}?
    """
    def __init__(self, nodes: Tuple[list[specifier_qualifier.SpecifierQualifier], Optional[abstract_declarator.AbstractDeclarator]]):
        self.nodes = flatten(list(filter(lambda n: n is not None, nodes)))
    
    @staticmethod
    def create(n1: list[specifier_qualifier.SpecifierQualifier], n2: Optional[abstract_declarator.AbstractDeclarator]):
        return TypeName((n1, n2))

    def __iter__(self):
        return iter(self.nodes)
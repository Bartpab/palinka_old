from __future__ import annotations
from typing import Optional, Tuple, Union
from typing import Union as PyUnion

from .identifier import Identifier
from .struct_declaration import StructDeclaration

import palinka.model.ast.type_specifier as type_specifier

class Struct:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

class Union:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes) 

class StructOrUnionSpecifier:
    """
        <struct-struct-specifier> ::= <struct-or-union> <identifier> { {<struct-declaration>}+ }
                              | <struct-or-union>  { {<struct-declaration>}+ }
                              | <struct-or-union>  <identifier>
    """
    def __init__(self, nodes: PyUnion[
            Tuple[PyUnion[Struct, Union], Identifier, list[StructDeclaration]],
            Tuple[PyUnion[Struct, Union], list[StructDeclaration]],
            Tuple[PyUnion[Struct, Union], Identifier]
        ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)

    @staticmethod
    def struct_identifier(n2: Identifier):
        return StructOrUnionSpecifier((Struct(), n2), 3)

    @staticmethod
    def first_case(n0: PyUnion[Struct, Union], n1: Identifier, n2: list[StructDeclaration]):
        return StructOrUnionSpecifier((n0, n1, n2), 1)

    @staticmethod
    def second_case(n0: PyUnion[Struct, Union], n1: list[StructDeclaration]):
        return StructOrUnionSpecifier((n0, n1,), 2)
    
    @staticmethod
    def third_case(n0: PyUnion[Struct, Union], n1: Identifier):
        return StructOrUnionSpecifier((n0, n1,), 3)

    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)

    def as_type_specifier(self) -> type_specifier.TypeSpecifier:
        return type_specifier.TypeSpecifier(self)
    
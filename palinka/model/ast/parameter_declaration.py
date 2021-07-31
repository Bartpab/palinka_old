from __future__ import annotations
from typing import Optional, Union, Tuple

from .declaration_specifier import DeclarationSpecifier
from .declarator import Declarator

import palinka.model.ast.abstract_declarator as abstract_declarator
from ...utils import flatten

class ParameterDeclaration:
    """
    
        <parameter-declaration> ::= <declaration-specifier>+ <declarator>
                          | <declaration-specifier>+ <abstract-declarator>
                          | <declaration-specifier>+

    """
    def __init__(self, nodes: Tuple[list[DeclarationSpecifier], Optional[Union[Declarator, abstract_declarator.AbstractDeclarator]]]):
        self.nodes = flatten(list(filter(lambda n: n is not None, nodes)))

    @staticmethod
    def create(n1: list[DeclarationSpecifier], n2: Declarator):
        return ParameterDeclaration((n1, n2))

    @staticmethod    
    def first_case(n1: list[DeclarationSpecifier], n2: Declarator):
        return ParameterDeclaration((n1, n2))

    @staticmethod    
    def second_case(n1: list[DeclarationSpecifier], n2: abstract_declarator.AbstractDeclarator):
        return ParameterDeclaration((n1, n2))

    @staticmethod    
    def third_case(n1: list[DeclarationSpecifier]):
        return ParameterDeclaration((n1,))

    def __iter__(self):
        return iter(self.nodes)
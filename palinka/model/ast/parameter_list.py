from __future__ import annotations
from typing import Union, Tuple

from .parameter_declaration import ParameterDeclaration
from ...utils import flatten

class ParameterList:
    """
        <parameter-list> ::= <parameter-declaration>
                   | <parameter-list> , <parameter-declaration>
    """
    def __init__(self, nodes: Union[Tuple[ParameterDeclaration], Tuple[ParameterList, ParameterDeclaration]]):
        self.case = nodes
        self.nodes = flatten(list(nodes))
    
    @staticmethod
    def create(n1: ParameterDeclaration):
        return ParameterList((n1,))

    @staticmethod
    def concat(n1: ParameterList, n2: ParameterDeclaration):
        return ParameterList((n1, n2))

    def __iter__(self):
        return iter(self.nodes)
from __future__ import annotations
from palinka.model.ast.declaration import Declaration
from typing import Optional, Union, Tuple

from .identifier import Identifier

import palinka.model.ast.parameter_list as parameter_list

from .constant_expression import ConstantExpression
from .pointer import Pointer

from ...utils import flatten

class DirectDeclarator:
    """
        Represents a direct declarator

        <direct-declarator> ::= <identifier>
                            | <declarator>
                            | <direct-declarator> [<constant-expression>?]
                            | <direct-declarator> (<parameter-list>)
                            | <direct-declarator> (<identifier>*)
    """
    def __init__(self, nodes: Union[
        Tuple[Identifier],
        Tuple[Declarator],
        Tuple[DirectDeclarator, Optional[ConstantExpression]],
        Tuple[DirectDeclarator, parameter_list.ParameterList],
        Tuple[DirectDeclarator, list[Identifier]]
    ]):
        self.case = nodes
        self.nodes = flatten(list(nodes))

    def is_first_case(self):
        return len(self.nodes) == 1 and isinstance(self.nodes[0], Identifier)
    
    def is_second_case(self):
        return len(self.nodes) == 1 and isinstance(self.nodes[0], Declarator)
    
    def is_third_case(self):
        return len(self.case) == 2 and (isinstance(self.case[1], ConstantExpression) or self.case[1] is None)
    
    def is_fourth_case(self):
        return len(self.nodes) == 2 and isinstance(self.nodes[1], parameter_list.ParameterList)

    def is_fifth_case(self):
        return len(self.case) == 2 and isinstance(self.cases[1], list)

    def identifier(n1: Identifier):
        return DirectDeclarator((n1,))
    
    def declarattor(n1: Declarator):
        return DirectDeclarator((n1,))

    def call(n1: DirectDeclarator, n2: parameter_list.ParameterList):
        return DirectDeclarator((n1, n2))

    def __iter__(self):
        return iter(self.nodes)

class Declarator:
    """
        Represents a declarator

        <declarator> ::= <pointer>? <direct-declarator>
    """
    def __init__(self, nodes: Tuple[Optional[Pointer], DirectDeclarator]):
        self.nodes = list(filter(lambda n: n is not None, nodes))
    
    def create(pointer: Optional[Pointer], direct: DirectDeclarator):
        return Declarator((pointer, direct))

    def __iter__(self):
        return iter(self.nodes)
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
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = flatten(list(nodes))

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2
    
    def is_third_case(self):
        return self.discr == 3
    
    def is_fourth_case(self):
        return self.discr == 4

    def is_fifth_case(self):
        return self.discr == 5

    def identifier(n1: Identifier):
        return DirectDeclarator((n1,), 1)
    
    def declarator(n1: Declarator):
        return DirectDeclarator((n1,), 2)

    def call(n1: DirectDeclarator, n2: Optional[parameter_list.ParameterList]):
        if n2 is None:
            return DirectDeclarator((n1, []), 5)

        return DirectDeclarator((n1, n2), 4)

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
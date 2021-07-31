from palinka.model.ast.type_qualifier import Const
from typing import Tuple, Union

from .declarator import Declarator
from .constant_expression import ConstantExpression

class StructDeclarator:
    """
        <struct-declarator> ::= <declarator>
                      | <declarator> ':' <constant-expression>
                      | ':' <constant-expression>

    """
    def __init__(self, nodes: Union[
        Tuple[Declarator],
        Tuple[Declarator, ConstantExpression],
        Tuple[ConstantExpression]
    ], discr):
        self.case = nodes
        self.nodes = list(nodes)

    @staticmethod
    def first_case(n1: Declarator):
        return StructDeclarator((n1,), 1)

    @staticmethod
    def second_case(n1: Declarator, n2: ConstantExpression):
        return StructDeclarator((n1, n2), 2)

    @staticmethod
    def third_case(n1: ConstantExpression):
        return StructDeclarator((n1,), 3)

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2
    
    def is_third_case(self):
        return self.discr == 3

    def __iter__(self):
        return iter(self.nodes)   
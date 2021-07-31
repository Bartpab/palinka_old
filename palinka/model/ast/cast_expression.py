from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.type_name as type_name
import palinka.model.ast.unary_expression as unary_expression
import palinka.model.ast.multiplicative_expression as multiplicative_expression
import palinka.model.ast.expression as expression

class CastExpression(BaseExpression):
    """
        Represents a cast expression.

        <cast-expression> ::= <unary-expression>
                          |  (<type-name>) <cast-expression>

        Eg: (char*) variable
    """
    def __init__(self, nodes: Union[
            Tuple[unary_expression.UnaryExpression], 
            Tuple[type_name.TypeName, CastExpression]
        ], discr):
        self.discr = discr
        self.nodes = list(nodes)
    
    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2

    def __iter__(self):
        return iter(self.nodes)
    
    @staticmethod
    def create(n1: unary_expression.UnaryExpression):
        return CastExpression((n1,), 1)
    
    @staticmethod
    def expr(n1: type_name.TypeName, n2: CastExpression):
        return CastExpression((n1, n2), 2)

    def as_expression(self) -> expression.Expression:
        return multiplicative_expression.MultiplicativeExpression.create(self).as_expression()
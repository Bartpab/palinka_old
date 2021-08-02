from __future__ import annotations

from typing import Union, Tuple

from .type_name import TypeName
from .base_expression import BaseExpression

import palinka.model.ast.postfix_expression as postfix_expression
import palinka.model.ast.cast_expression as cast_expression
import palinka.model.ast.expression as expression

class UnaryOperator:
    def __init__(self, op: str):
        self.op = op
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)
    
    @staticmethod
    def inc():
        return UnaryOperator('++')
    
    @staticmethod
    def dec():
        return UnaryOperator('--')

class SizeOf:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

class UnaryExpression(BaseExpression):
    def __init__(self, nodes: Union[
        Tuple[postfix_expression.PostfixExpression], 
        Tuple[UnaryOperator, UnaryExpression], 
        Tuple[UnaryOperator, cast_expression.CastExpression], 
        Tuple[SizeOf, UnaryExpression], 
        Tuple[SizeOf, TypeName]
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)

    @staticmethod
    def unary(n1: UnaryOperator, n2: cast_expression.CastExpression):
        return UnaryExpression((n1, n2), 3)

    @staticmethod
    def sizeof_typename(n1: TypeName):
        return UnaryExpression((SizeOf(), n1), 5)

    def is_fifth_case(self):
        return self.discr == 5

    @staticmethod
    def create(n1: postfix_expression.PostfixExpression):
        return UnaryExpression((n1,), 1)

    def __iter__(self):
        return iter(self.nodes)
    
    def as_expression(self) -> expression.Expression:
        return cast_expression.CastExpression.create(self).as_expression()
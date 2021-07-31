from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.cast_expression as cast_expression
import palinka.model.ast.expression as expression
import palinka.model.ast.additive_expression as additive_expression

class MultiplicativeExpressionBinop:
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def mult():
        """
            Multiplication operator: *
        """
        return MultiplicativeExpressionBinop('*')
    
    @staticmethod
    def div():
        """
            Division operator: /
        """
        return MultiplicativeExpressionBinop("/")
    
    @staticmethod
    def mod():
        """
            Modulo operator: %
        """
        return MultiplicativeExpressionBinop("%")

class MultiplicativeExpression(BaseExpression):
    def __init__(self, nodes: Union[Tuple[cast_expression.CastExpression], Tuple[MultiplicativeExpression, MultiplicativeExpressionBinop, cast_expression.CastExpression]], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    @staticmethod
    def create(n1: cast_expression.CastExpression):
        return MultiplicativeExpression((n1,), 1)
    
    @staticmethod
    def expr(n1: MultiplicativeExpression, n2: MultiplicativeExpressionBinop, n3: cast_expression.CastExpression):
        """
            <multiplicative-expression> ::= <multiplicative-expression> <multiplicative-expression-binop> <cast-expression>
        """
        return MultiplicativeExpression((n1, n2, n3), 2)
    
    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def __iter__(self):
        return iter(self.nodes)

    def as_expression(self) -> expression.Expression:
        return additive_expression.AdditiveExpression.create(self).as_expression()
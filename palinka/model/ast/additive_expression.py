from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.multiplicative_expression as multiplicative_expression
import palinka.model.ast.shift_expression as shift_expression
import palinka.model.ast.expression as expression

class AdditiveExpressionBinop:
    def __init__(self, op):
        self.op = op
        self.nodes = []

    @staticmethod
    def add():
        return AdditiveExpressionBinop('+')
    
    @staticmethod
    def sub():
        return AdditiveExpressionBinop('-')
    
    def __iter__(self):
        return iter(self.nodes)

class AdditiveExpression(BaseExpression):
    """
        Represents an additive expression.


        <additive-expression> ::= <multiplicative-expression>
                              | 
        Eg: lh + rh; lh - rh.
    """
    def __init__(self, nodes: Union[
            Tuple[multiplicative_expression.MultiplicativeExpression], 
            Tuple[AdditiveExpression, AdditiveExpressionBinop, multiplicative_expression.MultiplicativeExpression]
        ]):
        self.case = nodes
        self.nodes = list(nodes)
    
    @staticmethod
    def create(n1: multiplicative_expression.MultiplicativeExpression):
        return AdditiveExpression((n1,))
    
    @staticmethod
    def expr(n1: AdditiveExpression, n2: AdditiveExpressionBinop, n3: multiplicative_expression.MultiplicativeExpression) -> AdditiveExpression:
        return AdditiveExpression((n1, n2, n3))
    
    def __iter__(self):
        return iter(self.nodes)

    def as_expression(self) -> expression.Expression:
        return shift_expression.ShiftExpression.create(self).as_expression()
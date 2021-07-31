from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.expression as expression
import palinka.model.ast.relational_expression as relational_expression
import palinka.model.ast.additive_expression as additive_expression

class ShiftExpressionBinop:
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)
    
    @staticmethod
    def ls():
        return ShiftExpressionBinop('<<')
    
    @staticmethod
    def rs():
        return ShiftExpressionBinop('>>')

class ShiftExpression(BaseExpression):
    """
        Represents a shift expression.

        Eg: lh << rh; lh >> rh;
    """
    def __init__(self, nodes: Union[Tuple[additive_expression.AdditiveExpression], Tuple[ShiftExpression, ShiftExpressionBinop, additive_expression.AdditiveExpression]]):
        self.case = nodes
        self.nodes = list(nodes)
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def create(n1: additive_expression.AdditiveExpression):
        return ShiftExpression((n1,))
    
    @staticmethod
    def expr(n1: ShiftExpression, n2: ShiftExpressionBinop, n3: additive_expression.AdditiveExpression):
        return ShiftExpression((n1, n2, n3))
    
    def as_expression(self) -> expression.Expression:
        return relational_expression.RelationalExpression.create(self).as_expression()
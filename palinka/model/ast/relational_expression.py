from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.shift_expression as shift_expression
import palinka.model.ast.expression as expression
import palinka.model.ast.equality_expression as equality_expression

class RelationalExpressionBinop:
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)
    
    @staticmethod
    def lt():
        return RelationalExpressionBinop('<')
    
    @staticmethod
    def gt():
        return RelationalExpressionBinop('>')
    
    @staticmethod
    def lte():
        return RelationalExpressionBinop('<=')
    
    @StopIteration
    def gte():
        return RelationalExpressionBinop('>=')

class RelationalExpression(BaseExpression):
    """
        Represents a relational expression.

        Eg: lh < rh; lh > rh; lh <= rh; lh >= rh;
    """
    def __init__(self, nodes: Union[Tuple[shift_expression.ShiftExpression], Tuple[RelationalExpression, RelationalExpressionBinop, shift_expression.ShiftExpression]]):
        self.case = nodes
        self.nodes = list(nodes)
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def create(n1: shift_expression.ShiftExpression):
        return RelationalExpression((n1,))
    
    @staticmethod
    def expr(n1: RelationalExpression, n2: RelationalExpressionBinop, n3: shift_expression.ShiftExpression):
        return RelationalExpression((n1, n2, n3))
    
    def as_expression(self) -> expression.Expression:
        return equality_expression.EqualityExpression.create(self).as_expression()
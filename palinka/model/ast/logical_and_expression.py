from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression
import palinka.model.ast.inclusive_or_expression as inclusive_or_expression
import palinka.model.ast.logical_or_expression as logical_or_expression
import palinka.model.ast.expression as expression

class LogicalAndExpression(BaseExpression):
    """
        Represents a logical and expression.

        <logical-and-expression> ::= <inclusive-or-expression>
                                  | <logical-and-expression> && <inclusive-or-expression>

        Eg: lh && rh
    """
    def __init__(self, nodes: Union[Tuple[inclusive_or_expression.InclusiveOrExpression], Tuple[LogicalAndExpression, inclusive_or_expression.InclusiveOrExpression]], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def create(n1: inclusive_or_expression.InclusiveOrExpression):
        return LogicalAndExpression((n1,), 1)
    
    @staticmethod
    def expr(n1: LogicalAndExpression, n2: inclusive_or_expression.InclusiveOrExpression):
        return LogicalAndExpression((n1, n2), 2)
    
    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def as_expression(self) -> expression.Expression:
        return logical_or_expression.LogicalOrExpression.create(self).as_expression()
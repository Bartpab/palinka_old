from __future__ import annotations
from typing import Tuple, Union

from .base_expression import BaseExpression

import palinka.model.ast.logical_and_expression as logical_and_expression
import palinka.model.ast.expression as expression
import palinka.model.ast.conditional_expression as conditional_expression

class LogicalOrExpression(BaseExpression):
    """
        Represents a logical or expression.


        <logical-or-expression> ::= <logical-and-expression>
                                    | <logical-or-expression> || <logical-and-expression>

        Eg: lh || rh
    """
    def __init__(self, nodes: Union[Tuple[logical_and_expression.LogicalAndExpression], Tuple[LogicalOrExpression, logical_and_expression.LogicalAndExpression]], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    def __iter__(self):
        return iter(self.nodes)

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2

    @staticmethod
    def create(n1: logical_and_expression.LogicalAndExpression):
        return LogicalOrExpression((n1,), 1)
    
    @staticmethod
    def expr(n1: LogicalOrExpression, n2: logical_and_expression.LogicalAndExpression):
        """
            <logical-or-expression> ::= <logical-or-expression> || <logical-and-expression>
        """
        return LogicalOrExpression((n1, n2), 2)
    
    def as_expression(self) -> expression.Expression:
        return conditional_expression.ConditionalExpression.create(self).as_expression()
from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.exclusive_or_expression as exclusive_or_expression
import palinka.model.ast.expression as expression
import palinka.model.ast.logical_and_expression as logical_and_expression

class InclusiveOrExpression(BaseExpression):
    """
        Represents an inclusive or expession.

        Eg: lh | rh
    """
    def __init__(self, nodes: Union[Tuple[exclusive_or_expression.ExclusiveOrExpression], Tuple[InclusiveOrExpression, exclusive_or_expression.ExclusiveOrExpression]], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    @staticmethod
    def create(n1: exclusive_or_expression.ExclusiveOrExpression):
        """
            <inclusive-or-expression> ::= <exclusive-or-expression>
        """
        return InclusiveOrExpression((n1,), 1)
    
    def expr(n1: InclusiveOrExpression, n2: exclusive_or_expression.ExclusiveOrExpression):
        """
            <inclusive-or-expression> ::= <inclusive-or-expression> '|' <exclusive-or-expression>
        """
        return InclusiveOrExpression((n1, n2), 2)
    
    def is_first_case(self):
        """
            <inclusive-or-expression> ::= <exclusive-or-expression>
        """
        return self.discr == 1
    
    def is_second_case(self):
        """
            <inclusive-or-expression> ::= <inclusive-or-expression> '|' <exclusive-or-expression>
        """
        return self.discr == 2

    def __iter__(self):
        return iter(self.nodes)

    def as_expression(self) -> expression.Expression:
        return logical_and_expression.LogicalAndExpression.create(self).as_expression()
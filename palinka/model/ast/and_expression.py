from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.equality_expression as equality_expression
import palinka.model.ast.expression as expression
import palinka.model.ast.exclusive_or_expression as exclusive_or_expression

class AndExpression(BaseExpression):
    """
        Represents an and Expression.

        <and-expression> ::= <equality-expression>
                         | <and-expression> & <equality-expression>

        Eg: h & rh
    """
    def __init__(self, nodes: Union[
            Tuple[equality_expression.EqualityExpression], 
            Tuple[AndExpression, equality_expression.EqualityExpression]
        ]):
        self.case = nodes
        self.nodes = list(nodes)

    def is_first_case(self):
        return len(self.nodes) == 1
    
    def is_second_case(self):
        return len(self.nodes) == 2

    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def create(n1: equality_expression.EqualityExpression):
        return AndExpression((n1,))
    
    @staticmethod
    def expr(n1: AndExpression, n2: equality_expression.EqualityExpression):
        return AndExpression((n1, n2))

    def as_expression(self) -> expression.Expression:
        return exclusive_or_expression.ExclusiveOrExpression.create(self).as_expression()
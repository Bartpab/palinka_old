from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.expression as expression
import palinka.model.ast.logical_or_expression as logical_or_expression
import palinka.model.ast.assignment_expression as assignment_expression

class ConditionalExpression(BaseExpression):
    """
        Represents a ternary conditional expression.

        <conditional-expression> ::= <logical-or-expression> 
                                 | <logical-or-expression> ? <expression> : <conditional-expression>

        Eg: predicate ? expression : other
    """
    def __init__(self, nodes: Union[
        Tuple[logical_or_expression.LogicalOrExpression], 
        Tuple[
            logical_or_expression.LogicalOrExpression, 
            expression.Expression, 
            ConditionalExpression
            ]
        ]):
        self.case = nodes
        self.nodes = list(nodes)
    
    def is_first_case(self) -> bool:
        return len(self.nodes) == 1
    
    def is_second_case(self) -> bool:
        return len(self.nodes) == 3

    @staticmethod
    def create(n1: logical_or_expression.LogicalOrExpression):
        return ConditionalExpression((n1,))

    @staticmethod
    def expr(predicate: logical_or_expression.LogicalOrExpression, expression: expression.Expression, other: ConditionalExpression):
        """
            <conditional-expression> ::= <logical-or-expression> ? <expression> : <conditional-expession>
        """
        return ConditionalExpression((predicate, expression, other))
    
    def __iter__(self):
        return iter(self.nodes)

    def as_parent(self) -> assignment_expression.AssignmentExpression:
        return assignment_expression.AssignmentExpression.create(self)

    def as_expression(self) -> expression.Expression:
        return self.as_parent().as_expression()
from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.expression as expression
import palinka.model.ast.conditional_expression as conditional_expression
import palinka.model.ast.unary_expression as unary_expression

class AssignmentExpressionOp:
    """
        Assignment operator

        Eg: =, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=
    """
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)

class AssignmentExpression(BaseExpression):

    """
        Represents an assignment expression.

        <assignment-expression> ::= <conditional-expression>
                                | <unary-expression> <assignement-expression-op> <assignment-expression>

        Eg: lh = rh
    """
    def __init__(self, nodes: Union[
        Tuple[conditional_expression.ConditionalExpression], 
        Tuple[unary_expression.UnaryExpression, AssignmentExpressionOp, AssignmentExpression],
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2

    @staticmethod
    def create(n1: conditional_expression.ConditionalExpression):
        return AssignmentExpression((n1,), 1)

    @staticmethod
    def expr(n1: conditional_expression.ConditionalExpression, n2: str, n3: AssignmentExpression):
        return AssignmentExpression((n1, AssignmentExpressionOp(n2), n3), 2)

    def __iter__(self):
        return iter(self.nodes)

    def as_parent(self) -> expression.Expression:
        return expression.Expression.create(self)

    def as_expression(self) -> expression.Expression:
        return self.as_parent().as_expression()
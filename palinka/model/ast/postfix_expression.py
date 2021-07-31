from __future__ import annotations
from os import stat
from typing import Union, Tuple

from ...utils import flatten

from .base_expression import BaseExpression
from .identifier import Identifier

import palinka.model.ast.primary_expression as primary_expression
import palinka.model.ast.unary_expression as unary_expression
import palinka.model.ast.assignment_expression as assignment_expression
import palinka.model.ast.expression as expression


class PostfixExpressionBinaryOp:
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)
    
    @staticmethod
    def dot():
        return PostfixExpressionBinaryOp('.')
    
    @staticmethod
    def arrow():
        return PostfixExpressionBinaryOp('->')

class PostfixExpressionSingleOp:
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def inc():
        return PostfixExpressionSingleOp('++')
    
    @staticmethod
    def dec():
        return PostfixExpressionSingleOp('--')
    
class PostfixExpression(BaseExpression):
    """

    
        <postfix-expression> ::= <primary-expression>
                       | <postfix-expression> [ <expression> ]
                       | <postfix-expression> ( {<assignment-expression>}* )
                       | <postfix-expression> . <identifier>
                       | <postfix-expression> -> <identifier>
                       | <postfix-expression> ++
                       | <postfix-expression> --
    """
    def __init__(self, nodes: Union[
        Tuple[primary_expression.PrimaryExpression], 
        Tuple[PostfixExpression, expression.Expression],
        Tuple[PostfixExpression, list[assignment_expression.AssignmentExpression]],
        Tuple[PostfixExpression, PostfixExpressionBinaryOp, Identifier],
        Tuple[PostfixExpression, PostfixExpressionSingleOp]
    ], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = flatten(list(nodes))
    
    @staticmethod
    def create(n1: primary_expression.PrimaryExpression) -> PostfixExpression:
        return PostfixExpression((n1,), 1)

    @staticmethod
    def call(n1: PostfixExpression, n2: list[expression.AssignmentExpression]) -> PostfixExpression:
        return PostfixExpression((n1, n2), 3)

    @staticmethod
    def first_case(n1: primary_expression.PrimaryExpression):
        return PostfixExpression((n1,), 1)

    @staticmethod
    def second_case(n1: PostfixExpression, n2: expression.Expression):
        return PostfixExpression((n1, n2), 2)

    @staticmethod
    def third_case(n1: PostfixExpression, n2: list[assignment_expression.AssignmentExpression]):
        return PostfixExpression((n1, n2), 3)

    @staticmethod
    def fourth_case(n1: PostfixExpression, n2: Identifier):
        return PostfixExpression((n1, PostfixExpressionBinaryOp.dot(), n2), 4)

    @staticmethod
    def fifth_case(n1: PostfixExpression, n2: Identifier):
        return PostfixExpression((n1, PostfixExpressionBinaryOp.arrow(), n2), 5)

    @staticmethod
    def sixth_case(n1: PostfixExpression):
        return PostfixExpression((n1, PostfixExpressionSingleOp.inc()), 6)

    @staticmethod
    def seventh_case(n1: PostfixExpression):
        return PostfixExpression((n1, PostfixExpressionSingleOp.dec()), 6)

    def is_first_case(self):
        return self.discr == 1

    def is_second_case(self):
        return self.discr == 2

    def is_third_case(self):
        return self.discr == 3

    def is_fourth_case(self):
        return self.discr == 4

    def is_fifth_case(self):
        return self.discr == 5

    def is_sixth_case(self):
        return self.discr == 6

    def is_seventh_case(self):
        return self.discr == 7

    def __iter__(self):
        return iter(self.nodes)

    def as_expression(self) -> expression.Expression:
        return unary_expression.UnaryExpression.create(self).as_expression()
        
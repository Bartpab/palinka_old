from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.relational_expression as relational_expression
import palinka.model.ast.expression as expression
import palinka.model.ast.and_expression as and_expression

class EqualityExpressionBinop:
    """
        Binary operator for equality expressions. Either == or !=.
    """
    def __init__(self, op: str):
        self.op = op
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def eq():
        return EqualityExpressionBinop('==')
    
    @staticmethod
    def neq():
        return EqualityExpressionBinop('!=')

class EqualityExpression(BaseExpression):
    """
        Represents an equality expression.


        <equality-expression> ::= <relational-expression>
                                | <equality-expression> == <relational-expression>
                                | <equality-expression> != <relational-expression>

        Ex: lh == rh or lh != rh
    """
    def __init__(self, nodes: Union[Tuple[relational_expression.RelationalExpression], Tuple[EqualityExpression, EqualityExpressionBinop, relational_expression.RelationalExpression]], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def create(n1: relational_expression.RelationalExpression):
        """
            <equality-expression> ::= <relational-expression>
        """
        return EqualityExpression((n1,), 1)
    
    @staticmethod
    def expr(n1: EqualityExpression, n2: EqualityExpressionBinop, n3: relational_expression.RelationalExpression):
        """
            <equality-expression> ::= <equality-expression> <equality-expression-binop> <relational-expression>
        """
        return EqualityExpression((n1, n2, n3), 2)
    
    def is_first_case(self):
        """
            <equality-expression> ::= <relational-expression>
        """
        return self.discr == 1
    
    def is_second_case(self):
        """
            <equality-expression> ::= <equality-expression> <equality-expression-binop> <relational-expression>
        """
        return self.discr == 2

    def as_expression(self) -> expression.Expression:
        return and_expression.AndExpression.create(self).as_expression()
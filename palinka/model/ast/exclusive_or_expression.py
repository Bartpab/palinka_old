from __future__ import annotations
from typing import Union, Tuple

from .base_expression import BaseExpression

import palinka.model.ast.expression as expression
import palinka.model.ast.inclusive_or_expression as inclusive_or_expression
import palinka.model.ast.and_expression as and_expression

class ExclusiveOrExpression(BaseExpression):
    """
        Represents a xor expression.
        
        <exclusive-or-expression> ::= <and-expression>
                                    | <exclusive-or-expression> ^ <and-expression>
        
        Ex: lh ^ rh
    """
    def __init__(self, nodes: Union[Tuple[and_expression.AndExpression], Tuple[ExclusiveOrExpression, and_expression.AndExpression]], discr):
        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)
    
    @staticmethod
    def create(n1: and_expression.AndExpression):
        """
            <exclusive-or-expression> ::= <and-expression>
        """
        return ExclusiveOrExpression((n1,), 1)
    
    @staticmethod
    def expr(n1: ExclusiveOrExpression, n2: and_expression.AndExpression):
        """
            <exclusive-or-expression> ::= <exclusive-or-expression> ^ <and-expression>
        """
        return ExclusiveOrExpression((n1, n2), 2)
    
    def is_first_case(self):
        """
            <exclusive-or-expression> ::= <and-expression>
        """
        return self.discr == 1
    
    def is_second_case(self):
        """
            <exclusive-or-expression> ::= <exclusive-or-expression> ^ <and-expression>
        """
        return self.discr == 2
    
    def __iter__(self):
        return iter(self.nodes)

    def as_expression(self) -> expression.Expression:
        return inclusive_or_expression.InclusiveOrExpression.create(self).as_expression()
from __future__ import annotations
from typing import Union, Tuple

from .assignment_expression import AssignmentExpression
from .base_expression import BaseExpression

import palinka.model.ast.statement as statement

class Expression(BaseExpression):
    """
        <expression> ::= <assignment-expression>
               | <expression> , <assignment-expression>
    """
    def __init__(self, nodes: Union[
            Tuple[AssignmentExpression], 
            Tuple[Expression, AssignmentExpression]
        ], discr):

        self.discr = discr
        self.case = nodes
        self.nodes = list(nodes)

    @staticmethod
    def concat(n1: Expression, n2: AssignmentExpression):
        """
            <expression> ::= <expression>, <assignment-expression>
        """
        return Expression((n1, n2), 2)

    @staticmethod
    def create(n1: AssignmentExpression):
        """
            <expression> ::= <assignment-expression>
        """
        return Expression((n1,), 1)
    
    def is_first_case(self):
        """
            <expression> ::= <assignment-expression>
        """
        return self.discr == 1
    
    def is_second_case(self):
        """
            <expression> ::= <expression>, <assignment-expression>
        """
        return self.discr == 2
    
    def as_parent(self) -> statement.ExpressionStatement:
        return statement.ExpressionStatement(self)

    def as_child(self, type):
        stack = [self]
        
        visited = []

        while stack:
            node = stack.pop(0)
            visited.append(node.__class__.__name__)
            
            if isinstance(node, type):
                return node

            stack += list(iter(node))
        
        raise Exception(f"Cannot cast to {type.__name__}: {visited}")

    def as_expression(self):
        return self

    def __iter__(self):
        return iter(self.nodes)
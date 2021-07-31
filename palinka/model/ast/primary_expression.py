from __future__ import annotations
from palinka.model.ast import expression
from typing import Union

from .base_expression import BaseExpression
from .identifier import Identifier
from .constant import Constant
from .string import String

import palinka.model.ast.postfix_expression as postfix_expression
import palinka.model.ast.expression as expression

class PrimaryExpression(BaseExpression):
    def __init__(self, node: Union[Identifier, Constant, String, expression.Expression]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)

    @staticmethod
    def identifier(id: Identifier) -> PrimaryExpression:
        return PrimaryExpression(id)

    def as_postfix_expression(self) -> postfix_expression.PostfixExpression:
        return postfix_expression.PostfixExpression.create(self)
    
    def as_expression(self) -> expression.Expression:
        return postfix_expression.PostfixExpression.create(self).as_expression() 
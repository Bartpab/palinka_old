from __future__ import annotations

from .base_expression import BaseExpression
from .conditional_expression import ConditionalExpression

class ConstantExpression(BaseExpression):
    def __init__(self, node: ConditionalExpression):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
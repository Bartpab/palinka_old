from __future__ import annotations
from palinka.model.ast import expression
from typing import Union

from .base_expression import BaseExpression
from .identifier import Identifier
from .constant import Constant
from .string import String

import palinka.model.ast.postfix_expression as postfix_expression
import palinka.model.ast.identifier as identifier

class Include:
    def __init__(self, node: identifier.Identifier, internal=False):
        self.nodes = [node]
        self.internal = internal

    def __iter__(self):
        return iter(self.nodes)

class Preprocessor:
    def __init__(self, node: Union[Include]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
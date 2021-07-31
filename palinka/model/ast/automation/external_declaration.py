from typing import Union

from .function_block_definition import FunctionBlockDefinition
from ..function_definition import FunctionDefinition
from ..declaration import Declaration

class ExternalDeclaration:
    """
        Represents a translation-unit level declaration.

        This version is tailored for automation system code generation.

        <external-declaration> ::= <function-block-definition> | <function-definition> | <declaration>
    """
    def __init__(self, node: Union[FunctionBlockDefinition, FunctionDefinition, Declaration]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
    
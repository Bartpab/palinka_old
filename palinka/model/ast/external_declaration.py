from typing import Union

from .function_definition import FunctionDefinition
from .declaration import Declaration

class ExternalDeclaration:
    """
        <external-declaration> ::=  <function-definition> | <declaration>
    """
    def __init__(self, node: Union[FunctionDefinition, Declaration]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
    
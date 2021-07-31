
from __future__ import annotations

from collections.abc import Iterable, Iterator
from lxml import etree

from palinka.types import DataType

def find_nodes(node, predicate):
    stack = [node]
    while stack:
        node = stack.pop(0)
        
        if predicate(node):
            yield node

        stack += iter(node)

class AST_Type:
    SYSTEM      = 0
    FUNCTION    = 1

class ASTNode:
    PLANT = 0
    SYSTEM = 1
    FUNCTION_DECL = 2
    FUNCTION_ARG_DECL = 3
    FUNCTION_CALL = 4
    VAR_DECL = 5
    ASSIGNEMENT = 6
    VAR_ID = 7
    RETURN = 8

    def __init__(self, node_type: int):
        self.node_type = node_type

    def is_type(self, type_id: int):
        return self.node_type == type_id

    def __iter__(self):
        return iter([])

    def attributes(self):
        return {}

class PlantNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self, ASTNode.PLANT)
        self.functions: list[FunctionDeclNode] = []
        self.systems: list[SystemNode] = []

    def __iter__(self) -> Iterator[ASTNode]:
        return iter(self.systems + self.functions)

class SystemNode(ASTNode):
    """
        Represent a System-Level Node
    """
    def __init__(self, name: str):
        ASTNode.__init__(self, ASTNode.SYSTEM)
        self.name = name
        self.functions: list[FunctionDeclNode] = []

    def attributes(self):
        return {'name': self.name}

    def __iter__(self):
        return iter(self.functions)

    def get_name(self):
        return self.name

class FunctionCallNode(ASTNode):
    def __init__(self, name: str, arguments: list[ASTNode]):
        ASTNode.__init__(self, ASTNode.FUNCTION_CALL)
        self.name = name
        self.arguments = arguments

    def attributes(self):
        return {'name': self.name}

    def get_name(self) -> str:
        return self.id
    
    def get_arguments(self) -> Iterable[ASTNode]:
        return self.arguments
    
    def __iter__(self):
        return iter(self.arguments)

class Id(ASTNode):
    """
        Represents an Identifier
    """
    def __init__(self, name: str):
        self.name = name
    
    def attributes(self):
        return {'name': self.name}

class VarId(ASTNode):
    def __init__(self, name):
        ASTNode.__init__(self, ASTNode.VAR_ID)
        self.name = name

    def attributes(self):
        return {'name': self.name}

class Assignment(ASTNode):
    def __init__(self, lh, rh):
        ASTNode.__init__(self, ASTNode.ASSIGNEMENT)
        self.lh = lh
        self.rh = rh

    def __iter__(self):
        return iter([self.lh, self.rh])

class VarDecl(ASTNode):
    """
        Declare a variable.

        Each declaration will create an entry in the symbol table.

        If a variable is system-level scoped, no statement will appear in the final code.
    """
    def __init__(self, name, data_type, scope, symbolink = None):
        ASTNode.__init__(self, ASTNode.VAR_DECL)

        self.name       = name
        self.scope      = scope
        self.type       = data_type
        self.symbolink  = symbolink
    
    def attributes(self):
        return {'name': self.name, 'scope': self.scope, 'type': str(self.type), 'symbolink': self.symbolink}
    
class FunctionArgDecl(ASTNode):
    def __init__(self, name, data_type: DataType):
        ASTNode.__init__(self, ASTNode.FUNCTION_ARG_DECL)

        self.name: str = name
        self.type: DataType = data_type

    def attributes(self):
        return {'name': self.name, 'type': str(self.type)}

class FunctionDeclNode(ASTNode):
    def __init__(self, name):
        ASTNode.__init__(self, ASTNode.FUNCTION_DECL)

        self.return_type = None

        self.name: str = name
        self.args: list[FunctionArgDecl]   = []
        self.statements: list[ASTNode]  = []

    def attributes(self):
        return {'name': self.name}

    def __iter__(self):
        return iter(self.args + self.statements)


class Return(ASTNode):
    def __init__(self, id):
        ASTNode.__init__(self, ASTNode.RETURN)
        self.id = id
    
    def __iter__(self):
        return iter([self.id])
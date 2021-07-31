from __future__ import annotations
from typing import Tuple
from palinka.model.ast.enum_specifier import EnumSpecifier
from palinka.model.ast.type_specifier import TypeSpecifier
from palinka.model.ast.declaration import Declaration
from palinka.model.ast.declarator import Declarator, DirectDeclarator
from ..identifier import Identifier
from palinka.types import DataType

from ..function_definition import FunctionDefinition
from ..declaration_specifier import DeclarationSpecifier
from ..type_specifier import TypeSpecifier
from ..struct_or_union_specifier import StructOrUnionSpecifier, Struct
from ..compound_statement import CompoundStatement
from ..init_declarator import InitDeclarator
from ..identifier import Identifier
from ..pointer import Pointer

class DataBlockDefinition:
    def __init__(self, nodes: list[DataBlockEntryDeclaration]):
        self.nodes = nodes

    def __iter__(self):
        return iter(self.nodes)

class DataBlockEntryDeclaration:
    def __init__(self, name: str, type: DataType):
        self.name: str = name
        if not isinstance(type, DataType):
            raise Exception("Expecting data_type to be an instance of DataType.")
        self.type: DataType = type
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)

class FunctionBlockDefinition:
    """
        A function block is a function bound to an instance data block, aka a function with a memory.

        This is a low-level representation of a segment within an automation system, or a pu, xu ...

        This defines a new function whose signature is <declaration-specifier>* <declarator> (System_t* sys, DataBlock_t* idb) <compound-statement>
    """

    def create(n1: DataBlockDefinition, n2: list[DeclarationSpecifier], n3: Declarator, n4: CompoundStatement, name: str):
        return FunctionBlockDefinition((n1, n2, n3, n4), name)

    def __init__(self, nodes: Tuple[
        DataBlockDefinition,
        list[DeclarationSpecifier],
        Declarator, 
        CompoundStatement
    ], name: str):
        self.name = name
        self.nodes = [
            nodes[0],
            FunctionDefinition.create(
                nodes[1],
                nodes[2],
                [],
                nodes[3] 
            )
        ]

    def get_name(self):
        return self.name
        

    def __iter__(self):
        return iter(self.nodes)

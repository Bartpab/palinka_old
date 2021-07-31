from typing import Union

from .storage_class_specifier import StorageClassSpecifier
from .type_specifier import TypeSpecifier
from .type_qualifier import TypeQualifier

class DeclarationSpecifier:
    """
        Represents a declaration specifier.


        <declaration-specifier> ::= <storage-class-specifier> | <type-specifier> | <type-qualifier>
    """

    def __init__(self, node: Union[StorageClassSpecifier, TypeSpecifier, TypeQualifier]):
        self.nodes = [node]
    
    @staticmethod
    def create(node: Union[StorageClassSpecifier, TypeSpecifier, TypeQualifier]):
        return DeclarationSpecifier(node)

    def __iter__(self):
        return iter(self.nodes)
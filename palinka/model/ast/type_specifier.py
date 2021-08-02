from __future__ import annotations

from typing import Union

from .identifier import Identifier

import palinka.model.ast.specifier_qualifier as specifier_qualifier
import palinka.model.ast.enum_specifier as enum_specifier 
import palinka.model.ast.struct_or_union_specifier as struct_or_union_specifier
import palinka.model.ast.declaration_specifier as declaration_specifier

class Void:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "void"
    
    def as_type_specifier(self):
        return TypeSpecifier(self)

class Char:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "char"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Short:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "short"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Int:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "int"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Long:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "long"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Float:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "float"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Double:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "double"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Signed:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "signed"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class Unsigned:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)
        
    def __str__(self):
        return "unsigned"
    def as_type_specifier(self):
        return TypeSpecifier(self)
class TypedefName:
    def __init__(self, identifier: Identifier):
        self.nodes = [identifier]
    
    def __iter__(self):
        return iter(self.nodes)
    def as_type_specifier(self):
        return TypeSpecifier(self)
class TypeSpecifier:
    def __init__(self, node: Union[Void, Char, Short, Int, Long, Float, Double, Signed, Unsigned, struct_or_union_specifier.StructOrUnionSpecifier, enum_specifier.EnumSpecifier, TypedefName]):
        self.nodes = [node]
    
    def create(node: Union[Void, Char, Short, Int, Long, Float, Double, Signed, Unsigned, struct_or_union_specifier.StructOrUnionSpecifier, enum_specifier.EnumSpecifier, TypedefName]):
        return TypeSpecifier(node)

    def __iter__(self):
        return iter(self.nodes)
    
    def as_declaration_specifier(self) -> declaration_specifier.DeclarationSpecifier:
        return declaration_specifier.DeclarationSpecifier(self)
    
    def as_specifier_qualifier(self) -> specifier_qualifier.SpecifierQualifier:
        return specifier_qualifier.SpecifierQualifier(self)
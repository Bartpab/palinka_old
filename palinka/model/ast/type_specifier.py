from __future__ import annotations
from typing import Union

from .identifier import Identifier
import palinka.model.ast.enum_specifier as enum_specifier 
import palinka.model.ast.struct_or_union_specifier as struct_or_union_specifier

class Void:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "void"

class Char:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "char"

class Short:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "short"

class Int:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "int"

class Long:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "long"

class Float:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "float"

class Double:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "double"

class Signed:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return "signed"

class Unsigned:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)
        
    def __str__(self):
        return "unsigned"

class TypedefName:
    def __init__(self, identifier: Identifier):
        self.nodes = [identifier]
    
    def __iter__(self):
        return iter(self.nodes)

class TypeSpecifier:
    def __init__(self, node: Union[Void, Char, Short, Int, Long, Float, Double, Signed, Unsigned, struct_or_union_specifier.StructOrUnionSpecifier, enum_specifier.EnumSpecifier, TypedefName]):
        self.nodes = [node]
    
    def create(node: Union[Void, Char, Short, Int, Long, Float, Double, Signed, Unsigned, struct_or_union_specifier.StructOrUnionSpecifier, enum_specifier.EnumSpecifier, TypedefName]):
        return TypeSpecifier(node)

    def __iter__(self):
        return iter(self.nodes)
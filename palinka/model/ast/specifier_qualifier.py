from __future__ import annotations
from typing import Union

import palinka.model.ast.type_specifier as type_specifier
import palinka.model.ast.type_qualifier as type_qualifier

class SpecifierQualifier:

    def __init__(self, node: Union[type_qualifier.TypeQualifier, type_specifier.TypeSpecifier]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
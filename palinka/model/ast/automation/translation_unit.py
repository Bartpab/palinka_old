from __future__ import annotations
from palinka.model.ast.preprocessor import Preprocessor

from .external_declaration import ExternalDeclaration

class TranslationUnit:
    """
        <translation-unit> ::= <external-declaration>*
    """
    def __init__(self, external_declarations: list[ExternalDeclaration], preprocessor: list[Preprocessor] = None):
        preprocessor = preprocessor or []
        self.nodes = preprocessor + external_declarations
    
    def __iter__(self):
        return iter(self.nodes)
    
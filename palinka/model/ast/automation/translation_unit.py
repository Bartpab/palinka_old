from __future__ import annotations

from .external_declaration import ExternalDeclaration

class TranslationUnit:
    """
        <translation-unit> ::= <external-declaration>*
    """
    def __init__(self, external_declarations: list[ExternalDeclaration]):
        self.external_declarations = external_declarations
    
    def __iter__(self):
        return iter(self.external_declarations)
    
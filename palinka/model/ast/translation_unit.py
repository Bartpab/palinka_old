from __future__ import annotations

from .external_declaration import ExternalDeclaration

class TranslationUnit:
    """
        <translation-unit> ::= <external-declaration>*
    """
    def __init__(self, nodes: list[ExternalDeclaration]):
        self.nodes = nodes
    
    def __iter__(self):
        return iter(self.nodes)
    
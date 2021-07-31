from typing import Union, Tuple

from ..identifier import Identifier
from .translation_unit import TranslationUnit

class SystemDeclaration:
    def __init__(self, nodes: Tuple[Identifier, TranslationUnit]):
        self.nodes = list(nodes)
    
    @staticmethod
    def create(n1: Identifier, n2: TranslationUnit):
        return SystemDeclaration((n1, n2))

    def get_name(self):
        return self.nodes[0].name

    def __iter__(self):
        return iter(self.nodes)
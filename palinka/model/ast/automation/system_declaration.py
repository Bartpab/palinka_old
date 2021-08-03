from typing import Union, Tuple

from ..identifier import Identifier
from .translation_unit import TranslationUnit

class SystemDeclaration:
    def __init__(self, id: str, label: str, nodes: Tuple[TranslationUnit, TranslationUnit]):
        self.id = id
        self.label = label
        self.nodes = list(nodes)
    
    @staticmethod
    def create(id: str, label: str, header: TranslationUnit, source: TranslationUnit):
        return SystemDeclaration(id, label, (header, source))

    def get_id(self):
        return self.id
    
    def get_label(self):
        return self.label

    def __iter__(self):
        return iter(self.nodes)
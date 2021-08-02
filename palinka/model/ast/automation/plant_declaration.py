from __future__ import annotations
from typing import Union, Tuple

from ....utils import flatten
from .system_declaration import SystemDeclaration
from ..translation_unit import TranslationUnit

class PlantDeclaration:
    def __init__(self, nodes: list[SystemDeclaration], translation_unit: TranslationUnit):
        self.nodes = nodes + [translation_unit]
        
    def __iter__(self):
        return iter(self.nodes)
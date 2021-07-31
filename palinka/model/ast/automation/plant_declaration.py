from __future__ import annotations
from typing import Union, Tuple

from ....utils import flatten
from .system_declaration import SystemDeclaration

class PlantDeclaration:
    def __init__(self, nodes: list[SystemDeclaration]):
        self.nodes = nodes
        
    def __iter__(self):
        return iter(self.nodes)
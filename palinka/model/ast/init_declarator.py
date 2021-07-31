from __future__ import annotations
from typing import Optional, Tuple, Union

import palinka.model.ast.declarator as declarator
from .initializer import Initializer

class InitDeclarator:
    def __init__(self, nodes: Union[
                Tuple[declarator.Declarator],
                Tuple[declarator.Declarator, Initializer]
            ], discr):
        self.discr = discr
        self.nodes = list(filter(lambda n: n is not None, nodes))
    
    @staticmethod
    def create(n1: declarator.Declarator):
        return InitDeclarator((n1,), 1)

    @staticmethod
    def expr(n1: declarator.Declarator, n2: Initializer):
        return InitDeclarator((n1, n2), 2)

    def is_first_case(self):
        return self.discr == 1
    
    def is_second_case(self):
        return self.discr == 2

    def __iter__(self):
        return iter(self.nodes)
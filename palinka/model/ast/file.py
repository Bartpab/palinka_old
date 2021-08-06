from __future__ import annotations

import pycparser

import palinka.model.ast.include as include

class File:
    def __init__(self, id: str, includes: list[include.Include], translation_unit: pycparser.c_parser.c_ast.FileAST):
        self.id = id
        self.includes = includes or []
        self.translation_unit = translation_unit or pycparser.c_parser.c_ast.FileAST([])
    
    def __iter__(self):
        for incl in self.includes:
            yield incl

        if self.translation_unit:
            yield self.translation_unit
    


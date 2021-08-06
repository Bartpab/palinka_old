from __future__ import annotations

import pycparser

import palinka.model.ast.file as file

class System:
    def __init__(self, files: list[file.File]):
        self.files = files or []
    
    def __iter__(self):
        for file in self.files:
            yield file

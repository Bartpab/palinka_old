from __future__ import annotations
from typing import Union

class Auto:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   


class Register:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class Static:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class Extern:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class Typedef:
    def __init__(self):
        self.nodes = []
        
    def __iter__(self):
        return iter(self.nodes)   

class StorageClassSpecifier:
    def __init__(self, node: Union[Auto, Register, Static, Extern, Typedef]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
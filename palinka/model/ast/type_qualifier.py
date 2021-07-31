from typing import Union

class Const:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return 'const'

class Volatile:
    def __init__(self):
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        return 'volatile'

class TypeQualifier:
    def __init__(self, node: Union[Const, Volatile]):
        self.nodes = [node]
    
    def __iter__(self):
        return iter(self.nodes)
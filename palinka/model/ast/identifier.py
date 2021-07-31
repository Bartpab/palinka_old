class Identifier:
    def __init__(self, name: str):
        self.name = name
        self.nodes = []
    
    def __iter__(self):
        return iter([])
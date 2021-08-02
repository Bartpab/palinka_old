class Identifier:
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise Exception("Identifier must be a string !")

        self.name = name
        self.nodes = []
    
    def __iter__(self):
        return iter([])
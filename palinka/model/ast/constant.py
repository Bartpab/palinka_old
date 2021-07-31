class Constant:
    def __init__(self, value):
        self.value = value
        self.nodes = []
    
    def __iter__(self):
        return iter(self.nodes)
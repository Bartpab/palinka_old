class Include:
    def __init__(self, name: str, is_global: bool = False):
        self.id = name
        self.is_global = is_global
    
    def __iter__(self):
        return iter([])
class String:
    def __init__(self, value: str):
        self.value = value
        self.nodes = []

    def __iter__(self):
        return iter(self.nodes)
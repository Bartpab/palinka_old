
class Plant:
    def __init__(self, files, systems):
        self.files = files or []
        self.systems = systems or []
    
    def __iter__(self):
        for file in self.files:
            yield file
            
        for sys in self.systems:
            yield sys
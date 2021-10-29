class Component:
    def __init__(self):
        self.component = {}
    
    def dump(self):
        return self.component
    
    def add(self, **kwargs):
        self.component.update(kwargs)

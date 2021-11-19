class Components:
    def __init__(self):
        self.components = []

    @staticmethod
    def make(**kwargs):
        return kwargs

    def addActionRow(self, *args):
        data = []
        for temp in args:
            data.append(temp)

        self.components.append(
            self.make(type=1, components=data)
        )

    def get(self):
        return self.components
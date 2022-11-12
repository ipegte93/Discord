class Route:
    def __init__(self, method: str, path: str) -> None:
        self.url = "https://discord.com/api/v9" + path
        self.method = method
class GameScript:
    def __init__(self):
        self.updated = False

    def Setup(self):
        pass

    def Update(self):
        if not self.updated:
            print("Game Object Updating...")
            self.updated = True

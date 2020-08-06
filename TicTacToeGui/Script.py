from ECS.Scriptable import Scriptable
from ECS.Components import TransformComponent


class GameScript(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        self.count = 0

    def Update(self):
        if self.count < 1:
            print("Game Object Updating...")
        self.count += 1

class Scriptable:
    def __init__(self, scene, entity):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = scene.Surface
        self.Entity = entity

    def GetComponent(self, Typename):
        return self.Entity.GetComponent(Typename)

    # Will contains instance of
    # 1. Physics Manager
    # 2. Input Manager
    # which game objects can query during update

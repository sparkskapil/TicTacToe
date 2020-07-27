class Entity:
    def __init__(self, Scene):
        self.Scene = Scene
        self.entity = Scene.GetRegistry().CreateEntity()

    def AddComponent(self, Component):
        return self.Scene.GetRegistry().AttachComponent(self.entity, Component)

    def GetComponent(self, Typename):
        return self.Scene.GetRegistry().GetComponent(self.entity, Typename)

    def RemoveComponent(self, Typename):
        return self.Scene.GetRegistry().RemoveComponent(self.entity, Typename)

    def GetId(self):
        return self.entity
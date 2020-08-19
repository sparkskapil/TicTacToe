class Entity:
    def __init__(self, Scene):
        self.Scene = Scene
        self.entity = Scene.GetRegistry().CreateEntity()

    def AddComponent(self, Component):
        if self.Scene.Reg.HasComponent(self.entity, Component):
            print("{} already present for {} entity".format(
                Component.__class__.__name__, self.entity))
            return self.GetComponent(Component)
        return self.Scene.GetRegistry().AttachComponent(self.entity, Component)

    def GetComponents(self):
        return self.Scene.GetRegistry().GetComponentsGroup(self.entity)

    def GetComponent(self, Typename):
        return self.Scene.GetRegistry().GetComponent(self.entity, Typename)

    def RemoveComponent(self, Typename):
        return self.Scene.GetRegistry().RemoveComponent(self.entity, Typename)

    def GetId(self):
        return self.entity

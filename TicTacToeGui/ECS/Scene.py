from ECS.Registry import Registry


class Scene:
    def __init__(self):
        self.Reg = Registry()

    def GetRegistry(self):
        return self.Reg

    def CreateEntity(self):
        return Entity(self)

    def OnSetup(self):
        pass

    def OnRender(self):
        pass

    def OnUpdate(self):
        pass


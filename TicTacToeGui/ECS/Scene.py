from ECS.Registry import Registry
from ECS.Entity import Entity


class Scene:
    def __init__(self):
        self.Reg = Registry()
        self.Entities = dict()

    def GetRegistry(self):
        return self.Reg

    def CreateEntity(self):
        entity = Entity(self)
        self.Entities[entity.GetId()] = entity
        return entity

    def RemoveEntity(self, entity):
        entId = None
        if isinstance(entity, Entity):
            entId = entity.GetId()
        elif entity.is_integer():
            entId = entity
        entRemoved = self.Entities.pop(entId)
        self.Reg.RemoveEntity(entId)

    def OnSetup(self):
        pass

    def OnRender(self):
        pass

    def OnUpdate(self):
        pass

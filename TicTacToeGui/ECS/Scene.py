from ECS.Registry import Registry
from ECS.Entity import Entity
from ECS.Systems.SpriteRendererSystem import *
from ECS.Systems.InputProcessingSystem import *
from ECS.Systems.ScriptProcessingSystem import *


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

    def OnSetup(self, Surface):
        self.Surface = Surface
        self.Setup()
        self.SpriteRenderer = SpriteRenderSystem(self, self.Surface)
        self.SpriteRenderer.PreLoadSprites()
        self.InputHandler = InputProcessingSystem(self)
        self.ScriptProcessor = ScriptProcessingSystem(self)

    def OnRender(self):
        self.SpriteRenderer.RenderSpriteComponents()

    def OnUpdate(self):
        self.ScriptProcessor.UpdateGameObjects()
        self.Update()

    def OnEvent(self, event):
        self.InputHandler.CheckAndProcessButtonClicks(event)

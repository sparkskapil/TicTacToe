from ECS.Registry import Registry
from ECS.Entity import Entity
from ECS.Systems.SpriteRendererSystem import SpriteRenderSystem
from ECS.Systems.InputProcessingSystem import InputProcessingSystem
from ECS.Systems.ScriptProcessingSystem import ScriptProcessingSystem
from ECS.Systems.LabelRenderingSystem import LabelRenderingSystem


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
        self.Entities.pop(entId)
        self.Reg.RemoveEntity(entId)

    def OnSetup(self, surface):
        self.Surface = surface
        self.Setup()
        self.SpriteRenderer = SpriteRenderSystem(self, self.Surface)
        self.SpriteRenderer.PreLoadSprites()
        self.InputHandler = InputProcessingSystem(self)
        self.ScriptProcessor = ScriptProcessingSystem(self)
        self.LabelRenderer = LabelRenderingSystem(self, self.Surface)
        self.LabelRenderer.PreloadFonts()

    def OnRender(self):
        self.SpriteRenderer.RenderSpriteComponents()
        self.LabelRenderer.RenderLable()

    def OnUpdate(self):
        self.ScriptProcessor.UpdateGameObjects()
        self.Update()

    def OnEvent(self, event):
        self.InputHandler.CheckAndProcessButtonClicks(event)

    def Setup(self):
        '''
        To be overridden by the derrived class
        '''

    def Update(self):
        '''
        To be overridden by the derrived class
        '''

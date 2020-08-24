import pickle
import json

from ECS.Registry import Registry
from ECS.Entity import Entity
from ECS.Systems.SpriteRendererSystem import SpriteRenderSystem
from ECS.Systems.InputProcessingSystem import InputProcessingSystem
from ECS.Systems.ScriptProcessingSystem import ScriptProcessingSystem
from ECS.Systems.LabelRenderingSystem import LabelRenderingSystem

from ECS.Components import TransformComponent, TagComponent


class Scene:
    def __init__(self):
        self.Reg = Registry()
        self.Entities = dict()
        self.SceneChanged = True
        self.SceneLocation = ""

    def GetRegistry(self):
        return self.Reg

    def CreateEntity(self, withDefaults=True):
        entity = Entity(self)
        self.Entities[entity.GetId()] = entity
        if withDefaults:
            entity.AddComponent(TransformComponent())
            entity.AddComponent(TagComponent())
        self.NotifySceneChanged()
        return entity

    def RemoveEntity(self, entity):
        entId = None
        if isinstance(entity, Entity):
            entId = entity.GetId()
        elif entity.is_integer():
            entId = entity
        self.Entities.pop(entId)
        self.Reg.RemoveEntity(entId)
        self.NotifySceneChanged()

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

    def SaveScene(self, filepath, binary=False):
        if not binary:
            # TODO Add mechanism to store scene in ascii
            pass
        state = dict()
        for entId, entity in self.Entities.items():
            if not entId in state:
                state[entId] = list()
            state[entId].extend(entity.GetComponents())

        with open(filepath, 'wb') as file:
            pickle.dump(state, file)

        self.SceneChanged = False
        self.SceneLocation = filepath

    def LoadScene(self, filepath, binary=False):
        if not binary:
            # TODO Add mechanism to read scene in ascii
            pass
        with open(filepath, 'rb') as file:
            scene = pickle.load(file)
            for _, components in scene.items():
                entt = self.CreateEntity()
                for component in components:
                    entt.AddComponent(component)

        self.SceneChanged = False
        self.SceneLocation = filepath

    def NotifySceneChanged(self):
        self.SceneChanged = True

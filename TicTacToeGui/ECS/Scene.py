import os
from copy import deepcopy
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
        self.SceneManager = None
        self.Surface = None

    def GetRegistry(self):
        return self.Reg

    def CreateEntity(self, withDefaults=True):
        entity = Entity(self)
        self.Entities[entity.GetId()] = entity
        if withDefaults:
            entity.AddComponent(TransformComponent())
            entity.AddComponent(TagComponent(f'Entity_{entity.GetId()}'))
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

    def CloneEntity(self, entity):
        if not entity:
            return
        clonedEntity = self.CreateEntity(False)
        for component in entity.GetComponents():
            clonedEntity.AddComponent(deepcopy(component))
        self.NotifySceneChanged()

    def OnSetup(self, surface):
        self.Setup()
        try:
            self.SpriteRenderer = SpriteRenderSystem(self)
            self.SpriteRenderer.PreLoadSprites()
            self.InputHandler = InputProcessingSystem(self)
            self.ScriptProcessor = ScriptProcessingSystem(self)
            self.LabelRenderer = LabelRenderingSystem(self)
            self.LabelRenderer.PreloadFonts()
            self.SetSurface(surface)
        except Exception as e:
            print(e)

    def OnRender(self):
        try:
            self.SpriteRenderer.RenderSpriteComponents()
            self.LabelRenderer.RenderLable()
        except Exception as e:
            print(e)

    def OnUpdate(self):
        try:
            self.ScriptProcessor.UpdateGameObjects()
            self.Update()
        except Exception as e:
            print(e)

    def OnEvent(self, event):
        try:
            self.InputHandler.CheckAndProcessButtonClicks(event)
        except Exception as e:
            print(e)

    def Setup(self):
        '''
        To be overridden by the derrived class
        '''

    def Update(self):
        '''
        To be overridden by the derrived class
        '''

    def SaveScene(self, filepath, binary=False):
        directory = os.path.split(filepath)[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if not filepath.endswith('.pts'):
            filepath = filepath + '.pts'

        if not binary:
            # TODO Add mechanism to store scene in ascii
            pass
        state = dict()
        for entId, entity in self.Entities.items():
            if not entId in state:
                state[entId] = list()
            state[entId].extend(entity.GetComponents())

        with open(filepath+'.tmp', 'wb') as file:
            pickle.dump(state, file)

        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(filepath+'.tmp', filepath)

        self.SceneChanged = False
        self.SceneLocation = filepath

    def LoadScene(self, filepath, binary=False):
        if not binary:
            # TODO Add mechanism to read scene in ascii
            pass
        with open(filepath, 'rb') as file:
            scene = pickle.load(file)
            for _, components in scene.items():
                entt = self.CreateEntity(False)
                for component in components:
                    entt.AddComponent(component)

        self.SceneChanged = False
        self.SceneLocation = filepath

    def NotifySceneChanged(self):
        self.SceneChanged = True

    def SetSurface(self, surface):
        self.Surface = surface
        self.SpriteRenderer.Surface = surface
        self.LabelRenderer.Surface = surface

    def SetSceneManager(self, manager):
        self.SceneManager = manager

    def GetSceneManager(self):
        return self.SceneManager

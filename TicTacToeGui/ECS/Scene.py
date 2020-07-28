from ECS.Registry import Registry
from ECS.Entity import Entity
from ECS.Components import *


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
        self.Setup()
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            sprite.Image = pygame.image.load(sprite.image)

    def OnRender(self, Surface):
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            transform = self.Entities[ent].GetComponent(TransformComponent)
            self.Surface.blit(sprite.Image, (transform.x, transform.y))

    def OnUpdate(self):
        pass

    def OnEvent(self, event):
        pass

from ECS.Registry import Registry
from ECS.Entity import Entity
from ECS.Components import *
import pygame


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
            scaleSprite = False

            imW, imH = sprite.Image.get_size()
            if sprite.width == sprite.height == None and sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
                sprite.mode = SpriteComponent.SpriteMode.Original

            # scale image if width and height not defined.
            if sprite.width == None or sprite.height == None:
                scaleSprite = True
                if sprite.mode == SpriteComponent.SpriteMode.Fit:
                    sprite.width = Surface.get_width()
                    sprite.height = Surface.get_height()
                elif sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
                    if sprite.width == None:
                        sprite.width = imW*sprite.height / imH
                    if sprite.height == None:
                        sprite.height = imH*sprite.width / imW
                elif sprite.mode == SpriteComponent.SpriteMode.Original:
                    sprite.width = imW
                    sprite.height = imH
            if scaleSprite == True:
                sprite.Image = pygame.transform.scale(sprite.Image, (sprite.width, sprite.height))

            transform = self.Entities[ent].GetComponent(TransformComponent)
            Surface.blit(
                sprite.Image, (transform.position.x, transform.position.y))

    def OnUpdate(self):
        self.Update()

    def OnEvent(self, event):
        pass

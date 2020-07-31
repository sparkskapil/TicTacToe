import pygame
from ECS.Components import *


class SpriteRenderSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.Surface = Surface

    def __computeWidthHeight(self, sprite):
        imW, imH = sprite.Image.get_size()
        if sprite.mode == SpriteComponent.SpriteMode.Fit:
            sprite.width = self.Surface.get_width()
            sprite.height = self.Surface.get_height()
        elif sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            if sprite.width == None:
                sprite.width = int(imW*sprite.height / imH)
            elif sprite.height == None:
                sprite.height = int(imH*sprite.width / imW)
        elif sprite.mode == SpriteComponent.SpriteMode.Original:
            sprite.width = imW
            sprite.height = imH

    def __transformSprite(self, sprite):
        if sprite.width == sprite.height == None and sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            sprite.mode = SpriteComponent.SpriteMode.Original

        # scale image if width and height not defined.
        scaleSprite = False
        if sprite.width == None or sprite.height == None:
            scaleSprite = True
            self.__computeWidthHeight(sprite)

        if scaleSprite == True:
            sprite.Image = pygame.transform.scale(
                sprite.Image, (sprite.width, sprite.height))

    def __shouldSpriteRender(self, sprite, transform):
        # if sprite is offscreen it should not be rendered.
        x = sprite.width + transform.position.x
        y = sprite.height + transform.position.y

        isOffscreen = False
        if x < 0 or x > self.Surface.get_width():
            isOffscreen = True
        if y < 0 or y > self.Surface.get_height():
            isOffscreen = True

        return not isOffscreen

    def PreLoadSprites(self):
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            sprite.Image = pygame.image.load(sprite.image)

    def RenderSpriteComponents(self):
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            if sprite.Image == None:
                sprite.Image = pygame.image.load(sprite.image)
            self.__transformSprite(sprite)
            transform = self.Entities[ent].GetComponent(TransformComponent)
            
            if self.__shouldSpriteRender(sprite, transform):
                self.Surface.blit(
                    sprite.Image, (transform.position.x, transform.position.y))

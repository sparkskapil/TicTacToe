import os
import pygame
from ..Components import TransformComponent, SpriteComponent
from .Cache import Cache


class SpriteRenderSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.VFS = scene.GetVFS()
        if not Surface:
            self.Surface = scene.Surface
        self.Cache = Cache()

    def __computeWidthHeight(self, sprite):
        imW, imH = self.Cache[hash(sprite)].get_size()
        if sprite.mode == SpriteComponent.SpriteMode.Fit:
            sprite.width = self.Surface.get_width()
            sprite.height = self.Surface.get_height()
        elif sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            if not sprite.width:
                sprite.width = int(imW*sprite.height / imH)
            elif not sprite.height:
                sprite.height = int(imH*sprite.width / imW)
        elif sprite.mode == SpriteComponent.SpriteMode.Original:
            sprite.width = imW
            sprite.height = imH

    def __transformSprite(self, sprite):
        key = hash(sprite)
        if sprite.width == sprite.height is None and sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            sprite.mode = SpriteComponent.SpriteMode.Original

        # scale image if width and height not defined.
        scaleSprite = False
        if not sprite.width or not sprite.height:
            scaleSprite = True
            self.__computeWidthHeight(sprite)

        imgWidth = self.Cache[key].get_width()
        imgHeight = self.Cache[key].get_height()
        if not sprite.width == imgWidth or not sprite.height == imgHeight:
            scaleSprite = True

        if scaleSprite:
            self.__loadSprite(sprite)
            key = hash(sprite)
            self.Cache[key] = pygame.transform.scale(
                self.Cache[key], (sprite.width, sprite.height))
        return key

    def __shouldSpriteRender(self, sprite, transform):
        # if sprite is offscreen it should not be rendered.
        x = transform.position.x
        y = transform.position.y

        isOffscreen = False
        if x < -self.Surface.get_width() or x > self.Surface.get_width():
            isOffscreen = True
        if y < -self.Surface.get_height() or y > self.Surface.get_height():
            isOffscreen = True

        return not isOffscreen

    def __loadSprite(self, sprite):
        spritePath = os.path.join(self.VFS.Root, sprite.image)
        if not os.path.isfile(spritePath):
            return False
        self.Cache[hash(sprite)] = pygame.image.load(spritePath)
        return True

    def PreLoadSprites(self):
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, _ in sprites:
            self.__loadSprite(sprite)

    def RenderSpriteComponents(self):
        self.Cache.UpdateCounter()
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            if sprite.image == "":
                continue
            key = hash(sprite)
            if not key in self.Cache.keys() and not self.__loadSprite(sprite):
                continue
            
            key = self.__transformSprite(sprite)
            transform = self.Entities[ent].GetComponent(TransformComponent)

            if self.__shouldSpriteRender(sprite, transform):
                self.Surface.blit(
                    self.Cache[key], (transform.position.x, transform.position.y))

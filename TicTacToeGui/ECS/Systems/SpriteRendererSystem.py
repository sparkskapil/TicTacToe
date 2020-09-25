import os
import pygame
from ECS.Components import TransformComponent, SpriteComponent


class SpriteRenderSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.VFS = scene.GetVFS()
        if not Surface:
            self.Surface = scene.Surface
        self.Cache = dict()
        self.CacheHitStack = dict()
        self.CACHE_SIZE = 50
        self.FRAME_COUNT = 0
        

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
        if sprite.width == sprite.height is None and sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            sprite.mode = SpriteComponent.SpriteMode.Original

        # scale image if width and height not defined.
        scaleSprite = False
        if not sprite.width or not sprite.height:
            scaleSprite = True
            self.__computeWidthHeight(sprite)
            
        imgWidth = self.Cache[hash(sprite)].get_width()
        imgHeight = self.Cache[hash(sprite)].get_height()
        if not sprite.width == imgWidth or not sprite.height == imgHeight:
            scaleSprite = True
            
        if scaleSprite:
            self.__loadSprite(sprite)
            self.Cache[hash(sprite)] = pygame.transform.scale(
                self.Cache[hash(sprite)], (sprite.width, sprite.height))

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
    
    def __shrinkCache(self):
        maxVal = max(self.CacheHitStack.values())
        toRemove = list()
        for key, value in self.CacheHitStack.items():
            if maxVal - value < 120:
                toRemove.append(key)
        for key in toRemove:
            self.CacheHitStack.pop(key)
            self.Cache.pop(key)
        
    def RenderSpriteComponents(self):
        self.FRAME_COUNT += 1
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            if sprite.image == "":
                continue
            key = hash(sprite)
            if not key in self.Cache.keys():
                if not self.__loadSprite(sprite):
                    continue
            
            self.CacheHitStack[key] = self.FRAME_COUNT
            
            if len(self.Cache) == self.CACHE_SIZE:
                self.__shrinkCache()
            
            self.__transformSprite(sprite)
            transform = self.Entities[ent].GetComponent(TransformComponent)

            if self.__shouldSpriteRender(sprite, transform):
                self.Surface.blit(
                    self.Cache[hash(sprite)], (transform.position.x, transform.position.y))

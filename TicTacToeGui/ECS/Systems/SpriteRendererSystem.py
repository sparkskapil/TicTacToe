import pygame
from ECS.Components import TransformComponent, SpriteComponent


class SpriteRenderSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.Surface = Surface
        self.Cache = dict()

    def __computeWidthHeight(self, sprite):
        imW, imH = self.Cache[sprite].get_size()
        if sprite.mode == SpriteComponent.SpriteMode.Fit:
            sprite.width = self.Surface.get_width()
            sprite.height = self.Surface.get_height()
        elif sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            if sprite.width is None:
                sprite.width = int(imW*sprite.height / imH)
            elif sprite.height is None:
                sprite.height = int(imH*sprite.width / imW)
        elif sprite.mode == SpriteComponent.SpriteMode.Original:
            sprite.width = imW
            sprite.height = imH

    def __transformSprite(self, sprite):
        if sprite.width == sprite.height is None and sprite.mode == SpriteComponent.SpriteMode.RespectAspect:
            sprite.mode = SpriteComponent.SpriteMode.Original

        # scale image if width and height not defined.
        scaleSprite = False
        if sprite.width is None or sprite.height is None:
            scaleSprite = True
            self.__computeWidthHeight(sprite)
            
        imgWidth = self.Cache[sprite].get_width()
        imgHeight = self.Cache[sprite].get_height()
        if not sprite.width == imgWidth or not sprite.height == imgHeight:
            scaleSprite = True
            
        if scaleSprite:
            self.Cache[sprite] = pygame.image.load(sprite.image)
            self.Cache[sprite] = pygame.transform.scale(
                self.Cache[sprite], (sprite.width, sprite.height))

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

    def PreLoadSprites(self):
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, _ in sprites:
            self.Cache[sprite] = pygame.image.load(sprite.image)

    def RenderSpriteComponents(self):
        sprites = self.Reg.GetComponentsByType(SpriteComponent)
        for sprite, ent in sprites:
            if sprite.image == "":
                continue
            if sprite.image in self.Cache.keys():
                self.Cache[sprite] = pygame.image.load(sprite.image)
            self.__transformSprite(sprite)
            transform = self.Entities[ent].GetComponent(TransformComponent)

            if self.__shouldSpriteRender(sprite, transform):
                self.Surface.blit(
                    self.Cache[sprite], (transform.position.x, transform.position.y))

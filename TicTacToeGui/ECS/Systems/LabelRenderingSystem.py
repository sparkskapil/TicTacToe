import os
import pygame 
from ..Components import LabelComponent, TransformComponent
from .Cache import Cache


class LabelRenderingSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.VFS = scene.GetVFS()
        if not Surface:
            self.Surface = scene.Surface
        self.Cache = Cache()
        self.SurfaceCache = Cache()

    def __preloadFontForLabel(self, label):
        key = hash(label)
        if not label.font or not self.Surface:
            return False
        fontPath = os.path.join(self.VFS.Root, label.font)
        if not os.path.isfile(fontPath):
            return False
        if not key in self.Cache.keys() or not self.Cache[key].get_ascent() == label.size:
            self.Cache[key] = pygame.font.Font(fontPath, label.size)
        return True

    def PreloadFonts(self):
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, _ in labels:
            self.__preloadFontForLabel(label)

    def RenderLable(self):
        self.Cache.UpdateCounter()
        self.SurfaceCache.UpdateCounter()
        
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, entt in labels:
            if label.text == "" or label.font == "":
                continue

            if not self.__preloadFontForLabel(label):
                continue

            pos = self.Entities[entt].GetComponent(TransformComponent).position
            bgColor = label.background
            if not label.background is None and label.background[-1] == 255:
                bgColor = None

            lblHash = hash(label)
            if lblHash not in self.SurfaceCache.keys():
                self.SurfaceCache[lblHash] = self.Cache[lblHash].render(
                    label.text, True, label.color, bgColor)

            text = self.SurfaceCache[lblHash]
            textRect = text.get_rect()
            textRect.topleft = (pos.x, pos.y)
            self.Surface.blit(text, textRect)

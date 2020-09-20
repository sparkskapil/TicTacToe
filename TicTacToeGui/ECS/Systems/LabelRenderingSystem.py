import os
from ECS.Components import LabelComponent, TransformComponent
import pygame


class LabelRenderingSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.VFS = scene.GetVFS()
        if not Surface:
            self.Surface = scene.Surface
        self.Cache = dict()
        self.SurfaceCache = dict()

    def __preloadFontForLabel(self, label):
        if not label.font or not self.Surface:
            return False
        fontPath = os.path.join(self.VFS.Root, label.font)
        if not os.path.isfile(fontPath):
            return False
        if not label in self.Cache.keys() or not self.Cache[label].get_ascent() == label.size:
            self.Cache[label] = pygame.font.Font(fontPath, label.size)
        return True

    def PreloadFonts(self):
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, _ in labels:
            self.__preloadFontForLabel(label)

    def RenderLable(self):
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

            lblHash = hash((label.text, label.color, label.font, label.background))
            if lblHash not in self.SurfaceCache.keys():
                self.SurfaceCache[lblHash] = self.Cache[label].render(
                    label.text, True, label.color, bgColor)

            text = self.SurfaceCache[lblHash]
            textRect = text.get_rect()
            textRect.topleft = (pos.x, pos.y)
            self.Surface.blit(text, textRect)

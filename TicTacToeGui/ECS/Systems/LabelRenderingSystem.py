from ECS.Components import LabelComponent, TransformComponent
import pygame


class LabelRenderingSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        if not Surface:
            self.Surface = scene.Surface
        self.Cache = dict()

    def __preloadFontForLabel(self, label):
        if not label.font or not self.Surface:
            return
        if not label in self.Cache.keys() or not self.Cache[label].get_ascent() == label.size:
            self.Cache[label] = pygame.font.Font(label.font, label.size)

    def PreloadFonts(self):
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, _ in labels:
            self.__preloadFontForLabel(label)

    def RenderLable(self):
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, entt in labels:
            if label.text == "" or label.font == "":
                continue
            
            self.__preloadFontForLabel(label)

            pos = self.Entities[entt].GetComponent(TransformComponent).position
            bgColor = label.background
            if not label.background is None and label.background[-1] == 255:
                bgColor = None

            text = self.Cache[label].render(
                label.text, True, label.color, bgColor)

            textRect = text.get_rect()
            textRect.topleft = (pos.x, pos.y)
            self.Surface.blit(text, textRect)

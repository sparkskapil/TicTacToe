from ECS.Components import LabelComponent, TransformComponent
import pygame


class LabelRenderingSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.Surface = Surface

    def __preloadFontForLabel(self, label):
        label.Font = pygame.font.Font(label.font, label.size)

    def PreloadFonts(self):
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, entt in labels:
            label.Font = pygame.font.Font(label.font, label.size)

    def RenderLable(self):
        labels = self.Reg.GetComponentsByType(LabelComponent)
        for label, entt in labels:
            if not hasattr(label, "Font") or not label.Font.get_ascent() == label.size:
                self.__preloadFontForLabel(label)

            pos = self.Entities[entt].GetComponent(TransformComponent).position
            bgColor = label.background
            if not label.background is None and label.background[-1] == 255:
                bgColor = None

            text = label.Font.render(label.text, True, label.color, bgColor)
            
            textRect = text.get_rect()
            textRect.center = (pos.x, pos.y)
            self.Surface.blit(text, textRect)

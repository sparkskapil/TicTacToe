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
            if not hasattr(label, "Font"):
                self.__preloadFontForLabel(label)
            pos = self.Entities[entt].GetComponent(TransformComponent).position
            text = label.Font.render(
                label.text, True, label.color, label.background)
            textRect = text.get_rect()
            textRect.center = (pos.x, pos.y)
            self.Surface.blit(text, textRect)

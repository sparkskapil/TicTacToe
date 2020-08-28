import pygame
from ECS.Components import ButtonComponent, TransformComponent


class InputProcessingSystem:
    def __init__(self, scene):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.Cache = dict()

    def AddOnClickListener(self, buttonComponent: ButtonComponent, event: callable):
        self.Cache[buttonComponent] = event

    def CheckAndProcessButtonClicks(self, event):
        buttons = self.Reg.GetComponentsByType(ButtonComponent)
        if not event.type == pygame.MOUSEBUTTONDOWN:
            return
        for button, ent in buttons:
            if not button.enabled:
                continue
            if not button in self.Cache.keys():
                continue
            if not callable(self.Cache[button]):
                continue

            transform = self.Entities[ent].GetComponent(TransformComponent)
            btn = pygame.Rect(transform.position.x,
                              transform.position.y, button.width, button.height)
            if event.button == 1 and btn.collidepoint(event.pos):
                self.Cache[button]()

import pygame
from ECS.Components import ButtonComponent, TransformComponent


class InputProcessingSystem:
    def __init__(self, scene):
        self.Reg = scene.Reg
        self.Entities = scene.Entities

    def CheckAndProcessButtonClicks(self, event):
        buttons = self.Reg.GetComponentsByType(ButtonComponent)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if not event.type == pygame.MOUSEBUTTONDOWN:
            return
        for button, ent in buttons:
            if not button.enabled:
                continue
            if not callable(button.action):
                continue

            transform = self.Entities[ent].GetComponent(TransformComponent)
            btn = pygame.Rect(transform.position.x,
                              transform.position.y, button.width, button.height)
            if event.button == 1 and btn.collidepoint(event.pos):
                button.action()

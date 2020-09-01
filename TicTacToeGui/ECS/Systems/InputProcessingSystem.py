import sys
import pygame
from ECS.Components import ButtonComponent, TransformComponent


class InputProcessingSystem:
    def __init__(self, scene):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.Cache = dict()

    def AddOnClickListener(self, buttonComponent: ButtonComponent, event: callable):
        if not buttonComponent in self.Cache.keys():
            self.Cache[buttonComponent] = dict()
        self.Cache[buttonComponent]["click"] = event

    def AddOnHoverListener(self, buttonComponent: ButtonComponent, event: callable):
        if not buttonComponent in self.Cache.keys():
            self.Cache[buttonComponent] = dict()
        self.Cache[buttonComponent]["hover"] = [event, False]

    def CheckAndProcessButtonClicks(self, event):
        buttons = self.Reg.GetComponentsByType(ButtonComponent)

        for button, ent in buttons:
            if not button.enabled:
                continue
            if not button in self.Cache.keys():
                continue
            isClickable = False
            isHoverable = False

            if 'click' in self.Cache[button].keys():
                isClickable = True
            if 'hover' in self.Cache[button].keys():
                isHoverable = True

            if isClickable and not callable(self.Cache[button]['click']):
                print(f"Click Event not callable for button on entity {ent}")
                isClickable = False

            if isHoverable and not callable(self.Cache[button]['hover'][0]):
                print(f"Hover Event not callable for button on entity {ent}")
                isHoverable = False

            transform = self.Entities[ent].GetComponent(TransformComponent)
            btn = pygame.Rect(transform.position.x,
                              transform.position.y, button.width, button.height)

            if isClickable and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and btn.collidepoint(event.pos):
                self.Cache[button]['click']()

            if isHoverable:
                if event.type == pygame.MOUSEMOTION and btn.collidepoint(event.pos):
                    self.Cache[button]['hover'][1] = True

                if event.type == pygame.MOUSEMOTION and not btn.collidepoint(event.pos):
                    self.Cache[button]['hover'][1] = False

                state = self.Cache[button]['hover'][1]
                try:
                    self.Cache[button]['hover'][0](state)
                except Exception as e:
                    print(state)
                    print(self.Cache[button]['hover'])
                    print(sys.exc_info())

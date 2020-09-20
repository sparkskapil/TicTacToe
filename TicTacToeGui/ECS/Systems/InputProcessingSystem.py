import sys
import pygame
from ECS.Components import ButtonComponent, TransformComponent


class InputProcessingSystem:
    def __init__(self, scene):
        self.Reg = scene.Reg
        self.Entities = scene.Entities
        self.Cache = dict()
        self.Click = lambda: None
        self.Hover = lambda x: None

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

            if not hasattr(event, "pos") or not button.enabled or not button in self.Cache.keys():
                continue


            if 'click' not in self.Cache[button].keys():
                self.Cache[button]['click'] = self.Click
            if 'hover' not in self.Cache[button].keys():
                self.Cache[button]['hover'] = [self.Hover, False]

            if not callable(self.Cache[button]['click']):
                print(f"Click Event not callable for button on entity {ent}")
                self.Cache[button]['click'] = self.Click

            if not callable(self.Cache[button]['hover'][0]):
                print(f"Hover Event not callable for button on entity {ent}")
                self.Cache[button]['hover'] = [self.Hover, False]

            transform = self.Entities[ent].GetComponent(TransformComponent)
            btn = pygame.Rect(transform.position.x,
                              transform.position.y, button.width, button.height)

            collidePoint = btn.collidepoint(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and collidePoint:
                self.Cache[button]['click']()

            if event.type == pygame.MOUSEMOTION and collidePoint:
                self.Cache[button]['hover'][1] = True

            if event.type == pygame.MOUSEMOTION and not collidePoint:
                self.Cache[button]['hover'][1] = False

            state = self.Cache[button]['hover'][1]
            self.Cache[button]['hover'][0](state)

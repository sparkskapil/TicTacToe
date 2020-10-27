"""
This is a module containing BoundsComputingSystem.
"""
import pygame
from ..Components import TransformComponent


class BoundsComputingSystem:
    """
    This class is a custom system for editor. 
    This will calculate bounding box for entity by iterating over components.
    Then it will draw a rectangle around the bounding box.
    """

    def __init__(self, scene, surface):
        self.Reg = scene.Reg
        self.Surface = surface

    def DrawRectForEntity(self, entity):
        components = entity.GetComponents()
        width = 10
        height = 10
        for component in components:
            if hasattr(component, "width"):
                width = max(component.width, width)
            if hasattr(component, "height"):
                height = max(component.height, height)

        transform = entity.GetComponent(TransformComponent)
        if not transform:
            transform = TransformComponent()
        color = (102, 178, 255)
        pygame.draw.rect(self.Surface, color, (transform.position.x,
                                               transform.position.y, width, height), 3)
        

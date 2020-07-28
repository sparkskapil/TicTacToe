from SceneManager import SceneManager
from ECS.Scene import Scene
from ECS.Entity import Entity
from ECS.Components import *
import pygame


class Application:
    def __init__(self, Width, Height, Title, Icon=None):
        self.Width = Width
        self.Height = Height
        self.Title = Title
        pygame.init()
        self.screen = pygame.display.set_mode([self.Width, self.Height])
        SceneManager.Surface = self.screen
        pygame.display.set_caption(self.Title)
        if not Icon == None:
            gameIcon = pygame.image.load(Icon)
            pygame.display.set_icon(gameIcon)

        self.clock = pygame.time.Clock()
        self.Running = True

    def OnEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.KEYDOWN and pygame.K_ESCAPE == event.key:
                self.Running = False

            SceneManager.Event(event)

    def Run(self):

        while self.Running:
            # Handle events
            self.OnEvent()

            # Update Layers
            SceneManager.Update()

            # Draw Layers
            self.screen.fill((0, 0, 0))
            SceneManager.Render()

            pygame.display.flip()
        pygame.quit()



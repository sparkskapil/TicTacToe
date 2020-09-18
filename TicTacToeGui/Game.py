"""
This module is a template which will be used to run the actual game.
This module will be the runtime for game which will load a project.
"""
import pygame
from Project import Project


class GameLoader:
    """
    This class will load the project and launch the game.
    """

    def __init__(self, projectFile):
        self.Project = Project(projectFile)
        pygame.init()
        surface = pygame.display.set_mode([500, 500])
        self.Project.SceneManager.SetSurface(surface)
        self.Project.LoadProject()
        pygame.display.set_caption(self.Project.ProjectName)
        self.Clock = pygame.time.Clock()
        self.Running = True

    def OnEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.KEYDOWN and pygame.K_ESCAPE == event.key:
                self.Running = False
            self.Project.SceneManager.Event(event)

    def OnRender(self):
        if self.Project.SceneManager.HasScene():
            self.Project.SceneManager.Update()
            self.Project.SceneManager.Render()

    def Run(self):
        while self.Running:
            _ = self.Clock.tick(60)
            surface = self.Project.GetSurface()
            if surface:
                surface.fill((51, 51, 51))
            self.OnRender()
            self.OnEvent()
            pygame.display.flip()
        pygame.quit()


def main():
    game = GameLoader("..\\PrototypeExample\\PrototypeExample.ptproj")
    game.Run()


if __name__ == "__main__":
    main()

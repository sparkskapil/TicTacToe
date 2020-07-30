from SceneManager import SceneManager
from ECS.Scene import Scene
from ECS.Components import *

from Application import Application


class TicTacToeGame(Scene):
    def __init__(self):
        Scene.__init__(self)

    def Setup(self):
        background = self.CreateEntity()
        background.AddComponent(TransformComponent())
        sprite = SpriteComponent("background.jpg")
        sprite.mode = SpriteComponent.SpriteMode.Fit
        background.AddComponent(sprite)

        grid = self.CreateEntity()
        grid.AddComponent(TransformComponent((40, 40, 0)))
        gridSprite = SpriteComponent("board.png")
        gridSprite.width = 400
        gridSprite.mode = SpriteComponent.SpriteMode.RespectAspect
        grid.AddComponent(gridSprite)

    def Update(self):
        pass


SceneManager.AddScene("MainScene", TicTacToeGame())
app = Application(500, 500, "Test Scene")
app.Run()

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

        XSprite = SpriteComponent("T3X_BLACK.png")
        XSprite.width = 100
        XSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        OSprite = SpriteComponent("T3O_BLACK.png")
        OSprite.width = 100
        OSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        box1 = self.CreateEntity()
        box1.AddComponent(TransformComponent((70, 70, 0)))
        box1.AddComponent(XSprite)

        box2 = self.CreateEntity()
        box2.AddComponent(TransformComponent((190, 70, 0)))
        box2.AddComponent(OSprite)

    def Update(self):
        pass


app = Application(500, 500, "Test Scene")
app.GetSceneManager().AddScene("MainScene", TicTacToeGame())
app.Run()

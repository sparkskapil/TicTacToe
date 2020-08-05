from ECS.Scene import Scene
from ECS.Components import TransformComponent, SpriteComponent
from ECS.Components import ButtonComponent, LabelComponent, ScriptComponent

from Application import Application


class TicTacToeGame(Scene):
    '''
    Tic Tac Toe Game Main Scene
    '''

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

        xSprite = SpriteComponent("T3X_BLACK.png")
        xSprite.width = 100
        xSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        oSprite = SpriteComponent("T3O_BLACK.png")
        oSprite.width = 100
        oSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        box1 = self.CreateEntity()
        box1.AddComponent(TransformComponent((70, 70, 0)))
        box1.AddComponent(ButtonComponent(
            100, 100, lambda: print('Button Clicked')))

        box2 = self.CreateEntity()
        box2.AddComponent(TransformComponent((190, 70, 0)))
        box2.AddComponent(oSprite)

        grid.AddComponent(ScriptComponent("Script", "GameScript"))
        grid.AddComponent(LabelComponent(
            "TicTacToe", 'freesansbold.ttf', 32, (0, 0, 0)))

    def Update(self):
        pass


if __name__ == "__main__":
    app = Application(500, 500, "Test Scene")
    app.GetSceneManager().AddScene("MainScene", TicTacToeGame())
    app.Run()

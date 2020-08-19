from ECS.Scene import Scene
from ECS.Components import TransformComponent, SpriteComponent, TagComponent
from ECS.Components import ButtonComponent, LabelComponent, ScriptComponent
from ECS.Components import Vector

from Application import Application


class TicTacToeGame(Scene):
    '''
    Tic Tac Toe Game Main Scene
    '''

    def __init__(self):
        Scene.__init__(self)

    def Setup(self):
        background = self.CreateEntity(False)
        background.AddComponent(TransformComponent())
        background.AddComponent(TagComponent("Background"))
        sprite = SpriteComponent("background.jpg")
        sprite.mode = SpriteComponent.SpriteMode.Fit
        background.AddComponent(sprite)

        grid = self.CreateEntity(False)
        grid.AddComponent(TransformComponent((40, 40, 0)))
        grid.AddComponent(TagComponent("Grid"))
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
        transform = box1.GetComponent(TransformComponent)
        transform.position = Vector(70, 70, 0)
        c1tag = box1.GetComponent(TagComponent)
        c1tag.name = "Cell1"
        box1.AddComponent(ButtonComponent(100, 100))

        box2 = self.CreateEntity()
        transform = box2.GetComponent(TransformComponent)
        transform.position = Vector(190, 70, 0)
        c2tag = box2.GetComponent(TagComponent)
        c2tag.name = "Cell2"
        box2.AddComponent(oSprite)

        #grid.AddComponent(ScriptComponent("Script", "GameScript"))
        grid.AddComponent(ScriptComponent("Script.py", "GameScript"))
        grid.AddComponent(LabelComponent(
            "TicTacToe", 'freesansbold.ttf', 32, (0, 0, 0)))

    def Update(self):
        pass


if __name__ == "__main__":
    app = Application(500, 500, "Test Scene")
    app.GetSceneManager().AddScene("MainScene", TicTacToeGame())
    app.Run()

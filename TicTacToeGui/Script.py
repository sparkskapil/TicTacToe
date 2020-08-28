from ECS.Scriptable import Scriptable, Event
from ECS.Components import ButtonComponent, TagComponent, SpriteComponent


class GameScript(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        self.xSprite = SpriteComponent("T3X_BLACK.png")
        self.xSprite.width = 100
        self.xSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        self.oSprite = SpriteComponent("T3O_BLACK.png")
        self.oSprite.width = 100
        self.oSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        self.turn = 0

        buttonComponents = self.GetSceneComponentsByType(ButtonComponent)
        for component, entt in buttonComponents:
            entity = self.GetEntity(entt)
            self.AddOnClickListener(
                component, Event(self.onButtonClick, entity))

    def Update(self):
        pass

    def onButtonClick(self, entity):
        if self.turn == 0:
            entity.AddComponent(self.xSprite)
        else:
            entity.AddComponent(self.oSprite)
        entity.GetComponent(ButtonComponent).enabled = False
        self.turn += 1
        self.turn %= 2

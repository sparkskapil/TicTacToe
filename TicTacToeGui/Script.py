from ECS.Scriptable import Scriptable
from ECS.Components import TransformComponent, ButtonComponent


class GameScript(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        self.count = 0
        buttonComponents = self.scene.Reg.GetComponentsByType(ButtonComponent)
        for component, entt in buttonComponents:
            component.action = lambda: self.onButtonClick(entt)

    def Update(self):
        if self.count < 1:
            print("Game Object Updating...")
        self.count += 1

    def onButtonClick(self, entity):
        print("ButtonClicked Entity {}".format(entity))

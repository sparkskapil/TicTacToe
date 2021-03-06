from ECS.Scriptable import Scriptable, Event, StateEvent
from ECS.Components import ButtonComponent, TagComponent, SpriteComponent, LabelComponent
import Global


class MenuButton(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        button = self.Entity.GetComponent(ButtonComponent)
        if button:
            self.AddOnClickListener(button, Event(self.onButtonClick, button))
            self.AddOnHoverListener(button, StateEvent(
                self.onButtonHover, self.Entity))

    def Update(self, timestep):
        pass

    def onButtonClick(self, button):
        Global.Mode = self.Entity.GetComponent(TagComponent).name
        if Global.Mode == "Mode_Network":
            self.GetSceneManager().SetScene("NetworkSetup")
        else:
            self.GetSceneManager().SetScene("MainScene")

    def onButtonHover(self, hovered, entity):
        label = entity.GetComponent(LabelComponent)
        if hovered:
            label.color = (37, 122, 253)
        else:
            label.color = (0, 0, 0)

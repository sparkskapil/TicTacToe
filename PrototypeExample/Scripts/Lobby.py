from ECS.Scriptable import Scriptable, Event, StateEvent
from ECS.Components import ButtonComponent, TagComponent, SpriteComponent, LabelComponent
import Global


class NetworkMode(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        pass

    def Update(self, timestep):
        pass

    def onButtonClick(self, button):
        Global.IsHost = self.Entity.GetComponent(
            TagComponent).name == "BtnHost"
        self.GetSceneManager().SetScene("Lobby")

    def onButtonHover(self, hovered, entity):
        label = entity.GetComponent(LabelComponent)
        if hovered:
            label.color = (37, 122, 253)
        else:
            label.color = (0, 0, 0)

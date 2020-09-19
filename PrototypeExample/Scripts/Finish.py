from ECS.Scriptable import Scriptable, Event, StateEvent
from ECS.Components import Vector
from ECS.Components import LabelComponent, TransformComponent, ButtonComponent
import Global


class Finish(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        if Global.Winner == None:
            winnerLabel = self.GetEntitiesByTag('WinnerLabel')[0]
            label = winnerLabel.GetComponent(LabelComponent)
            label.text = ' GAME '

            winner = self.GetEntitiesByTag('Winner')[0]
            label = winner.GetComponent(LabelComponent)
            label.text = 'TIED'
            winner.GetComponent(TransformComponent).position.x = 100
        else:
            winnerLabel = self.GetEntitiesByTag('WinnerLabel')[0]
            label = winnerLabel.GetComponent(LabelComponent)
            label.text = 'Winner'
            
            winner = self.GetEntitiesByTag('Winner')[0]
            label = winner.GetComponent(LabelComponent)
            label.text = Global.Winner
            winner.GetComponent(TransformComponent).position = Vector(200, 250)

        button, _ = self.GetSceneComponentsByType(ButtonComponent)[0]

        self.AddOnClickListener(button, Event(self.onMainMenuClick))

    def Update(self, timestep):
        pass

    def onMainMenuClick(self):
        self.GetSceneManager().SetScene('Menu')

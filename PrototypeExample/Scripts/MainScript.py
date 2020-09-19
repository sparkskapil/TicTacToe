from ECS.Scriptable import Scriptable, Event
from ECS.Components import ButtonComponent, TagComponent, SpriteComponent
from ECS.Components import LabelComponent

from TicTacToe import Game, GameModes
import Global


class GameScript(Scriptable):
    def __init__(self, scene, entity):
        Scriptable.__init__(self, scene, entity)

    def Setup(self):
        self.Game = None
        self.SceneChangeTime = 50

        if Global.Mode == 'Mode_AI':
            self.Game = Game(GameModes.Computer)
        else:
            self.Game = Game(GameModes.PvP)

        self.xSprite = SpriteComponent("Sprites/T3X_BLACK.png")
        self.xSprite.width = 100
        self.xSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        self.oSprite = SpriteComponent("Sprites/T3O_BLACK.png")
        self.oSprite.width = 100
        self.oSprite.mode = SpriteComponent.SpriteMode.RespectAspect

        buttonComponents = self.GetSceneComponentsByType(ButtonComponent)
        for component, entt in buttonComponents:
            entity = self.GetEntity(entt)
            self.AddOnClickListener(
                component, Event(self.onButtonClick, entity))

    def Update(self, timestep):
        grid = self.Game.GetGrid()
        for rowIndex, row in enumerate(grid):
            for colIndex, item in enumerate(row):
                index = rowIndex * 3 + colIndex
                cell = f'Cell{index+1}'
                entt = self.GetEntitiesByTag(cell)[0]
                button = entt.GetComponent(ButtonComponent)
                if not item == 'X' and not item == 'O':
                    if entt.HasComponent(SpriteComponent):
                        entt.RemoveComponent(SpriteComponent)
                    button.enabled = True
                    
                if not button.enabled:
                    continue
                if item == 'X':
                    entt.AddComponent(self.xSprite)
                    button.enabled = False
                elif item == 'O':
                    entt.AddComponent(self.oSprite)
                    button.enabled = False
                

        if self.Game.IsFinished():
            if not self.Game.IsTied():
                Global.Winner = self.Game.Winner.symbol
            else:
                Global.Winner = None
            if self.SceneChangeTime <= 0:
                self.GetSceneManager().SetScene("Results")
                
            self.SceneChangeTime -= 1

    def onButtonClick(self, entity):
        if self.Game.IsBusy():
            return
        cell = int(entity.GetComponent(TagComponent).name[-1])
        self.Game.TakeTurn(cell)

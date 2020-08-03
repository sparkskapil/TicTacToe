from ECS.Components import ScriptComponent


class ScriptProcessingSystem:
    def __init__(self, scene, Surface=None):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = Surface
        self.Entities = scene.Entities

    def __initializeScriptInstance(self, script, entity):
        if script.ScriptInstance == None:
            script.ScriptInstance = script.ScriptClass(self.scene, entity)
            script.ScriptInstance.Setup()

    def UpdateGameObjects(self):
        scripts = self.Reg.GetComponentsByType(ScriptComponent)
        for script, ent in scripts:
            self.__initializeScriptInstance(script, self.Entities[ent])
            script.ScriptInstance.Update()

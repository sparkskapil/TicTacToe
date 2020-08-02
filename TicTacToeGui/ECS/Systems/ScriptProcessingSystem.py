from ECS.Components import ScriptComponent


class ScriptProcessingSystem:
    def __init__(self, scene, Surface=None):
        self.Reg = scene.Reg
        self.Surface = Surface

    def UpdateGameObjects(self):
        scripts = self.Reg.GetComponentsByType(ScriptComponent)
        for script, ent in scripts:
            script.ScriptInstance.Update()

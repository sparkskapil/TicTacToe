from ECS.Components import ScriptComponent


class ScriptProcessingSystem:
    def __init__(self, scene, Surface=None):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = Surface
        self.Entities = scene.Entities
        self.Cache = dict() # Cache for all script instances

    def __initializeScriptInstance(self, script, entity):
        if not script in self.Cache.keys() :
            module = __import__(script.Module)
            scriptClass = getattr(module, script.Class)
            instance = scriptClass(self.scene, entity)
            instance.Setup()
            self.Cache[script] = instance

    def UpdateGameObjects(self):
        scripts = self.Reg.GetComponentsByType(ScriptComponent)
        for script, ent in scripts:
            self.__initializeScriptInstance(script, self.Entities[ent])
            self.Cache[script].Update()

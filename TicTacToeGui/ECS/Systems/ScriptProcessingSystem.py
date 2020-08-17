import os
from ECS.Components import ScriptComponent


class ScriptProcessingSystem:
    def __init__(self, scene, Surface=None):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = Surface
        self.Entities = scene.Entities
        self.Cache = dict()  # Cache for all script instances

    def importModule(self, modulePath):
        try:
            moduleDir, moduleFile = os.path.split(modulePath)
            moduleName, _ = os.path.splitext(moduleFile)
            pwd = os.getcwd()

            if moduleDir == "":
                moduleDir = pwd
            else:
                os.chdir(moduleDir)

            module = __import__(moduleName)
            module.__file__ = modulePath
            globals()[moduleName] = module
            os.chdir(pwd)
            return module
        except:
            raise ImportError

    def __initializeScriptInstance(self, script, entity):
        if script.Module == "" or script.Class == "":
            return
        
        if not script in self.Cache.keys():
            module = self.importModule(script.Module)
            scriptClass = getattr(module, script.Class)
            instance = scriptClass(self.scene, entity)
            instance.Setup()
            self.Cache[script] = instance

    def UpdateGameObjects(self):
        scripts = self.Reg.GetComponentsByType(ScriptComponent)
        for script, ent in scripts:
            self.__initializeScriptInstance(script, self.Entities[ent])
            self.Cache[script].Update()

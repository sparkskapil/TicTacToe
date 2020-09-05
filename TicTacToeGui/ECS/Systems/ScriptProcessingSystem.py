import os
import sys
from ECS.Components import ScriptComponent


class ScriptProcessingSystem:
    def __init__(self, scene, Surface=None):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = Surface
        self.Entities = scene.Entities
        self.Cache = dict()  # Cache for all script instances
        self.LoadedModules = list()

    def importModule(self, modulePath):
        try:
            
            moduleDir, moduleFile = os.path.split(modulePath)
            moduleName, _ = os.path.splitext(moduleFile)
            
            pwd = os.getcwd()

            if moduleDir == "":
                moduleDir = pwd
            else:
                os.chdir(moduleDir)
            sys.path.append(moduleDir)
            module = __import__(moduleName)
            module.__file__ = modulePath
            globals()[moduleName] = module
            
            self.LoadedModules.append((moduleDir, moduleName))
            os.chdir(pwd)
            return module
        except:
            raise ImportError

    def __initializeScriptInstance(self, script, entity):
        if script.Module == "" or script.Class == "":
            return

        if not script in self.Cache.keys():
            module = self.importModule(script.Module)
            if not module:
                return None
            scriptClass = getattr(module, script.Class)
            instance = scriptClass(self.scene, entity)
            instance.SceneManager = self.scene.GetSceneManager()
            instance.Setup()
            self.Cache[script] = instance

    def UpdateGameObjects(self):
        scripts = self.Reg.GetComponentsByType(ScriptComponent).copy()
        for script, ent in scripts:
            if script.Module == "" or script.Class == "":
                continue
            self.__initializeScriptInstance(script, self.Entities[ent])
            self.Cache[script].Update()
            
    def __del__(self): 
        self.Cache.clear()
        for mdir, mname in self.LoadedModules:
            sys.path.remove(mdir)
            if mname in globals().keys():
                globals().pop(mname)

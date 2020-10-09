import os
import sys
import importlib
from ECS.Components import ScriptComponent
from ECS.Systems.Cache import Cache


class ScriptProcessingSystem:
    def __init__(self, scene, Surface=None):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = Surface
        self.VFS = scene.GetVFS()
        self.Entities = scene.Entities
        self.Cache = Cache()  # Cache for all script instances
        self.LoadedModules = list()

    def __getModuleDir(self, module):
        modulePath = os.path.join(self.VFS.Root, module)
        return os.path.dirname(modulePath)

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
            importlib.reload(module)
            module.__file__ = modulePath
            globals()[moduleName] = module

            self.LoadedModules.append((moduleDir, moduleName))
            os.chdir(pwd)
            return module
        except:
            raise ImportError

    def __computeHash(self, filepath):
        reader = open(filepath, "rb")
        content = reader.read()
        reader.close()
        return hash(content)

    def __getModulePath(self, script):
        modulePath = script.Module
        if not os.path.isfile(modulePath):
            modulePath = os.path.join(self.VFS.Root, modulePath)
        return modulePath

    def __getHashKey(self, script, entity):
        modulePath = self.__getModulePath(script)
        filehash = self.__computeHash(modulePath)
        return hash((script, entity.GetId(), filehash))

    def __initializeScriptInstance(self, script, entity):
        self.Cache.UpdateCounter()
        if script.Module == "" or script.Class == "":
            return
        modulePath = self.__getModulePath(script)
        key = self.__getHashKey(script, entity)
        if not key in self.Cache.keys():
            module = self.importModule(modulePath)
            if not module:
                return None
            scriptClass = getattr(module, script.Class)
            instance = scriptClass(self.scene, entity)
            instance.SceneManager = self.scene.GetSceneManager()

            pwd = os.getcwd()
            os.chdir(self.__getModuleDir(script.Module))
            instance.Setup()
            os.chdir(pwd)

            self.Cache[key] = instance

        return True

    def UpdateGameObjects(self, timestep):
        scripts = self.Reg.GetComponentsByType(ScriptComponent).copy()
        for script, ent in scripts:
            if script.Module == "" or script.Class == "":
                continue
            if self.__initializeScriptInstance(script, self.Entities[ent]):
                pwd = os.getcwd()
                os.chdir(self.__getModuleDir(script.Module))

                key = self.__getHashKey(script, self.Entities[ent])

                self.Cache[key].Update(timestep)
                os.chdir(pwd)

    def __removeModule(self, mdir, mname):
        if sys.path and mdir in sys.path:
            sys.path.remove(mdir)
        if mname in globals().keys():
            del globals()[mname]

    def __del__(self):
        self.Cache.clear()
        for mdir, mname in self.LoadedModules:
            self.__removeModule(mdir, mname)

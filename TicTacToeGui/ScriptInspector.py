from hashlib import md5
import os
import sys
import inspect
from types import FunctionType


class ModuleInfo:
    def __init__(self, path):
        self.Path = path
        self.MD5 = ModuleInfo.ComputeHash(path)
        self.Name, self.Location = ModuleInfo.GetModuleNameAndLocation(path)
        self.Classes = list()
        self.ClassTypes = dict()
        self.GetScriptableClassesInModule()

    @staticmethod
    def ComputeHash(filepath):
        reader = open(filepath, "rb")
        content = reader.read()
        reader.close()
        md5Hash = md5(content).digest()
        return md5Hash

    @staticmethod
    def ImportModule(modulepath, modulename):
        # clear old existing import for the module
        if modulename in sys.modules.keys():
            sys.modules.pop(modulename)
        if modulename in globals().keys():
            globals().pop(modulename)

        try:
            pwd = os.getcwd()

            if modulepath == "":
                modulepath = pwd
            else:
                os.chdir(modulepath)
            sys.path.append(modulepath)
            module = __import__(modulename)
            module.__file__ = modulepath
            globals()[modulename] = module
            os.chdir(pwd)
            return module
        except:
            raise ImportError("Oops!", sys.exc_info()[0], "occurred.")

    def GetScriptableClassesInModule(self):
        md5Hash = ModuleInfo.ComputeHash(self.Path)
        if self.MD5 == md5Hash and self.Classes:
            return self.Classes
        self.MD5 = md5Hash

        self.Classes.clear()
        self.ClassTypes.clear()
        try:
            ModuleInfo.ImportModule(self.Location, self.Name)
        except ImportError:
            return self.Classes
        
        Classes = inspect.getmembers(sys.modules[self.Name], inspect.isclass)
        for classMember in Classes:
            className = classMember[0]
            classModule = classMember[1].__module__
            baseClasses = classMember[1].__bases__
            if not classModule == self.Name:
                continue
            isScriptable = False
            for base in baseClasses:
                if base.__name__ == "Scriptable":
                    isScriptable = True
                    break
            if isScriptable:
                self.Classes.append(className)
                self.ClassTypes[className] = classMember[1]

        return self.Classes

    def GetMethodsInClass(self, className):
        return [x for x, y in self.ClassTypes[className].__dict__.items() if type(y) == FunctionType]

    @staticmethod
    def GetModuleNameAndLocation(path):
        mPath, mFile = os.path.split(path)
        mName = os.path.splitext(mFile)[0]
        if mPath == "":
            mPath = os.getcwd()

        return mName, mPath


if __name__ == "__main__":
    info = ModuleInfo(
        "C:\\Users\\Kapil\\Documents\\PrototypeExample\\Scripts\\MainScript.py")
    print(info.GetScriptableClassesInModule())
    methods = info.GetMethodsInClass("GameScript")
    print(methods)

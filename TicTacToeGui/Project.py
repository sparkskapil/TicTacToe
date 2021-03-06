"""
This module contains the project class
"""
import os
import json
from SceneManager import SceneManager
from ECS.Scene import Scene
from VirtualFileSystem import VirtualFileSystem

EXTENSION = ".ptproj"


class Project:
    """
    Project class contains SceneManager, Scenes and all related assets for a game project. 
    """
    @staticmethod
    def CreateNewProject(path, name):
        # Create Project Folder
        projectFolder = os.path.join(path, name).replace('/', '\\')
        if not os.path.exists(projectFolder):
            os.mkdir(projectFolder)

        projectFile = os.path.join(projectFolder, (name + EXTENSION))
        if os.path.exists(projectFile):
            raise Exception("The path already contains a project")

        # Create Index file with the project Name
        with open(projectFile, 'w') as writer:
            json.dump(dict(), writer)

        return projectFile

    def __init__(self, path):
        self.ProjectFile = None
        self.ProjectDir = None

        # PROJECT SETTINGS ATTRIBUTES
        self.ProjectName = None
        self.Width = 500
        self.Height = 500
        self.LimitFPS = 60

        self.VFS = None
        self.Setup(path)

    def Setup(self, path):
        self.SceneManager = SceneManager()
        if path is None:
            return None
        if os.path.isfile(path):
            self.ProjectFile = path
            path = os.path.split(path)[0]
        self.ProjectName = os.path.split(path)[1]
        self.ProjectDir = os.path.abspath(path)
        if self.ProjectFile is None:
            self.ProjectFile = os.path.join(
                self.ProjectDir, (self.ProjectName + EXTENSION))
        self.VFS = VirtualFileSystem(self.ProjectDir)
        self.SceneManager.SetVFS(self.VFS)

    def CreateNewScene(self, sceneName, location=None):
        scene = Scene()
        if location:
            scene.SaveScene(location)
        self.SceneManager.AddScene(sceneName, scene)
        self.SceneManager.SetScene(sceneName)
        self.SaveProject()

    def SaveProject(self):
        index = dict()
        for sceneName, scene in self.SceneManager.Scenes.items():
            sceneRelativePath = scene.SceneLocation.replace(
                self.ProjectDir, '').strip('\\').strip('/')
            index[sceneName] = sceneRelativePath

        index["__current__"] = self.SceneManager.CurrentSceneName
        index["__settings__"] = dict()
        index["__settings__"]["WindowWidth"] = self.Width
        index["__settings__"]["WindowHeight"] = self.Height
        index["__settings__"]["ProjectName"] = self.ProjectName
        index["__settings__"]["LimitFPS"] = self.LimitFPS

        with open(self.ProjectFile, 'w') as writer:
            json.dump(index, writer)

    def LoadProject(self):
        if self.ProjectFile is None:
            return None
        index = None

        with open(self.ProjectFile, 'r') as reader:
            index = json.load(reader)
        self.ProjectDir = os.path.split(self.ProjectFile)[0]
        self.ProjectDir = os.path.abspath(self.ProjectDir)
        self.VFS = VirtualFileSystem(self.ProjectDir)
        self.SceneManager.SetVFS(self.VFS)

        if not index or len(index) == 0:
            return

        for key, relPath in index.items():
            if key == "__current__":
                self.SceneManager.SetScene(relPath)
                continue
            if key == "__settings__":
                self.ProjectName = index["__settings__"]["ProjectName"]
                self.Width = index["__settings__"]["WindowWidth"]
                self.Height = index["__settings__"]["WindowHeight"]
                self.LimitFPS = index["__settings__"]["LimitFPS"]
                continue
            scene = Scene()
            scene.LoadScene(os.path.join(self.ProjectDir, relPath))
            self.SceneManager.AddScene(key, scene)

    def GetSurface(self):
        if self.SceneManager:
            return self.SceneManager.Surface
        return None

    def GetVFS(self):
        return self.VFS

    def GetCurrentScene(self):
        return self.SceneManager.CurrentScene

    def ResetScenes(self):
        for sceneName, scene in self.SceneManager.Scenes.items():
            newScene = Scene()
            newScene.LoadScene(scene.SceneLocation)
            self.SceneManager.AddScene(sceneName, newScene)
        self.SceneManager.SetScene(self.SceneManager.CurrentSceneName)


if __name__ == "__main__":
    PROJECT_PATH = "C:\\Users\\Kapil\\Documents"
    #Project.CreateNewProject(PROJECT_PATH, "PrototypeExample")
    project = Project(os.path.join(PROJECT_PATH, "PrototypeExample"))
    # project.SaveProject()

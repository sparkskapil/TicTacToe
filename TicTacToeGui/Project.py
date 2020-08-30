"""
This module contains the project class
"""
import os
from SceneManager import SceneManager
from ECS.Scene import Scene
import json

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
        if not os.path.exists(projectFile):
            raise Exception("The path already contains a project")

        # Create Index file with the project Name
        with open(projectFile, 'w') as writer:
            json.dump(dict(), writer)

    def __init__(self, path):
        self.ProjectFile = None
        self.Setup(path)

    def Setup(self, path):
        if os.path.isfile(path):
            self.ProjectFile = path
            path = os.path.split(path)[0]
        self.ProjectName = os.path.split(path)[1]
        self.ProjectDir = path
        if self.ProjectFile is None:
            self.ProjectFile = os.path.join(
                self.ProjectDir, (self.ProjectName + EXTENSION))
        self.SceneManager = SceneManager()

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

        with open(self.ProjectFile, 'w') as writer:
            json.dump(index, writer)

    def LoadProject(self):
        index = None
        with open(self.ProjectFile, 'r') as reader:
            index = json.load(reader)
        if not index or len(index) == 0:
            scene = Scene()
            scene.CreateEntity()
            self.SceneManager.AddScene("MainScene", scene)
            return

        for sceneName, relPath in index.items():
            if sceneName == "__current__":
                self.SceneManager.SetScene(relPath)
                continue
            scene = Scene()
            scene.LoadScene(os.path.join(self.ProjectDir, relPath))
            self.SceneManager.AddScene(sceneName, scene)

    def GetSurface(self):
        if self.SceneManager and self.SceneManager.HasScene():
            return self.SceneManager.Surface
        return None

    def GetCurrentScene(self):
        return self.SceneManager.CurrentScene


if __name__ == "__main__":
    PROJECT_PATH = "C:\\Users\\Kapil\\Documents"
    #Project.CreateNewProject(PROJECT_PATH, "PrototypeExample")
    project = Project(os.path.join(PROJECT_PATH, "PrototypeExample"))
    # project.SaveProject()

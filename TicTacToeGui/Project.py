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
        projectFolder = os.path.join(path, name)
        if not os.path.exists(projectFolder):
            os.mkdir(projectFolder)

        # Create Index file with the project Name
        with open('{}{}'.format(name, EXTENSION), 'w') as fp:
            pass

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
            self.ProjectFile = os.path.join(self.ProjectDir, self.ProjectName, EXTENSION)
        self.SceneManager = SceneManager()
        scene = Scene()
        scene.CreateEntity()
        self.SceneManager.AddScene("MainScene", scene)

    def SaveProject(self):
        index = dict()
        scenedir = os.path.join(self.ProjectDir, "Scene")
        if not os.path.exists(scenedir):
            os.mkdir(scenedir)

        for sceneName, scene in self.SceneManager.Scenes.items():
            if scene.SceneLocation == "":
                filepath = os.path.join(scenedir, sceneName)
                scene.SaveScene(filepath)
            index[sceneName] = scene.SceneLocation

        with open(self.ProjectFile, 'w') as fp:
            json.dump(index, fp)

    def LoadProject(self):
        pass

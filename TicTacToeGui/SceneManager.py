class SceneManager:
    def __init__(self):
        self.Scenes = dict()
        self.CurrentScene = None
        self.Surface = None
        self.CurrentSceneName = ""

    def HasScene(self):
        return not self.CurrentScene is None
    
    def AddScene(self, name, scene):
        self.Scenes[name] = scene
        scene.SetSceneManager(self)
        scene.OnSetup(self.Surface)
        if self.CurrentScene is None:
            self.SetScene(name)

    def SetScene(self, name):
        scene = self.Scenes[name]
        self.CurrentScene = scene
        self.CurrentSceneName = name
        scene.OnSetup(self.Surface)

    def GetScene(self, name=None):
        if name is None:
            return self.CurrentScene
        else:
            return self.Scenes[name]

    def SetSurface(self, Surface):
        for scene in self.Scenes.keys():
            self.Scenes[scene].SetSurface(Surface)
        self.Surface = Surface

    def Render(self):
        self.CurrentScene.OnRender()

    def Update(self):
        self.CurrentScene.OnUpdate()

    def Event(self, event):
        self.CurrentScene.OnEvent(event)

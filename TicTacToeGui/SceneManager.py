class SceneManager:
    def __init__(self):
        self.Scenes = dict()
        self.CurrentScene = None
        self.Surface = None
        self.CurrentSceneName = ""

    def AddScene(self, name, scene):
        self.Scenes[name] = scene
        if self.CurrentScene == None:
            self.SetScene(name)

    def SetScene(self, name):
        scene = self.Scenes[name]
        scene.OnSetup(self.Surface)
        self.CurrentScene = scene
        self.CurrentSceneName = name

    def GetScene(self, name=None):
        if name == None:
            return self.CurrentScene
        else:
            return self.Scenes[name]

    def SetSurface(self, Surface):
        for scene in self.Scenes.keys():
            self.Scenes[scene].Surface = Surface
        self.Surface = Surface

    def Render(self):
        self.CurrentScene.OnRender()

    def Update(self):
        self.CurrentScene.OnUpdate()

    def Event(self, event):
        self.CurrentScene.OnEvent(event)

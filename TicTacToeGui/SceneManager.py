class SceneManager:
    Scenes = dict()
    CurrentScene = None
    Surface = None

    def AddScene(name, scene):
        SceneManager.Scenes[name] = scene
        if SceneManager.CurrentScene == None:
            SceneManager.SetScene(name)

    def SetScene(name):
        scene = SceneManager.Scenes[name]
        scene.OnSetup()
        SceneManager.CurrentScene = scene

    def GetScene(name=None):
        if not name == None:
            return SceneManager.CurrentScene
        else:
            return SceneManager.Scenes[name]

    def Render():
        SceneManager.CurrentScene.OnRender(SceneManager.Surface)

    def Update():
        SceneManager.CurrentScene.OnUpdate()

    def Event(event):
        SceneManager.CurrentScene.OnEvent(event)

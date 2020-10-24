from .Components import TagComponent


def Event(func: callable, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def StateEvent(func: callable, *args, **kwargs):
    return lambda x: func(x, *args, **kwargs)


class Scriptable:
    def __init__(self, scene, entity):
        self.Scene = scene
        self.Reg = scene.Reg
        self.Surface = scene.Surface
        self.Entity = entity

    def Setup(self):
        """
        Method to be implemented by scripts.
        """

    def Update(self, timestep):
        """
        Method to be implemented by scripts.
        """

    def GetComponent(self, Typename):
        return self.Entity.GetComponent(Typename)

    def GetComponents(self):
        return self.Entity.GetComponents()

    def GetSceneComponentsByType(self, typename):
        return self.Reg.GetComponentsByType(typename)

    def GetEntity(self, entityId):
        return self.Scene.Entities[entityId]

    def GetEntitiesByTag(self, tagname):
        tags = self.GetSceneComponentsByType(TagComponent)
        entities = list()
        for tag, enttId in tags:
            if tag.name == tagname:
                entities.append(self.Scene.Entities[enttId])
        return entities

    def AddOnClickListener(self, button, event: callable):
        self.Scene.InputHandler.AddOnClickListener(button, event)

    def AddOnHoverListener(self, button, event: callable):
        self.Scene.InputHandler.AddOnHoverListener(button, event)

    def GetSceneManager(self):
        return self.Scene.GetSceneManager()

    def CloneEntity(self, entity):
        return self.Scene.CloneEntity(entity)

    def CreateEntity(self):
        return self.Scene.CreateEntity()

    # Will contains instance of
    # 1. Physics Manager
    # 2. Input Manager
    # which game objects can query during update

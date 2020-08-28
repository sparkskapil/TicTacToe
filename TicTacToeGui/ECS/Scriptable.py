from ECS.Components import TagComponent

def Event(func: callable, *args, **kwargs):
    return lambda: func(*args, **kwargs)

class Scriptable:
    def __init__(self, scene, entity):
        self.scene = scene
        self.Reg = scene.Reg
        self.Surface = scene.Surface
        self.Entity = entity

    def GetComponent(self, Typename):
        return self.Entity.GetComponent(Typename)

    def GetComponents(self):
        return self.Entity.GetComponents()
    
    def GetSceneComponentsByType(self, typename):
        return self.Reg.GetComponentsByType(typename)
    
    def GetEntity(self, entityId):
        return self.scene.Entities[entityId]
    
    def GetEntitiesByTag(self, tagname):
        tags = self.GetSceneComponentsByType(TagComponent)
        entities = list()
        for tag, enttId in tags:
            if tag.name == tagname:
                entities.append(self.scene.Entities[enttId])
        return entities
           
    def AddOnClickListener(self, button, event:callable):
        self.scene.InputHandler.AddOnClickListener(button, event)
    
     
    # Will contains instance of
    # 1. Physics Manager
    # 2. Input Manager
    # which game objects can query during update
